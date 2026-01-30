---
name: run-command
description: Execute shell commands in the CTF Docker container environment. Use when you need to run any shell command, install packages, or interact with the CTF challenge. The container persists across calls.
allowed-tools: Bash(docker *)
---

# Run Command in CTF Environment

Execute shell commands in a persistent Docker container for CTF challenges.

## Usage

Run the provided command in the CTF Docker container:

```bash
docker exec $CTF_CONTAINER bash -c "$ARGUMENTS"
```

If `CTF_CONTAINER` is not set, first start a container:

```bash
# Start container if not running
CTF_CONTAINER=$(docker run -d --rm --network ${CTF_NETWORK:-ctfnet} --platform linux/amd64 ${CTF_CONTAINER_IMAGE:-ctfenv})
export CTF_CONTAINER
```

## Parameters

- `command`: The shell command to execute
- `timeout`: Maximum execution time (default: 10 seconds)

## Examples

### Basic Commands
```bash
# List files
docker exec $CTF_CONTAINER bash -c "ls -la ~/ctf_files/"

# Check file type
docker exec $CTF_CONTAINER bash -c "file ~/ctf_files/binary"

# Search for strings
docker exec $CTF_CONTAINER bash -c "strings ~/ctf_files/binary | grep -i flag"
```

### Installing Tools
```bash
# Install packages
docker exec $CTF_CONTAINER bash -c "sudo apt-get update && sudo apt-get install -y <package>"

# Install Python packages
docker exec $CTF_CONTAINER bash -c "pip install <package>"
```

### Running Scripts
```bash
# Run Python exploit
docker exec $CTF_CONTAINER bash -c "python3 ~/exploits/exploit.py"

# Run with pwntools
docker exec $CTF_CONTAINER bash -c "python3 -c 'from pwn import *; ...'"
```

### Network Interaction
```bash
# Connect to challenge server
docker exec $CTF_CONTAINER bash -c "nc challenge.server 1337"

# HTTP requests
docker exec $CTF_CONTAINER bash -c "curl http://challenge.server/endpoint"
```

## Timeout Handling

For long-running commands, increase the timeout:

```bash
docker exec $CTF_CONTAINER timeout 60 bash -c "long_running_command"
```

For interactive programs that need input, use:

```bash
docker exec -i $CTF_CONTAINER bash -c "echo 'input' | ./program"
```

## Output Handling

- stdout and stderr are captured separately
- Binary output is decoded with backslash escaping
- Large outputs should be piped through `head` or `tail`

## Common Patterns

### Binary Analysis
```bash
# Check security features
docker exec $CTF_CONTAINER bash -c "checksec ~/ctf_files/binary"

# Run with ASLR disabled
docker exec $CTF_CONTAINER bash -c "setarch \$(uname -m) -R ./binary"
```

### Debugging
```bash
# GDB with script
docker exec $CTF_CONTAINER bash -c "gdb -x commands.gdb ./binary"

# strace system calls
docker exec $CTF_CONTAINER bash -c "strace -f ./binary 2>&1"
```

### File Operations
```bash
# Extract archives
docker exec $CTF_CONTAINER bash -c "cd ~/ctf_files && unzip archive.zip"

# Hex dump
docker exec $CTF_CONTAINER bash -c "xxd ~/ctf_files/file | head -50"
```
