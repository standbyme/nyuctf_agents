---
name: giveup
description: Give up this challenge to terminate it immediately. Use this to stop solving the challenge when you've exhausted all approaches.
---

# Give Up

Terminate the current CTF challenge attempt.

## When to use this skill

Use this skill when you:
- Have exhausted all possible approaches
- Cannot make further progress on the challenge
- Need to stop the current solving session

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `confirm` | boolean | No | Confirm that you want to give up (default true) |

## How to use

1. Call this skill when you want to stop working on the challenge
2. The challenge will be marked as given up
3. The session will terminate

## Examples

### Give up on a challenge
```
confirm: true
```

## Return format

Returns a JSON object with:
- `success: true` when the give up is processed

## Tips

- Only use this as a last resort
- Make sure you've tried multiple approaches before giving up
- Consider if there are other tools or techniques you haven't tried
- Review the challenge description again for any missed hints
