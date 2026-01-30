---
name: check-flag
description: Verify if a captured flag is correct for the CTF challenge. Use when you have found a potential flag and want to check if it matches the expected flag format and value.
---

# Check Flag

Verify if a flag is correct for the current CTF challenge.

## Usage

To check a flag, compare it against the expected flag stored in the challenge configuration.

## How to Check

1. The flag should match the expected format (e.g., `flag{...}`, `CTF{...}`)
2. Compare the flag value exactly (case-sensitive)

## Flag Verification Script

```bash
# Check if flag matches expected value
EXPECTED_FLAG="${CTF_EXPECTED_FLAG}"
PROVIDED_FLAG="$ARGUMENTS"

if [ "$PROVIDED_FLAG" = "$EXPECTED_FLAG" ]; then
    echo "✓ Correct flag!"
    echo "Flag: $PROVIDED_FLAG"
else
    echo "✗ Incorrect flag"
    echo "Provided: $PROVIDED_FLAG"
    # Don't reveal expected flag
fi
```

## Common Flag Formats

- `flag{...}` - Most common format
- `CTF{...}` - Competition-specific
- `picoCTF{...}` - picoCTF format
- `HTB{...}` - HackTheBox format
- Custom formats specified in challenge description

## Before Checking

1. Make sure you have the complete flag
2. Check for trailing whitespace or newlines
3. Verify encoding (base64, hex, etc.) is decoded
4. Look for multi-part flags that need combining

## Examples

```
Good: flag{th1s_1s_th3_fl4g}
Bad:  flag{th1s_1s_th3_fl4g}   (trailing space)
Bad:  FLAG{th1s_1s_th3_fl4g}   (wrong case)
Bad:  th1s_1s_th3_fl4g         (missing wrapper)
```

## After Finding the Flag

1. Document how you found it
2. Save your exploit/solution
3. Note any interesting techniques used
