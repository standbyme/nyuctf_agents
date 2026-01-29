---
name: run-command
description: Run a shell command in the Docker container. Returns stdout, stderr, returncode, and timed_out. Use this skill when you need to execute commands in the CTF environment.
---

# Run Command

Execute shell commands in the Docker container environment.

## When to use this skill

Use this skill when you need to:
- Execute shell commands in the CTF environment
- Run scripts or programs
- Interact with files and directories
- Use command-line tools like `cat`, `ls`, `python`, `nc`, etc.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `command` | string | Yes | The command to run |
| `timeout` | number | No | Timeout in seconds (default 300) |

## How to use

1. Provide the command you want to execute as a string
2. Optionally specify a timeout value in seconds
3. The tool returns stdout, stderr, returncode, and whether the command timed out

## Examples

### Basic command execution
```
command: "ls -la /home/ctfplayer/ctf_files"
```

### Running a Python script
```
command: "python3 solve.py"
timeout: 60
```

### Network commands
```
command: "nc challenge.server 1234"
timeout: 30
```

## Return format

Returns a JSON object with:
- `stdout`: Standard output from the command
- `stderr`: Standard error output from the command
- `returncode`: Exit code of the command (null if timed out)
- `timed_out`: Boolean indicating if the command timed out

## Tips

- Use `hexdump` to parse binary data instead of dumping it raw
- Write python scripts with `pwntools` to pass inputs to programs instead of using shell piping
- Remember to handle timeouts appropriately for long-running commands
