"""Final v3 refinement — clean up remaining residuals."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

REFINEMENTS = {
    # SURGE-E (5458) — SLA
    5458: [
        ('We guarantee 99.9% 在线率 SLA with critical alert response under 35 seconds. Our infrastructure includes redundant servers, automated failover, and continuous monitoring for production-grade reliability.',
         '我们保证 99.9% 在线率 SLA,关键告警响应 35 秒内。基础设施包括冗余服务器、自动故障转移和持续监控,提供生产级可靠性。'),
    ],
    # THM-30MD (5462) — mid-sentence splice fix
    5462: [
        ('该设备采用高性能 SHT30 Sensirion 传感器,确保精确的环境监toring in even the toughest industrial conditions. Protecting your equipment, processes, and products.',
         '该设备采用高性能 SHT30 Sensirion 传感器,即使在最严苛的工业条件下也能确保精确的环境监测。保护您的设备、流程和产品。'),
    ],
    # Contact (5465)
    5465: [
        ('Within 24 hours, we route your inquiry to the right domain expert (IoT, SCADA, water, solar, electrical).',
         '24 小时内,我们将您的咨询转给对应领域专家(IoT、SCADA、水务、太阳能、电气)。'),
    ],
    # IoT (5468) — mid-sentence splice fix
    5468: [
        ('SURIOTA 设计并部署能在印尼工业条件下生存的 IIoT 系统 - 高湿度、电力波动、间歇性连接。我们的技术栈涵盖边缘传感器和网关、 secure protocol translation (Modbus, BACnet, OPC UA, MQTT), cellular and LoRaWAN backhaul, and cloud analytics on our SURGE platfor',
         'SURIOTA 设计并部署能在印尼工业条件下生存的 IIoT 系统 - 高湿度、电力波动、间歇性连接。我们的技术栈涵盖边缘传感器与网关、安全协议转换(Modbus、BACnet、OPC UA、MQTT)、蜂窝和 LoRaWAN 回传,以及在 SURGE 平台'),
    ],
    # DC (5470) — 4 chunks
    5470: [
        ('许多数字化转型项目停滞,因为路线图是由从未真正建造过任何东西的顾问编写的。SURIOTA 顾问是实践工程师 - 我们已交付 64+ 工业系统 - so our advice is rooted in what actually works on the plant floor.',
         '许多数字化转型项目停滞,因为路线图是由从未真正建造过任何东西的顾问编写的。SURIOTA 顾问是实践工程师 - 我们已交付 64+ 工业系统 - 因此我们的建议根植于真正在车间起作用的实践。'),
        ('If you choose to execute, the same team that scoped the plan can implement it. No handover gap.',
         '如果您选择执行,负责规划范围的同一团队可以实施它。没有交接断层。'),
        ('Of course. Confidentiality is fundamental to consulting. We sign mutual NDAs before any non-public discussion.',
         '当然。保密性是咨询的基本要求。在任何非公开讨论之前,我们都会签署双向 NDA。'),
        ('Free initial consultation - share your context, our consulting team responds within 24 hours with a scoped engagement proposal aligned to your business outcomes.',
         '免费初步咨询 - 分享您的背景,我们的咨询团队将在 24 小时内提供与您业务成果对齐的合作提案范围。'),
    ],
    # Privacy (5466) — 10 chunks
    5466: [
        ('in the event of merger, acquisition, or asset transfer, with continuity of this Policy\\u2019s protections.',
         '在合并、收购或资产转让时,本政策的保护持续有效。'),
        ('We retain personal data only as long as necessary for the purposes for which it was collected, or as required by law:',
         '我们仅在收集目的所需期间或法律要求期间保留个人数据:'),
        ('Some of our service providers may process data outside Indonesia. When transferring personal data internationally, we ensure adequate protection through Standard Contractual Clauses (SCCs), adequacy d',
         '我们的部分服务提供商可能在印尼境外处理数据。在跨境传输个人数据时,我们通过标准合同条款(SCC)、充分性决'),
        (', our products (including the SURGE platform, SRT-MGATE-1210 Modbus Gateway, ISO-M485, THM-30MD, PM1611-WD, and RS-485 Surge Protector), and any related services.',
         '、我们的产品(包括 SURGE 平台、SRT-MGATE-1210 Modbus Gateway、ISO-M485、THM-30MD、PM1611-WD 和 RS-485 浪涌保护器)以及任何相关服务。'),
        ('billing address and invoice details. We do not store full credit-card numbers \\u2014 payments are processed by certified third-party gateways.',
         '账单地址和发票详情。我们不存储完整信用卡号 — 支付由经认证的第三方网关处理。'),
        ('Successor entities', '继承实体'),
        ('Lead &amp; inquiry data: up to 24 months from last interaction.',
         '潜在客户和咨询数据:自最后一次互动起最多 24 个月。'),
        ('Lead & inquiry data: up to 24 months from last interaction.',
         '潜在客户和咨询数据:自最后一次互动起最多 24 个月。'),
        ('Client / project records: for the duration of the engagement plus 10 years (Indonesian commercial-records requirement).',
         '客户/项目记录:合作期间外加 10 年(印尼商业记录要求)。'),
        ('IoT telemetry: as defined in the service-specific data-processing agreement.',
         'IoT 遥测:依据服务专属数据处理协议中的定义。'),
    ],
    # Terms (5467) — 24 chunks
    5467: [
        ('您同意为 SURIOTA、其高级职员、董事、雇员和代理人辩护、赔偿并使其免受任何索赔、损害、损失、责任、费用和支出(包括合onable legal fees) arising from: (a) your breach of these Terms; (b) your misuse of the Services or Products; (c) your violation of any law',
         '您同意为 SURIOTA、其高级职员、董事、雇员和代理人辩护、赔偿并使其免受任何索赔、损害、损失、责任、费用和支出(包括合理的法律费用),这些来自:(a)您违反本条款;(b)您滥用服务或产品;(c)您违反任何法律'),
        ('These Terms are governed by the laws of the Republic of Indonesia, without regard to its conflict-of-laws principles. Subject to Section 14 below, any legal proceeding shall be brought exclusively in',
         '本条款受印度尼西亚共和国法律管辖,不考虑其法律冲突原则。在符合下文第 14 条的前提下,任何法律诉讼应专属于'),
        ('The agreement that governs your use of the SURIOTA website, our products (SURGE platform, SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 Surge Protector), and our engineering services. Please r',
         '关于您使用 SURIOTA 网站、我们的产品(SURGE 平台、SRT-MGATE-1210、ISO-M485、THM-30MD、PM1611-WD、RS-485 浪涌保护器)及工程服务的协议。请仔'),
        ('\\u201d, \\u201cwe\\u201d, \\u201cus\\u201d, or \\u201cour\\u201d). By accessing our website, purchasing our products, or using our services, you agree to be bound by these Terms together with our',
         '","我们")。通过访问我们的网站、购买我们的产品或使用我们的服务,您同意受本条款以及我们的'),
        ('SURIOTA 提供工业物联网系统集成、自动化、水处理仪表、可再生能源服务、电气工程以及 SURGE 软件即服务平台,用于能rgy mapping, vessel tracking, and water analytics. Specific scope, deliverables, timelines, and acceptance criteria are defined in the app',
         'SURIOTA 提供工业物联网系统集成、自动化、水处理仪表、可再生能源服务、电气工程以及 SURGE 软件即服务平台,用于能源监测、船舶追踪和水质分析。具体范围、交付物、时间表和验收标准在适'),
        ('Privacy Policy</a>. If you do not agree, you may not use the Services.',
         '隐私政策</a>。如您不同意,则不得使用本服务。'),
        ('You must be at least 18 years of age and have authority to bind the entity you represent.',
         '您必须年满 18 岁,并有权代表您所代表的实体签订合同。'),
        ('Refunds - the SaaS subscription is non-refundable after 14 days of activation. Hardware refunds follow the manufacturer warranty and return policy.',
         '退款 - SaaS 订阅在激活 14 天后不可退款。硬件退款遵循制造商的保修和退货政策。'),
        ('You may not use the Services or Products to:',
         '您不得将服务或产品用于:'),
        ('engage in illegal activities or infringe upon third-party rights',
         '从事违法活动或侵犯第三方权利'),
        ('attempt to reverse-engineer or interfere with the operation of the SURGE platform',
         '试图反向工程或干扰 SURGE 平台的运行'),
        ('upload malicious code or attempt unauthorised access',
         '上传恶意代码或试图未授权访问'),
        ('SURIOTA Materials', 'SURIOTA 材料'),
        ('We grant you a non-exclusive, non-transferable licence to use the Products and Services solely for their intended business purpose.',
         '我们授予您非独占、不可转让的许可,仅供您将产品和服务用于其预期商业目的。'),
        ('Client Materials', '客户材料'),
        ('You retain ownership of materials you provide to us. You grant SURIOTA a license to use such materials as necessary to perform the Services.',
         '您保留向我们提供的材料的所有权。您授予 SURIOTA 在履行服务所必需的范围内使用此类材料的许可。'),
        ('Deliverables', '交付物'),
        ('Unless otherwise specified in the Engagement, custom Deliverables developed for you become your property upon full payment.',
         '除非合作中另有规定,为您开发的定制交付物在全额付款后归您所有。'),
        ('Open-source components retain their original licences.', '开源组件保留其原始许可证。'),
        ('Hardware Warranty', '硬件保修'),
        ('Service Warranty', '服务保修'),
        ('Disclaimers', '免责声明'),
        ('Limitation of Liability', '责任限制'),
        ('Indemnification', '赔偿'),
        ('Term &amp; Termination', '期限与终止'),
        ('Term & Termination', '期限与终止'),
        ('Dispute Resolution', '争议解决'),
        ('Governing Law &amp; Jurisdiction', '管辖法律与司法管辖'),
        ('Governing Law & Jurisdiction', '管辖法律与司法管辖'),
        ('General Provisions', '通用条款'),
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
