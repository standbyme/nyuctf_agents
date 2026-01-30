---
name: decompile
description: Decompile a function from a binary using Ghidra. Use for reverse engineering and binary analysis to understand program logic. Returns C-like pseudocode for the specified function.
---

# Decompile Function

Decompile binary functions to C-like pseudocode using Ghidra.

## Usage

```bash
python3 scripts/ghidra_decompile.py <binary_path> <function_name>
```

## Parameters

- `path`: Path to the binary file to decompile
- `function`: Function name to decompile (default: "main")

## Function Name Formats

- Named functions: `main`, `check_password`, `decrypt`
- Entry points: `_start`, `invoke_main`
- Radare2 format: `fcn.00401234` (address-based)
- Mangled C++ names: `_Z10myFunctionv`

## Examples

### Basic Usage
```bash
# Decompile main function
python3 ~/.claude/skills/decompile/scripts/ghidra_decompile.py ~/ctf_files/binary main

# Decompile specific function
python3 ~/.claude/skills/decompile/scripts/ghidra_decompile.py ~/ctf_files/binary check_password
```

### Output Format

The decompiler returns C-like pseudocode:

```c
int main(int argc, char **argv) {
    char buffer[64];
    printf("Enter password: ");
    scanf("%s", buffer);
    if (check_password(buffer)) {
        system("/bin/sh");
    }
    return 0;
}
```

## Finding Functions

If you don't know the function names:

1. Use `disassemble` skill first to see function list
2. Look for symbols: `nm binary | grep -i function`
3. Check strings for references: `strings binary | grep -i func`
4. Use radare2: `r2 -qc 'afl' binary`

## Common Entry Points

When `main` isn't found, try:
- `_start` - Program entry point
- `invoke_main` - C++ main wrapper
- `entry0` - Radare2 naming
- `WinMain` - Windows executables

## Caching

Decompilation results are cached. If you need to re-analyze:
```bash
rm ~/.cache/ghidra_decomp/<binary>.decomp.json
```

## Troubleshooting

### "Function not found"
- Check exact function name spelling
- Try lowercase/uppercase variants
- Use address-based lookup

### "Decompilation not available"
- Binary may be stripped
- Unsupported architecture
- Corrupted binary

### Large Functions
- Decompilation may be slow for large functions
- Consider using disassembly first for overview

## See Also

- [disassemble](../disassemble/SKILL.md) - For assembly-level analysis
- [run-command](../run-command/SKILL.md) - For running analysis tools
