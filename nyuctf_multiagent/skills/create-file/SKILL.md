---
name: create-file
description: Create a file in the container environment with the given contents. You may overwrite existing files with this tool. Relative paths will be taken from the home directory.
---

# Create File

Create or overwrite a file in the Docker container environment.

## When to use this skill

Use this skill when you need to:
- Create exploit scripts
- Write solver programs
- Create configuration files
- Store data for later use
- Create input files for programs

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | The full path of the file to create |
| `contents` | string | Yes | The file contents |

## How to use

1. Specify the path where you want to create the file
2. Provide the contents of the file
3. The file will be created (or overwritten if it exists)

## Examples

### Create a Python exploit script
```
path: "/home/ctfplayer/exploit.py"
contents: |
  from pwn import *
  
  r = remote('challenge.server', 1234)
  r.sendline(b'payload')
  print(r.recvall())
```

### Create a simple text file
```
path: "notes.txt"
contents: "Important notes about the challenge"
```

### Create a binary payload file
```
path: "/home/ctfplayer/payload.bin"
contents: "\x90\x90\x90\x90"
```

## Return format

Returns a JSON object with:
- `success: true` and `path: "<created_path>"` on success
- `error: "Path or contents not provided!"` if parameters are missing

## Tips

- Relative paths are relative to `/home/ctfplayer/`
- You can overwrite existing files without error
- Use this to create Python scripts with pwntools for exploits
- Consider creating helper scripts for complex operations
