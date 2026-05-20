"""Refine ZH pages — fill remaining English chunks."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Per-page translation refinements (exact match strings)
REFINEMENTS = {
    # ==================== ABOUT (5450) ====================
    5450: [
        (', we have been designing and manufacturing industrial connectivity solutions. From Modbus gateways to complete IoT platforms.',
         ',我们一直在设计和制造工业连接解决方案。从 Modbus 网关到完整的物联网平台。'),
        ('PT Surya Inovasi Prioritas (SURIOTA)</strong> is a technology company specializing in <strong>Industrial IoT Services and System Integration',
         'PT Surya Inovasi Prioritas (SURIOTA)</strong> 是专注于<strong>工业物联网服务与系统集成'),
        ('headquartered in Batam Centre, Riau Islands', '总部位于廖内群岛巴淡岛中心'),
        ('industrial projects across manufacturing, energy, logistics, and maritime sectors',
         '个工业项目,覆盖制造、能源、物流和海事行业'),
        ('In-house products: <strong>SURGE</strong>', '自研产品: <strong>SURGE</strong>'),
        ('IIoT platform (Energy Mapping, Vessel Tracking, Water Analytic)', 'IIoT 平台(能源监测、船舶追踪、水质分析)'),
        ('<strong>Modbus Gateway IIoT</strong>', '<strong>Modbus 网关 IIoT</strong>'),
    ],

    # ==================== AUTOMATION (5451) ====================
    5451: [
        ('In the Industry 4.0 era, automation and smart monitoring are no longer luxuries - they are essentials for survival and growth. SURIOTA delivers IoT, SCADA, and control system solutions designed for Indonesian industry.',
         '在工业 4.0 时代,自动化与智能监控不再是奢侈品 - 而是生存与发展的必需。SURIOTA 为印尼工业提供 IoT、SCADA 与控制系统解决方案。'),
        ('platform - an integrated IIoT ecosystem - we deliver energy monitoring, water analytics, vessel tracking, and automated control accessible real-time from anywhere.',
         '平台 - 集成的 IIoT 生态系统 - 我们提供能源监控、水质分析、船舶追踪与自动化控制,可随时随地实时访问。'),
        ('. Picking the right controller for your plant, not for our supply chain.',
         '。为您的工厂选择合适的控制器,而非我们的供应链。'),
        ('With our in-house', '凭借我们自研的'),
        ('SURGE</strong> platform', 'SURGE</strong> 平台'),
        ('We integrate Siemens, Schneider, Mitsubishi, Omron, Allen-Bradley', '我们集成 Siemens、Schneider、Mitsubishi、Omron、Allen-Bradley'),
    ],

    # ==================== ELECTRICAL (5452) ====================
    5452: [
        ('Reliable and safe electrical systems are the foundation of every efficient business operation. Untreated electrical issues not only disrupt productivity but also threaten the safety of your assets and personnel.',
         '可靠安全的电气系统是每个高效业务运营的基础。未处理的电气问题不仅会扰乱生产力,还会威胁您资产和人员的安全。'),
        ('Free initial consultation. Share your scope, our engineering team responds within 24 hours with an SNI\\/IEC\\/PUIL-compliant feasibility check.',
         '免费初步咨询。分享您的范围,我们的工程团队将在 24 小时内提供符合 SNI/IEC/PUIL 标准的可行性检查。'),
    ],

    # ==================== RE (5453) ====================
    5453: [
        ('Renewable energy is the future - and the future starts now. SURIOTA delivers integrated renewable energy solutions for industries, public facilities, and communities across Indonesia.',
         '可再生能源是未来 - 而未来从此刻开始。SURIOTA 为印尼工业、公共设施和社区提供集成的可再生能源解决方案。'),
        ('(wind) systems standalone or hybrid. Our PLTS-PLTB hybrid systems are ideal for off-grid applications like IoT-based street lighting (PJU).',
         '(风能)系统独立或混合部署。我们的 PLTS-PLTB 混合系统非常适合离网应用,如基于物联网的路灯(PJU)。'),
        ('SURIOTA has experience designing PLTS (solar) and PLTB',
         'SURIOTA 拥有 PLTS(太阳能)与 PLTB 设计经验'),
    ],

    # ==================== PORTFOLIO (5454) ====================
    5454: [
        ('Discuss your IoT, automation, electrical, and water treatment needs with the SURIOTA engineering team. Free consultation, response within 1 business day.',
         '与 SURIOTA 工程团队讨论您的 IoT、自动化、电气和水处理需求。免费咨询,1 个工作日内回复。'),
    ],

    # ==================== WW LOGGER (5455) ====================
    5455: [
        ('Introducing the latest Wastewater Logger from Suriota, a powerful device that supports Modbus RS232, SDI-12, Wi-Fi, and Bluetooth protocols for seamless integration. This logger enables real-time data',
         '介绍 Suriota 最新的 Wastewater Logger,一款支持 Modbus RS232、SDI-12、Wi-Fi 和蓝牙协议的强大设备,实现无缝集成。该记录器支持实时数据'),
        ("Suriota's Wastewater Logger V.3 can take your water management to the next level. Increase operational efficiency and ensure environmental compliance with our innovative solution.",
         'Suriota 的 Wastewater Logger V.3 可将您的水资源管理提升到新水平。通过我们的创新解决方案提高运营效率并确保环境合规。'),
        ('Yes. Pre-configured for KLHK SPARING reporting per Permen LHK No. 80\\/2019. Compliance-ready data submission with proper sampling intervals, parameter mapping, and government server integration out of',
         '是。预配置为根据 Permen LHK No. 80/2019 进行 KLHK SPARING 报告。合规就绪的数据提交,具有正确的采样间隔、参数映射和政府服务器集成,'),
    ],

    # ==================== MGATE (5456) ====================
    5456: [
        ('The gateway operates reliably from -40\\u00b0C to 75\\u00b0C, with 2kV isolation protection on RS-485 ports. It is designed for harsh industrial environments including outdoor cabinets, manufacturing fl',
         '网关在 -40°C 至 75°C 范围内可靠运行,RS-485 端口具有 2kV 隔离保护。专为恶劣工业环境设计,包括户外机柜、制造厂'),
        ('Configuration is done via the Suriota Config mobile app (Android\\/iOS) over Bluetooth Low Energy (BLE 5.0, up to 50m range). No PC, no cables, no Telnet. Set up register maps, MQTT credentials, and TL',
         '通过 Suriota Config 移动应用(Android/iOS)经低功耗蓝牙(BLE 5.0,最远 50 米)进行配置。无需 PC、电缆或 Telnet。设置寄存器映射、MQTT 凭据和 TL'),
        ('Request a quote, RFQ, or live technical demo. Our engineering team responds within 24 hours with sample register-map configurations for your existing equipment.',
         '请求报价、RFQ 或现场技术演示。我们的工程团队将在 24 小时内为您现有设备提供示例寄存器映射配置。'),
        ('Yes. The MicroSD slot enables local data logging (CSV\\/JSON) during network outages. Data is automatically synced back to your IoT platform once connectivity is restored, ensuring zero data loss.',
         '是。MicroSD 插槽支持在网络中断期间进行本地数据记录(CSV/JSON)。一旦连接恢复,数据将自动同步回您的 IoT 平台,确保零数据丢失。'),
    ],

    # ==================== WT (5457) ====================
    5457: [
        ('Clean water is a fundamental need for every industrial operation, public facility, and community. Well-designed water treatment systems ensure consistent high-quality water supply while complying with',
         '清洁的水是每个工业运营、公共设施和社区的基本需求。设计良好的水处理系统可确保持续高质量的供水,同时符合'),
        ('platform, we help you respond to water quality changes in real-time.',
         '平台,我们帮助您实时响应水质变化。'),
    ],

    # ==================== SURGE-E (5458) ====================
    5458: [
        ('by Suriota is a powerful, integrated solution designed to give you complete visibility and control over your energy usage. Our web-based SaaS platform empowers you to monitor, control, and optimize yo',
         '由 Suriota 推出,是一款强大、集成的解决方案,旨在让您全面掌握并控制能源使用。我们的基于网络的 SaaS 平台让您能够监控、控制和优化您的'),
        ('The platform scales from tens to thousands of devices simultaneously. We support multi-location portfolios with centralized visibility, so retail chains, building portfolios, and industrial campuses a',
         '该平台可同时扩展到数十至数千台设备。我们支持多地点组合管理,提供集中可视化,让零售连锁、楼宇组合和工业园区'),
        ('SURGE Energy Mapping is a fully cloud-based SaaS platform. No installation required. Access your dashboard from any modern browser. Data is hosted on secure servers with role-based multi-level user ac',
         'SURGE Energy Mapping 是完全基于云的 SaaS 平台。无需安装。可从任何现代浏览器访问您的仪表盘。数据托管在安全服务器上,具有基于角色的多级用户访'),
        ('Yes. SURGE Energy Mapping provides REST APIs for integration with ERP systems, SCADA, BMS, and custom dashboards. Webhooks deliver real-time alerts to your existing workflow tools (email, WhatsApp, Sl',
         '是。SURGE Energy Mapping 提供 REST API,可与 ERP 系统、SCADA、BMS 和自定义仪表盘集成。Webhook 可向您现有工作流程工具(电子邮件、WhatsApp、Sl'),
        ('Request a free demo of SURGE Energy Mapping. We&#39;ll walk you through a real dashboard with your property type in under 24 hours.',
         '申请 SURGE Energy Mapping 的免费演示。我们将在 24 小时内为您完整演示一个您的物业类型的真实仪表盘。'),
    ],

    # ==================== SURGE-V (5459) ====================
    5459: [
        ('Yes. Engine hours, fuel consumption, RPM, and alarms are integrated via NMEA-2000 or Modbus connections to the vessel ECU. This helps reduce idle waste, detect fuel theft, and schedule predictive main',
         '是。引擎运行时间、燃油消耗、RPM 和警报通过 NMEA-2000 或 Modbus 连接集成到船舶 ECU。这有助于减少空转浪费、检测燃油盗窃和安排预测性维'),
        ('Request a live demo of SURGE Vessel Tracking. Our team will simulate your fleet operations with sample vessels and geofences within 24 hours.',
         '申请 SURGE Vessel Tracking 的现场演示。我们的团队将在 24 小时内使用示例船只和地理围栏模拟您的船队运营。'),
        ('Managing a fleet of vessels comes with unique and complex challenges. Without an integrated system, you might be dealing with:',
         '管理船队伴随着独特而复杂的挑战。没有集成系统,您可能面临:'),
        ('Yes. Full voyage replay, daily\\/weekly reports, and compliance documentation are available. Data can be exported as CSV or PDF for fleet audit, port authority compliance, and operational review.',
         '是。提供完整的航程回放、日/周报告和合规文档。数据可导出为 CSV 或 PDF,用于船队审计、港口当局合规和运营审查。'),
    ],

    # ==================== SURGE-W (5460) ====================
    5460: [
        ('is an advanced solution from Suriota, specifically designed to address the challenges of water quality management. This platform empowers Wastewater Treatment Plants (WWTPs), Sewage Treatment Plants (',
         '是 Suriota 推出的先进解决方案,专为解决水质管理挑战而设计。该平台赋能废水处理厂(WWTP)、污水处理厂('),
        ('Managing water quality, whether for consumption or wastewater discharge, requires rigorous monitoring and regulatory adherence. Without an integrated system, you may be facing:',
         '无论是饮用水还是废水排放,水质管理都需要严格的监控和合规遵守。没有集成系统,您可能面临:'),
        ('Yes. The platform integrates directly with KLHK SPARING servers per Permen LHK No. 80\\/2019, automating regulatory data submission. We handle the parameter mapping, sampling intervals, and report form',
         '是。该平台根据 Permen LHK No. 80/2019 直接与 KLHK SPARING 服务器集成,自动化合规数据提交。我们处理参数映射、采样间隔和报告格'),
    ],

    # ==================== ISO-M485 (5461) ====================
    5461: [
        ('When your operations depend on fast, stable, and secure data communication, you can&rsquo;t afford downtime or interference. The ISO-M485 Series is engineered for industrial-grade RS-485 connections w',
         '当您的运营依赖快速、稳定和安全的数据通信时,您无法承受停机或干扰。ISO-M485 系列专为工业级 RS-485 连接而设计'),
        ('With the ISO-M485 Series, you get speed, stability, and protection all in one compact, reliable device.',
         '使用 ISO-M485 系列,您可在一台紧凑可靠的设备中获得速度、稳定性和保护。'),
        ('2.5kV optocoupler isolation between RS-485 ports protects upstream PLC\\/SCADA equipment from ground loops, common-mode noise, and field-side faults. Galvanic isolation prevents damaging currents from ',
         'RS-485 端口之间的 2.5kV 光耦隔离可保护上游 PLC/SCADA 设备免受地环路、共模噪声和现场故障影响。电气隔离可防止损坏电流从'),
        ('-40\\u00b0C to +85\\u00b0C continuous operation. Designed for harsh field cabinets, outdoor enclosures, and unconditioned spaces typical in industrial and utility deployments.',
         '-40°C 至 +85°C 连续运行。专为工业和公用事业部署中典型的恶劣现场机柜、户外外壳和无空调空间设计。'),
        ('Request a quote or technical sample. Our team responds within 24 hours with wiring diagram and isolation topology recommendations.',
         '申请报价或技术样品。我们的团队将在 24 小时内提供接线图和隔离拓扑建议。'),
    ],

    # ==================== THM-30MD (5462) ====================
    5462: [
        ('When your operations demand accuracy, stability, and long-term durability, the THM-30MD delivers. Powered by the high-performance SHT30 Sensirion sensor, this device ensures precise environmental moni',
         '当您的运营需要准确性、稳定性和长期耐用性时,THM-30MD 即能交付。该设备采用高性能 SHT30 Sensirion 传感器,确保精确的环境监'),
        ('\\u00b10.3\\u00b0C for temperature and \\u00b12%RH for humidity across the full operating range. The Sensirion-grade element delivers calibration stability over years of continuous operation with minimal',
         '温度 ±0.3°C,湿度 ±2%RH,覆盖整个工作范围。Sensirion 级元件可在多年连续运行中保持校准稳定性,最低'),
        ('Request a quote with sample Modbus register map. We respond within 24 hours with mounting and calibration guidance for your application.',
         '申请报价及示例 Modbus 寄存器映射。我们将在 24 小时内为您的应用提供安装和校准指导。'),
        ('The THM-30MD gives you the insight you need to maintain optimal conditions, maximize efficiency, and protect what matters most.',
         'THM-30MD 为您提供所需的洞察,以维持最佳条件、最大化效率并保护最重要的事物。'),
        ('Modbus RTU over RS-485 with configurable slave ID and baud rate (4800-115200). Plug-and-play with any PLC, SCADA, BMS, or IoT gateway. Standard 9600-8-N-1 default settings.',
         '基于 RS-485 的 Modbus RTU,可配置从机 ID 和波特率(4800-115200)。可与任何 PLC、SCADA、BMS 或 IoT 网关即插即用。标准 9600-8-N-1 默认设置。'),
    ],

    # ==================== PM1611 (5463) ====================
    5463: [
        ('Control energy usage, eliminate billing disputes, and improve operational efficiency with the PM1611-WD Prepaid Energy Meter IoT. Designed for rental spaces, kiosks, offices, and machinery, this smart',
         '通过 PM1611-WD 预付费电能计量物联网设备控制能耗、消除计费争议并提高运营效率。专为出租空间、商铺、办公室和机械设计,这款智能'),
        ('Yes. Built-in relay enables remote connect\\/disconnect via WiFi or 4G cellular. No site visit needed for activation, tenant changeovers, or non-payment disconnections. Service control from your dashbo',
         '是。内置继电器支持通过 WiFi 或 4G 蜂窝远程连接/断开。激活、租户更换或欠费断电无需现场访问。从您的仪表盘控制服务'),
        ('Tenants top-up credit via app, e-wallet, or your billing portal. The meter consumes credit based on real-time energy usage and auto-disconnects at zero balance. Low-balance alerts notify before cut-of',
         '租户通过应用、电子钱包或您的计费门户充值。计量器根据实时能源使用量消耗信用额,余额为零时自动断电。低余额警报会在断电前通'),
        ('Request a quote for bulk deployment. Our team responds within 24 hours with site survey checklist and installation timeline.',
         '申请批量部署报价。我们的团队将在 24 小时内提供现场调查清单和安装时间表。'),
    ],

    # ==================== SPD-T485 (5464) ====================
    5464: [
        ('When it comes to industrial communication networks, downtime from surge damage is not an option. The SPD-T485-105 RS-485 Surge Protector is the first in Indonesia certified to EN 61643-21, delivering ',
         '对于工业通信网络,因浪涌损坏导致的停机绝不是选择。SPD-T485-105 RS-485 浪涌保护器是印尼首款获得 EN 61643-21 认证的产品,提供 '),
        ('Engineered for RS-485 systems operating up to 1 Mbps, it safeguards your data flow against lightning strikes, electrical surges, and electromagnetic interference, ensuring uninterrupted connectivity i',
         '专为运行速度高达 1 Mbps 的 RS-485 系统设计,保护您的数据流免受雷击、电涌和电磁干扰,确保不间断的连接'),
        ('Request a quote with site survey. Our engineers recommend SPD topology and grounding scheme for your specific cable runs within 24 hours.',
         '申请报价及现场调查。我们的工程师将在 24 小时内为您的特定线缆走线推荐 SPD 拓扑和接地方案。'),
        ('With the SPD-T485-105, you get certified, proven surge protection keeping your RS-485 communication stable, safe, and running at peak speed.',
         '使用 SPD-T485-105,您将获得经认证、经验证的浪涌保护,让您的 RS-485 通信保持稳定、安全并以峰值速度运行。'),
    ],

    # ==================== CONTACT (5465) ====================
    5465: [
        ('Whether you are scoping an IoT deployment, evaluating our SURGE platform, or looking for SCADA \\/ PLC integration \\u2014 we will match you with the right engineer within 24 hours.',
         '无论您是在规划 IoT 部署、评估我们的 SURGE 平台,还是寻求 SCADA / PLC 集成 — 我们都将在 24 小时内为您匹配合适的工程师。'),
        ('Absolutely. We offer a 30-minute discovery call with one of our engineers \\u2014 free, no obligation. Reach us via WhatsApp or email admin@suriota.com to schedule.',
         '当然。我们提供 30 分钟的需求电话,与我们的工程师交流 — 免费,无义务。通过 WhatsApp 或邮箱 admin@suriota.com 预约。'),
        ('Yes \\u2014 SURIOTA has completed 64+ projects across Indonesia in manufacturing, energy, maritime, and utilities. Our team travels for site surveys, commissioning, and on-site training.',
         '是 — SURIOTA 已在印尼完成 64+ 个项目,涵盖制造、能源、海事和公用事业。我们的团队会出差进行现场调查、调试和现场培训。'),
        ('我们回复 within 24 hours on business days. For urgent matters or live discussions, WhatsApp is the fastest channel.',
         '工作日 24 小时内回复。对于紧急事务或现场讨论,WhatsApp 是最快的渠道。'),
        ('For Modbus Gateway, ISO-M485, THM-30MD, PM1611-WD, and RS-485 SPD \\u2014 visit our official Tokopedia store or contact us for bulk pricing and project quotations.',
         '对于 Modbus Gateway、ISO-M485、THM-30MD、PM1611-WD 和 RS-485 SPD — 请访问我们的 Tokopedia 官方店或联系我们获取批量定价和项目报价。'),
    ],
}

print(f'Refining {len(REFINEMENTS)} pages...')
total_changes = 0
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
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
            print(f'  {pid}: +{page_changes}')
            total_changes += page_changes
        except Exception as e:
            print(f'  {pid} push fail: {e}')

print(f'\nTotal refinement changes: {total_changes}')

# Clear cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')

# Health check
import time as t
t.sleep(2)
for u in ['https://suriota.com/', 'https://suriota.com/id/beranda/', 'https://suriota.com/shouye/']:
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
    print(f'  {u}: {r.status}')
