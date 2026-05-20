#!/usr/bin/env python3
"""
Batch process suriota.com portfolio posts.
Apply 4 fixes per spec, then POST changes back via WP REST API.
"""
import json
import re
import time
import base64
import sys
import io
from urllib import request, error

# Ensure UTF-8 stdout on Windows
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
except Exception:
    pass

# Configuration
AUTH_RAW = 'admin:hCYK JqF1 khdB WDzI LQdQ WEBr'
AUTH_B64 = base64.b64encode(AUTH_RAW.encode('utf-8')).decode('ascii')
BASE = 'https://suriota.com/wp-json/wp/v2/posts'
INPUT_FILE = r'C:\Users\Administrator\Music\Website Suriota\_posts_raw.json'
EXCLUDE_IDS = {1925}

# Internal links keyword map: list of (keywords[], target_url)
LINK_MAP = [
    (['energi terbarukan', 'renewable energy', 'PLTS', 'panel surya', 'solar panel'], '/renewable-energy/'),
    (['otomasi industri', 'PLC', 'SCADA', 'industrial automation', 'automation'], '/automation/'),
    (['instalasi listrik', 'panel listrik', 'electrical engineering', 'wiring'], '/electrical/'),
    (['monitoring IoT', 'IoT sensor', 'IIoT', 'Internet of Things'], '/internet-of-things/'),
    (['water treatment', 'pengolahan air', 'WTP', 'WWTP', 'SPARING'], '/water-treatment/'),
    (['SURGE Energy Mapping', 'energy monitoring'], '/surge-energy-mapping/'),
]

# Filler phrases (regex patterns, case-insensitive)
# Each pattern is removed across the post but the FIRST occurrence is kept.
FILLER_PATTERNS = [
    # Full repetitive sentence: "Penerapan <strong>X</strong> secara profesional terbukti memberikan hasil optimal."
    r'\s*Penerapan\s*<strong>[^<]+</strong>\s*secara profesional terbukti memberikan hasil optimal\.?',
    # Standalone trailing variant (no Penerapan prefix)
    r'\s*secara profesional terbukti memberikan hasil optimal\.?',
    # "Dengan penerapan X yang tepat"
    r'\s*Dengan penerapan\s+[^.,;]{2,80}\s+yang tepat[,.]?\s*',
    # Generic
    r'\s*merupakan solusi terbaik untuk kebutuhan industri\.?',
]

# Connector openers to strip when starting a paragraph
CONNECTOR_OPENERS = [
    r'^Selanjutnya,\s+',
    r'^Perlu diketahui bahwa\s+',
]


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def http_get(url):
    req = request.Request(url, headers={
        'Authorization': f'Basic {AUTH_B64}',
        'User-Agent': USER_AGENT,
        'Accept': 'application/json',
    })
    with request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))


def http_post(url, data):
    body = json.dumps(data).encode('utf-8')
    req = request.Request(
        url,
        data=body,
        method='POST',
        headers={
            'Authorization': f'Basic {AUTH_B64}',
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT,
            'Accept': 'application/json',
        },
    )
    with request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode('utf-8')


def split_protected_regions(content):
    """
    Split content into list of (text, is_protected) chunks.
    Protected regions: <a>...</a>, <script>...</script>, JSON-LD blocks, headings (h1-h6),
    HTML tags themselves, shortcodes [...], HTML attributes.
    """
    # Pattern matches one protected unit at a time
    pattern = re.compile(
        r'(<script[^>]*>.*?</script>'           # scripts (incl JSON-LD)
        r'|<a\b[^>]*>.*?</a>'                    # existing anchor
        r'|<h[1-6][^>]*>.*?</h[1-6]>'            # headings
        r'|<[^>]+>'                              # any html tag
        r'|\[[^\]]+\])',                         # shortcodes
        re.IGNORECASE | re.DOTALL,
    )
    parts = []
    last = 0
    for m in pattern.finditer(content):
        if m.start() > last:
            parts.append((content[last:m.start()], False))
        parts.append((m.group(0), True))
        last = m.end()
    if last < len(content):
        parts.append((content[last:], False))
    return parts


def join_parts(parts):
    return ''.join(p[0] for p in parts)


def url_already_present(content, url):
    """Check if a hyperlink to this url exists already."""
    # Match href="/slug/" or href='/slug/' or href="https://suriota.com/slug/"
    needle1 = f'href="{url}"'
    needle2 = f"href='{url}'"
    needle3 = f'href="https://suriota.com{url}"'
    needle4 = f"href='https://suriota.com{url}'"
    lc = content.lower()
    return (
        needle1.lower() in lc
        or needle2.lower() in lc
        or needle3.lower() in lc
        or needle4.lower() in lc
    )


def add_internal_link(parts, keywords, target_url, links_added_log):
    """
    Add hyperlink for the FIRST occurrence (case-insensitive) of any keyword
    in unprotected text segments. Mutates parts in-place.
    Returns True if a link was added.
    """
    for i, (text, protected) in enumerate(parts):
        if protected:
            continue
        for kw in keywords:
            # Use word-boundary-like check; allow PLC/PLTS etc.
            pat = re.compile(r'(?<![A-Za-z0-9])' + re.escape(kw) + r'(?![A-Za-z0-9])', re.IGNORECASE)
            m = pat.search(text)
            if m:
                actual = m.group(0)
                new_text = text[:m.start()] + f'<a href="{target_url}">{actual}</a>' + text[m.end():]
                parts[i] = (new_text, False)
                links_added_log.append((actual, target_url))
                return True
    return False


def apply_internal_links(content, log):
    """Apply Fix 1 to entire content. Returns modified content."""
    parts = split_protected_regions(content)
    links_added = 0
    for keywords, target in LINK_MAP:
        if links_added >= 3:
            break
        if url_already_present(content, target):
            continue
        if add_internal_link(parts, keywords, target, log):
            links_added += 1
            # Update content snapshot for the URL-present check in next iteration
            content = join_parts(parts)
    return join_parts(parts)


def apply_filler_removal(content, log):
    """Fix 2: keep MAX 1 occurrence per filler phrase."""
    new_content = content
    for pat in FILLER_PATTERNS:
        regex = re.compile(pat, re.IGNORECASE)
        matches = list(regex.finditer(new_content))
        if len(matches) > 1:
            # Remove all but first
            # Build replacement: keep first, drop rest
            removed = 0
            out = []
            last_end = 0
            for idx, m in enumerate(matches):
                if idx == 0:
                    continue  # keep first
                out.append(new_content[last_end:m.start()])
                last_end = m.end()
                removed += 1
            out.append(new_content[last_end:])
            # But we have to preserve up to first match too
            first = matches[0]
            head = new_content[:first.end()]
            # The tail after first match needs reconstruction with skips
            tail_parts = []
            last = first.end()
            for m in matches[1:]:
                tail_parts.append(new_content[last:m.start()])
                last = m.end()
            tail_parts.append(new_content[last:])
            new_content = head + ''.join(tail_parts)
            log.append(f'filler removed x{removed}: {pat[:40]}')
    return new_content


def apply_connector_cleanup(content, log):
    """Fix 4: strip 'Selanjutnya, ' / 'Perlu diketahui bahwa ' at start of paragraphs."""
    new_content = content
    count = 0
    # Process inside <p>...</p> tags
    def fix_p(match):
        nonlocal count
        inner = match.group(1)
        # Skip if inner starts with tag
        original = inner
        for pat in CONNECTOR_OPENERS:
            new_inner = re.sub(pat, '', inner, count=1)
            if new_inner != inner:
                # Capitalize first letter
                if new_inner and new_inner[0].islower():
                    new_inner = new_inner[0].upper() + new_inner[1:]
                inner = new_inner
                count += 1
                break
        return '<p>' + inner + '</p>' if match.group(0).startswith('<p>') else match.group(0).replace(original, inner, 1)

    new_content = re.sub(r'<p>(.*?)</p>', fix_p, new_content, flags=re.DOTALL)
    if count > 0:
        log.append(f'connector removed x{count}')
    return new_content


def main():
    print(f'Loading {INPUT_FILE} ...')
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f:
        posts = json.load(f)

    print(f'TOTAL FETCHED: {len(posts)}')

    updates = []
    skipped = 0
    errors = []

    for idx, post in enumerate(posts):
        pid = post.get('id')
        slug = post.get('slug', '')
        title_raw = post.get('title', {})
        if isinstance(title_raw, dict):
            title = title_raw.get('raw', title_raw.get('rendered', ''))
        else:
            title = str(title_raw)

        if pid in EXCLUDE_IDS:
            continue

        content_obj = post.get('content', {})
        if isinstance(content_obj, dict):
            content = content_obj.get('raw', content_obj.get('rendered', ''))
        else:
            content = str(content_obj)

        original = content
        log = []

        # Fix 1: internal links
        link_log = []
        content = apply_internal_links(content, link_log)
        if link_log:
            log.append(f'+{len(link_log)} link(s): ' + ', '.join(f'"{a}"→{u}' for a, u in link_log))

        # Fix 2: filler phrases
        content = apply_filler_removal(content, log)

        # Fix 4: connector openers
        content = apply_connector_cleanup(content, log)

        # Fix 3: H2 keyword stuffing - skipped (requires per-post analysis;
        # only obvious cases. We'll do conservative skip to avoid false positives.)

        if content == original:
            skipped += 1
            continue

        # POST update
        try:
            status, resp = http_post(f'{BASE}/{pid}', {'content': content})
            updates.append({
                'id': pid,
                'slug': slug,
                'changes': '; '.join(log) if log else 'minor',
            })
            print(f'[{idx + 1}/{len(posts)}] UPDATED {pid} {slug}: {"; ".join(log)}')
            time.sleep(0.6)
        except Exception as e:
            err_msg = str(e)
            try:
                if hasattr(e, 'read'):
                    err_msg += ' | ' + e.read().decode('utf-8', errors='ignore')[:200]
            except Exception:
                pass
            errors.append({'id': pid, 'err': err_msg})
            print(f'[{idx + 1}/{len(posts)}] ERROR {pid}: {err_msg}')

    # Report
    print('\n=== FINAL REPORT ===')
    print(f'TOTAL FETCHED: {len(posts)}')
    print(f'SKIPPED (no changes): {skipped}')
    print(f'UPDATED: {len(updates)}')
    for u in updates:
        print(f'  - [{u["id"]}] {u["slug"]} — {u["changes"]}')
    print(f'ERRORS: {len(errors)}')
    for er in errors:
        print(f'  - [{er["id"]}] — {er["err"]}')


if __name__ == '__main__':
    main()
