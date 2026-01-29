---
name: disassemble
description: Disassemble a function from a binary using Ghidra. Use this skill when you need to analyze assembly code of binary files.
---

# Disassemble

Disassemble functions from binary files using Ghidra.

## When to use this skill

Use this skill when you need to:
- Analyze assembly code of a binary
- Understand the low-level behavior of a function
- Look for vulnerabilities at the instruction level
- Examine function prologues, epilogues, or specific instructions

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `binary` | string | Yes | Path of the binary to disassemble |
| `function` | string | No | Function name to disassemble (default 'main') |

## How to use

1. Specify the path to the binary file
2. Optionally specify the function name (defaults to 'main')
3. The tool returns the disassembly of the specified function

## Examples

### Disassemble main function
```
binary: "/home/ctfplayer/ctf_files/challenge"
```

### Disassemble specific function
```
binary: "/home/ctfplayer/ctf_files/challenge"
function: "vulnerable_function"
```

### Analyze entry point
```
binary: "/home/ctfplayer/ctf_files/challenge"
function: "_start"
```

## Return format

Returns a JSON object with:
- `disassembly: "<assembly code>"` on success
- `error: "Failed to run Ghidra..."` if the binary cannot be analyzed
- `error: "Function X not found..."` if the function doesn't exist

## Tips

- Try disassembling 'main' first to understand the program flow
- If 'main' is not found, try '_start', 'invoke_main', or 'entry'
- Use this alongside decompile for a complete picture
- Look for common vulnerability patterns like missing bounds checks
- Prefer this tool over radare2 or objdump for initial analysis

## Common function names to try

- `main` - Main entry point
- `_start` - Program entry point
- `invoke_main` - Alternative main entry
- `entry` - Generic entry point
- `check_password` - Authentication functions
- `read_input` - Input handling functions
- `process_data` - Data processing functions
