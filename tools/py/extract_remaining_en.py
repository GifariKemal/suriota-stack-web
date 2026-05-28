import json, re
from bs4 import BeautifulSoup, NavigableString

with open('translations/extract.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all English text from untranslated fields
en_phrases = []

for item in data:
    text = item['original']
    widget = item['widget_type']

    # Skip JSON-LD scripts
    if '<script type="application/ld+json"' in text:
        text = re.sub(r'<script type="application/ld\+json">.*?</script>', '', text, flags=re.S)

    # Skip CSS in style tags
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)

    # Parse HTML to get text nodes
    soup = BeautifulSoup(text, 'html.parser')

    for node in soup.find_all(string=True):
        if isinstance(node, NavigableString):
            t = str(node).strip()
            if not t:
                continue
            # Skip if parent is style/script
            if node.parent and node.parent.name in ['style', 'script']:
                continue

            # Check if contains English words
            en_words = re.findall(r'[A-Za-z][A-Za-z\s,\'\-]{2,}[A-Za-z]', t)
            for w in en_words:
                w = w.strip()
                if len(w.split()) >= 3:
                    en_phrases.append((item['page_id'], widget, w))

# Deduplicate
seen = set()
unique = []
for pid, widget, phrase in en_phrases:
    key = (pid, phrase.lower())
    if key not in seen:
        seen.add(key)
        unique.append((pid, widget, phrase))

# Group by page
from collections import defaultdict
by_page = defaultdict(list)
for pid, widget, phrase in unique:
    by_page[pid].append((widget, phrase))

for pid in sorted(by_page):
    print(f'\n=== Page {pid} ===')
    for widget, phrase in by_page[pid][:20]:
        print(f'  [{widget}] {phrase}')
    if len(by_page[pid]) > 20:
        print(f'  ... and {len(by_page[pid]) - 20} more')

print(f'\nTotal unique English phrases: {len(unique)}')
