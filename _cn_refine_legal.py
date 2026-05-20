"""Refine Privacy + Terms ZH pages (legal boilerplate)."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

REFINEMENTS = {
    # PRIVACY (5466)
    5466: [
        ('We implement technical and organisational measures including encryption in transit (TLS 1.2+), encryption at rest, role-based access controls, audit logging, regular security assessments, and staff training. While we strive to safeguard your data, no method of transmission or storage is 100% secure; we will notify you and the relevant authority within 72 hours of becoming aware of a personal-data breach that materially affects your rights.',
         '我们实施技术和组织措施,包括传输中加密(TLS 1.2+)、静态加密、基于角色的访问控制、审计日志、定期安全评估和员工培训。尽管我们努力保护您的数据,但没有任何传输或存储方法是 100% 安全的;我们将在意识到对您的权利产生实质影响的个人数据泄露后 72 小时内通知您和相关机构。'),
        ('Our services are intended for businesses and adult professionals. We do not knowingly collect personal data from individuals under 18 years of age. If you believe a minor has provided us with personal',
         '我们的服务面向企业和成年专业人士。我们不会故意收集 18 岁以下个人的数据。如果您认为未成年人向我们提供了个人'),
        ('We may update this 隐私政策 from time to time. The latest version will always be posted on this page, with the \\u201c最后更新\\u201d date revised. Material changes will be communicated by email or prominent notice on our website at least 14 days before they take effect.',
         '我们可能会不时更新本隐私政策。最新版本将始终发布在此页面,并修订"最后更新"日期。重大变更将通过电子邮件或我们网站上的显著通知至少在生效前 14 天告知。'),
        ('\\u201d, \\u201cwe\\u201d, \\u201cus\\u201d, or \\u201cour\\u201d) respects your privacy and is committed to protecting your personal data. This 隐私政策 explains how we collect, use, store, share, and protect p',
         '","我们")尊重您的隐私并致力于保护您的个人数据。本隐私政策说明了我们如何收集、使用、存储、共享和保护您的个'),
        ('By accessing our website, using our products, or engaging our services, you acknowledge that you have read and understood this 隐私政策.',
         '通过访问我们的网站、使用我们的产品或使用我们的服务,您确认已阅读并理解本隐私政策。'),
        ('Account credentials: if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens.',
         '账户凭据:如果您在 SURGE 平台上创建账户,我们将收集您的用户名、哈希密码和身份验证令牌。'),
        ('Payment data: billing address and invoice details. We do not store full credit card numbers',
         '支付数据:账单地址和发票详情。我们不存储完整信用卡号'),
        ('Correspondence: emails, WhatsApp messages, and call logs you exchange with our team.',
         '通信:您与我们团队交换的电子邮件、WhatsApp 消息和通话记录。'),
        ('Telemetry from products: for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the purpose of operating the contracted service.',
         '产品遥测:对于使用 SURGE 平台的 IoT 部署,我们收集设备标识符、传感器读数、地理位置(经同意时)和事件日志,严格用于运营所签订服务的目的。'),
        ('Contract performance - to fulfil engagement and service agreements.',
         '合同履行 - 履行合作和服务协议。'),
        ('Legitimate interests - to operate our business, secure our services, and develop our products.',
         '合法利益 - 运营我们的业务、保护我们的服务并开发我们的产品。'),
        ('Consent - for marketing and optional cookies. You may withdraw consent at any time.',
         '同意 - 用于营销和可选 cookie。您可随时撤回同意。'),
        ('Legal obligation - to comply with tax, accounting, and regulatory requirements.',
         '法律义务 - 遵守税收、会计和监管要求。'),
        ('Service providers processing data on our behalf (cloud hosting, email delivery, analytics, payment) under written data-processing agreements.',
         '代表我们处理数据的服务提供商(云托管、电子邮件投递、分析、支付),依据书面数据处理协议。'),
        ('Analytics cookies - to understand traffic and improve content (e.g., Google Analytics). You may opt out via your browser settings.',
         '分析 cookie - 用于了解流量和改进内容(例如 Google Analytics)。您可通过浏览器设置选择退出。'),
        ('Marketing cookies - only set with your explicit consent (where applicable).',
         '营销 cookie - 仅在您明确同意时设置(如适用)。'),
        ('Under UU PDP No.27\\/2022 (Indonesia) and GDPR (EU), you have the right to:',
         '根据印尼 UU PDP No.27/2022 和欧盟 GDPR,您有权:'),
        ('To exercise these rights, contact admin@suriota.com. We will respond within 30 calendar days.',
         '要行使这些权利,请联系 admin@suriota.com。我们将在 30 个日历日内回复。'),
        ('For questions about this 隐私政策 or to exercise your data-protection rights, please contact:',
         '如对本隐私政策有疑问或行使数据保护权利,请联系:'),
        ('Data Protection Officer', '数据保护官'),
    ],
    # TERMS (5467)
    5467: [
        ('The parties will first attempt to resolve any dispute through good-faith negotiation between authorised representatives. If unresolved within thirty (30) days, the dispute shall be submitted to binding arbitration administered by the Indonesian National Arbitration Board (BANI) in Jakarta, in the English language. The arbitral award shall be final and binding. Nothing in this section prevents either party from seeking injunctive relief in court for IP or confidentiality breaches.',
         '双方将首先通过授权代表之间的诚信谈判尝试解决任何争议。如三十(30)天内未能解决,争议应提交雅加达印尼国家仲裁委员会(BANI)进行有约束力的仲裁,使用英语进行。仲裁裁决应为最终且有约束力。本节内容不阻止任何一方就 IP 或保密违约向法院寻求禁令救济。'),
        ('All firmware, software, designs, schematics, documentation, trademarks, and know-how created or owned by SURIOTA \\u2014 including the SURGE platform and all Products \\u2014 remain the exclusive property of SURIOTA',
         'SURIOTA 创建或拥有的所有固件、软件、设计、原理图、文档、商标和专有技术 — 包括 SURGE 平台和所有产品 — 仍为 SURIOTA 的专有财产'),
        ('Each party will protect the other\\u2019s Confidential Information with the same degree of care it uses to protect its own (no less than reasonable care), use it solely to perform the Engagement, and n',
         '每一方应以保护自身机密信息相同的谨慎程度(不低于合理的谨慎)保护对方的机密信息,仅将其用于履行合作,且不'),
        ('You agree to defend, indemnify, and hold harmless SURIOTA, its officers, directors, employees, and agents from and against any claims, damages, losses, liabilities, costs, and expenses (including reas',
         '您同意为 SURIOTA、其高级职员、董事、雇员和代理人辩护、赔偿并使其免受任何索赔、损害、损失、责任、费用和支出(包括合'),
        ('These Terms remain in effect while you use the Services. Either party may terminate an Engagement with thirty (30) days\\u2019 written notice, or immediately for material breach not cured within fiftee',
         '本条款在您使用服务期间持续有效。任何一方均可提前三十(30)天书面通知终止合作,或在重大违约且未在十五'),
        ('These Terms (\\u201c<strong>Terms<\\/strong>\\u201d) form a binding agreement between you (\\u201cyou\\u201d or \\u201cClient\\u201d) and PT Surya Inovasi Prioritas (\\u201c<strong>SURIOTA<\\/strong>\\u201d, \\u201cwe\\u201d, \\u201cus\\u201d, or \\u201cour\\u201d). By accessing our website, purchasing our products, or engaging our services, you agree to these Terms.',
         '本条款("<strong>条款</strong>")构成您("您"或"客户")与 PT Surya Inovasi Prioritas("<strong>SURIOTA</strong>","我们")之间具有约束力的协议。通过访问我们的网站、购买我们的产品或使用我们的服务,您同意本条款。'),
        ('Services - engineering, integration, consultation, and SaaS offerings provided by SURIOTA, including the SURGE platform.',
         '服务 - SURIOTA 提供的工程、集成、咨询和 SaaS 产品,包括 SURGE 平台。'),
        ('Products - hardware manufactured or distributed by SURIOTA (SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 SPD, Wastewater Logger, and successors).',
         '产品 - SURIOTA 制造或分销的硬件(SRT-MGATE-1210、ISO-M485、THM-30MD、PM1611-WD、RS-485 SPD、Wastewater Logger 及其继任产品)。'),
        ('Engagement - a project, support contract, or subscription agreed in writing (Statement of Work, Purchase Order, or service plan).',
         '合作 - 书面约定的项目、支持合同或订阅(工作说明书、采购订单或服务计划)。'),
        ('Deliverables - documents, designs, code, configurations, reports, or installed equipment produced under an Engagement.',
         '交付物 - 在合作下产生的文档、设计、代码、配置、报告或已安装设备。'),
        ('Confidential Information - any non-public information disclosed by either party that should reasonably be understood to be confidential.',
         '机密信息 - 任何一方披露的、合理应被理解为机密的非公开信息。'),
        ('SURIOTA provides system integration of Industrial IoT, automation, water treatment instrumentation, renewable energy services, electrical engineering, and the SURGE Software-as-a-Service platform for energy management, vessel tracking, and water analytics. Specific scope, deliverables, timelines, and acceptance criteria are defined in the applicable Statement of Work or service plan.',
         'SURIOTA 提供工业物联网、自动化、水处理仪表、可再生能源服务、电气工程以及 SURGE 软件即服务平台的系统集成,用于能源管理、船舶追踪和水质分析。具体范围、交付物、时间表和验收标准在适用的工作说明书或服务计划中定义。'),
        ('SURIOTA may modify, suspend, or discontinue any part of the Services with reasonable notice, except where prohibited by contract.',
         'SURIOTA 可在合理通知下修改、暂停或终止任何部分的服务,除非合同禁止。'),
        ('Pricing - as quoted in writing. Quotes are valid for 30 days unless extended.',
         '定价 - 按书面报价。报价有效期 30 天,除非延长。'),
        ('Taxes - VAT (PPN), withholding tax (PPh), and other applicable taxes are added to invoiced amounts unless quoted as tax-inclusive.',
         '税费 - 增值税(PPN)、预扣税(PPh)及其他适用税费将添加到发票金额中,除非报价为含税。'),
        ('Late payment - we may suspend services and charge interest at 1.5% per month on overdue balances, to the extent permitted by law.',
         '逾期付款 - 在法律允许的范围内,我们可暂停服务并按每月 1.5% 对逾期余额收取利息。'),
        ('Entire Agreement - these Terms (together with any Engagement and our Privacy Policy) constitute the entire agreement.',
         '完整协议 - 本条款(连同任何合作和我们的隐私政策)构成完整协议。'),
        ('Amendments - SURIOTA may update these Terms; material changes will be notified at least 14 days in advance.',
         '修订 - SURIOTA 可更新本条款;重大变更将至少提前 14 天通知。'),
        ('Severability - if any provision is held unenforceable, the remainder remains in effect.',
         '可分性 - 如任何条款被认定不可执行,其余部分仍然有效。'),
        ('Assignment - you may not assign these Terms without our written consent; SURIOTA may assign to an affiliate or successor.',
         '转让 - 未经我们书面同意,您不得转让本条款;SURIOTA 可转让给关联方或继任者。'),
        ('Force Majeure - neither party is liable for delays caused by events beyond reasonable control (natural disasters, war, pandemic, government action).',
         '不可抗力 - 任何一方对因合理控制范围之外的事件(自然灾害、战争、疫情、政府行为)造成的延迟不承担责任。'),
        ('Notices - written notices to admin@suriota.com for SURIOTA, or to the address you provided.',
         '通知 - 致 SURIOTA 的书面通知发至 admin@suriota.com,或致您提供的地址。'),
    ],
}

print(f'Refining {len(REFINEMENTS)} legal pages...')
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
import time as t
t.sleep(2)
for u in ['https://suriota.com/', 'https://suriota.com/id/beranda/']:
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
    print(f'  {u}: {r.status}')
