#!/usr/bin/env python3
"""Dry-run: show what would change for first N posts. NO writes."""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\Users\Administrator\Music\Website Suriota')
import json
import re
from _batch_process import (
    INPUT_FILE,
    EXCLUDE_IDS,
    apply_internal_links,
    apply_filler_removal,
    apply_connector_cleanup,
)

with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

print(f'Total: {len(posts)}')
shown = 0
for post in posts:
    pid = post.get('id')
    slug = post.get('slug', '')
    if pid in EXCLUDE_IDS:
        continue
    content_obj = post.get('content', {})
    content = content_obj.get('raw', '') if isinstance(content_obj, dict) else str(content_obj)
    original = content
    log = []
    lk = []
    content = apply_internal_links(content, lk)
    if lk:
        log.append(f'+{len(lk)} link(s): ' + ', '.join(f'"{a}"→{u}' for a, u in lk))
    content = apply_filler_removal(content, log)
    content = apply_connector_cleanup(content, log)
    if content != original:
        shown += 1
        print(f'\n=== POST {pid} [{slug}] ===')
        print('CHANGES:', '; '.join(log))
        # Show first diff snippet
        for i, (a, b) in enumerate(zip(original.split('\n'), content.split('\n'))):
            if a != b:
                print(f'  - OLD: {a[:200]}')
                print(f'  + NEW: {b[:200]}')
        if shown >= 5:
            break

print(f'\n(showed {shown} posts that would change)')
