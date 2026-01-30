#!/usr/bin/env python3
"""
Ghidra Disassembly Script for CTF Challenges

This script uses Ghidra's headless analyzer to disassemble binary functions.
It caches results for faster subsequent lookups.
"""

import json
import sys
import os
import re
import tempfile
import subprocess
from pathlib import Path

# Configuration
GHIDRA_HOME = os.environ.get("GHIDRA_HOME", "/opt/ghidra")
GHIDRA_HEADLESS = Path(GHIDRA_HOME) / "support" / "analyzeHeadless"
SCRIPT_DIR = Path(__file__).parent.parent.parent.parent
GHIDRA_SCRIPTS = SCRIPT_DIR / "ghidra_scripts"
CACHE_DIR = Path.home() / ".cache" / "ghidra_decomp"


def find_function(disasm_data: dict, function: str) -> dict | None:
    """Find a function in the disassembly data."""
    functions = disasm_data.get("functions", {})
    
    # Direct match
    if function in functions:
        return functions[function]
    
    # Try main entry point alternatives
    if function == "main":
        for alt in ["_start", "invoke_main", "entry0"]:
            if alt in functions:
                return functions[alt]
    
    # Radare2 address format: fcn.00401234
    if re.match(r"fcn\.[0-9a-f]+$", function):
        addr = function[4:]
        addresses = disasm_data.get("addresses", {})
        if addr in addresses:
            return functions.get(addresses[addr])
    
    return None


def run_ghidra(binary_path: Path, output_path: Path) -> bool:
    """Run Ghidra headless analyzer to disassemble binary."""
    if not GHIDRA_HEADLESS.exists():
        print(f"Error: Ghidra not found at {GHIDRA_HEADLESS}", file=sys.stderr)
        return False
    
    if not binary_path.exists():
        print(f"Error: Binary not found at {binary_path}", file=sys.stderr)
        return False
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [
                str(GHIDRA_HEADLESS),
                tmpdir,
                "DisasmProject",
                "-scriptpath", str(GHIDRA_SCRIPTS),
                "-import", str(binary_path),
                "-postscript", "DisassembleToJson.java", str(output_path),
            ],
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0:
            print(f"Ghidra error: {result.stderr}", file=sys.stderr)
        
        return output_path.exists()


def disassemble(binary_path: str, function: str = "main") -> dict:
    """Disassemble a function from a binary."""
    binary = Path(binary_path).resolve()
    
    if not binary.exists():
        return {"error": f"Binary not found: {binary_path}"}
    
    # Check cache
    cache_file = CACHE_DIR / f"{binary.name}.disas.json"
    
    if cache_file.exists():
        try:
            disasm_data = json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            disasm_data = None
    else:
        disasm_data = None
    
    # Run Ghidra if not cached
    if disasm_data is None:
        print(f"Running Ghidra disassembly on {binary.name}...", file=sys.stderr)
        if not run_ghidra(binary, cache_file):
            return {"error": f"Disassembly failed for {binary_path}"}
        
        try:
            disasm_data = json.loads(cache_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {"error": f"Failed to read disassembly output"}
    
    # Find the function
    result = find_function(disasm_data, function)
    
    if result:
        return {"disassembly": result}
    else:
        available = list(disasm_data.get("functions", {}).keys())[:20]
        return {
            "error": f"Function '{function}' not found in {binary.name}",
            "available_functions": available,
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: ghidra_disassemble.py <binary_path> [function_name]")
        print("  binary_path: Path to the binary file")
        print("  function_name: Name of function to disassemble (default: main)")
        sys.exit(1)
    
    binary_path = sys.argv[1]
    function = sys.argv[2] if len(sys.argv) > 2 else "main"
    
    result = disassemble(binary_path, function)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
