---
name: finish-task
description: Finish the task assigned by the planner and return the task summary. Use this skill when you have completed your assigned task as an executor agent.
---

# Finish Task

Complete the current task and return a summary to the planner agent.

## When to use this skill

Use this skill when you are an executor agent and:
- Have completed the task assigned by the planner
- Need to report your findings back to the planner
- Want to hand control back to the planner with results

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `summary` | string | Yes | A detailed summary of the task performed |

## How to use

1. Complete the work assigned by the planner
2. Compile your findings, results, and any relevant information
3. Call this skill with a comprehensive summary
4. Control returns to the planner agent

## Examples

### Report successful analysis
```
summary: "Analysis complete. The binary 'challenge' is a 64-bit ELF executable with a buffer overflow vulnerability in the read_input() function at offset 0x1234. The vulnerability allows overwriting the return address with 136 bytes of input. The binary has no stack canaries but has NX enabled. Recommended next step: develop a ROP chain exploit."
```

### Report partial progress
```
summary: "Examined the challenge server protocol. The server expects a username followed by a password. Found that the authentication can be bypassed using SQL injection in the username field. Payload 'admin' OR '1'='1' -- grants access. Additional analysis needed to find the flag location."
```

### Report findings with code
```
summary: "Created exploit script at /home/ctfplayer/exploit.py. The script successfully exploits the format string vulnerability to leak the flag address from the stack. Running the script outputs the flag. Tested locally and confirmed working."
```

## Return format

The summary is passed back to the planner agent for further processing.

## Tips

- Be thorough in your summary - include all relevant findings
- Mention file paths of any scripts or files you created
- Include specific technical details (addresses, offsets, etc.)
- Suggest next steps if the task is part of a larger challenge
