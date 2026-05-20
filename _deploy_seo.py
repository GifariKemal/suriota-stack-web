import json, urllib.request, urllib.error, base64, time, sys

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

def req(url, method='GET', payload=None):
    data = json.dumps(payload).encode() if payload else None
    r = urllib.request.Request(url, data=data, method=method, headers=HDRS)
    try:
        return urllib.request.urlopen(r, timeout=60).read().decode()
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:500]}"

# Read PHP snippet code
with open('_seo_v4.php', 'r', encoding='utf-8') as f:
    code = f.read()

print(f"PHP snippet size: {len(code)} chars")

# Try Code Snippets REST API
endpoints = [
    ('https://suriota.com/wp-json/code-snippets/v1/snippets/5', 'POST'),
    ('https://suriota.com/wp-json/code-snippets/v1/snippets/5', 'PUT'),
]

# First GET to verify snippet exists
print("\n[1] GET snippet 5...")
r = req('https://suriota.com/wp-json/code-snippets/v1/snippets/5')
print(r[:300])

# Update code via POST
print("\n[2] POST snippet 5 with new code...")
r = req('https://suriota.com/wp-json/code-snippets/v1/snippets/5', method='POST', payload={
    'code': code,
    'active': True,
    'name': 'SX: SEO v4 deploy slot'
})
print(r[:500])

# Activate
print("\n[3] Activate snippet 5...")
r = req('https://suriota.com/wp-json/code-snippets/v1/snippets/5/activate', method='POST', payload={})
print(r[:500])

# Trigger by visiting frontend
print("\n[4] Trigger via frontend visit...")
time.sleep(2)
trigger = urllib.request.Request('https://suriota.com/?seo_trigger=1', headers={'User-Agent': 'Mozilla/5.0'})
try:
    urllib.request.urlopen(trigger, timeout=30).read()
    print("Frontend hit OK")
except Exception as e:
    print(f"Trigger error: {e}")

# Check log
print("\n[5] Check log file...")
time.sleep(2)
log_url = 'https://suriota.com/wp-content/uploads/seo-v4.txt'
try:
    log = urllib.request.urlopen(log_url, timeout=15).read().decode()
    print(log)
except Exception as e:
    print(f"Log not found: {e}")
