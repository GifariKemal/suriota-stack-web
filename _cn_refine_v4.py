"""Final v4 — last legal chunks. SaaS schema.org JSON-LD stays EN (SEO)."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

REFINEMENTS = {
    # Privacy (5466)
    5466: [
        ('emails, WhatsApp messages, and call logs you exchange with our team.',
         '电子邮件、WhatsApp 消息和您与我们团队的通话记录。'),
        ('\\u2014 for marketing and optional cookies. You may withdraw consent at any time.',
         '— 用于营销和可选 cookie。您可随时撤回同意。'),
        ('\\u2014 integrators, certified installers, or auditors involved in delivering your project, only as necessary.',
         '— 在交付您的项目中所涉及的集成商、认证安装商或审计师,仅在必要范围内。'),
        ('\\u2014 to understand traffic and improve content (e.g., Google Analytics). You may opt out via your browser settings.',
         '— 用于了解流量和改进内容(例如 Google Analytics)。您可通过浏览器设置选择退出。'),
        ('\\u2014 obtain confirmation of and a copy of your data we hold.',
         '— 获取我们持有的您数据的确认和副本。'),
        ('Correspondence', '通信'),
        ('Consent', '同意'),
        ('Project partners', '项目合作伙伴'),
        ('Analytics cookies', '分析 cookie'),
        ('Access', '访问'),
        ('Rectification', '更正'),
        ('Erasure', '删除'),
        ('Restriction', '限制'),
        ('Portability', '可移植性'),
        ('Objection', '反对'),
        ('Account credentials', '账户凭据'),
        ('Payment data', '支付数据'),
        ('Telemetry from products', '产品遥测数据'),
        ('Contract performance', '合同履行'),
        ('Legitimate interests', '合法利益'),
        ('Legal obligation', '法律义务'),
        ('Service providers', '服务提供商'),
        ('Marketing cookies', '营销 cookie'),
    ],
    # Terms (5467)
    5467: [
        ('SURIOTA may modify, suspend, or discontinue any portion of the Services with reasonable notice, except where prohibited by contract.',
         'SURIOTA 可在合理通知下修改、暂停或停止任何部分的服务,除非合同禁止。'),
        ('Unless otherwise stated in the Engagement, custom 交付物 are licensed (not sold) to you upon full payment. SURIOTA retains rights to reusable components, frameworks, and tooling.',
         '除非合作中另有说明,定制交付物在全额付款后授权(非出售)给您。SURIOTA 保留可复用组件、框架和工具的权利。'),
        ('Upload malware, conduct security testing without prior written consent, or otherwise interfere with the integrity of our systems.',
         '上传恶意软件、未经事先书面同意进行安全测试或以其他方式干扰我们系统的完整性。'),
        ('You retain ownership of materials you provide to us. You grant SURIOTA a licence to use such materials as necessary to perform the Services.',
         '您保留向我们提供的材料的所有权。您授予 SURIOTA 在履行服务所必需的范围内使用此类材料的许可。'),
        ('\\u2014 we may suspend services and charge interest at 1.5% per month on overdue balances, to the extent permitted by law.',
         '— 在法律允许的范围内,我们可暂停服务并按每月 1.5% 对逾期余额收取利息。'),
        ('Indonesia, in accordance with the prevailing laws.', '印度尼西亚,依据现行法律。'),
        ('Pricing', '定价'),
        ('Taxes', '税费'),
        ('Late payment', '逾期付款'),
        ('Hardware Products carry the manufacturer-specified warranty period as printed on packaging or specification sheets.',
         '硬件产品按制造商指定的保修期(印于包装或规格表)提供。'),
        ('Acceptance of Terms', '条款接受'),
        ('Definitions', '定义'),
        ('Services Description', '服务说明'),
        ('Accounts &amp; Registration', '账户与注册'),
        ('Accounts & Registration', '账户与注册'),
        ('Acceptable Use', '可接受使用'),
        ('Intellectual Property', '知识产权'),
        ('Fees &amp; Payment', '费用与支付'),
        ('Fees & Payment', '费用与支付'),
        ('Confidentiality', '保密'),
        ('Warranties &amp; Disclaimers', '保证与免责'),
        ('Warranties & Disclaimers', '保证与免责'),
        ('Limitation of Liability', '责任限制'),
        ('Indemnification', '赔偿'),
        ('Term &amp; Termination', '期限与终止'),
        ('Term & Termination', '期限与终止'),
        ('Governing Law', '管辖法律'),
        ('Dispute Resolution', '争议解决'),
        ('General Provisions', '通用条款'),
        ('Entire Agreement', '完整协议'),
        ('Amendments', '修订'),
        ('Severability', '可分性'),
        ('Assignment', '转让'),
        ('Force Majeure', '不可抗力'),
        ('Notices', '通知'),
        ('Contact', '联系'),
        ('Confidential Information', '机密信息'),
        ('Engagement', '合作'),
        ('Refunds', '退款'),
    ],
}

print(f'Refining {len(REFINEMENTS)} pages...')
total = 0
for pid, pairs in REFINEMENTS.items():
    r = urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS), timeout=30)
    d = json.loads(r.read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): continue
    new_ed = ed
    page_changes = 0
    for old, new in pairs:
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            page_changes += c
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  {pid}: +{page_changes}')
        total += page_changes

print(f'\nTotal: {total}')
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')
time.sleep(2)
for u in ['https://suriota.com/', 'https://suriota.com/id/beranda/']:
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
    print(f'  {u}: {r.status}')
