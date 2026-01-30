---
name: rev
description: Reverse engineering techniques and methodology. Use when analyzing binaries, understanding program logic, bypassing protections, or solving crackme challenges.
---

# Reverse Engineering (Rev)

Techniques and methodology for reverse engineering CTF challenges.

## Pre-installed Tools

- `pwntools` - Binary manipulation
- `radare2` - Analysis and disassembly
- `gdb` + `pwndbg` - Dynamic analysis
- `objdump` - Quick disassembly
- `strings` - String extraction
- `strace/ltrace` - System/library call tracing

## Initial Analysis

### 1. File Identification

```bash
docker exec $CTF_CONTAINER file ~/ctf_files/binary
docker exec $CTF_CONTAINER strings ~/ctf_files/binary | head -50
docker exec $CTF_CONTAINER readelf -a ~/ctf_files/binary | head -100
```

### 2. Quick Symbol Check

```bash
# List functions
docker exec $CTF_CONTAINER nm ~/ctf_files/binary

# List dynamic symbols
docker exec $CTF_CONTAINER nm -D ~/ctf_files/binary
```

## Analysis Workflow

### Step 1: Static Analysis

Use `/decompile` to understand program logic:
```
/decompile ~/ctf_files/binary main
/decompile ~/ctf_files/binary check_password
```

### Step 2: Dynamic Analysis

```bash
# Trace system calls
docker exec $CTF_CONTAINER strace ./binary

# Trace library calls
docker exec $CTF_CONTAINER ltrace ./binary

# Run with input
docker exec $CTF_CONTAINER bash -c "echo 'test' | ./binary"
```

### Step 3: Interactive Debugging

```bash
docker exec -it $CTF_CONTAINER gdb -q ~/ctf_files/binary
```

## Common Challenge Types

### Password/Key Verification

```python
# Common patterns to look for:
# - strcmp(), strncmp() comparisons
# - XOR encoding
# - Character-by-character checks
# - Hash comparisons

# GDB breakpoint on strcmp
break strcmp
run
# Check arguments when it breaks
x/s $rdi
x/s $rsi
```

### Encoded/Encrypted Data

```python
# XOR decryption
def xor_decrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# Base64
import base64
decoded = base64.b64decode(encoded)

# Custom encoding - trace the algorithm
```

### Anti-Debugging

**Detection techniques**:
- `ptrace(PTRACE_TRACEME)` - Only one debugger
- Timing checks
- `/proc/self/status` checks
- INT3 detection

**Bypassing**:
```bash
# LD_PRELOAD fake ptrace
docker exec $CTF_CONTAINER bash -c 'cat > /tmp/fake_ptrace.c << EOF
long ptrace(int request, ...) { return 0; }
EOF'
docker exec $CTF_CONTAINER gcc -shared -o /tmp/fake_ptrace.so /tmp/fake_ptrace.c
docker exec $CTF_CONTAINER LD_PRELOAD=/tmp/fake_ptrace.so ./binary
```

```gdb
# GDB - catch and skip ptrace
catch syscall ptrace
commands
set $rax = 0
continue
end
```

### Packed/Obfuscated Binaries

```bash
# Check for packers
docker exec $CTF_CONTAINER strings binary | grep -i upx

# UPX unpacking
docker exec $CTF_CONTAINER upx -d binary

# Dump from memory after unpacking
docker exec $CTF_CONTAINER gdb -q binary -ex 'start' -ex 'dump memory unpacked.bin 0x400000 0x401000'
```

## Radare2 Commands

```bash
docker exec $CTF_CONTAINER r2 ~/ctf_files/binary

# Analysis
aaa          # Analyze all
afl          # List functions
pdf @ main   # Disassemble main

# Strings
iz           # Strings in data section
izz          # All strings

# Cross references
axt @ sym.func    # Find references to function
axf @ sym.func    # Find references from function

# Visual mode
VV @ main    # Graph view
```

## Python Analysis Script

```python
#!/usr/bin/env python3
from pwn import *

# Load binary
binary = ELF('./binary')

# Find interesting addresses
main_addr = binary.symbols.get('main', None)
check_func = binary.symbols.get('check_password', None)

# Search for strings
flag_ref = list(binary.search(b'flag{'))
password_ref = list(binary.search(b'password'))

# Analyze sections
for section in binary.sections:
    print(f"{section.name}: {section.header.sh_addr:#x}")

# Read data from binary
data_section = binary.get_section_by_name('.data')
if data_section:
    data = binary.read(data_section.header.sh_addr, 0x100)
```

## GDB Analysis

```gdb
# Set Intel syntax
set disassembly-flavor intel

# Useful breakpoints
break main
break *0x401234

# Watch memory
watch *0x404000

# Conditional breakpoints
break check_password if $rdi == 0x41

# Examine memory
x/20wx $rsp      # 20 words from stack
x/s $rdi         # String at rdi
x/10i $rip       # Next 10 instructions

# Modify execution
set $rax = 1     # Set return value
jump *0x401234   # Jump to address
```

## See Also

- [decompile](../decompile/SKILL.md) - C-like decompilation
- [disassemble](../disassemble/SKILL.md) - Assembly analysis
- [pwn](../pwn/SKILL.md) - Exploitation after finding vulns
