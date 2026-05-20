"""Final ZH refinement pass — remaining service + legal chunks."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

REFINEMENTS = {
    # SURGE-E (5458) — 1 remaining
    5458: [
        ('Our web-based SaaS platform empowers you to monitor', '我们的基于网络的 SaaS 平台让您能够监控'),
    ],

    # THM-30MD (5462) — 1 remaining
    5462: [
        ('with configurable slave ID and baud rate', '可配置从机 ID 和波特率'),
    ],

    # Contact (5465) — 1 remaining (residual chunk)
    5465: [
        ('Reach us via WhatsApp or email', '通过 WhatsApp 或邮箱联系'),
    ],

    # IoT (5468)
    5468: [
        ('SURIOTA designs and deploys IIoT systems that survive Indonesian industrial conditions - high humidity, fluctuating power, intermittent connectivity. Our stack covers sensors and gateways at the edge,',
         'SURIOTA 设计并部署能在印尼工业条件下生存的 IIoT 系统 - 高湿度、电力波动、间歇性连接。我们的技术栈涵盖边缘传感器和网关、'),
        ('Whether you are starting with a single line or scaling across multiple plants, we deliver a unified architecture - not a patchwork of point solutions.',
         '无论您是从单条生产线开始,还是跨多个工厂扩展,我们都提供统一架构 - 而非零散的点解决方案。'),
        ('Free initial consultation - share your scope, our engineering team responds within 24 hours with a feasibility check aligned to IEC 62443 security and IIoT best practices.',
         '免费初步咨询 - 分享您的范围,我们的工程团队将在 24 小时内提供符合 IEC 62443 安全和 IIoT 最佳实践的可行性检查。'),
        ('Yes. Our Modbus Gateway family bridges legacy automation (Modbus RTU/TCP) to modern IoT (MQTT). We support OPC UA, BACnet, and custom protocols.',
         '是。我们的 Modbus Gateway 系列将传统自动化(Modbus RTU/TCP)桥接到现代 IoT(MQTT)。我们支持 OPC UA、BACnet 和自定义协议。'),
        ('Both options. We can deploy our SURGE platform, or build on AWS, Azure, or GCP using your existing infrastructure.',
         '两种选项都可以。我们可以部署 SURGE 平台,或使用您现有的基础设施在 AWS、Azure 或 GCP 上构建。'),
    ],

    # SysInt (5469)
    5469: [
        ('Most industrial operations run a patchwork of vendor systems: PLCs from one brand, SCADA from another, an ERP that does not talk to either. SURIOTA designs integration architectures &mdash; data buses',
         '大多数工业运营运行着零散的厂商系统:一个品牌的 PLC、另一个品牌的 SCADA、与两者都无法对话的 ERP。SURIOTA 设计集成架构 — 数据总线'),
        ('No. We use non-invasive read-mostly integration patterns, and any write-back is gated by phased rollout with rollback capability.',
         '不会。我们使用非侵入式以读为主的集成模式,任何写回操作都通过具有回滚能力的分阶段推出来管控。'),
        ('Yes, including legacy or undocumented systems. We reverse-engineer protocols, write adapters, and document the interface for you.',
         '是的,包括传统或无文档的系统。我们逆向工程协议、编写适配器并为您记录接口文档。'),
        ('Every integration ships with API specs, runbooks, monitoring, and handover so you stay in control.',
         '每次集成都附带 API 规范、操作手册、监控和交接文档,让您保持掌控。'),
        ('Free initial consultation &mdash; share your stack, our engineering team responds within 24 hours with a phased integration plan that minimises operational risk.',
         '免费初步咨询 — 分享您的技术栈,我们的工程团队将在 24 小时内提供最小化运营风险的分阶段集成方案。'),
    ],

    # DC (5470)
    5470: [
        ('Many digital transformation programs stall because the roadmap was written by consultants who never built a thing. SURIOTA consultants are practising engineers - we have shipped 64+ industrial systems',
         '许多数字化转型项目停滞,因为路线图是由从未真正建造过任何东西的顾问编写的。SURIOTA 顾问是实践工程师 - 我们已交付 64+ 工业系统'),
        ('No. We are vendor-neutral. If an open-source tool or competitor product is the best fit, we will say so.',
         '不会。我们厂商中立。如果开源工具或竞争对手的产品更合适,我们会直说。'),
        ('Yes - we present jointly with you to the board, CFO, or steering committee. We answer the hard questions.',
         '是 - 我们与您一起向董事会、CFO 或指导委员会汇报。我们回答棘手的问题。'),
        ('No reseller incentive. We pick the right stack for your business, not the one with the best margin for us.',
         '没有经销商激励。我们为您的业务挑选合适的技术栈,而非利润最高的那个。'),
        ('Deliver the plan to your team, or execute it with you. Your call.',
         '将计划交付给您的团队,或与您一起执行。由您决定。'),
        ('We help you pick the right Industri 4.0 use cases',
         '我们帮助您选择正确的工业 4.0 用例'),
        ('sequence them by ROI and risk, and budget realistically',
         '按 ROI 和风险排序,并制定现实预算'),
        ('Then we can build them too, if you want one accountable partner.',
         '然后我们也可以构建它们,如果您想要一个负责任的合作伙伴。'),
    ],

    # AI (5471)
    5471: [
        ('Many industrial AI projects die in POC. SURIOTA treats AI like any other engineering discipline &mdash; with version control, observability, model registries, and SLA. We pick high-ROI use cases, trai',
         '许多工业 AI 项目在 POC 阶段失败。SURIOTA 像对待其他工程学科一样对待 AI — 配备版本控制、可观测性、模型注册表和 SLA。我们选择高 ROI 用例、训'),
        ('From predictive maintenance on rotating equipment to computer-vision quality control on production lines, our models run reliably in conditions where cloud GPUs are not available.',
         '从旋转设备的预测性维护到生产线的计算机视觉质量控制,我们的模型在没有云 GPU 的条件下也能可靠运行。'),
        ('Yes for inference. We quantise and compile models to run on edge devices (Jetson, x86 industrial PCs).',
         '推理可以。我们量化和编译模型以在边缘设备(Jetson、x86 工业 PC)上运行。'),
        ('Free initial consultation &mdash; share your data and use case, our ML team responds within 24 hours with a feasibility check including data sufficiency, baseline, and target metrics.',
         '免费初步咨询 — 分享您的数据和用例,我们的 ML 团队将在 24 小时内提供可行性检查,包括数据充分性、基线和目标指标。'),
    ],

    # DA (5472) — 1
    5472: [
        ('Free initial consultation - share your data sources, our team responds within 24 hours with a KPI map and a phased dashboard delivery plan.',
         '免费初步咨询 - 分享您的数据源,我们的团队将在 24 小时内提供 KPI 映射和分阶段仪表盘交付计划。'),
    ],

    # SaaS (5473)
    5473: [
        ('No infrastructure required. Our team will walk you through SURGE on data similar to yours within 24 hours of request - energy, vessel, water, or custom.',
         '无需基础设施。我们的团队将在请求后 24 小时内,使用与您类似的数据为您演示 SURGE - 能源、船舶、水或定制。'),
        ('SURGE is SURIOTA&rsquo;s multi-tenant SaaS platform - built for asset-heavy industries that need real-time monitoring, regulatory reporting, and operational insight without standing up their own infra',
         'SURGE 是 SURIOTA 的多租户 SaaS 平台 - 专为资产密集型行业打造,这些行业需要实时监控、合规报告和运营洞察,而无需建立自己的基础设'),
        ('Brand SURGE as your own product. Common for systems integrators and regional partners.',
         '将 SURGE 作为您自己的产品品牌。常用于系统集成商和区域合作伙伴。'),
        ('2-week trial tenant with your devices. We help connect the first few.',
         '2 周试用租户,使用您的设备。我们帮助连接前几台。'),
        ('Yes - on-prem SURGE is available for enterprise customers with strict data-locality needs. Includes Kubernetes Helm charts and runbooks.',
         '是 - 本地部署 SURGE 适用于有严格数据本地化需求的企业客户。包括 Kubernetes Helm chart 和操作手册。'),
        ('Three flagship modules ship today: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Need something different? We build custom SaaS on the same proven platform.',
         '今天有三个旗舰模块:SURGE-Energy Mapping、SURGE-Vessel Tracking、SURGE-Water Analytics。需要不同的?我们在同一经过验证的平台上构建定制 SaaS。'),
    ],

    # Privacy (5466) — remaining
    5466: [
        ('if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens.',
         '如果您在 SURGE 平台上创建账户,我们将收集您的用户名、哈希密码和身份验证令牌。'),
        ('Marketing communications \\u2014 only with your opt-in consent for the newsletter. You may unsubscribe at any time.',
         '营销通讯 — 仅在您选择订阅邮件列表时进行。您可随时取消订阅。'),
        ('This policy is aligned with Indonesia\\u2019s Personal Data Protection Law (UU PDP No.27\\/2022) and the EU General Data Protection Regulation (GDPR).',
         '本政策符合印尼个人数据保护法(UU PDP No.27/2022)和欧盟通用数据保护条例(GDPR)。'),
        ('for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the purpose of operating the contracted service.',
         '对于使用 SURGE 平台的 IoT 部署,我们收集设备标识符、传感器读数、地理位置(经同意时)和事件日志,严格用于运营所签订服务的目的。'),
        ('We may receive information from publicly available business directories, professional networks (e.g., LinkedIn), and our partners (e.g., distributors, integrators) when you interact with them about SU',
         '当您与我们的合作伙伴(例如经销商、集成商)就 SURIOTA 进行互动时,我们可能会从公开可用的商业目录、专业网络(例如 LinkedIn)和合作伙伴处接收信息'),
    ],

    # Terms (5467) — remaining major
    5467: [
        ('We warrant that the Services will be performed in a professional and workmanlike manner consistent with industry standards. Hardware Products carry the manufacturer-specified warranty period as printe',
         '我们保证服务将以专业的、符合工艺规范的方式履行,符合行业标准。硬件产品按制造商指定的保修期(如印'),
        ('EXCEPT AS EXPRESSLY STATED, THE SERVICES AND PRODUCTS ARE PROVIDED \\u201cAS IS\\u201d AND \\u201cAS AVAILABLE\\u201d, WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNES',
         '除明确声明外,服务和产品按"现状"和"可获得"提供,不提供任何明示或暗示的保证,包括适销性、适用'),
        ('TO THE MAXIMUM EXTENT PERMITTED BY LAW, SURIOTA\\u2019S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THESE TERMS OR ANY ENGAGEMENT SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO SURIOTA UNDER TH',
         '在法律允许的最大范围内,SURIOTA 因本条款或任何合作而产生或相关的总累计责任不应超过您根据'),
        ('SURIOTA provides Industrial IoT system integration, automation, water-treatment instrumentation, renewable-energy services, electrical engineering, and the SURGE Software-as-a-Service platform for ene',
         'SURIOTA 提供工业物联网系统集成、自动化、水处理仪表、可再生能源服务、电气工程以及 SURGE 软件即服务平台,用于能'),
        ('Some Services require account registration. You agree to: (a) provide accurate, current information; (b) maintain the security of your credentials; (c) promptly notify us of unauthorised access; and (',
         '某些服务需要账户注册。您同意:(a)提供准确、最新的信息;(b)维护您凭据的安全;(c)及时通知我们任何未经授权的访问;以及('),
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
import time as t
t.sleep(2)
for u in ['https://suriota.com/', 'https://suriota.com/id/beranda/']:
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
    print(f'  {u}: {r.status}')
