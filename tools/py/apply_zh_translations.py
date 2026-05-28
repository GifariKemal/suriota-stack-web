"""
Apply translated text back to Elementor _elementor_data for ZH pages.
Reads translations/extract.json and backups/elementor_zh_original/, then posts via WP REST.
"""
import requests, json, os

BASE = 'https://suriota.com'
PAGES = [5450, 5451, 5452, 5453, 5454, 5456, 5457, 5461, 5465, 5466, 5467, 5468, 5469, 5470, 5471, 5472, 5473]

BACKUP_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'backups', 'elementor_zh_original')
EXTRACT_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'translations', 'extract.json')

# Load extract.json
with open(EXTRACT_PATH, 'r', encoding='utf-8') as f:
    extract = json.load(f)

# Group translations by page_id
translations_by_page = {}
for item in extract:
    if item.get('translated'):
        pid = item['page_id']
        translations_by_page.setdefault(pid, []).append(item)

print(f"Pages with translations: {list(translations_by_page.keys())}")

# Auth
sess = requests.Session()
r = sess.post(f'{BASE}/wp-login.php', data={
    'log': 'admin',
    'pwd': 'REDACTED_ADMIN_PASSWORD',
    'wp-submit': 'Log In',
    'redirect_to': f'{BASE}/wp-admin',
    'testcookie': '1'
})

nonce = sess.get(f'{BASE}/wp-admin/admin-ajax.php?action=rest-nonce').text.strip()
print('Nonce:', nonce)

headers = {'X-WP-Nonce': nonce, 'Content-Type': 'application/json'}

def set_nested(obj, path, value):
    """Set value in nested dict/list by dot-bracket path like 'settings.tabs[0].tab_title'"""
    parts = []
    i = 0
    s = path
    while i < len(s):
        if s[i] == '.':
            if i > 0:
                parts.append(s[:i])
            s = s[i+1:]
            i = 0
        elif s[i] == '[':
            if i > 0:
                parts.append(s[:i])
            j = s.find(']', i)
            idx = int(s[i+1:j])
            parts.append(idx)
            s = s[j+1:]
            if s.startswith('.'):
                s = s[1:]
            i = 0
        else:
            i += 1
    if s:
        parts.append(s)

    cur = obj
    for p in parts[:-1]:
        cur = cur[p]
    cur[parts[-1]] = value

def find_element(tree, target_id):
    """Find element by id in nested elements tree."""
    for el in tree:
        if el.get('id') == target_id:
            return el
        if el.get('elements'):
            found = find_element(el['elements'], target_id)
            if found:
                return found
    return None

success_count = 0
fail_count = 0

for pid in PAGES:
    if pid not in translations_by_page:
        print(f'Page {pid}: no translations, skipping')
        continue

    # Load backup
    backup_path = os.path.join(BACKUP_DIR, f'page_{pid}.json')
    with open(backup_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    # Parse elementor_data
    if isinstance(raw, str):
        tree = json.loads(raw)
    else:
        tree = raw

    page_trans = translations_by_page[pid]
    applied = 0

    for item in page_trans:
        el_id = item['element_id']
        field_path = item['field']
        translated = item['translated']

        el = find_element(tree, el_id)
        if not el:
            print(f"  Page {pid}: element {el_id} not found")
            continue

        try:
            set_nested(el, field_path, translated)
            applied += 1
        except Exception as e:
            print(f"  Page {pid}: failed to set {field_path} on {el_id}: {e}")

    print(f"Page {pid}: applied {applied} / {len(page_trans)} translations")

    # POST back
    payload = {'meta': {'_elementor_data': json.dumps(tree, ensure_ascii=False)}}
    r = sess.post(f'{BASE}/wp-json/wp/v2/pages/{pid}', headers=headers, json=payload)
    if r.status_code in (200, 201):
        print(f"  -> OK {r.status_code}")
        success_count += 1
    else:
        print(f"  -> FAIL {r.status_code}: {r.text[:300]}")
        fail_count += 1

print(f"\nDone. Success: {success_count}, Failed: {fail_count}")
