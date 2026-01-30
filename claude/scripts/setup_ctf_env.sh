#!/bin/bash
# Setup CTF Environment for Claude Code
# This script initializes the Docker environment for CTF challenges

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default configuration
CTF_CONTAINER_IMAGE="${CTF_CONTAINER_IMAGE:-ctfenv}"
CTF_NETWORK="${CTF_NETWORK:-ctfnet}"
CONTAINER_HOME="/home/ctfplayer"

echo "=== CTF Environment Setup ==="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

# Create network if not exists
if ! docker network ls | grep -q "$CTF_NETWORK"; then
    echo "Creating Docker network: $CTF_NETWORK"
    docker network create "$CTF_NETWORK"
else
    echo "Docker network exists: $CTF_NETWORK"
fi

# Check if image exists
if ! docker image ls | grep -q "$CTF_CONTAINER_IMAGE"; then
    echo "Warning: Docker image '$CTF_CONTAINER_IMAGE' not found"
    echo "Build it with: docker build -t $CTF_CONTAINER_IMAGE -f docker/Dockerfile ."
    exit 1
else
    echo "Docker image exists: $CTF_CONTAINER_IMAGE"
fi

# Start container
start_container() {
    local name="${1:-ctf_agent}"
    
    # Check if already running
    if docker ps --format '{{.Names}}' | grep -q "^${name}$"; then
        echo "Container '$name' already running"
        CTF_CONTAINER=$(docker ps -q -f "name=$name")
    else
        echo "Starting container: $name"
        CTF_CONTAINER=$(docker run -d --rm \
            --name "$name" \
            --network "$CTF_NETWORK" \
            --platform linux/amd64 \
            "$CTF_CONTAINER_IMAGE")
    fi
    
    export CTF_CONTAINER
    echo "Container ID: $CTF_CONTAINER"
}

# Stop container
stop_container() {
    local name="${1:-ctf_agent}"
    if docker ps --format '{{.Names}}' | grep -q "^${name}$"; then
        echo "Stopping container: $name"
        docker stop "$name"
    else
        echo "Container '$name' not running"
    fi
}

# Copy files into container
copy_files() {
    local source_dir="$1"
    local target_dir="${2:-ctf_files}"
    
    if [ -z "$CTF_CONTAINER" ]; then
        echo "Error: CTF_CONTAINER not set"
        return 1
    fi
    
    echo "Copying files from $source_dir to container..."
    docker exec "$CTF_CONTAINER" mkdir -p "$CONTAINER_HOME/$target_dir"
    docker cp "$source_dir/." "$CTF_CONTAINER:$CONTAINER_HOME/$target_dir/"
}

# Execute command in container
exec_cmd() {
    if [ -z "$CTF_CONTAINER" ]; then
        echo "Error: CTF_CONTAINER not set"
        return 1
    fi
    
    docker exec "$CTF_CONTAINER" bash -c "$*"
}

# Main
case "${1:-}" in
    start)
        start_container "${2:-ctf_agent}"
        ;;
    stop)
        stop_container "${2:-ctf_agent}"
        ;;
    copy)
        copy_files "$2" "$3"
        ;;
    exec)
        shift
        exec_cmd "$@"
        ;;
    shell)
        start_container "${2:-ctf_agent}"
        docker exec -it "$CTF_CONTAINER" bash
        ;;
    status)
        docker ps --filter "ancestor=$CTF_CONTAINER_IMAGE"
        ;;
    *)
        echo "Usage: $0 {start|stop|copy|exec|shell|status} [args...]"
        echo ""
        echo "Commands:"
        echo "  start [name]        Start a CTF container"
        echo "  stop [name]         Stop a CTF container"
        echo "  copy <src> [dest]   Copy files into container"
        echo "  exec <command>      Execute command in container"
        echo "  shell [name]        Open interactive shell"
        echo "  status              Show running containers"
        echo ""
        echo "Environment variables:"
        echo "  CTF_CONTAINER_IMAGE  Docker image (default: ctfenv)"
        echo "  CTF_NETWORK          Docker network (default: ctfnet)"
        ;;
esac
