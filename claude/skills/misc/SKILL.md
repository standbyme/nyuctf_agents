---
name: misc
description: Miscellaneous CTF challenge techniques. Use for OSINT, encoding puzzles, esoteric languages, networking, and challenges that don't fit other categories.
---

# Miscellaneous (Misc)

Techniques for miscellaneous CTF challenges including OSINT, encoding, esoteric languages, and general puzzles.

## Common Challenge Types

### Encoding/Decoding

```bash
# Base64
docker exec $CTF_CONTAINER base64 -d <<< "ZmxhZ3t0ZXN0fQ=="

# Base32
docker exec $CTF_CONTAINER base32 -d <<< "MZWGCZ33..."

# Hex
docker exec $CTF_CONTAINER xxd -r -p <<< "666c6167"

# URL encoding
docker exec $CTF_CONTAINER python3 -c "from urllib.parse import unquote; print(unquote('%66%6c%61%67'))"

# ROT13
docker exec $CTF_CONTAINER tr 'A-Za-z' 'N-ZA-Mn-za-m' <<< "message"
```

**Python Encoding Toolkit**:
```python
#!/usr/bin/env python3
import base64
import binascii
from urllib.parse import quote, unquote

data = "YOUR_DATA_HERE"

# Base encodings
print("Base64:", base64.b64encode(data.encode()))
print("Base32:", base64.b32encode(data.encode()))
print("Hex:", data.encode().hex())

# Decode attempts
def try_decode(data):
    decoders = [
        ('base64', lambda x: base64.b64decode(x)),
        ('base32', lambda x: base64.b32decode(x)),
        ('hex', lambda x: bytes.fromhex(x)),
        ('url', lambda x: unquote(x).encode()),
    ]
    for name, decoder in decoders:
        try:
            result = decoder(data)
            print(f"{name}: {result}")
        except:
            pass
```

### QR Codes & Barcodes

```bash
# Decode QR code
docker exec $CTF_CONTAINER zbarimg ~/ctf_files/qr.png

# Generate QR code
docker exec $CTF_CONTAINER qrencode -o output.png "data"

# Multiple QR codes
docker exec $CTF_CONTAINER bash -c 'for f in *.png; do zbarimg "$f" 2>/dev/null; done'
```

### Esoteric Languages

**Brainfuck**:
```bash
# Run brainfuck
docker exec $CTF_CONTAINER beef ~/ctf_files/program.bf
```

**Ook/Whitespace/Malbolge**:
```bash
# Use online interpreters or dedicated tools
# https://esolangs.org/wiki/
```

**Piet** (color-based language):
```bash
docker exec $CTF_CONTAINER npiet ~/ctf_files/image.png
```

### OSINT (Open Source Intelligence)

**Techniques**:
- Reverse image search (Google, TinEye, Yandex)
- Username search (namechk.com, whatsmyname.app)
- Domain/IP lookup (whois, dig, nslookup)
- Social media investigation
- Wayback Machine (archive.org)
- EXIF data analysis

```bash
# Domain info
docker exec $CTF_CONTAINER whois example.com
docker exec $CTF_CONTAINER dig example.com ANY

# SSL certificate
docker exec $CTF_CONTAINER openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -text

# Wayback Machine
curl "http://archive.org/wayback/available?url=example.com"
```

### Number Systems

```python
# Binary/Octal/Decimal/Hex conversions
n = 0x41
print(f"Decimal: {n}")
print(f"Binary: {bin(n)}")
print(f"Octal: {oct(n)}")
print(f"Hex: {hex(n)}")
print(f"ASCII: {chr(n)}")

# Multiple number bases in sequence
data = "65 66 67"  # Decimal ASCII
result = ''.join(chr(int(x)) for x in data.split())
print(result)  # ABC
```

### Morse Code

```python
MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.'
}
MORSE_REV = {v: k for k, v in MORSE.items()}

def decode_morse(code):
    words = code.split('   ')
    return ' '.join(''.join(MORSE_REV.get(c, '?') for c in word.split()) for word in words)
```

### Scripting/Automation

**pwntools for networking**:
```python
from pwn import *

# TCP connection
io = remote('challenge.server', 1337)

# Receive until prompt
io.recvuntil(b'> ')

# Send data
io.sendline(b'answer')

# Interactive mode
io.interactive()
```

**Solving with regex**:
```python
import re
import requests

resp = requests.get('http://challenge.server/')
# Extract flag from response
match = re.search(r'flag\{[^}]+\}', resp.text)
if match:
    print(match.group())
```

### Jail Escapes

**Python jail**:
```python
# Get builtins
().__class__.__base__.__subclasses__()

# File read
''.__class__.__mro__[1].__subclasses__()[40]('flag.txt').read()

# Command execution
__import__('os').system('cat flag.txt')
```

**Bash jail**:
```bash
# Without certain characters
$0       # Run shell
$'\x63\x61\x74'   # cat in hex
/???/??t /???/p????d   # cat /etc/passwd
```

### Pyjails Online Resources

- [PayloadsAllTheThings - Python](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization/Python)
- [HackTricks - Python Sandbox Escape](https://book.hacktricks.xyz/misc/basic-python/bypass-python-sandboxes)

## Tools Reference

| Task | Tool |
|------|------|
| QR codes | zbarimg, qrencode |
| Barcodes | zbarimg |
| Encoding | CyberChef, dcode.fr |
| OSINT | theHarvester, Maltego |
| Networking | netcat, nmap |
| Automation | pwntools, requests |

## See Also

- [run-command](../run-command/SKILL.md) - Execute tools
- [create-file](../create-file/SKILL.md) - Save scripts
