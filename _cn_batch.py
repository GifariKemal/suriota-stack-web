"""Batch-create all remaining ZH pages."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass
from _cn_rollout import create_zh_page, health_check, MASTER_TRANSLATIONS

# (en_pid, zh_slug, zh_title, [extra_translations])
PAGES_TO_CREATE = [
    # Skip 12 (Home — already created as 5448)
    (29, 'guanyu-women', '关于 SURIOTA', [
        ('About SURIOTA', '关于 SURIOTA'),
        ('Next Gen. Industrial Partner | Industrial IoT &amp; System Integration in Batam, Indonesia',
         '新一代工业合作伙伴 | 印尼巴淡岛工业物联网与系统集成'),
        ('Next Gen. Industrial Partner | Industrial IoT & System Integration in Batam, Indonesia',
         '新一代工业合作伙伴 | 印尼巴淡岛工业物联网与系统集成'),
        ('Transforming industries through smart, connected solutions.', '通过智能互联解决方案变革工业。'),
        ("Transforming Indonesia's industries through smart, connected end-to-end IoT, AI, and SaaS solutions.",
         '通过智能互联的端到端物联网、人工智能和 SaaS 解决方案,变革印尼工业。'),
        ('Transforming Indonesia&#8217;s industries through smart, connected end-to-end IoT, AI, and SaaS solutions.',
         '通过智能互联的端到端物联网、人工智能和 SaaS 解决方案,变革印尼工业。'),
        ('SURIOTA | Industrial IoT &amp; System Integration', 'SURIOTA | 工业物联网与系统集成'),
        ('SURIOTA | Industrial IoT & System Integration', 'SURIOTA | 工业物联网与系统集成'),
        # MISI items
        ('DELIVER', '交付'),
        ('ENABLE', '赋能'),
        ('BUILD', '构建'),
        ('DEVELOP', '发展'),
        ('UPHOLD', '坚守'),
        # VISI/MISI
        ('VISI', '愿景'),
        ('MISI', '使命'),
    ]),
    (35, 'zidonghua', '自动化与物联网服务', [
        ('Automation Services', '自动化与物联网服务'),
        ('Automation &amp; IoT Services', '自动化与物联网服务'),
        ('Automation & IoT Services', '自动化与物联网服务'),
        ('PLC, SCADA &amp; IIoT integration with Modbus gateway for Industry 4.0', 'PLC、SCADA 与 IIoT 集成,基于 Modbus 网关,服务工业 4.0'),
        ('PLC, SCADA & IIoT integration with Modbus gateway for Industry 4.0', 'PLC、SCADA 与 IIoT 集成,基于 Modbus 网关,服务工业 4.0'),
        ('Vendor-agnostic automation across manufacturing, oil &amp; gas, shipyard, energy &amp; utilities',
         '厂商中立的自动化方案,覆盖制造业、石油天然气、船厂、能源与公用事业'),
        ('Vendor-agnostic automation across manufacturing, oil & gas, shipyard, energy & utilities',
         '厂商中立的自动化方案,覆盖制造业、石油天然气、船厂、能源与公用事业'),
    ]),
    (37, 'dianqi-gongcheng', '电气工程服务', [
        ('Electrical Services', '电气工程服务'),
        ('Electrical Engineering Services', '电气工程服务'),
        ('Industrial electrical installation, panel building, and commissioning compliant with SNI, IEC, PUIL 2011',
         '工业电气安装、配电柜组装与调试,符合 SNI、IEC、PUIL 2011 标准'),
    ]),
    (39, 'kezaisheng-nengyuan', '可再生能源服务', [
        ('Renewable Energy Services', '可再生能源服务'),
        ('Solar PV PLTS, hybrid PLTS-PLTB &amp; smart street light (PJU) with IoT energy monitoring',
         '太阳能光伏 PLTS、PLTS-PLTB 混合系统与智能路灯(PJU),集成物联网能源监控'),
        ('Solar PV PLTS, hybrid PLTS-PLTB & smart street light (PJU) with IoT energy monitoring',
         '太阳能光伏 PLTS、PLTS-PLTB 混合系统与智能路灯(PJU),集成物联网能源监控'),
    ]),
    (839, 'anli', '项目案例', [
        ('Portfolio', '项目案例'),
        ('Project Archive', '项目档案'),
        ('PROJECT ARCHIVE \\u2014 2023 TO 2025', '项目档案 \\u2014 2023 至 2025'),
    ]),
    (929, 'wastewater-logger', 'Wastewater Logger V.3', [
        ('Waste Water Logger', 'Wastewater Logger V.3'),
        ('Waste Water Logger V.3', 'Wastewater Logger V.3'),
    ]),
    (934, 'modbus-gateway', 'Modbus 网关 IIoT', [
        ('Modbus Gateway IIoT', 'Modbus 网关 IIoT'),
        ('SURIOTA MODULE \\u2013 MODBUS GATEWAY IIOT', 'SURIOTA 模块 \\u2013 Modbus 网关 IIoT'),
    ]),
    (945, 'shuichuli', '水处理服务', [
        ('Water Treatment Services', '水处理服务'),
        ('WTP, WWTP &amp; KLHK SPARING-compliant monitoring with IoT-integrated sensors',
         'WTP、WWTP 与 KLHK SPARING 合规监测,集成物联网传感器'),
        ('WTP, WWTP & KLHK SPARING-compliant monitoring with IoT-integrated sensors',
         'WTP、WWTP 与 KLHK SPARING 合规监测,集成物联网传感器'),
    ]),
    (1542, 'surge-energy-mapping', 'SURGE-Energy Mapping', [
        ('SURGE-Energy Mapping', 'SURGE-Energy Mapping'),
        ('99.9% Uptime SLA', '99.9% 在线率 SLA'),
        ('Multi-location energy monitoring across industries', '跨行业多地点能源监控'),
        ('Your all-in-one SaaS platform for real-time energy monitoring, smart device control, and significant operational cost reduction.',
         '您的一体化 SaaS 平台,提供实时能源监控、智能设备控制和大幅运营成本降低。'),
    ]),
    (1546, 'surge-vessel-tracking', 'SURGE-Vessel Tracking', [
        ('SURGE-Vessel Tracking', 'SURGE-Vessel Tracking'),
    ]),
    (1547, 'surge-water-analytic', 'SURGE-Water Analytic', [
        ('SURGE-Water Analytic', 'SURGE-Water Analytic'),
    ]),
    (1740, 'iso-m485', 'ISO-M485 系列', [
        ('ISO-M485 SERIES', 'ISO-M485 系列'),
        ('Where ISO-M485 is deployed', 'ISO-M485 部署应用'),
        ('Reliable RS-485 Communication, Reinforced with Isolation &amp; Surge Protection',
         '可靠的 RS-485 通信,加固隔离与浪涌保护'),
        ('Reliable RS-485 Communication, Reinforced with Isolation & Surge Protection',
         '可靠的 RS-485 通信,加固隔离与浪涌保护'),
    ]),
    (1741, 'thm-30md', 'THM-30MD', [
        ('THM-30MD', 'THM-30MD'),
    ]),
    (1742, 'pm1611-wd', 'PM1611-WD', [
        ('PM1611-WD', 'PM1611-WD'),
    ]),
    (1765, 'rs-485-spd', 'RS-485 Surge Protector SPD-T485-105', [
        ('RS-485 Surge Protector SPD-T485-105', 'RS-485 浪涌保护器 SPD-T485-105'),
    ]),
    (4983, 'lianxi', '联系我们', [
        ('Contact', '联系我们'),
        ('Get in Touch with SURIOTA', '联系 SURIOTA'),
        ('Talk to our engineers about Industrial IoT, system integration, or a custom project. We respond within 24 hours on business days.',
         '与我们的工程师讨论工业物联网、系统集成或定制项目。工作日 24 小时内回复。'),
        ('PHONE', '电话'),
        ('Mon\\u2013Fri \\u00b7 09:00\\u201318:00 WIB', '周一至周五 \\u00b7 09:00\\u201318:00 WIB'),
        ('Fastest response \\u00b7 Direct chat', '最快响应 \\u00b7 直接聊天'),
        ('Tell us about your project', '告诉我们您的项目'),
        ('From message to engagement \\u2014 in 4 steps', '从消息到合作 \\u2014 仅需 4 步'),
        ('You reach out', '您联系我们'),
        ('We reply', '我们回复'),
        ('Discovery call', '需求电话'),
        ('Engagement', '正式合作'),
    ]),
    (4985, 'yinsi-zhengce', '隐私政策', [
        ('Privacy Policy', '隐私政策'),
        ('How PT Surya Inovasi Prioritas (SURIOTA) collects, uses, and protects your personal data.',
         'PT Surya Inovasi Prioritas (SURIOTA) 如何收集、使用和保护您的个人数据。'),
        ('Effective', '生效'),
        ('Last updated', '最后更新'),
        ('Version', '版本'),
        ('IN THIS PAGE', '本页目录'),
    ]),
    (4987, 'fuwu-tiaokuan', '服务条款', [
        ('Terms of Service', '服务条款'),
        ('Agreement governing the use of SURIOTA website, products (SURGE platform, SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 Surge Protector), and engineering services. Please read carefully.',
         '关于使用 SURIOTA 网站、产品(SURGE 平台、SRT-MGATE-1210、ISO-M485、THM-30MD、PM1611-WD、RS-485 浪涌保护器)及工程服务的协议。请仔细阅读。'),
    ]),
    (5029, 'iot', '物联网与系统集成', [
        ('Internet of Things', '物联网'),
        ('IoT &amp; System Integration', '物联网与系统集成'),
        ('IoT & System Integration', '物联网与系统集成'),
    ]),
    (5031, 'xitong-jicheng', '系统集成', [
        ('System Integration', '系统集成'),
    ]),
    (5033, 'shuzihua-zixun', '数字化咨询', [
        ('Digital Consulting', '数字化咨询'),
    ]),
    (5035, 'rengong-zhineng', '人工智能与数据分析', [
        ('Artificial Intelligence', '人工智能'),
        ('AI &amp; Data Analytics', '人工智能与数据分析'),
        ('AI & Data Analytics', '人工智能与数据分析'),
    ]),
    (5037, 'shujufenxi', '数据分析', [
        ('Data Analytics', '数据分析'),
    ]),
    (5039, 'saas', '软件即服务 SaaS', [
        ('Software as a Service', '软件即服务 SaaS'),
        ('SaaS Platform', 'SaaS 平台'),
    ]),
]

created = []
failed = []
for en_pid, slug, title, extra in PAGES_TO_CREATE:
    print(f'\n--- [{en_pid}] {title} ({slug}) ---')
    zh_id = create_zh_page(en_pid, slug, title, extra)
    if zh_id:
        created.append((en_pid, zh_id, slug, title))
    else:
        failed.append((en_pid, slug))

print('\n========== SUMMARY ==========')
print(f'Created: {len(created)} / {len(PAGES_TO_CREATE)}')
print(f'Failed: {len(failed)}')
for en, zh, slug, title in created:
    print(f'  EN:{en:5d} → ZH:{zh} /{slug}/ {title}')
if failed:
    print('Failed pages:')
    for en, slug in failed:
        print(f'  EN:{en} {slug}')

# Save mapping for manual linking
with open('_zh_manual_link_checklist.txt', 'w', encoding='utf-8') as f:
    f.write('=== MANUAL POLYLANG LINKING REQUIRED ===\n')
    f.write('Go to WP admin → Pages, for each ZH page below:\n')
    f.write('1. Edit page\n2. Set Language to 中文 (zh)\n3. Set Translations: link to EN sibling + ID sibling\n\n')
    f.write('EN_ID\tZH_ID\tZH_SLUG\tZH_TITLE\n')
    f.write(f'12\t5448\tshouye\t首页\n')
    for en, zh, slug, title in created:
        f.write(f'{en}\t{zh}\t{slug}\t{title}\n')
print(f'\nManual link checklist saved: _zh_manual_link_checklist.txt')
