#!/usr/bin/env python3
"""
Ghidra Analysis Wrapper

This script provides a unified interface for running Ghidra analysis
(decompilation and disassembly) on binary files.
"""

import json
import sys
import os
import re
import tempfile
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Dict, Any


# Configuration
GHIDRA_HOME = os.environ.get("GHIDRA_HOME", "/opt/ghidra")
CACHE_DIR = Path.home() / ".cache" / "ghidra_analysis"


def get_ghidra_headless() -> Path:
    """Get path to Ghidra headless analyzer."""
    headless = Path(GHIDRA_HOME) / "support" / "analyzeHeadless"
    if not headless.exists():
        # Try common locations
        for path in [
            "/opt/ghidra/support/analyzeHeadless",
            "/usr/share/ghidra/support/analyzeHeadless",
            Path.home() / "ghidra" / "support" / "analyzeHeadless",
        ]:
            if Path(path).exists():
                return Path(path)
    return headless


def get_script_dir() -> Path:
    """Get path to Ghidra scripts."""
    # Check for scripts in various locations
    script_locations = [
        Path(__file__).parent.parent / "ghidra_scripts",
        Path(__file__).parent.parent.parent / "nyuctf_baseline" / "ghidra_scripts",
        Path(__file__).parent.parent.parent / "docker" / "multiagent" / "ghidra_scripts",
    ]
    for loc in script_locations:
        if loc.exists():
            return loc
    return script_locations[0]  # Return first as default


def find_function(data: Dict, function: str) -> Optional[str]:
    """Find a function in the analysis data."""
    functions = data.get("functions", {})
    
    # Direct match
    if function in functions:
        return functions[function]
    
    # Try main entry point alternatives
    if function == "main":
        for alt in ["_start", "invoke_main", "entry0", "WinMain"]:
            if alt in functions:
                return functions[alt]
    
    # Radare2 address format: fcn.00401234
    if re.match(r"fcn\.[0-9a-f]+$", function):
        addr = function[4:]
        addresses = data.get("addresses", {})
        if addr in addresses:
            return functions.get(addresses[addr])
    
    return None


def run_ghidra_analysis(
    binary_path: Path,
    output_path: Path,
    script_name: str
) -> bool:
    """Run Ghidra headless analysis."""
    headless = get_ghidra_headless()
    scripts_dir = get_script_dir()
    
    if not headless.exists():
        print(f"Error: Ghidra not found at {headless}", file=sys.stderr)
        print("Set GHIDRA_HOME environment variable", file=sys.stderr)
        return False
    
    if not binary_path.exists():
        print(f"Error: Binary not found: {binary_path}", file=sys.stderr)
        return False
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [
                str(headless),
                tmpdir,
                "AnalysisProject",
                "-scriptpath", str(scripts_dir),
                "-import", str(binary_path),
                "-postscript", script_name, str(output_path),
            ],
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0 and not output_path.exists():
            print(f"Ghidra error:\n{result.stderr}", file=sys.stderr)
            return False
        
        return output_path.exists()


def decompile(binary_path: str, function: str = "main") -> Dict[str, Any]:
    """Decompile a function from a binary."""
    binary = Path(binary_path).resolve()
    
    if not binary.exists():
        return {"error": f"Binary not found: {binary_path}"}
    
    # Check cache
    cache_file = CACHE_DIR / f"{binary.name}.decomp.json"
    
    if cache_file.exists():
        try:
            data = json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            data = None
    else:
        data = None
    
    # Run Ghidra if not cached
    if data is None:
        print(f"Running Ghidra decompilation on {binary.name}...", file=sys.stderr)
        if not run_ghidra_analysis(binary, cache_file, "DecompileToJson.java"):
            return {"error": f"Decompilation failed for {binary_path}"}
        
        try:
            data = json.loads(cache_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {"error": "Failed to read decompilation output"}
    
    # Find the function
    result = find_function(data, function)
    
    if result:
        return {"decompilation": result, "function": function}
    else:
        available = list(data.get("functions", {}).keys())[:20]
        return {
            "error": f"Function '{function}' not found in {binary.name}",
            "available_functions": available,
        }


def disassemble(binary_path: str, function: str = "main") -> Dict[str, Any]:
    """Disassemble a function from a binary."""
    binary = Path(binary_path).resolve()
    
    if not binary.exists():
        return {"error": f"Binary not found: {binary_path}"}
    
    # Check cache
    cache_file = CACHE_DIR / f"{binary.name}.disas.json"
    
    if cache_file.exists():
        try:
            data = json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            data = None
    else:
        data = None
    
    # Run Ghidra if not cached
    if data is None:
        print(f"Running Ghidra disassembly on {binary.name}...", file=sys.stderr)
        if not run_ghidra_analysis(binary, cache_file, "DisassembleToJson.java"):
            return {"error": f"Disassembly failed for {binary_path}"}
        
        try:
            data = json.loads(cache_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {"error": "Failed to read disassembly output"}
    
    # Find the function
    result = find_function(data, function)
    
    if result:
        return {"disassembly": result, "function": function}
    else:
        available = list(data.get("functions", {}).keys())[:20]
        return {
            "error": f"Function '{function}' not found in {binary.name}",
            "available_functions": available,
        }


def list_functions(binary_path: str) -> Dict[str, Any]:
    """List all functions in a binary."""
    binary = Path(binary_path).resolve()
    
    if not binary.exists():
        return {"error": f"Binary not found: {binary_path}"}
    
    # Try to get from cache
    for suffix in [".decomp.json", ".disas.json"]:
        cache_file = CACHE_DIR / f"{binary.name}{suffix}"
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                functions = list(data.get("functions", {}).keys())
                return {"functions": functions, "count": len(functions)}
            except json.JSONDecodeError:
                pass
    
    # Run decompilation to get function list
    result = decompile(binary_path, "main")
    if "error" in result and "available_functions" in result:
        return {
            "functions": result["available_functions"],
            "note": "Partial list, run full analysis for complete list"
        }
    elif "error" in result:
        return result
    
    # Re-read cache for full list
    cache_file = CACHE_DIR / f"{binary.name}.decomp.json"
    if cache_file.exists():
        data = json.loads(cache_file.read_text())
        functions = list(data.get("functions", {}).keys())
        return {"functions": functions, "count": len(functions)}
    
    return {"error": "Could not list functions"}


def clear_cache(binary_path: Optional[str] = None):
    """Clear analysis cache."""
    if binary_path:
        binary = Path(binary_path).name
        for suffix in [".decomp.json", ".disas.json"]:
            cache_file = CACHE_DIR / f"{binary}{suffix}"
            if cache_file.exists():
                cache_file.unlink()
                print(f"Removed: {cache_file}")
    else:
        if CACHE_DIR.exists():
            for f in CACHE_DIR.iterdir():
                f.unlink()
                print(f"Removed: {f}")


def main():
    parser = argparse.ArgumentParser(
        description="Ghidra Analysis Wrapper for CTF Challenges"
    )
    subparsers = parser.add_subparsers(dest="command", help="Analysis command")
    
    # Decompile
    decomp = subparsers.add_parser("decompile", help="Decompile a function")
    decomp.add_argument("binary", help="Path to binary")
    decomp.add_argument("function", nargs="?", default="main", help="Function name")
    
    # Disassemble
    disasm = subparsers.add_parser("disassemble", help="Disassemble a function")
    disasm.add_argument("binary", help="Path to binary")
    disasm.add_argument("function", nargs="?", default="main", help="Function name")
    
    # List functions
    listfn = subparsers.add_parser("list", help="List functions in binary")
    listfn.add_argument("binary", help="Path to binary")
    
    # Clear cache
    clear = subparsers.add_parser("clear-cache", help="Clear analysis cache")
    clear.add_argument("binary", nargs="?", help="Binary to clear (all if omitted)")
    
    args = parser.parse_args()
    
    if args.command == "decompile":
        result = decompile(args.binary, args.function)
    elif args.command == "disassemble":
        result = disassemble(args.binary, args.function)
    elif args.command == "list":
        result = list_functions(args.binary)
    elif args.command == "clear-cache":
        clear_cache(args.binary)
        return
    else:
        parser.print_help()
        return
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
