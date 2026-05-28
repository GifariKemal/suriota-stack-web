#!/usr/bin/env python3
"""
Publish all 15 service restructure pages (EN/ID/ZH)
Usage: python publish-all-pages.py
"""

import urllib.request
import urllib.error
import json
import sys

# All page IDs to publish
PAGES = {
    'EN': [5554, 5555, 5556, 5557, 5558],
    'ID': [5566, 5567, 5568, 5569, 5570],
    'ZH': [5571, 5572, 5573, 5574, 5575],
}

def read_cookie():
    with open('cookies.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) >= 7 and 'wordpress_logged_in' in parts[5]:
                return f'{parts[5]}={parts[6]}'
    return None

def fetch_nonce(cookie):
    req = urllib.request.Request(
        'https://suriota.com/wp-admin/admin-ajax.php?action=rest-nonce',
        headers={'Cookie': cookie}
    )
    resp = urllib.request.urlopen(req, timeout=30)
    return resp.read().decode().strip()

def publish_page(page_id, nonce, cookie):
    payload = json.dumps({'status': 'publish'}).encode('utf-8')
    req = urllib.request.Request(
        f'https://suriota.com/wp-json/wp/v2/pages/{page_id}',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'X-WP-Nonce': nonce,
            'Cookie': cookie,
        },
        method='POST'
    )
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read().decode())
        return True, data.get('slug'), data.get('link')
    except urllib.error.HTTPError as e:
        return False, str(e.code), e.read().decode()[:200]

def main():
    cookie = read_cookie()
    if not cookie:
        print('ERROR: No wordpress_logged_in cookie found')
        sys.exit(1)
    
    nonce = fetch_nonce(cookie)
    print(f'Nonce: {nonce}')
    
    success = 0
    failed = 0
    
    for lang, ids in PAGES.items():
        print(f'\n=== Publishing {lang} pages ===')
        for page_id in ids:
            ok, slug, link = publish_page(page_id, nonce, cookie)
            if ok:
                print(f'  ID {page_id}: PUBLISHED -> {link}')
                success += 1
            else:
                print(f'  ID {page_id}: FAILED ({slug})')
                failed += 1
    
    print(f'\n=== Summary ===')
    print(f'Success: {success}')
    print(f'Failed: {failed}')

if __name__ == '__main__':
    main()
