---
name: crypto
description: Cryptographic analysis techniques and methodology. Use when solving challenges involving encryption, hashing, number theory, or cryptographic protocols.
---

# Cryptography (Crypto)

Techniques and methodology for cryptography CTF challenges.

## Pre-installed Tools

- `gmpy2` - Fast arbitrary precision arithmetic
- `sagemath` - Mathematical software system
- `pycryptodome` - Cryptographic library
- `sympy` - Symbolic mathematics
- `z3-solver` - SMT solver

## Initial Analysis

### 1. Identify Cryptosystem

```python
# Check for common patterns
# - Large numbers suggest RSA/DH
# - Repeated blocks suggest ECB mode
# - IV present suggests CBC mode
# - Known ciphertext length patterns
```

### 2. Analyze Given Data

```bash
docker exec $CTF_CONTAINER python3 << 'EOF'
import json

# Load challenge data
with open('challenge.json') as f:
    data = json.load(f)

# Analyze key sizes, formats
for key, value in data.items():
    if isinstance(value, int):
        print(f"{key}: {value.bit_length()} bits")
    elif isinstance(value, str):
        print(f"{key}: {len(value)} chars")
EOF
```

## Common Cryptosystems

### RSA

**Parameters**:
- `n = p * q` (modulus)
- `e` (public exponent, often 65537)
- `d` (private exponent)
- `c = m^e mod n` (ciphertext)

**Common Attacks**:

```python
from Crypto.Util.number import long_to_bytes, inverse
import gmpy2

# Small e attack (e=3)
if e == 3:
    m = gmpy2.iroot(c, 3)[0]
    print(long_to_bytes(m))

# Common modulus attack
# Same n, different e values
def common_modulus(n, e1, c1, e2, c2):
    g, s, t = gmpy2.gcdext(e1, e2)
    m = (pow(c1, s, n) * pow(c2, t, n)) % n
    return long_to_bytes(m)

# Fermat factorization (p, q close)
def fermat_factor(n):
    a = gmpy2.isqrt(n) + 1
    b2 = a*a - n
    while not gmpy2.is_square(b2):
        a += 1
        b2 = a*a - n
    b = gmpy2.isqrt(b2)
    return a-b, a+b

# Wiener's attack (small d)
# Use: https://github.com/pablocelayes/rsa-wiener-attack

# Hastad's broadcast attack (same m, different n)
from sympy.ntheory.modular import crt
def hastad(pairs, e):
    ns, cs = zip(*pairs)
    c_combined = crt(ns, cs)[0]
    m = gmpy2.iroot(c_combined, e)[0]
    return long_to_bytes(m)
```

### AES

**Analysis**:
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ECB mode - same plaintext blocks = same ciphertext
def detect_ecb(ciphertext, block_size=16):
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    return len(blocks) != len(set(blocks))

# CBC padding oracle
def padding_oracle_attack(ciphertext, oracle):
    # Implement byte-by-byte decryption
    pass

# CBC bit flipping
def cbc_bitflip(ciphertext, position, original, target):
    c = bytearray(ciphertext)
    c[position - 16] ^= original ^ target
    return bytes(c)
```

### XOR Cipher

```python
# Single-byte XOR
def single_byte_xor(data):
    for key in range(256):
        result = bytes([b ^ key for b in data])
        if result.isascii():
            print(f"Key {key}: {result}")

# Repeating key XOR
def repeating_key_xor(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

# Finding key length (Kasiski/Friedman)
def find_key_length(ciphertext):
    # Look for repeated patterns
    pass
```

### Hash Functions

```python
# Length extension attack (MD5, SHA1, SHA256)
import hashpumpy
new_hash, new_msg = hashpumpy.hashpump(
    original_hash,
    original_data,
    data_to_add,
    secret_key_length
)

# Hash collision (MD5)
# Use hashclash or other tools

# Rainbow tables
# Use online services or generate with rtgen
```

## SageMath Solutions

```python
# Run in SageMath
docker exec $CTF_CONTAINER sage << 'EOF'
# Discrete log
p = 0x...
g = 2
h = 0x...  # h = g^x mod p
x = discrete_log(h, Mod(g, p))
print(x)

# Elliptic curve discrete log
E = EllipticCurve(GF(p), [a, b])
G = E(Gx, Gy)
P = E(Px, Py)
n = G.discrete_log(P)
print(n)

# Lattice attacks (LLL)
M = matrix([
    [1, 0, v1],
    [0, 1, v2],
    [0, 0, n]
])
reduced = M.LLL()
EOF
```

## Z3 Solver

```python
from z3 import *

# Solving for unknown values
s = Solver()
x = BitVec('x', 32)
y = BitVec('y', 32)

s.add(x ^ y == 0x12345678)
s.add(x + y == 0xdeadbeef)

if s.check() == sat:
    m = s.model()
    print(f"x = {m[x]}, y = {m[y]}")
```

## Online Resources

- [factordb.com](http://factordb.com) - Factor known numbers
- [dcode.fr](https://www.dcode.fr) - Classical ciphers
- [CyberChef](https://gchq.github.io/CyberChef/) - Data transformations
- [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool) - RSA attacks

## Python Template

```python
#!/usr/bin/env python3
from Crypto.Util.number import *
from pwn import *
import gmpy2

# Load challenge data
n = 0x...
e = 0x10001
c = 0x...

# Attack implementation
# ...

# Decrypt
m = pow(c, d, n)
flag = long_to_bytes(m)
print(flag)
```

## See Also

- [run-command](../run-command/SKILL.md) - Run crypto scripts
- [create-file](../create-file/SKILL.md) - Save exploit scripts
