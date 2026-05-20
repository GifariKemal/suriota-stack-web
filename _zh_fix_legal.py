"""Restore ZH Privacy + Terms — JSON-safe translation approach."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Safe translation pairs — careful to not break JSON structure
# All replacements happen INSIDE JSON string values, must preserve quote escaping
SAFE_PAIRS = [
    # Headers (h2 inside JSON string)
    ('1. Introduction', '1. 概述'),
    ('2. Data Controller', '2. 数据控制方'),
    ('3. Information We Collect', '3. 我们收集的信息'),
    ('4. How We Use Information', '4. 我们如何使用信息'),
    ('5. Legal Basis (GDPR)', '5. 法律依据 (GDPR)'),
    ('6. Sharing &amp; Disclosure', '6. 共享与披露'),
    ('7. Cookies &amp; Tracking', '7. Cookies 与追踪'),
    ('8. Data Retention', '8. 数据保留'),
    ('9. Security', '9. 安全'),
    ('10. International Data Transfers', '10. 跨境数据传输'),
    ('11. Your Rights', '11. 您的权利'),
    ('12. Children\\u2019s Data', '12. 儿童数据'),
    ('13. Changes to this Policy', '13. 政策变更'),
    ('14. Contact Us', '14. 联系我们'),
    # Terms section h2s
    ('1. Acceptance of Terms', '1. 接受条款'),
    ('2. Definitions', '2. 定义'),
    ('3. Services Description', '3. 服务描述'),
    ('4. Accounts &amp; Registration', '4. 账户与注册'),
    ('5. Acceptable Use', '5. 可接受使用'),
    ('6. Intellectual Property', '6. 知识产权'),
    ('7. Fees &amp; Payment', '7. 费用与支付'),
    ('8. Confidentiality', '8. 保密'),
    ('9. Warranties &amp; Disclaimers', '9. 保证与免责'),
    ('10. Limitation of Liability', '10. 责任限制'),
    ('11. Indemnification', '11. 赔偿'),
    ('12. Term &amp; Termination', '12. 期限与终止'),
    ('13. Governing Law &amp; Jurisdiction', '13. 管辖法律与司法管辖'),
    ('14. Dispute Resolution', '14. 争议解决'),
    ('15. General Provisions', '15. 通用条款'),
    ('16. Contact', '16. 联系'),
    # Hero subtitle for privacy
    ('How PT Surya Inovasi Prioritas (SURIOTA) collects, uses, and protects your personal data.',
     'PT Surya Inovasi Prioritas (SURIOTA) 如何收集、使用和保护您的个人数据。'),
    # Hero subtitle for terms
    ('Agreement governing the use of SURIOTA website, products (SURGE platform, SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 Surge Protector), and engineering services. Please read carefully.',
     '关于使用 SURIOTA 网站、产品(SURGE 平台、SRT-MGATE-1210、ISO-M485、THM-30MD、PM1611-WD、RS-485 浪涌保护器)及工程服务的协议。请仔细阅读。'),
    # Common labels
    ('Effective', '生效日期'),
    ('Last updated', '最后更新'),
    ('Version', '版本'),
    # Eyebrow
    ('LEGAL', '法律信息'),
    # In this page TOC
    ('In this page', '本页目录'),
    # Privacy Policy page-specific (escaping-aware)
    ('Privacy Policy', '隐私政策'),
    ('Terms of Service', '服务条款'),
    ('Privacy Officer', '隐私官'),
    ('Data Protection Officer', '数据保护官'),
]

for src_en, zh_pid, title in [(4985, 5466, '隐私政策'), (4987, 5467, '服务条款')]:
    print(f'\n=== Restoring ZH page {zh_pid} from EN {src_en} ===')
    # Fetch EN
    r = urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{src_en}?context=edit&_fields=meta,template', headers=HDRS), timeout=30)
    src = json.loads(r.read())
    ed = src.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    ps = src.get('meta',{}).get('_elementor_page_settings', {})

    # Verify EN is valid JSON
    try:
        json.loads(ed)
        print(f'  EN data valid JSON ({len(ed)} chars)')
    except Exception as e:
        print(f'  EN parse error: {e}')
        continue

    # Apply translations
    new_ed = ed
    changes = 0
    for old, new in SAFE_PAIRS:
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            changes += c

    # Validate new still JSON
    try:
        json.loads(new_ed)
        print(f'  Translated data valid JSON ({changes} changes)')
    except Exception as e:
        print(f'  ✗ JSON broken after translation: {e}')
        continue

    # Push to ZH page
    payload = json.dumps({
        'title': title,
        'template': src.get('template', ''),
        'meta': {
            '_elementor_data': new_ed,
            '_elementor_page_settings': ps if isinstance(ps, dict) else {},
            '_elementor_edit_mode': 'builder',
            '_elementor_template_type': 'wp-page',
        }
    }).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{zh_pid}', data=payload, method='POST', headers=HDRS), timeout=60).read()
        print(f'  ✅ {zh_pid} restored')
    except Exception as e:
        print(f'  ✗ Push failed: {e}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('\nCache cleared')
time.sleep(2)
for u in ['https://suriota.com/yinsi-zhengce/', 'https://suriota.com/fuwu-tiaokuan/']:
    urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Warmed')
