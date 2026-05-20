"""ZH polish v2 — mixed-case eyebrows (CSS uppercases them)."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

ALL_ZH = [5448, 5450, 5451, 5452, 5453, 5454, 5455, 5456, 5457, 5458, 5459, 5460,
          5461, 5462, 5463, 5464, 5465, 5466, 5467, 5468, 5469, 5470, 5471, 5472, 5473]

# Mixed-case eyebrow translations (source uses Title Case, CSS uppercases for display)
GLOBAL_PATTERNS = [
    ('>Capabilities<', '>核心能力<'),
    ('>Applications<', '>应用场景<'),
    ('>Key Features<', '>核心功能<'),
    ('>Why Choose SURIOTA<', '>为何选择 SURIOTA<'),
    ('>Why SURIOTA<', '>为何选择 SURIOTA<'),
    ('>Industries We Serve<', '>我们服务的行业<'),
    ('>Industries We Power<', '>我们供能的行业<'),
    ('>Industries We Automate<', '>我们自动化的行业<'),
    ('>What We Deliver<', '>我们交付什么<'),
    ('>How We Work<', '>我们的工作方式<'),
    ('>Built For<', '>专为...打造<'),
    ('>Our Services<', '>我们的服务<'),
    ('>Our 5 Core Services<', '>五大核心服务<'),
    ('>Why SURGE<', '>为何选择 SURGE<'),
    ('>Our Process<', '>我们的流程<'),
    ('>Our Principles<', '>我们的原则<'),
    ('>Our Approach<', '>我们的方法<'),
    ('>Key Capabilities<', '>核心能力<'),
    ('>Vision<', '>愿景<'),
    ('>Mission<', '>使命<'),
    ('>Contact<', '>联系方式<'),
    ('>Start a Conversation<', '>开始对话<'),
    ('>What Happens Next<', '>下一步流程<'),
    ('>Ready to Start?<', '>准备开始？<'),
    ('>Legal<', '>法律信息<'),
    ('>About Us<', '>关于我们<'),
    ('>Ready to Deploy<', '>即刻部署<'),
    ('>Get a Quote<', '>获取报价<'),
    ('>Related Products<', '>相关产品<'),
    ('>Related Insights<', '>相关洞察<'),
    ('>Specifications<', '>技术规格<'),
    ('>How It Works<', '>工作原理<'),
    # Possible all-caps variants
    ('>WHY CHOOSE SURIOTA<', '>为何选择 SURIOTA<'),
    ('>INDUSTRIES WE SERVE<', '>我们服务的行业<'),
    ('>INDUSTRIES WE POWER<', '>我们供能的行业<'),
    ('>APPLICATIONS<', '>应用场景<'),
    ('>KEY FEATURES<', '>核心功能<'),
    ('>CAPABILITIES<', '>核心能力<'),
    # Lowercase variants
    ('>Capabilities<', '>核心能力<'),
]

PAGE_FIXES = {
    5457: [
        ('Our long-term partnership with PDAM Tirta Kepri proves SURIOTA\\u2019s competence in managing city-scale water infrastructure \\u2013 from WTP, WWTP, to KLHK-integrated SPARING monitoring systems.',
         '我们与 PDAM Tirta Kepri 的长期合作证明了 SURIOTA 在管理城市规模水基础设施方面的能力 — 从 WTP、WWTP 到 KLHK 集成的 SPARING 监测系统。'),
    ],
    5470: [
        ('We help you pick the right Industry 4.0 use cases, sequence them by ROI and risk, and budget realistically.',
         '我们帮助您选择正确的工业 4.0 用例,按 ROI 和风险排序,并制定切合实际的预算。'),
        ('Then we can build them too', '然后我们也可以构建它们'),
    ],
    5460: [
        ('Difficulty ensuring compliance with quality standards set by the government (like KLHK) and international bodies.',
         '难以确保符合政府(如 KLHK)和国际机构设定的质量标准。'),
        ('A lack of accurate, structured historical data for analysis and strategic decision-making.',
         '缺乏用于分析和战略决策的准确、结构化的历史数据。'),
    ],
    5456: [
        ('The Suriota Modbus Gateway IIoT is an industrial-standard gateway solution designed to efficiently bridge Modbus-based automation systems with Internet of Things (IoT) platforms.',
         'Suriota Modbus Gateway IIoT 是工业标准的网关解决方案,旨在高效地将基于 Modbus 的自动化系统与物联网(IoT)平台桥接。'),
    ],
    5463: [
        ('Review up to 6 days of detailed energy usage per tenant. Identify abnormal consumption and resolve disputes with data.',
         '查看每个租户最多 6 天的详细能耗记录。识别异常消耗并通过数据解决争议。'),
        ('Local LCD shows balance and consumption. WhatsApp/SMS notifications on low balance, anomalies, and top-ups.',
         '本地 LCD 显示余额和能耗。WhatsApp/SMS 通知低余额、异常和充值。'),
        ('Configure and monitor remotely via web interface using Blynk or MQTT protocol. RTC with NTP sync ensures accurate billing time.',
         '通过 Web 界面使用 Blynk 或 MQTT 协议远程配置和监控。RTC 配 NTP 同步确保准确的计费时间。'),
    ],
}

print('=== Applying eyebrow + body fixes ===')
total = 0
for pid in ALL_ZH:
    r = urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS), timeout=30)
    d = json.loads(r.read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): continue
    new_ed = ed
    page_changes = 0
    for old, new in GLOBAL_PATTERNS:
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            page_changes += c
    if pid in PAGE_FIXES:
        for old, new in PAGE_FIXES[pid]:
            c = new_ed.count(old)
            if c > 0:
                new_ed = new_ed.replace(old, new)
                page_changes += c
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
            print(f'  {pid}: +{page_changes}')
            total += page_changes
        except Exception as e:
            print(f'  {pid} fail: {e}')

print(f'\nTotal: {total}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')
time.sleep(2)
for u in ['https://suriota.com/', 'https://suriota.com/shouye/']:
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
    print(f'  {u}: {r.status}')
