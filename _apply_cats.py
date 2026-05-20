import json, urllib.request, urllib.error, base64

auth = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
hdrs = {'Authorization': f'Basic {auth}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# 1) Fetch all posts (to get current cats)
all_posts = []
for page in [1,2,3,4]:
    req = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/posts?per_page=20&page={page}&_fields=id,title,slug,categories', headers=hdrs)
    try:
        d = json.loads(urllib.request.urlopen(req).read())
        if not d: break
        all_posts.extend(d)
    except: break
print(f"Fetched {len(all_posts)} posts")

# 2) Fetch existing categories
req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/categories?per_page=100&_fields=id,name,slug', headers=hdrs)
existing = json.loads(urllib.request.urlopen(req).read())
existing_map = {c['name'].lower(): c['id'] for c in existing}
print("Existing cats:", existing_map)

# 3) Categories needed
cats_needed = ['Renewable Energy','Water Treatment','IoT & Monitoring','Automation','Electrical','Manufacturing','Design & CAD','IT Services']
cat_ids = {}
for name in cats_needed:
    key = name.lower()
    if key in existing_map:
        cat_ids[name] = existing_map[key]
        print(f"  EXISTS: {name} = {cat_ids[name]}")
    else:
        # Create
        payload = json.dumps({'name': name, 'slug': name.lower().replace(' & ','-').replace(' ','-')}).encode()
        req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/categories', data=payload, method='POST', headers=hdrs)
        try:
            r = json.loads(urllib.request.urlopen(req).read())
            cat_ids[name] = r['id']
            print(f"  CREATED: {name} = {r['id']}")
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            print(f"  FAILED to create {name}: {body[:200]}")

# 4) Categorization rules (same as preview)
rules = [
    ('Renewable Energy', ['plts','pltb','solar','renewable','panel-surya','hybrid-pju']),
    ('Water Treatment',  ['water','wwtp','flowmeter','pengolahan-air','sparing','pompa-submersible','pompa-sentrifugal','rewinding-pompa','maintenance-wtp','waste-water','npk','plantation','ph-suhu']),
    ('IoT & Monitoring', ['iot','monitoring','sensor','modbus','prototype','iiot','absensi-iot','robot-tank','yolo']),
    ('Automation',       ['vfd','automation','scada','plc','ats','kontrol-monitoring','schematic-programming','kapasitor-bank','load-suppression','lifa-programming']),
    ('Electrical',       ['electrical','wiring','genset','panel','setup-genset','sistem-kapasitor','penangkal-petir','pengaman-phase','ethernet']),
    ('Manufacturing',    ['machining','cnc','pemesinan','material','bubut','milling','drilling','surface-grinding','quality-control','produksi-batch','stainless-steel']),
    ('Design & CAD',     ['design-cad','desain-logo','logo','stiker','desain-stiker','design-cad-sld','gambar-pid','digital-stamp','site-plan','wedding-invitation','jamu-logo','logo-icon-printup','sld-single-line','perhitungan-flow','perhitungan-teknik']),
    ('IT Services',      ['webmail','website','website-sekolah','procurement-module','migrasi-server','jasa-maintenance','program-pendeteksi','deteksi-objek','pengadaan-sensor','pengadaan-material','setup-ethernet']),
]

def categorize(slug, title):
    text = (slug + ' ' + (title or '')).lower()
    for cat, kws in rules:
        for kw in kws:
            if kw in text:
                return cat
    return None

# 5) Assign categories
ok, fail = 0, 0
for p in all_posts:
    cat_name = categorize(p['slug'], p['title']['rendered'])
    if not cat_name or cat_name not in cat_ids:
        continue
    new_cat_id = cat_ids[cat_name]
    # Build new categories list — REPLACE all categories with just this one
    payload = json.dumps({'categories': [new_cat_id]}).encode()
    req = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/posts/{p["id"]}', data=payload, method='POST', headers=hdrs)
    try:
        r = json.loads(urllib.request.urlopen(req).read())
        ok += 1
    except urllib.error.HTTPError as e:
        fail += 1
        print(f"  FAILED post {p['id']}: {e.read().decode()[:100]}")

print(f"\nDone: {ok} updated, {fail} failed")
