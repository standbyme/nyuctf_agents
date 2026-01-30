---
name: forensics
description: Digital forensics analysis techniques and methodology. Use when analyzing disk images, memory dumps, network captures, or recovering hidden/deleted data.
---

# Digital Forensics (Forensics)

Techniques and methodology for digital forensics CTF challenges.

## Pre-installed Tools

- `sleuthkit` - Disk image analysis
- `binwalk` - Firmware/file analysis
- `volatility` - Memory forensics
- `foremost` - File carving
- `steghide` - Steganography
- `exiftool` - Metadata extraction
- `xxd` - Hex viewing

## Initial Analysis

### 1. File Type Identification

```bash
docker exec $CTF_CONTAINER file ~/ctf_files/*
docker exec $CTF_CONTAINER binwalk ~/ctf_files/mystery_file
```

### 2. Strings Search

```bash
docker exec $CTF_CONTAINER strings ~/ctf_files/image | grep -i flag
docker exec $CTF_CONTAINER strings -e l ~/ctf_files/image  # Unicode
```

### 3. Metadata Extraction

```bash
docker exec $CTF_CONTAINER exiftool ~/ctf_files/image.jpg
```

## File Analysis

### Embedded Files (Binwalk)

```bash
# Scan for embedded files
docker exec $CTF_CONTAINER binwalk ~/ctf_files/file

# Extract embedded files
docker exec $CTF_CONTAINER binwalk -e ~/ctf_files/file

# Extract specific signatures
docker exec $CTF_CONTAINER binwalk -D 'png:png' ~/ctf_files/file
```

### File Carving

```bash
# Foremost
docker exec $CTF_CONTAINER foremost -i ~/ctf_files/disk.img -o ~/output/

# Scalpel (more configurable)
docker exec $CTF_CONTAINER scalpel ~/ctf_files/disk.img -o ~/output/
```

### Hex Analysis

```bash
# View hex dump
docker exec $CTF_CONTAINER xxd ~/ctf_files/file | head -50

# Search in hex
docker exec $CTF_CONTAINER xxd ~/ctf_files/file | grep -i "666c6167"  # "flag" in hex

# Edit hex
docker exec $CTF_CONTAINER hexedit ~/ctf_files/file
```

## Disk Image Analysis

### The Sleuth Kit

```bash
# Image info
docker exec $CTF_CONTAINER mmls ~/ctf_files/disk.img

# File system info
docker exec $CTF_CONTAINER fsstat ~/ctf_files/disk.img

# List files
docker exec $CTF_CONTAINER fls -r ~/ctf_files/disk.img

# Extract file by inode
docker exec $CTF_CONTAINER icat ~/ctf_files/disk.img 1234 > extracted_file
```

### Mounting Images

```bash
# Mount disk image
docker exec $CTF_CONTAINER mkdir -p /mnt/disk
docker exec $CTF_CONTAINER mount -o loop,ro ~/ctf_files/disk.img /mnt/disk

# For partitioned images
docker exec $CTF_CONTAINER losetup -fP ~/ctf_files/disk.img
docker exec $CTF_CONTAINER mount /dev/loop0p1 /mnt/disk
```

### Deleted File Recovery

```bash
# PhotoRec
docker exec $CTF_CONTAINER photorec ~/ctf_files/disk.img

# extundelete (ext filesystems)
docker exec $CTF_CONTAINER extundelete ~/ctf_files/disk.img --restore-all
```

## Memory Forensics

### Volatility 2

```bash
# Identify profile
docker exec $CTF_CONTAINER volatility -f ~/ctf_files/memory.dmp imageinfo

# Process list
docker exec $CTF_CONTAINER volatility -f ~/ctf_files/memory.dmp --profile=Win7SP1x64 pslist

# Network connections
docker exec $CTF_CONTAINER volatility -f ~/ctf_files/memory.dmp --profile=Win7SP1x64 netscan

# Command history
docker exec $CTF_CONTAINER volatility -f ~/ctf_files/memory.dmp --profile=Win7SP1x64 cmdscan

# File extraction
docker exec $CTF_CONTAINER volatility -f ~/ctf_files/memory.dmp --profile=Win7SP1x64 filescan
docker exec $CTF_CONTAINER volatility -f ~/ctf_files/memory.dmp --profile=Win7SP1x64 dumpfiles -Q 0x... -D ~/output/
```

### Volatility 3

```bash
# Windows processes
docker exec $CTF_CONTAINER vol -f ~/ctf_files/memory.dmp windows.pslist

# Linux processes
docker exec $CTF_CONTAINER vol -f ~/ctf_files/memory.dmp linux.pslist
```

## Network Forensics

### PCAP Analysis

```bash
# Tshark statistics
docker exec $CTF_CONTAINER tshark -r ~/ctf_files/capture.pcap -q -z conv,tcp

# Extract HTTP objects
docker exec $CTF_CONTAINER tshark -r ~/ctf_files/capture.pcap --export-objects http,~/output/

# Filter specific traffic
docker exec $CTF_CONTAINER tshark -r ~/ctf_files/capture.pcap -Y "http.request.method == POST"

# Follow TCP stream
docker exec $CTF_CONTAINER tshark -r ~/ctf_files/capture.pcap -q -z follow,tcp,ascii,0
```

### Wireshark Filters

```
# HTTP traffic
http
http.request.method == "POST"
http.response.code == 200

# Find strings
frame contains "flag"

# Specific host
ip.addr == 192.168.1.1
```

## Steganography

### Image Steganography

```bash
# Steghide (JPEG)
docker exec $CTF_CONTAINER steghide extract -sf ~/ctf_files/image.jpg

# Zsteg (PNG/BMP)
docker exec $CTF_CONTAINER zsteg ~/ctf_files/image.png

# LSB extraction
docker exec $CTF_CONTAINER python3 << 'EOF'
from PIL import Image
img = Image.open('image.png')
# Extract LSB
EOF

# Stegsolve (manual analysis)
docker exec $CTF_CONTAINER stegsolve ~/ctf_files/image.png
```

### Audio Steganography

```bash
# Spectrogram analysis
docker exec $CTF_CONTAINER sox ~/ctf_files/audio.wav -n spectrogram

# Audacity (visual analysis)
docker exec $CTF_CONTAINER audacity ~/ctf_files/audio.wav
```

## Archive Analysis

```bash
# ZIP file analysis
docker exec $CTF_CONTAINER zipinfo ~/ctf_files/archive.zip

# Password cracking
docker exec $CTF_CONTAINER fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt ~/ctf_files/archive.zip

# RAR analysis
docker exec $CTF_CONTAINER unrar l ~/ctf_files/archive.rar
```

## Python Analysis Script

```python
#!/usr/bin/env python3
from PIL import Image
import struct

# Read file header
with open('file', 'rb') as f:
    header = f.read(16)
    print(f"Header: {header.hex()}")
    
    # Check magic bytes
    if header[:4] == b'\x89PNG':
        print("PNG file")
    elif header[:2] == b'PK':
        print("ZIP archive")
    elif header[:2] == b'MZ':
        print("Windows executable")

# LSB extraction from image
img = Image.open('image.png')
pixels = list(img.getdata())
bits = ''.join([str(p[0] & 1) for p in pixels[:1000]])
chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
print(''.join(chars))
```

## See Also

- [run-command](../run-command/SKILL.md) - Run forensics tools
- [create-file](../create-file/SKILL.md) - Save analysis scripts
