#!/usr/bin/env python3
"""
Docker Execution Wrapper for CTF Challenges

This script provides a Python interface for executing commands
in the CTF Docker container, similar to the CommandExec tool
in the original nyuctf_baseline framework.
"""

import subprocess
import json
import sys
import os
import argparse
from pathlib import Path
from typing import Optional, Dict, Any


class DockerExec:
    """Execute commands in a CTF Docker container."""
    
    def __init__(
        self,
        container: Optional[str] = None,
        image: str = "ctfenv",
        network: str = "ctfnet"
    ):
        self.container = container or os.environ.get("CTF_CONTAINER")
        self.image = image
        self.network = network
        self.container_home = Path("/home/ctfplayer")
    
    def ensure_container(self) -> str:
        """Ensure a container is running, start one if needed."""
        if self.container:
            # Check if container exists
            result = subprocess.run(
                ["docker", "inspect", self.container],
                capture_output=True
            )
            if result.returncode == 0:
                return self.container
        
        # Start new container
        print(f"Starting new container with image {self.image}...", file=sys.stderr)
        result = subprocess.run(
            [
                "docker", "run", "-d", "--rm",
                "--network", self.network,
                "--platform", "linux/amd64",
                self.image
            ],
            capture_output=True,
            text=True,
            check=True
        )
        self.container = result.stdout.strip()
        os.environ["CTF_CONTAINER"] = self.container
        print(f"Started container: {self.container[:12]}", file=sys.stderr)
        return self.container
    
    @staticmethod
    def _clean(text: Optional[bytes]) -> Optional[str]:
        """Clean command output."""
        if text is None:
            return None
        return text.decode('utf-8', errors='backslashreplace').replace('\r\n', '\n')
    
    def run_command(
        self,
        command: str,
        timeout: float = 10.0
    ) -> Dict[str, Any]:
        """
        Run a command in the Docker container.
        
        Returns:
            Dict with keys: stdout, stderr, returncode, timed_out
        """
        container = self.ensure_container()
        
        try:
            p = subprocess.Popen(
                ["docker", "exec", container, "bash", "-c", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = p.communicate(timeout=timeout)
            return {
                "stdout": self._clean(stdout),
                "stderr": self._clean(stderr),
                "returncode": p.returncode,
                "timed_out": False
            }
        except subprocess.TimeoutExpired:
            p.kill()
            stdout, stderr = p.communicate(timeout=timeout)
            return {
                "stdout": self._clean(stdout),
                "stderr": self._clean(stderr),
                "returncode": None,
                "timed_out": True
            }
        except subprocess.CalledProcessError as e:
            return {
                "stdout": self._clean(e.stdout),
                "stderr": self._clean(e.stderr),
                "returncode": e.returncode,
                "timed_out": False
            }
    
    def copy_into_container(
        self,
        hostpath: str,
        containerpath: str
    ) -> Dict[str, Any]:
        """Copy a file into the container."""
        container = self.ensure_container()
        
        path = Path(containerpath)
        if not path.is_absolute():
            path = self.container_home / path
        
        # Create parent directory
        parent_dir = str(path.parent)
        subprocess.run(
            ["docker", "exec", container, "mkdir", "-p", parent_dir],
            capture_output=True
        )
        
        # Copy file
        try:
            subprocess.run(
                ["docker", "cp", "-aq", hostpath, f"{container}:{path}"],
                capture_output=True,
                check=True
            )
            return {"success": True, "path": str(path)}
        except subprocess.CalledProcessError as e:
            return {
                "error": f"Failed to copy file: {e.stderr.decode('utf-8', errors='replace')}"
            }
    
    def create_file(
        self,
        path: str,
        contents: str,
        decode_escapes: bool = False
    ) -> Dict[str, Any]:
        """Create a file in the container with given contents."""
        import tempfile
        
        if decode_escapes:
            try:
                contents_bytes = bytes(contents, 'utf-8').decode('unicode_escape').encode('latin-1')
            except UnicodeDecodeError as e:
                return {"error": f"Invalid escape sequence: {e}"}
        else:
            contents_bytes = contents.encode()
        
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            f.write(contents_bytes)
            temp_path = f.name
        
        try:
            result = self.copy_into_container(temp_path, path)
            return result
        finally:
            os.unlink(temp_path)
    
    def stop_container(self):
        """Stop the container."""
        if self.container:
            subprocess.run(
                ["docker", "stop", self.container],
                capture_output=True
            )
            self.container = None


def main():
    parser = argparse.ArgumentParser(
        description="Execute commands in CTF Docker container"
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to execute"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=10.0,
        help="Command timeout in seconds"
    )
    parser.add_argument(
        "--container",
        help="Container ID or name"
    )
    parser.add_argument(
        "--image",
        default="ctfenv",
        help="Docker image name"
    )
    parser.add_argument(
        "--network",
        default="ctfnet",
        help="Docker network name"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--create-file",
        nargs=2,
        metavar=("PATH", "CONTENTS"),
        help="Create a file in the container"
    )
    parser.add_argument(
        "--copy",
        nargs=2,
        metavar=("HOST", "CONTAINER"),
        help="Copy file into container"
    )
    
    args = parser.parse_args()
    
    docker = DockerExec(
        container=args.container,
        image=args.image,
        network=args.network
    )
    
    if args.create_file:
        result = docker.create_file(args.create_file[0], args.create_file[1])
    elif args.copy:
        result = docker.copy_into_container(args.copy[0], args.copy[1])
    elif args.command:
        result = docker.run_command(args.command, args.timeout)
    else:
        parser.print_help()
        sys.exit(1)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        elif "stdout" in result:
            if result["stdout"]:
                print(result["stdout"], end="")
            if result["stderr"]:
                print(result["stderr"], file=sys.stderr, end="")
            if result["timed_out"]:
                print("\n[Command timed out]", file=sys.stderr)
            sys.exit(result["returncode"] or 0)
        else:
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
