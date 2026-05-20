"""Fix ID-Privacy intro sentence to Bahasa."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Raw exact match — \u201c is the literal 6-char escape in storage
OLD = r'PT Surya Inovasi Prioritas (\u201c<strong>SURIOTA<\/strong>\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d) respects your privacy and is committed to protecting your personal data.'
NEW = r'PT Surya Inovasi Prioritas (\u201c<strong>SURIOTA<\/strong>\u201d, \u201ckami\u201d) menghormati privasi Anda dan berkomitmen melindungi data pribadi Anda.'

r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5379?context=edit&_fields=meta', headers=HDRS)
d = json.loads(urllib.request.urlopen(r, timeout=30).read())
ed = d.get('meta',{}).get('_elementor_data','')
if isinstance(ed, list): ed = json.dumps(ed)
c = ed.count(OLD)
print(f'Found: {c}')
if c > 0:
    new_ed = ed.replace(OLD, NEW)
    payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5379', data=payload, method='POST', headers=HDRS), timeout=30).read()
    print(f'Updated: +{c}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/kebijakan-privasi/?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
