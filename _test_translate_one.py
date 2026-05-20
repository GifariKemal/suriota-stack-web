"""POC: Create Indonesian translation of homepage.
Workflow: clone EN page meta+content -> create new page with lang=id -> link translation via Polylang.
"""
import json, urllib.request, urllib.error, base64, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Fetch EN homepage
print('1) Fetching EN homepage (id=12)...')
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/12?context=edit&_fields=id,title,content,slug,template,meta', headers=HDRS)
en_page = json.loads(urllib.request.urlopen(r, timeout=30).read())
print(f"   title: {en_page['title']['raw']}")
print(f"   slug: {en_page['slug']}")
print(f"   content size: {len(en_page['content']['raw'])} chars")
print(f"   has _elementor_data: {bool(en_page.get('meta', {}).get('_elementor_data'))}")

# Try creating ID translation via POST with ?lang=id
# Note: Polylang assigns lang via the 'lang' query param (per Polylang REST docs)
print('\n2) Creating ID page stub (title only — content to be filled later)...')
id_title = 'Beranda — SURIOTA Mitra Industri Generasi Baru'
payload = {
    'title': id_title,
    'content': '<!-- wp:html --><p>Halaman dalam pengerjaan — terjemahan Bahasa Indonesia akan segera tersedia.</p><!-- /wp:html -->',
    'status': 'draft',  # Draft first for safety
    'slug': 'beranda',
}
data = json.dumps(payload).encode()
req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?lang=id', data=data, method='POST', headers=HDRS)
try:
    resp = urllib.request.urlopen(req, timeout=30)
    id_page = json.loads(resp.read())
    print(f"   Created ID page: id={id_page['id']} link={id_page['link']}")
    new_id = id_page['id']
except urllib.error.HTTPError as e:
    print(f'   FAIL: HTTP {e.code} {e.read().decode()[:400]}')
    sys.exit(1)

# Verify language assignment via Polylang taxonomy
print('\n3) Verifying language assignment...')
r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{new_id}?_fields=id,link,title', headers=HDRS)
verify = json.loads(urllib.request.urlopen(r).read())
print(f"   link: {verify['link']}")
print(f"   in /id/ subdir: {'/id/' in verify['link']}")
