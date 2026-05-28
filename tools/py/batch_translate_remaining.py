"""
Batch translate remaining English text nodes in ZH pages using Google Translate.
Updates translations/extract.json in-place.
"""
import json, re
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator
from collections import Counter

with open('translations/extract.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

translator = GoogleTranslator(source='auto', target='zh-CN')

# Collect all English text nodes that need translation
texts_to_translate = []
field_map = []  # (item_index, node_path, original_text)

for idx, item in enumerate(data):
    # Use translated if available and different, else original
    base = item.get('translated') if item.get('translated') and item.get('translated') != item['original'] else item['original']

    # Skip if already fully Chinese (no English words)
    if not re.search(r'[A-Za-z]{3,}', base):
        continue

    # Skip JSON-LD
    if '<script type="application/ld+json"' in base:
        base_clean = re.sub(r'<script type="application/ld\+json">.*?</script>', '', base, flags=re.S)
    else:
        base_clean = base
    base_clean = re.sub(r'<style[^>]*>.*?</style>', '', base_clean, flags=re.S)

    soup = BeautifulSoup(base_clean, 'html.parser')
    for node in soup.find_all(string=True):
        if isinstance(node, NavigableString):
            t = str(node).strip()
            if not t:
                continue
            if node.parent and node.parent.name in ['style', 'script']:
                continue

            # Check if contains meaningful English (at least 3 words, 15+ chars)
            en_matches = re.findall(r'[A-Za-z][A-Za-z\s,\.\'\-\&;]{2,}[A-Za-z]', t)
            total_en = sum(len(m.split()) for m in en_matches)
            if total_en >= 3 and len(t) >= 15:
                # Skip if mostly numbers/symbols
                if re.match(r'^[\d\s\-\+\.\,\(\)\%]+$', t):
                    continue
                texts_to_translate.append(t)
                field_map.append((idx, t))

# Deduplicate while preserving order
seen = set()
unique_texts = []
for t in texts_to_translate:
    if t not in seen:
        seen.add(t)
        unique_texts.append(t)

print(f'Found {len(texts_to_translate)} text nodes, {len(unique_texts)} unique')

# Translate in batches
batch_size = 50
translation_cache = {}

for i in range(0, len(unique_texts), batch_size):
    batch = unique_texts[i:i+batch_size]
    print(f'Translating batch {i//batch_size + 1}/{(len(unique_texts)-1)//batch_size + 1} ({len(batch)} items)...')
    for text in batch:
        try:
            # Skip if already mostly Chinese
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
            total_chars = len(text.strip())
            if chinese_chars / total_chars > 0.5:
                translation_cache[text] = text
                continue

            translated = translator.translate(text)
            # Don't translate if result is identical (usually means it failed)
            if translated and translated != text:
                translation_cache[text] = translated
            else:
                translation_cache[text] = text
        except Exception as e:
            print(f'  Error translating "{text[:50]}": {e}')
            translation_cache[text] = text

# Apply translations back to each field
modified_count = 0
for idx, item in enumerate(data):
    base = item.get('translated') if item.get('translated') and item.get('translated') != item['original'] else item['original']

    if '<script type="application/ld+json"' in base:
        base_clean = re.sub(r'<script type="application/ld\+json">.*?</script>', '', base, flags=re.S)
        json_ld = re.search(r'(<script type="application/ld\+json">.*?</script>)', base, flags=re.S)
        json_ld_part = json_ld.group(1) if json_ld else ''
    else:
        base_clean = base
        json_ld_part = ''

    base_clean = re.sub(r'<style[^>]*>.*?</style>', '', base_clean, flags=re.S)

    soup = BeautifulSoup(base_clean, 'html.parser')
    field_modified = False

    for node in soup.find_all(string=True):
        if isinstance(node, NavigableString):
            t = str(node).strip()
            if not t or (node.parent and node.parent.name in ['style', 'script']):
                continue

            if t in translation_cache and translation_cache[t] != t:
                node.replace_with(translation_cache[t])
                field_modified = True

    if field_modified:
        result = str(soup)
        # Re-attach JSON-LD if it was removed
        if json_ld_part:
            result = result + '\n' + json_ld_part
        item['translated'] = result
        modified_count += 1

with open('translations/extract.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nModified {modified_count} / {len(data)} fields')
