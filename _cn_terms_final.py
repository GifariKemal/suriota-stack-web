"""Last Terms cleanup — em-dash issue."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Use raw string to preserve \u2014 as 6 chars (storage format)
PAIRS = [
    (r'\u2014 these Terms (together with any 合作 and our Privacy Policy) constitute the entire agreement.',
     r'\u2014 本条款(连同任何合作和我们的隐私政策)构成完整协议。'),
    (r'\u2014 you may not assign these Terms without our written consent; SURIOTA may assign to an affiliate or successor.',
     r'\u2014 未经我们书面同意,您不得转让本条款;SURIOTA 可转让给关联方或继任者。'),
    (r'\u2014 any non-public information disclosed by either party that should reasonably be understood to be confidential.',
     r'\u2014 任何一方披露的、合理应被理解为机密的非公开信息。'),
    (r'\u2014 as quoted in writing. Quotes are valid for 30 days unless extended.',
     r'\u2014 按书面报价。报价有效期 30 天,除非延长。'),
    (r'\u2014 VAT (PPN), withholding tax (PPh), and other applicable taxes are added to invoiced amounts unless quoted as tax-inclusive.',
     r'\u2014 增值税(PPN)、预扣税(PPh)及其他适用税费将添加到发票金额中,除非报价为含税。'),
    # Likely more with em-dash prefix
    (r'\u2014 we may suspend services and charge interest at 1.5% per month on overdue balances, to the extent permitted by law.',
     r'\u2014 在法律允许的范围内,我们可暂停服务并按每月 1.5% 对逾期余额收取利息。'),
    (r'\u2014 if any provision is held unenforceable, the remainder remains in effect.',
     r'\u2014 如任何条款被认定不可执行,其余部分仍然有效。'),
    (r'\u2014 SURIOTA may update these Terms; material changes will be notified at least 14 days in advance.',
     r'\u2014 SURIOTA 可更新本条款;重大变更将至少提前 14 天通知。'),
    (r'\u2014 neither party is liable for delays caused by events beyond reasonable control (natural disasters, war, pandemic, government action).',
     r'\u2014 任何一方对因合理控制范围之外的事件(自然灾害、战争、疫情、政府行为)造成的延迟不承担责任。'),
    (r'\u2014 written notices to admin@suriota.com for SURIOTA, or to the address you provided.',
     r'\u2014 致 SURIOTA 的书面通知发至 admin@suriota.com,或致您提供的地址。'),
    (r'\u2014 customer service available Monday to Friday, 9am to 6pm WIB.',
     r'\u2014 客户服务时间为周一至周五,上午 9 点至下午 6 点 WIB。'),
]

r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5467?context=edit&_fields=meta', headers=HDRS), timeout=30)
d = json.loads(r.read())
ed = d.get('meta',{}).get('_elementor_data','')
if isinstance(ed, list): ed = json.dumps(ed)
new_ed = ed
total = 0
for old, new in PAIRS:
    c = new_ed.count(old)
    if c > 0:
        new_ed = new_ed.replace(old, new)
        total += c
        print(f'  +{c}: {old[:60]}')

if new_ed != ed:
    payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5467', data=payload, method='POST', headers=HDRS), timeout=30).read()
    print(f'\n5467 updated: +{total}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')
