---
name: create-file
description: Create a file in the CTF Docker container with specified contents. Use when you need to write exploit scripts, payloads, or configuration files to the container filesystem.
allowed-tools: Bash(docker *)
---

# Create File in CTF Environment

Create a file with specified contents in the CTF Docker container.

## Usage

Create a file at the specified path with the given contents:

```bash
# Method 1: Using heredoc
docker exec $CTF_CONTAINER bash -c 'cat > "$PATH" << "EOF"
$CONTENTS
EOF'

# Method 2: Using echo (for simple content)
docker exec $CTF_CONTAINER bash -c 'echo "$CONTENTS" > "$PATH"'

# Method 3: Using docker cp for complex files
echo "$CONTENTS" > /tmp/tmpfile
docker cp /tmp/tmpfile $CTF_CONTAINER:$PATH
rm /tmp/tmpfile
```

## Parameters

- `path`: Path where the file should be created (relative paths are relative to `/home/ctfplayer/`)
- `contents`: The content to write to the file
- `decode_escapes`: Whether to decode escape sequences (default: false)

## Path Handling

- `~/exploit.py` → `/home/ctfplayer/exploit.py`
- `exploit.py` → `/home/ctfplayer/exploit.py`
- `/tmp/payload` → `/tmp/payload`

## Examples

### Python Exploit Script
```bash
docker exec $CTF_CONTAINER bash -c 'cat > ~/exploit.py << "EOF"
#!/usr/bin/env python3
from pwn import *

# Connection setup
HOST = "challenge.server"
PORT = 1337

# Exploit code
io = remote(HOST, PORT)
payload = b"A" * 64 + p64(0xdeadbeef)
io.sendline(payload)
io.interactive()
EOF'
```

### Binary Payload
```bash
# For binary content with escape sequences
docker exec $CTF_CONTAINER bash -c 'printf "\x41\x41\x41\x41\xef\xbe\xad\xde" > ~/payload.bin'
```

### Shell Script
```bash
docker exec $CTF_CONTAINER bash -c 'cat > ~/run.sh << "EOF"
#!/bin/bash
cd ~/ctf_files
./binary < payload.txt
EOF'
docker exec $CTF_CONTAINER chmod +x ~/run.sh
```

### Configuration File
```bash
docker exec $CTF_CONTAINER bash -c 'cat > ~/gdb_commands.txt << "EOF"
set disassembly-flavor intel
break main
run
EOF'
```

## Making Files Executable

After creating a script, make it executable:

```bash
docker exec $CTF_CONTAINER chmod +x ~/exploit.py
```

## Creating Directories

If the parent directory doesn't exist:

```bash
docker exec $CTF_CONTAINER mkdir -p ~/exploits/pwn
docker exec $CTF_CONTAINER bash -c 'cat > ~/exploits/pwn/exploit.py << "EOF"
...
EOF'
```

## Handling Special Characters

For content with special characters, use base64 encoding:

```bash
# Encode on host
ENCODED=$(echo -n "$CONTENTS" | base64)

# Decode in container
docker exec $CTF_CONTAINER bash -c "echo '$ENCODED' | base64 -d > $PATH"
```
