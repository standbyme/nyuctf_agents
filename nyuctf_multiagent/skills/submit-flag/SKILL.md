---
name: submit-flag
description: Submit the flag for the CTF challenge. If the flag is correct, the challenge ends with success, else this command returns error and you can continue with the challenge.
---

# Submit Flag

Submit a flag to verify if it is the correct solution for the CTF challenge.

## When to use this skill

Use this skill when you have:
- Found what you believe is the flag
- Want to verify if a potential flag is correct
- Are ready to submit your solution

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `flag` | string | Yes | The flag to submit |

## How to use

1. Extract the flag from your analysis or exploitation
2. Submit the exact flag string including the format wrapper (e.g., `flag{...}`)
3. If correct, the challenge is marked as solved
4. If incorrect, you receive an error and can continue working

## Examples

### Submitting a standard flag
```
flag: "flag{example_flag_content}"
```

### Submitting a custom format flag
```
flag: "CTF{s0m3_f14g_h3r3}"
```

## Return format

Returns a JSON object with:
- `success: true` if the flag is correct
- `error: "Flag is wrong!"` if the flag is incorrect
- `error: "Flag not provided!"` if no flag was given

## Tips

- Make sure to include the entire flag format, not just the content
- Check the challenge description for the expected flag format
- If a flag submission fails, review your approach and try again
- Don't guess randomly - analyze the challenge thoroughly first
