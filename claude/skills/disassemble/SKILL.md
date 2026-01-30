---
name: disassemble
description: Disassemble a function from a binary using Ghidra. Use for low-level binary analysis to examine assembly instructions. Returns assembly code for the specified function.
---

# Disassemble Function

Disassemble binary functions to assembly code using Ghidra.

## Usage

```bash
python3 scripts/ghidra_disassemble.py <binary_path> <function_name>
```

## Parameters

- `path`: Path to the binary file to disassemble
- `function`: Function name to disassemble (default: "main")

## When to Use

- **Decompile**: Understanding program logic, variable flow
- **Disassemble**: Analyzing exact instructions, gadget hunting, understanding calling conventions

## Examples

### Basic Usage
```bash
# Disassemble main function
python3 ~/.claude/skills/disassemble/scripts/ghidra_disassemble.py ~/ctf_files/binary main

# Disassemble specific function
python3 ~/.claude/skills/disassemble/scripts/ghidra_disassemble.py ~/ctf_files/binary vulnerable_func
```

### Output Format

The disassembler returns assembly instructions:

```asm
push   rbp
mov    rbp,rsp
sub    rsp,0x40
lea    rdi,[rip+0x1234]
call   printf
mov    eax,0x0
leave
ret
```

## Architecture Support

- x86 (32-bit)
- x86-64 (64-bit)
- ARM
- MIPS
- Other architectures supported by Ghidra

## Finding ROP Gadgets

Use disassembly with grep for gadget hunting:

```bash
# Find ret instructions
python3 scripts/ghidra_disassemble.py binary all | grep -B5 "ret"

# Find pop gadgets
python3 scripts/ghidra_disassemble.py binary all | grep "pop"
```

## Common Patterns to Look For

### Buffer Overflows
```asm
lea    rdi,[rbp-0x40]    ; Buffer on stack
call   gets              ; Dangerous function
```

### Format String Vulnerabilities
```asm
lea    rdi,[rbp-0x20]    ; User input
xor    eax,eax
call   printf            ; Format string vuln if input controlled
```

### Return to Libc
```asm
pop    rdi               ; Gadget for setting first argument
ret
```

## Caching

Disassembly results are cached. To clear cache:
```bash
rm ~/.cache/ghidra_decomp/<binary>.disas.json
```

## See Also

- [decompile](../decompile/SKILL.md) - For C-like pseudocode
- [run-command](../run-command/SKILL.md) - For running analysis tools
