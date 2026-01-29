---
name: delegate
description: Delegate a task to an executor LLM agent. The executor agent is fully autonomous and equipped with various tools for CTF challenges.
---

# Delegate

Delegate a task to an executor agent in a multi-agent system.

## When to use this skill

Use this skill when you are the planner agent and need to:
- Assign a specific task to an executor agent
- Break down the challenge into manageable sub-tasks
- Have detailed analysis or exploitation performed

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task` | string | Yes | A detailed task description |

## How to use

1. Analyze the CTF challenge and identify what needs to be done
2. Formulate a clear, detailed task description
3. Delegate the task to the executor agent
4. Wait for the executor to complete and return results

## Examples

### Delegate binary analysis
```
task: "Analyze the binary file 'challenge' in the ctf_files folder. Identify the main function, look for vulnerabilities such as buffer overflows or format string bugs, and report your findings."
```

### Delegate exploit development
```
task: "Develop an exploit for the buffer overflow vulnerability identified in the 'challenge' binary. The vulnerability is in the read_input function. Create a Python script using pwntools to exploit it and retrieve the flag."
```

### Delegate network reconnaissance
```
task: "Connect to the challenge server at challenge.server:1234 and analyze the protocol. Document the expected inputs and outputs, and identify any potential vulnerabilities."
```

## Return format

Returns a JSON object containing the executor's summary of the completed task.

## Tips

- Provide detailed, specific task descriptions
- Include relevant context from previous analysis
- Break complex challenges into smaller, focused tasks
- The executor has access to tools like run_command, create_file, disassemble, and decompile
