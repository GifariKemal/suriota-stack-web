"""Final ZH polish — fix all remaining EN chunks across all 25 pages."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Sitewide untranslated patterns found via deep audit
GLOBAL_PATTERNS = [
    # CTA buttons - using literal arrow char (not \u2192 escape)
    ('"text":"Free Consultation \u2192"', '"text":"免费咨询 \u2192"'),
    ('"text":"Free Consultation"', '"text":"免费咨询 \u2192"'),
    ('"text":"View All Portfolio"', '"text":"查看全部案例"'),
    ('"text":"Send Message"', '"text":"发送消息"'),
    ('"text":"Request a Quote"', '"text":"申请报价"'),
    ('"text":"Learn More"', '"text":"了解更多"'),
    ('"text":"Get Started"', '"text":"开始"'),
    # Heading widget titles
    ('"title":"Trusted By"', '"title":"信赖伙伴"'),
    ('"title":"Our Location"', '"title":"我们的位置"'),
    ('"title":"Contact Us"', '"title":"联系我们"'),
    ('"title":"View All Portfolio"', '"title":"查看全部案例"'),
    ('"title":"Free Consultation"', '"title":"免费咨询"'),
    ('"title":"Send Us a Message"', '"title":"发送消息"'),
    # Stats labels (in HTML content)
    ('>INDUSTRIAL PROJECTS<', '>工业项目<'),
    ('>IN-HOUSE PRODUCTS<', '>自研产品<'),
    ('>CORE SERVICES<', '>核心服务<'),
    ('>TEAM PROFESSIONALS<', '>专业团队<'),
    ('>Industrial Projects<', '>工业项目<'),
    ('>In-House Products<', '>自研产品<'),
    ('>Core Services<', '>核心服务<'),
    ('>Team Professionals<', '>专业团队<'),
    # Common label spans
    ('>Trusted By<', '>信赖伙伴<'),
    ('>Our Location<', '>我们的位置<'),
    ('>Contact Us<', '>联系我们<'),
    ('>View All Portfolio<', '>查看全部案例<'),
    ('>Send<', '>发送<'),
    ('>SEND<', '>发送<'),
    # Form placeholders / labels
    ('"placeholder":"Name"', '"placeholder":"姓名"'),
    ('"placeholder":"Email"', '"placeholder":"邮箱"'),
    ('"placeholder":"Message"', '"placeholder":"留言"'),
    ('"placeholder":"Your Name"', '"placeholder":"您的姓名"'),
    ('"placeholder":"Your Email"', '"placeholder":"您的邮箱"'),
    ('"placeholder":"Your Message"', '"placeholder":"您的留言"'),
    ('"field_label":"Name"', '"field_label":"姓名"'),
    ('"field_label":"Email"', '"field_label":"邮箱"'),
    ('"field_label":"Message"', '"field_label":"留言"'),
    ('"button_text":"Send"', '"button_text":"发送"'),
    ('"button_text":"SEND"', '"button_text":"发送"'),
    # Common headings
    ('"title":"Capabilities"', '"title":"核心能力"'),
    ('"title":"Products"', '"title":"产品"'),
    ('"title":"Portfolio"', '"title":"项目案例"'),
    ('"title":"Why SURIOTA"', '"title":"为何选择 SURIOTA"'),
    ('"title":"Our Services"', '"title":"我们的服务"'),
]

ALL_ZH = [5448, 5450, 5451, 5452, 5453, 5454, 5455, 5456, 5457, 5458, 5459, 5460,
          5461, 5462, 5463, 5464, 5465, 5466, 5467, 5468, 5469, 5470, 5471, 5472, 5473]

total = 0
for pid in ALL_ZH:
    r = urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS), timeout=30)
    d = json.loads(r.read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): continue
    new_ed = ed
    changes = 0
    for old, new in GLOBAL_PATTERNS:
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            changes += c
    # Validate JSON before saving
    if new_ed != ed:
        try:
            json.loads(new_ed)
        except Exception as e:
            print(f'  {pid}: JSON invalid after edit, skip ({e})')
            continue
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  {pid}: +{changes}')
        total += changes

print(f'\nTotal: {total}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')
time.sleep(2)
for u in ['https://suriota.com/shouye/', 'https://suriota.com/guanyu-women/']:
    urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Warmed')
