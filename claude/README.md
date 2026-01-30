# NYU CTF Agent Skills for Claude Code

This directory contains Claude Code skills for autonomous CTF (Capture The Flag) challenge solving. These skills are refactored from the original `nyuctf_baseline` framework to work with Claude Code's agent system.

## Overview

The D-CIPHER framework has been adapted into modular Agent Skills following the [Agent Skills](https://agentskills.io) open standard. These skills enable Claude Code to solve CTF challenges across multiple categories:

- **Pwn** (Binary Exploitation)
- **Rev** (Reverse Engineering)
- **Crypto** (Cryptography)
- **Web** (Web Security)
- **Forensics** (Digital Forensics)
- **Misc** (Miscellaneous)

## Directory Structure

```
claude/
├── CLAUDE.md                    # Project-level context for Claude Code
├── README.md                    # This file
├── skills/
│   ├── ctf-solve/              # Main CTF solving orchestration skill
│   │   └── SKILL.md
│   ├── run-command/            # Execute commands in CTF environment
│   │   └── SKILL.md
│   ├── decompile/              # Binary decompilation with Ghidra
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── ghidra_decompile.py
│   ├── disassemble/            # Binary disassembly with Ghidra
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── ghidra_disassemble.py
│   ├── check-flag/             # Flag verification
│   │   └── SKILL.md
│   ├── create-file/            # Create files in CTF environment
│   │   └── SKILL.md
│   ├── give-up/                # Give up on challenge
│   │   └── SKILL.md
│   ├── pwn/                    # Binary exploitation guidance
│   │   └── SKILL.md
│   ├── rev/                    # Reverse engineering guidance
│   │   └── SKILL.md
│   ├── crypto/                 # Cryptography guidance
│   │   └── SKILL.md
│   ├── web/                    # Web security guidance
│   │   └── SKILL.md
│   ├── forensics/              # Digital forensics guidance
│   │   └── SKILL.md
│   └── misc/                   # Miscellaneous challenges
│       └── SKILL.md
└── scripts/
    ├── setup_ctf_env.sh        # Setup CTF Docker environment
    ├── docker_exec.py          # Execute commands in Docker container
    └── ghidra_wrapper.py       # Ghidra analysis wrapper
```

## Installation

### 1. Copy skills to Claude Code

Copy the skills to your Claude Code skills directory:

```bash
# For personal skills (available across all projects)
cp -r skills/* ~/.claude/skills/

# Or for project-specific skills
cp -r skills/* .claude/skills/
```

### 2. Copy CLAUDE.md for project context

```bash
cp CLAUDE.md /path/to/your/ctf/workspace/.claude/CLAUDE.md
```

### 3. Setup CTF Environment

The CTF environment requires Docker. Run from the repository root (`nyuctf_agents/`):

```bash
# Build the CTF environment Docker image
docker build -t ctfenv -f docker/baseline/Dockerfile .

# Create the CTF network
docker network create ctfnet
```

## Usage

### Solving a CTF Challenge

Invoke the main skill directly:

```
/ctf-solve
```

Or let Claude automatically detect when you're working on a CTF:

```
I need to solve this CTF challenge. The category is pwn, and the binary is in ~/ctf_files/
```

### Individual Skills

You can also use individual skills:

```
/run-command ls -la ~/ctf_files/
/decompile ~/ctf_files/binary main
/check-flag flag{example}
```

### Category-Specific Guidance

Category skills are automatically loaded based on the challenge type:

- `/pwn` - Binary exploitation techniques
- `/rev` - Reverse engineering workflow
- `/crypto` - Cryptographic analysis
- `/web` - Web security testing
- `/forensics` - Digital forensics analysis

## Environment Variables

Set these in your shell or `.env` file:

```bash
# CTF Docker container image
export CTF_CONTAINER_IMAGE=ctfenv

# CTF Docker network
export CTF_NETWORK=ctfnet

# Path to Ghidra installation
export GHIDRA_HOME=/path/to/ghidra

# Flag format (regex pattern)
export CTF_FLAG_FORMAT="flag{.*}"
```

## Extending

### Adding New Skills

Create a new skill directory with `SKILL.md`:

```bash
mkdir -p ~/.claude/skills/my-ctf-skill
```

Create `~/.claude/skills/my-ctf-skill/SKILL.md`:

```yaml
---
name: my-ctf-skill
description: Description of what this skill does
---

Instructions for Claude...
```

### Custom Scripts

Add executable scripts to `scripts/` directory within the skill folder. Reference them in your `SKILL.md`.

## Migration from nyuctf_baseline

This implementation replaces the following components from `nyuctf_baseline`:

| Original Component | Claude Code Equivalent |
|-------------------|----------------------|
| `tools/tools.py` (CommandExec) | `skills/run-command/` |
| `tools/tools.py` (Decompile) | `skills/decompile/` |
| `tools/tools.py` (Disassemble) | `skills/disassemble/` |
| `tools/tools.py` (CheckFlag) | `skills/check-flag/` |
| `tools/tools.py` (CreateFile) | `skills/create-file/` |
| `prompts/templates/` | `CLAUDE.md` + category skills |
| `environment.py` | `scripts/docker_exec.py` |
| `conversation.py` | Claude Code's native conversation |

## References

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills.md)
- [Agent Skills Specification](https://agentskills.io/specification.md)
- [Original D-CIPHER Paper](../paper.tex)
