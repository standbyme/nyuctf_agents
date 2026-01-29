---
name: generate-prompt
description: Generate a prompt for the Planner agent to solve the CTF challenge. Used by the auto-prompter to create customized prompts.
---

# Generate Prompt

Generate a customized prompt for the planner agent based on challenge analysis.

## When to use this skill

Use this skill when you are the auto-prompter agent and:
- Have analyzed the CTF challenge
- Want to create a tailored prompt for the planner
- Need to provide context-specific guidance

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The prompt for the Planner agent |

## How to use

1. Analyze the challenge using available tools
2. Identify the challenge type, complexity, and approach
3. Generate a comprehensive prompt with relevant guidance
4. The prompt will be used to initialize the planner agent

## Examples

### Generate prompt for a pwn challenge
```
prompt: |
  This is a binary exploitation challenge. The binary has a buffer overflow 
  vulnerability. Key observations:
  - 64-bit ELF with NX enabled but no PIE or canaries
  - Vulnerable function: gets() in main
  - Buffer size: 64 bytes before return address
  
  Recommended approach:
  1. Leak libc address using puts@GOT
  2. Calculate system() and "/bin/sh" addresses
  3. Build ROP chain to call system("/bin/sh")
  4. Extract the flag from the shell
```

### Generate prompt for a crypto challenge
```
prompt: |
  This is a cryptography challenge involving RSA. Key observations:
  - Small public exponent e=3
  - Three ciphertexts encrypted with the same message
  - Classic Hastad's broadcast attack scenario
  
  Recommended approach:
  1. Use Chinese Remainder Theorem to combine ciphertexts
  2. Take the cube root of the result
  3. Convert the integer to bytes to reveal the flag
```

## Return format

The generated prompt is passed to the planner agent to guide its solving approach.

## Tips

- Include specific technical observations from your analysis
- Provide a clear recommended approach
- Mention any tools or techniques that might be useful
- Highlight potential pitfalls or edge cases
