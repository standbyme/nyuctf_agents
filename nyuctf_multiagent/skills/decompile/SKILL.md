---
name: decompile
description: Decompile a function from a binary using Ghidra. Use this skill when you need to analyze the high-level code structure of binary files.
---

# Decompile

Decompile functions from binary files using Ghidra to produce C-like pseudocode.

## When to use this skill

Use this skill when you need to:
- Understand the high-level logic of a binary
- Analyze C/C++ source reconstruction
- Identify vulnerabilities in a more readable format
- Understand data structures and control flow

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `binary` | string | Yes | Path of the binary to decompile |
| `function` | string | No | Function name to decompile (default 'main') |

## How to use

1. Specify the path to the binary file
2. Optionally specify the function name (defaults to 'main')
3. The tool returns the decompiled C-like pseudocode

## Examples

### Decompile main function
```
binary: "/home/ctfplayer/ctf_files/challenge"
```

### Decompile specific function
```
binary: "/home/ctfplayer/ctf_files/challenge"
function: "vulnerable_function"
```

### Analyze encryption function
```
binary: "/home/ctfplayer/ctf_files/challenge"
function: "encrypt"
```

## Return format

Returns a JSON object with:
- `decompilation: "<C-like pseudocode>"` on success
- `error: "Failed to run Ghidra..."` if the binary cannot be analyzed
- `error: "Function X not found..."` if the function doesn't exist

## Tips

- Decompilation provides a higher-level view than disassembly
- Variable names are auto-generated and may not be meaningful
- Use this alongside disassemble for a complete picture
- Look for common vulnerabilities:
  - Buffer overflows (unsafe strcpy, gets, sprintf)
  - Format string bugs (printf with user input)
  - Integer overflows
  - Use-after-free
- Prefer this tool over radare2 or objdump for initial analysis

## Common function names to try

- `main` - Main entry point
- `_start` - Program entry point  
- `check_password` - Authentication functions
- `read_input` - Input handling functions
- `process_data` - Data processing functions
- `encrypt` / `decrypt` - Cryptographic functions
