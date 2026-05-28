"""
Extract translatable text from Elementor _elementor_data for ZH pages.
Saves backups and generates translations/extract.json
"""
import requests, json, os, re

BASE = 'https://suriota.com'
PAGES = [5450, 5451, 5452, 5453, 5454, 5456, 5457, 5461, 5465, 5466, 5467, 5468, 5469, 5470, 5471, 5472, 5473]

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'translations')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'backups', 'elementor_zh_original')

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

sess = requests.Session()

# Login
r = sess.post(f'{BASE}/wp-login.php', data={
    'log': 'admin',
    'pwd': 'REDACTED_ADMIN_PASSWORD',
    'wp-submit': 'Log In',
    'redirect_to': f'{BASE}/wp-admin',
    'testcookie': '1'
})

# Get REST nonce
nonce = sess.get(f'{BASE}/wp-admin/admin-ajax.php?action=rest-nonce').text.strip()
print('Nonce:', nonce)

headers = {'X-WP-Nonce': nonce}

def traverse(elements, results, page_id, path=''):
    for idx, el in enumerate(elements):
        el_type = el.get('elType', '')
        el_id = el.get('id', f'_{idx}')
        current_path = f"{path}.{el_id}" if path else el_id

        settings = el.get('settings', {})
        widget_type = el.get('widgetType', '')

        if widget_type:
            # heading
            if widget_type == 'heading' and settings.get('title'):
                results.append({
                    'page_id': page_id,
                    'element_id': el_id,
                    'widget_type': 'heading',
                    'field': 'settings.title',
                    'original': settings['title'],
                    'translated': ''
                })
            # text-editor
            if widget_type == 'text-editor' and settings.get('editor'):
                results.append({
                    'page_id': page_id,
                    'element_id': el_id,
                    'widget_type': 'text-editor',
                    'field': 'settings.editor',
                    'original': settings['editor'],
                    'translated': ''
                })
            # button
            if widget_type == 'button' and settings.get('text'):
                results.append({
                    'page_id': page_id,
                    'element_id': el_id,
                    'widget_type': 'button',
                    'field': 'settings.text',
                    'original': settings['text'],
                    'translated': ''
                })
            # html
            if widget_type == 'html' and settings.get('html'):
                results.append({
                    'page_id': page_id,
                    'element_id': el_id,
                    'widget_type': 'html',
                    'field': 'settings.html',
                    'original': settings['html'],
                    'translated': ''
                })
            # accordion / tabs
            if widget_type in ('accordion', 'tabs') and settings.get('tabs'):
                for tidx, tab in enumerate(settings['tabs']):
                    if tab.get('tab_title'):
                        results.append({
                            'page_id': page_id,
                            'element_id': el_id,
                            'widget_type': widget_type,
                            'field': f'settings.tabs[{tidx}].tab_title',
                            'original': tab['tab_title'],
                            'translated': ''
                        })
                    if tab.get('tab_content'):
                        results.append({
                            'page_id': page_id,
                            'element_id': el_id,
                            'widget_type': widget_type,
                            'field': f'settings.tabs[{tidx}].tab_content',
                            'original': tab['tab_content'],
                            'translated': ''
                        })

        # recurse into child elements
        if el.get('elements'):
            traverse(el['elements'], results, page_id, current_path)

all_results = []

for pid in PAGES:
    print(f'Fetching page {pid}...')
    r = sess.get(f'{BASE}/wp-json/wp/v2/pages/{pid}?context=edit', headers=headers)
    if r.status_code != 200:
        print(f'  ERROR {r.status_code}: {r.text[:200]}')
        continue

    data = r.json()
    meta = data.get('meta', {})
    elementor_data = meta.get('_elementor_data', '')

    if not elementor_data:
        print(f'  No _elementor_data found')
        continue

    # Backup
    backup_path = os.path.join(BACKUP_DIR, f'page_{pid}.json')
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(elementor_data, f, ensure_ascii=False, indent=2)
    print(f'  Backed up to {backup_path}')

    # Parse
    try:
        tree = json.loads(elementor_data) if isinstance(elementor_data, str) else elementor_data
    except Exception as e:
        print(f'  Parse error: {e}')
        continue

    # Traverse
    page_results = []
    traverse(tree, page_results, pid)
    all_results.extend(page_results)
    print(f'  Extracted {len(page_results)} fields')

# Save extract.json
extract_path = os.path.join(OUT_DIR, 'extract.json')
with open(extract_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f'\nTotal extracted fields: {len(all_results)}')
print(f'Saved to {extract_path}')
