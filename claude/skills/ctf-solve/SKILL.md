---
name: ctf-solve
description: Main orchestration skill for solving CTF (Capture The Flag) challenges. Use when approaching any CTF challenge. Provides structured methodology for reconnaissance, analysis, exploitation, and flag capture.
context: fork
agent: general-purpose
allowed-tools: Bash(docker *), Read, Write, Grep, Glob
---

# CTF Challenge Solving Methodology

This skill provides a structured approach to solving Capture The Flag challenges.

## Challenge Information

Parse the challenge details:
- **Name**: Challenge title
- **Category**: pwn/rev/crypto/web/forensics/misc
- **Points**: Difficulty indicator
- **Description**: May contain hints
- **Files**: Available in `~/ctf_files/`
- **Server**: Network service if applicable

## Phase 1: Reconnaissance

### 1.1 Examine Challenge Files

```bash
# List all challenge files
docker exec $CTF_CONTAINER ls -la ~/ctf_files/

# Check file types
docker exec $CTF_CONTAINER file ~/ctf_files/*

# Look for strings
docker exec $CTF_CONTAINER strings ~/ctf_files/* | head -100
```

### 1.2 Category-Specific Initial Analysis

**For Binaries (pwn/rev)**:
```bash
# Check security features
docker exec $CTF_CONTAINER checksec ~/ctf_files/binary

# Get binary info
docker exec $CTF_CONTAINER readelf -h ~/ctf_files/binary
```

**For Web**:
```bash
# Check web server
docker exec $CTF_CONTAINER curl -I http://challenge.server/

# Directory enumeration
docker exec $CTF_CONTAINER nikto -h http://challenge.server/
```

**For Crypto**:
```bash
# Analyze encrypted data
docker exec $CTF_CONTAINER python3 -c "
import base64
data = open('~/ctf_files/encrypted', 'rb').read()
print(f'Length: {len(data)}')
print(f'Hex: {data[:50].hex()}')"
```

**For Forensics**:
```bash
# Analyze file
docker exec $CTF_CONTAINER binwalk ~/ctf_files/image

# Check for hidden data
docker exec $CTF_CONTAINER exiftool ~/ctf_files/image
```

## Phase 2: Deep Analysis

### 2.1 Understand the Challenge

Based on category:

**Binary Analysis**:
- Decompile main functions using `/decompile`
- Identify vulnerability classes
- Map control flow

**Web Analysis**:
- Identify technologies used
- Find input vectors
- Check for common vulns (SQLi, XSS, etc.)

**Crypto Analysis**:
- Identify cipher/algorithm
- Look for implementation weaknesses
- Check for known attacks

### 2.2 Identify Attack Vectors

Common vulnerabilities by category:

| Category | Common Vulns |
|----------|-------------|
| pwn | Buffer overflow, format string, use-after-free, heap |
| rev | Anti-debugging, obfuscation, packing |
| crypto | Weak keys, bad RNG, side channels |
| web | SQLi, XSS, SSRF, command injection |
| forensics | Hidden data, deleted files, memory artifacts |

## Phase 3: Exploitation

### 3.1 Develop Exploit

Create exploit script using `/create-file`:

```python
#!/usr/bin/env python3
from pwn import *

# Setup
context.binary = ELF('./binary')
# context.log_level = 'debug'

# Connection
if args.REMOTE:
    io = remote('challenge.server', 1337)
else:
    io = process('./binary')

# Exploit
# [YOUR EXPLOIT CODE HERE]

io.interactive()
```

### 3.2 Test and Iterate

```bash
# Local testing
docker exec $CTF_CONTAINER python3 ~/exploit.py

# Remote exploitation
docker exec $CTF_CONTAINER python3 ~/exploit.py REMOTE
```

## Phase 4: Flag Capture

### 4.1 Extract the Flag

Look for flag in:
- Program output
- Files on server
- Memory/registers
- Network responses

### 4.2 Verify Flag

Use `/check-flag` to verify:
```
/check-flag flag{captured_flag_here}
```

## Troubleshooting

### Common Issues

1. **Binary won't run**: Check architecture, dependencies
2. **Exploit works locally, not remote**: Check for ASLR, different libc
3. **Can't find vulnerability**: Review all inputs, edge cases
4. **Partial flag**: Check for multi-part challenges

### Debugging Techniques

```bash
# GDB debugging
docker exec $CTF_CONTAINER gdb -q ~/ctf_files/binary

# strace system calls
docker exec $CTF_CONTAINER strace ./binary

# ltrace library calls
docker exec $CTF_CONTAINER ltrace ./binary
```

## Success Criteria

- [ ] Challenge files analyzed
- [ ] Vulnerability identified
- [ ] Exploit developed
- [ ] Exploit works locally
- [ ] Exploit works remotely (if applicable)
- [ ] Flag captured and verified
