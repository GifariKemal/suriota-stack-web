"""
Direct translation script for legal pages 5466 (Privacy Policy) and 5467 (Terms).
Uses regex-based replacement for robustness against Unicode punctuation differences.
"""
import json, re

with open('translations/extract.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def normalize_apostrophes(text):
    """Normalize Unicode apostrophes to ASCII for matching."""
    return text.replace('\u2019', "'").replace('\u2018', "'")

# Privacy Policy replacements - using regex for flexibility
PRIVACY_REPLS = [
    # Hero subtitle
    (r'PT Surya Inovasi Prioritas \(SURIOTA\) [^<]*? This policy is aligned with [^\']+s Personal Data Protection Law \(UU PDP No\.27/2022\) and the EU General Data Protection Regulation \(GDPR\)\.',
     'PT Surya Inovasi Prioritas (SURIOTA) 如何收集、使用和保护您的个人数据。本政策符合印度尼西亚《个人数据保护法》（UU PDP No.27/2022）和欧盟《通用数据保护条例》（GDPR）。'),

    # Dates
    (r'生效日期：</strong> 18 May 2026', '生效日期：</strong> 2026年5月18日'),
    (r'最后更新：</strong> 18 May 2026', '最后更新：</strong> 2026年5月18日'),

    # Breadcrumb
    (r'<a href="/">Home</a>', '<a href="/">首页</a>'),

    # Section 1
    (r'PT Surya Inovasi Prioritas \("<strong>SURIOTA</strong>", "we", "us", or "our"\) respects your privacy and is committed to protecting your personal data\. This 隐私政策 explains how we collect, use, store, share, and protect personal data obtained through our website <a href="https://suriota\.com/">suriota\.com</a>, our products \(including the SURGE platform, SRT-MGATE-1210 Modbus 网关, ISO-M485, THM-30MD, PM1611-WD, and RS-485 Surge Protector\), and any related services\.',
     'PT Surya Inovasi Prioritas（"<strong>SURIOTA</strong>"、"我们"）尊重您的隐私并致力于保护您的个人数据。本隐私政策说明我们如何收集、使用、存储、共享和保护通过我们的网站 <a href="https://suriota.com/">suriota.com</a>、我们的产品（包括 SURGE 平台、SRT-MGATE-1210 Modbus 网关、ISO-M485、THM-30MD、PM1611-WD 和 RS-485 浪涌保护器）以及任何相关服务获得的个人数据。'),

    (r'By accessing our website, using our products, or engaging our services, you acknowledge that you have read and understood this 隐私政策\.',
     '访问我们的网站、使用我们的产品或接受我们的服务，即表示您确认已阅读并理解本隐私政策。'),

    # Section 2
    (r'The data controller responsible for your personal data is:', '负责您个人数据的数据控制方为：'),

    # Section 3
    (r'3\.1 Information You Provide', '3.1 您提供的信息'),
    (r'Contact details:', '联系方式：'),
    (r'name, email, phone, company, job role — when you submit RFQs, contact forms, or newsletter subscriptions\.',
     '姓名、邮箱、电话、公司、职位——当您提交询价单、联系表单或订阅新闻稿时。'),
    (r'Project information:', '项目信息：'),
    (r'technical specifications, deployment scope, location, and compliance requirements shared during quotation or consultation\.',
     '报价或咨询期间分享的技术规格、部署范围、位置和合规要求。'),
    (r'Account credentials:', '账户凭据：'),
    (r'if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens\.',
     '如果您在 SURGE 平台创建账户，我们会收集您的用户名、哈希密码和认证令牌。'),
    (r'Payment data:', '支付数据：'),
    (r'billing address and invoice details\. We do not store full credit-card numbers — payments are processed by certified third-party gateways\.',
     '账单地址和发票详情。我们不存储完整的信用卡号——支付由经认证的第三方网关处理。'),
    (r'Correspondence:', '通信记录：'),
    (r'emails, WhatsApp messages, and call logs you exchange with our team\.',
     '您与我们团队交换的电子邮件、WhatsApp 消息和通话记录。'),

    (r'3\.2 Information Collected Automatically', '3.2 自动收集的信息'),
    (r'Device &amp; usage:', '设备与使用情况：'),
    (r'IP address, browser type, operating system, referring URL, pages visited, time on site, and clickstream data\.',
     'IP 地址、浏览器类型、操作系统、来源网址、访问页面、停留时间和点击流数据。'),
    (r'Telemetry from products:', '产品遥测数据：'),
    (r'for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation \(when consented\), and event logs strictly for the purpose of operating the contracted service\.',
     '对于使用 SURGE 平台的物联网部署，我们仅出于运营合同服务的目的收集设备标识符、传感器读数、地理位置（经同意后）和事件日志。'),
    (r'Cookies &amp; similar technologies:', 'Cookies 与类似技术：'),
    (r'see Section 7 below\.', '见下方第7节。'),

    (r'3\.3 Information from Third Parties', '3.3 来自第三方的信息'),
    (r'We may receive information from publicly available business directories, professional networks \(e\.g\., LinkedIn\), and our partners \(e\.g\., distributors, integrators\) when you interact with them about SURIOTA products\.',
     '当您就 SURIOTA 产品与我们的合作伙伴（如分销商、集成商）互动时，我们可能会从公开的商业名录、专业社交网络（如 LinkedIn）以及合作伙伴处收到信息。'),

    # Section 4
    (r'We use personal data for the following purposes:', '我们将个人数据用于以下目的：'),
    (r'Responding to inquiries, quotations, and providing customer support\.', '回复咨询、报价并提供客户支持。'),
    (r'Delivering, operating, and improving our products and services \(including the SURGE platform\)\.', '交付、运营和改进我们的产品与服务（包括 SURGE 平台）。'),
    (r'Processing transactions, invoicing, and managing service contracts\.', '处理交易、开具发票和管理服务合同。'),
    (r'Sending service notifications, security alerts, and administrative messages\.', '发送服务通知、安全警报和管理消息。'),
    (r'Marketing communications — only with your opt-in consent for the newsletter\. You may unsubscribe at any time\.', '营销通讯——仅在您选择订阅新闻稿时发送。您可随时取消订阅。'),
    (r'Compliance with legal obligations under 印尼n law and applicable foreign jurisdictions\.', '遵守印尼法律及适用外国司法管辖区的法律义务。'),
    (r'Fraud prevention, security monitoring, and protecting our rights\.', '欺诈防范、安全监控和保护我们的权利。'),

    # Section 5
    (r'For users in the European Economic Area, our legal bases under GDPR Article 6 are:', '对于欧洲经济区用户，我们依据 GDPR 第6条的合法基础为：'),
    (r'<strong>Contract performance</strong> — to fulfil engagement and service agreements\.', '<strong>合同履行</strong>——履行合作与服务协议。'),
    (r'<strong>Legitimate interests</strong> — to operate our business, secure our services, and develop our products\.', '<strong>合法权益</strong>——运营我们的业务、保障服务安全并开发产品。'),
    (r'<strong>Consent</strong> — for marketing and optional cookies\. You may withdraw consent at any time\.', '<strong>同意</strong>——用于营销和可选 Cookies。您可随时撤回同意。'),
    (r'<strong>Legal obligation</strong> — to comply with tax, accounting, and regulatory requirements\.', '<strong>法律义务</strong>——遵守税务、会计和监管要求。'),

    # Section 6
    (r'We do <strong>not</strong> sell personal data\. We may share information with:', '我们<strong>不会</strong>出售个人数据。我们可能在以下情况下共享信息：'),
    (r'<strong>Service providers</strong> processing data on our behalf \(cloud hosting, email delivery, analytics, payment\) under written data-processing agreements\.',
     '<strong>服务提供商</strong>代表我们处理数据（云托管、电子邮件发送、分析、支付），受书面数据处理协议约束。'),
    (r'<strong>Project partners</strong> — integrators, certified installers, or auditors involved in delivering your project, only as necessary\.',
     '<strong>项目合作伙伴</strong>——参与交付您项目的集成商、认证安装商或审计师，仅在必要时。'),
    (r'<strong>Authorities</strong> — if required by law, court order, or to protect rights, property, or safety\.',
     '<strong>主管机关</strong>——如法律、法院命令要求，或为保护权利、财产或安全。'),
    (r'<strong>Successor entities</strong> in the event of merger, acquisition, or asset transfer, with continuity of this Policy[\'\u2019]s protections\.',
     '<strong>继任实体</strong>——在合并、收购或资产转让时，本政策的保护措施继续适用。'),

    # Section 7
    (r'We use cookies and similar technologies for:', '我们使用 Cookies 和类似技术用于：'),
    (r'<strong>Strictly necessary cookies</strong> — site functionality, login state, and security\. Cannot be disabled\.',
     '<strong>绝对必要 Cookies</strong>——网站功能、登录状态和安全。不可禁用。'),
    (r'<strong>Analytics cookies</strong> — to understand traffic and improve content \(e\.g\., Google Analytics\)\. You may opt out via your browser settings\.',
     '<strong>分析 Cookies</strong>——了解流量并改进内容（如 Google Analytics）。您可通过浏览器设置选择退出。'),
    (r'<strong>Marketing cookies</strong> — only set with your explicit consent \(where applicable\)\.', '<strong>营销 Cookies</strong>——仅在您明确同意时设置（如适用）。'),
    (r'Most browsers allow you to refuse or delete cookies\. Disabling strictly-necessary cookies may impact site functionality\.',
     '大多数浏览器允许您拒绝或删除 Cookies。禁用绝对必要 Cookies 可能影响网站功能。'),

    # Section 8
    (r'We retain personal data only as long as necessary for the purposes for which it was collected, or as required by law:', '我们仅在为实现收集目的所必需或法律要求的期限内保留个人数据：'),
    (r'<strong>Lead &amp; inquiry data:</strong> up to 24 months from last interaction\.', '<strong>线索与咨询数据：</strong>自上次互动起最多24个月。'),
    (r'<strong>Customer / project records:</strong> for the duration of the engagement plus 10 years \(印尼n commercial-records requirement\)\.', '<strong>客户/项目记录：</strong>合作期间加10年（印尼商业记录要求）。'),
    (r'<strong>Financial / tax records:</strong> minimum 10 years \(印尼n Taxation Law\)\.', '<strong>财务/税务记录：</strong>最少10年（印尼税法）。'),
    (r'<strong>Marketing subscribers:</strong> until you unsubscribe\.', '<strong>营销订阅者：</strong>直到您取消订阅。'),
    (r'<strong>IoT telemetry:</strong> as defined in the service-specific data-processing agreement\.', '<strong>物联网遥测数据：</strong>按具体服务的数据处理协议定义。'),

    # Section 9
    (r'We implement technical and organisational measures including encryption in transit \(TLS 1\.2\+\), encryption at rest, role-based access controls, audit logging, regular security assessments, and staff training\. While we strive to safeguard your data, no method of transmission or storage is 100% secure; we will notify you and the relevant authority within 72 hours of becoming aware of a personal-data breach that materially affects your rights\.',
     '我们实施技术和组织措施，包括传输加密（TLS 1.2+）、静态加密、基于角色的访问控制、审计日志、定期安全评估和员工培训。虽然我们努力保护您的数据，但没有任何传输或存储方法是100%安全的；我们在发现影响您权利的个人数据泄露后72小时内通知您和相关主管机关。'),

    # Section 10
    (r'Some of our service providers may process data outside 印尼\. When transferring personal data internationally, we ensure adequate protection through Standard Contractual Clauses \(SCCs\), adequacy decisions, or other lawful safeguards under UU PDP and GDPR\.',
     '我们的一些服务提供商可能在印尼境外处理数据。在进行国际个人数据传输时，我们通过标准合同条款（SCC）、充分性认定或 UU PDP 和 GDPR 下的其他合法保障措施确保充分保护。'),

    # Section 11
    (r'Under <strong>UU PDP No\.27/2022</strong> \(印尼\) and <strong>GDPR</strong> \(EU\), you have the right to:', '依据<strong>UU PDP No.27/2022</strong>（印尼）和<strong>GDPR</strong>（欧盟），您有权：'),
    (r'<strong>Access</strong> — obtain confirmation of and a copy of your data we hold\.', '<strong>访问</strong>——获取确认并复制我们持有的您的数据。'),
    (r'<strong>Rectification</strong> — correct inaccurate or incomplete data\.', '<strong>更正</strong>——更正不准确或不完整的数据。'),
    (r'<strong>Erasure / Right to be Forgotten</strong> — request deletion where legally permissible\.', '<strong>删除/被遗忘权</strong>——在法律允许的情况下请求删除。'),
    (r'<strong>Restriction</strong> — limit processing in certain circumstances\.', '<strong>限制处理</strong>——在特定情况下限制处理。'),
    (r'<strong>Portability</strong> — receive your data in a structured, machine-readable format\.', '<strong>可携带性</strong>——以结构化、机器可读的格式接收您的数据。'),
    (r'<strong>Objection</strong> — object to processing based on legitimate interests, including profiling for marketing\.', '<strong>反对</strong>——反对基于合法权益的处理，包括用于营销的分析。'),
    (r'<strong>Withdraw consent</strong> — at any time, without affecting prior lawful processing\.', '<strong>撤回同意</strong>——随时撤回，不影响之前合法的处理。'),
    (r'<strong>Lodge a complaint</strong> with 印尼[\'\u2019]s Personal Data Protection Agency or your EU supervisory authority\.',
     '<strong>提出投诉</strong>——向印尼个人数据保护机构或您的欧盟监管机构提出投诉。'),
    (r'To exercise these rights, contact <a href="mailto:admin@suriota\.com">admin@suriota\.com</a>\. We will respond within 30 calendar days\.',
     '如需行使这些权利，请联系 <a href="mailto:admin@suriota.com">admin@suriota.com</a>。我们将在30个日历日内回复。'),

    # Section 12
    (r'Our services are intended for businesses and adult professionals\. We do not knowingly collect personal data from individuals under 18 years of age\. If you believe a minor has provided us with personal data, please contact us so we can delete it\.',
     '我们的服务面向企业和成年专业人士。我们不会在知情的情况下收集18岁以下未成年人的个人数据。如果您认为未成年人向我们提供了个人数据，请联系我们以便删除。'),

    # Section 13
    (r'We may update this 隐私政策 from time to time\. The latest version will always be posted on this page, with the ["\u201c]最后更新["\u201d] date revised\. Material changes will be communicated by email or prominent notice on our website at least 14 days before they take effect\.',
     '我们可能会不时更新本隐私政策。最新版本将始终发布在本页面，并更新"最后更新"日期。重大变更将在生效前至少14天通过电子邮件或网站显著通知告知。'),

    # Section 14
    (r'For questions about this 隐私政策 or to exercise your data-protection rights, please contact:', '如有关于本隐私政策的问题或希望行使您的数据保护权利，请联系：'),
]

TERMS_REPLS = [
    # Dates
    (r'生效日期：</strong> 18 May 2026', '生效日期：</strong> 2026年5月18日'),
    (r'最后更新：</strong> 18 May 2026', '最后更新：</strong> 2026年5月18日'),
    (r'<a href="/">Home</a>', '<a href="/">首页</a>'),

    # Section 1
    (r'These 服务条款 \("<strong>Terms</strong>"\) form a binding agreement between you \("you" or "Client"\) and PT Surya Inovasi Prioritas \("<strong>SURIOTA</strong>", "we", "us", or "our"\)\. By accessing our website, purchasing our products, or using our services, you agree to be bound by these Terms together with our <a href="/privacy-policy/">隐私政策</a>\. If you do not agree, you may not use the services\.',
     '本服务条款（"<strong>条款</strong>"）构成您（"您"或"客户"）与 PT Surya Inovasi Prioritas（"<strong>SURIOTA</strong>"、"我们"）之间具有约束力的协议。访问我们的网站、购买我们的产品或使用我们的服务，即表示您同意受本条款及我们的<a href="/privacy-policy/">隐私政策</a>约束。如您不同意，请勿使用服务。'),

    # Section 2
    (r'<li><strong>服务</strong> — engineering, integration, consultation, and SaaS offerings provided by SURIOTA, including the SURGE platform\.</li>',
     '<li><strong>服务</strong>——SURIOTA 提供的工程、集成、咨询和 SaaS 产品，包括 SURGE 平台。</li>'),
    (r'<li><strong>Products</strong> — hardware manufactured or distributed by SURIOTA \(SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 SPD, Wastewater Logger, and successors\)\.</li>',
     '<li><strong>产品</strong>——SURIOTA 制造或分销的硬件（SRT-MGATE-1210、ISO-M485、THM-30MD、PM1611-WD、RS-485 SPD、废水记录仪及后续产品）。</li>'),
    (r'<li><strong>Engagement</strong> — a project, support contract, or subscription agreed in writing \(Statement of Work, Purchase Order, or service plan\)\.</li>',
     '<li><strong>合作项目</strong>——书面约定的项目、支持合同或订阅（工作说明书、采购订单或服务计划）。</li>'),
    (r'<li><strong>Deliverables</strong> — documents, designs, code, configurations, reports, or installed equipment produced under an Engagement\.</li>',
     '<li><strong>交付物</strong>——合作项目下产生的文件、设计、代码、配置、报告或已安装设备。</li>'),
    (r'<li><strong>Confidential Information</strong> — any non-public information disclosed by either party that should reasonably be understood to be confidential\.</li>',
     '<li><strong>保密信息</strong>——任何一方披露的、理应被理解为保密的非公开信息。</li>'),

    # Section 3
    (r'SURIOTA provides Industrial IoT system integration, automation, water-treatment instrumentation, renewable-energy services, electrical engineering, and the SURGE Software-as-a-Service platform for energy mapping, vessel tracking, and water analytics\. Specific scope, deliverables, timelines, and acceptance criteria are defined in the applicable Statement of Work or service plan\.',
     'SURIOTA 提供工业物联网系统集成、自动化、水处理仪表、可再生能源服务、电气工程，以及用于能源图谱、船舶追踪和水质分析的 SURGE 软件即服务平台。具体范围、交付物、时间表和验收标准在适用的工作说明书或服务计划中定义。'),
    (r'SURIOTA may modify, suspend, or discontinue any portion of the 服务 with reasonable notice, except where prohibited by contract\.',
     'SURIOTA 可在合理通知的情况下修改、暂停或停止任何部分服务，但合同禁止的除外。'),

    # Section 4
    (r'Some 服务 require account registration\. You agree to: \(a\) provide accurate, current information; \(b\) maintain the security of your credentials; \(c\) promptly notify us of unauthorised access; and \(d\) accept responsibility for all activities under your account\. SURIOTA may suspend accounts for security or compliance reasons\.',
     '部分服务需要账户注册。您同意：（a）提供准确、最新的信息；（b）维护凭据安全；（c）及时通知我们未经授权的访问；以及（d）对账户下的所有活动承担责任。SURIOTA 可出于安全或合规原因暂停账户。'),

    # Section 5
    (r'You agree not to:', '您同意不从事以下行为：'),
    (r'Reverse-engineer, decompile, or disassemble our software except as permitted by law\.', '对我们的软件进行逆向工程、反编译或反汇编，除非法律允许。'),
    (r'Use the 服务 to violate any law or regulation, including export controls\.', '使用服务违反任何法律或法规，包括出口管制。'),
    (r'Upload malware, conduct security testing without prior written consent, or otherwise interfere with the integrity of our systems\.', '上传恶意软件、未经事先书面同意进行安全测试，或以其他方式干扰我们系统的完整性。'),
    (r'Resell, sublicense, or commercially exploit the 服务 without our written agreement\.', '未经我们书面同意转售、再许可或商业性利用服务。'),
    (r'Misrepresent SURIOTA, its personnel, or our deliverables\.', '对 SURIOTA、其人员或我们的交付物作虚假陈述。'),

    # Section 6
    (r'All firmware, software, designs, schematics, documentation, trademarks, and know-how created or owned by SURIOTA — including the SURGE platform and all Products — remain the exclusive property of SURIOTA\. We grant you a non-exclusive, non-transferable licence to use the Products and 服务 solely for their intended business purpose\.',
     'SURIOTA 创建或拥有的所有固件、软件、设计、原理图、文档、商标和专有技术——包括 SURGE 平台和所有产品——仍为 SURIOTA 的专属财产。我们授予您非独占、不可转让的许可，仅将产品和服务用于其预期的商业目的。'),
    (r'You retain ownership of materials you provide to us\. You grant SURIOTA a licence to use such materials as necessary to perform the 服务\.',
     '您保留向我们提供的材料的所有权。您授予 SURIOTA 为履行服务而必要使用这些材料的许可。'),
    (r'Unless otherwise stated in the Engagement, custom Deliverables are licensed \(not sold\) to you upon full payment\. SURIOTA retains rights to reusable components, frameworks, and tooling\.',
     '除非合作项目另有说明，定制交付物在全额付款后许可（而非出售）给您。SURIOTA 保留对可复用组件、框架和工具的权​​利。'),

    # Section 7
    (r'<li><strong>Pricing</strong> — as quoted in writing\. Quotes are valid for 30 days unless extended\.</li>',
     '<li><strong>定价</strong>——以书面报价为准。报价有效期为30天，除非延长。</li>'),
    (r'<li><strong>Currency</strong> — 印尼n Rupiah \(IDR\) unless otherwise stated\.</li>',
     '<li><strong>货币</strong>——印尼盾（IDR），除非另有说明。</li>'),
    (r'<li><strong>Taxes</strong> — VAT \(PPN\), withholding tax \(PPh\), and other applicable taxes are added to invoiced amounts unless quoted as tax-inclusive\.</li>',
     '<li><strong>税费</strong>——增值税（PPN）、预扣税（PPh）及其他适用税费将加入发票金额，除非报价已含税。</li>'),
    (r'<li><strong>Payment terms</strong> — standard Net 14 days from invoice; project deposits or milestone payments may apply\.</li>',
     '<li><strong>付款条件</strong>——标准自发票日起14天内付款；项目可能需要定金或里程碑付款。</li>'),
    (r'<li><strong>Late payment</strong> — we may suspend services and charge interest at 1\.5% per month on overdue balances, to the extent permitted by law\.</li>',
     '<li><strong>逾期付款</strong>——我们可暂停服务，并在法律允许的范围内对逾期余额按月收取1.5%的利息。</li>'),
    (r'<li><strong>Disputes</strong> — invoice disputes must be raised in writing within 7 business days of receipt\.</li>',
     '<li><strong>争议</strong>——发票争议必须在收到后7个工作日内以书面形式提出。</li>'),

    # Section 8
    (r'Each party will protect the other[\'\u2019]s Confidential Information with the same degree of care it uses to protect its own \(no less than reasonable care\), use it solely to perform the Engagement, and not disclose it to third parties without consent, except as required by law\. Confidentiality obligations survive termination for five \(5\) years\.',
     '各方将以保护自身保密信息同等的谨慎程度（不低于合理谨慎）保护对方的保密信息，仅将其用于履行合作项目，未经同意不向第三方披露，但法律要求的除外。保密义务在终止后继续有效五年。'),

    # Section 9
    (r'We warrant that the 服务 will be performed in a professional and workmanlike manner consistent with industry standards\. Hardware Products carry the manufacturer-specified warranty period as printed on the datasheet \(typically 12–24 months from delivery\)\.',
     '我们保证服务将以符合行业标准的专业方式执行。硬件产品享有制造商在数据表中规定的保修期（通常为交付后12-24个月）。'),
    (r'EXCEPT AS EXPRESSLY STATED, THE SERVICES AND PRODUCTS ARE PROVIDED ["\u201c]AS IS["\u201d] AND ["\u201c]AS AVAILABLE["\u201d], WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT\. SURIOTA DOES NOT WARRANT UNINTERRUPTED OR ERROR-FREE OPERATION OF SAAS SERVICES\.',
     '除明确声明外，服务和产品按"原样"和"可用"提供，不作任何明示或暗示的保证，包括适销性、特定用途适用性或非侵权。SURIOTA 不保证 SaaS 服务不间断或无错误运行。'),

    # Section 10
    (r'TO THE MAXIMUM EXTENT PERMITTED BY LAW, SURIOTA[\'\u2019]S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THESE TERMS OR ANY ENGAGEMENT SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO SURIOTA UNDER THE APPLICABLE ENGAGEMENT IN THE TWELVE \(12\) MONTHS PRECEDING THE EVENT GIVING RISE TO THE CLAIM\.',
     '在法律允许的最大范围内，因本条款或任何合作项目引起的 SURIOTA 总累计责任不超过您在引起索赔的事件发生前十二（12）个月内就该合作项目向 SURIOTA 支付的金额。'),
    (r'IN NO EVENT SHALL SURIOTA BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR FOR LOSS OF PROFITS, REVENUE, DATA, OR USE — EVEN IF ADVISED OF THE POSSIBILITY\.',
     '在任何情况下，SURIOTA 不对间接、附带、特殊、后果性或惩罚性损害，或利润、收入、数据或使用损失承担责任——即使已告知该等可能性。'),

    # Section 11
    (r'You agree to defend, indemnify, and hold harmless SURIOTA, its officers, directors, employees, and agents from and against any claims, damages, losses, liabilities, costs, and expenses \(including reasonable legal fees\) arising from: \(a\) your breach of these Terms; \(b\) your misuse of the 服务 or Products; \(c\) your violation of any law or third-party right; or \(d\) materials you provided to us\.',
     '您同意就以下原因引起的任何索赔、损害、损失、责任、费用和开支（包括合理的法律费用）为 SURIOTA、其管理人员、董事、员工和代理进行辩护、赔偿并使其免受损害：（a）您违反本条款；（b）您滥用服务或产品；（c）您违反任何法律或第三方权利；或（d）您向我们提供的材料。'),

    # Section 12
    (r'These Terms remain in effect while you use the 服务\. Either party may terminate an Engagement with thirty \(30\) days[\'\u2019] written notice, or immediately for material breach not cured within fifteen \(15\) days of written notice\. Sections 6, 8, 9\.2, 10, 11, 13, and 14 survive termination\. Upon termination, you remain responsible for fees accrued before termination\.',
     '本条款在您使用服务期间持续有效。任何一方可提前三十（30）天书面通知终止合作项目，或在重大违约且收到书面通知后十五（15）天内未纠正的情况下立即终止。第6、8、9.2、10、11、13和14条在终止后继续有效。终止后，您仍需承担终止前产生的费用。'),

    # Section 13
    (r'These Terms are governed by the laws of the Republic of 印尼, without regard to its conflict-of-laws principles\. Subject to Section 14 below, any legal proceeding shall be brought exclusively in the competent courts of Batam, Kepulauan Riau, 印尼\.',
     '本条款受印度尼西亚共和国法律管辖，不考虑其法律冲突原则。除下文第14条外，任何法律程序应仅在印尼廖内群岛巴淡岛的有管辖权法院提起。'),

    # Section 14
    (r'The parties will first attempt to resolve any dispute through good-faith negotiation between authorised representatives\. If unresolved within thirty \(30\) days, the dispute shall be submitted to binding arbitration administered by the 印尼n National Arbitration Board \(BANI\) in Jakarta, in the English language\. The arbitral award shall be final and binding\. Nothing in this section prevents either party from seeking injunctive relief in court for IP or confidentiality breaches\.',
     '双方应首先通过授权代表之间的善意谈判解决任何争议。如三十（30）天内未解决，争议应提交印尼国家仲裁委员会（BANI）在雅加达进行的具有约束力的仲裁，仲裁语言为英语。仲裁裁决为终局裁决并具有约束力。本条不妨碍任何一方就知识产权或保密违约向法院寻求禁令救济。'),

    # Section 15
    (r'<li><strong>Entire Agreement</strong> — these Terms \(together with any Engagement and our 隐私政策\) constitute the entire agreement\.</li>',
     '<li><strong>完整协议</strong>——本条款（连同任何合作项目及我们的隐私政策）构成完整协议。</li>'),
    (r'<li><strong>Amendments</strong> — SURIOTA may update these Terms; material changes will be notified at least 14 days in advance\.</li>',
     '<li><strong>修订</strong>——SURIOTA 可更新本条款；重大变更将至少提前14天通知。</li>'),
    (r'<li><strong>Severability</strong> — if any provision is held unenforceable, the remainder remains in effect\.</li>',
     '<li><strong>可分割性</strong>——如任何条款被认定不可执行，其余条款仍然有效。</li>'),
    (r'<li><strong>No Waiver</strong> — failure to enforce a right does not waive it\.</li>',
     '<li><strong>不放弃权利</strong>——未行使权利不构成放弃。</li>'),
    (r'<li><strong>Assignment</strong> — you may not assign these Terms without our written consent; SURIOTA may assign to an affiliate or successor\.</li>',
     '<li><strong>转让</strong>——未经我们书面同意，您不得转让本条款；SURIOTA 可转让给关联方或继任者。</li>'),
    (r'<li><strong>Force Majeure</strong> — neither party is liable for delays caused by events beyond reasonable control \(natural disasters, war, pandemic, government action\)\.</li>',
     '<li><strong>不可抗力</strong>——任何一方不对超出合理控制的事件（自然灾害、战争、疫情、政府行为）造成的延误承担责任。</li>'),
    (r'<li><strong>Notices</strong> — written notices to <a href="mailto:admin@suriota\.com">admin@suriota\.com</a> for SURIOTA, or to the address you provided\.</li>',
     '<li><strong>通知</strong>——致 SURIOTA 的书面通知请发送至 <a href="mailto:admin@suriota.com">admin@suriota.com</a>，或发送至您提供的地址。</li>'),

    # Section 16
    (r'Questions about these Terms\? We are happy to clarify before you commit\.',
     '对这些条款有疑问？我们很乐意在您承诺前为您解答。'),
]

def translate_page(html, replacements):
    result = html
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result)
    return result

# Find and update pages
for item in data:
    if item['page_id'] == 5466:
        original = item['original']
        translated = translate_page(original, PRIVACY_REPLS)
        item['translated'] = translated
        # Count changes
        changes = sum(1 for p, r in PRIVACY_REPLS if re.search(p, original))
        print(f'Page 5466: applied {changes}/{len(PRIVACY_REPLS)} regex replacements')

    if item['page_id'] == 5467:
        original = item['original']
        translated = translate_page(original, TERMS_REPLS)
        item['translated'] = translated
        changes = sum(1 for p, r in TERMS_REPLS if re.search(p, original))
        print(f'Page 5467: applied {changes}/{len(TERMS_REPLS)} regex replacements')

# Save
with open('translations/extract.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved extract.json')

# Verify
for item in data:
    if item['page_id'] in (5466, 5467):
        text = item.get('translated', item['original'])
        chinese = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        ascii_words = len(re.findall(r'[a-zA-Z]+', text))
        print(f"Page {item['page_id']}: Chinese chars={chinese}, English words={ascii_words}")
