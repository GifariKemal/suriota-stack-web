"""ZH rollout master script — REST only, no PHP."""
import urllib.request, base64, json, time, sys, io
# Reconfigure stdout for UTF-8 (safe if called multiple times)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}
ZH_TERM_ID = 176  # from add_lang result

# ============== MASTER GLOSSARY (sitewide common terms) ==============
MASTER_TRANSLATIONS = [
    # Eyebrows (must be in >text< form to be safe — only inside HTML tags)
    ('>ABOUT US<', '>关于我们<'),
    ('>OUR SERVICES<', '>我们的服务<'),
    ('>OUR 5 CORE SERVICES<', '>五大核心服务<'),
    ('>FAQ<', '>常见问题<'),
    ('>KEY FEATURES<', '>核心功能<'),
    ('>WHY SURIOTA<', '>为何选择 SURIOTA<'),
    ('>WHY CHOOSE SURIOTA<', '>为何选择 SURIOTA<'),
    ('>WHAT WE DELIVER<', '>我们交付什么<'),
    ('>HOW WE WORK<', '>我们的工作方式<'),
    ('>APPLICATIONS<', '>应用场景<'),
    ('>BUILT FOR<', '>专为...打造<'),
    ('>INDUSTRIES WE SERVE<', '>我们服务的行业<'),
    ('>INDUSTRIES WE AUTOMATE<', '>我们自动化的行业<'),
    ('>INDUSTRIES WE POWER<', '>我们供能的行业<'),
    ('>WHY SURGE<', '>为何选择 SURGE<'),
    ('>CONTACT<', '>联系方式<'),
    ('>START A CONVERSATION<', '>开始对话<'),
    ('>WHAT HAPPENS NEXT<', '>下一步流程<'),
    ('>READY TO START?<', '>准备开始？<'),
    ('>LEGAL<', '>法律信息<'),
    ('>SAAS \\u00b7 ENERGY MONITORING<', '>SAAS \\u00b7 能源监控<'),
    ('>RS-485 ISOLATION MODULE<', '>RS-485 隔离模块<'),
    ('>INDUSTRIAL IOT GATEWAY<', '>工业物联网网关<'),

    # CTA texts (in Elementor button text or HTML)
    ('"text":"Free Consultation \\u2192"', '"text":"免费咨询 \\u2192"'),
    ('"text":"Free Consultation"', '"text":"免费咨询 \\u2192"'),
    ('"text":"Request Free Demo \\u2192"', '"text":"申请免费演示 \\u2192"'),
    ('"text":"Request Quote \\u2192"', '"text":"申请报价 \\u2192"'),
    ('>Free Consultation \\u2192<', '>免费咨询 \\u2192<'),
    ('>Free Consultation<', '>免费咨询<'),
    ('>Request Free Demo \\u2192<', '>申请免费演示 \\u2192<'),
    ('>Request a Quote<', '>申请报价<'),
    ('>Message on WhatsApp<', '>WhatsApp 联系<'),
    ('>Chat via WhatsApp<', '>WhatsApp 联系<'),
    ('>View All Portfolio<', '>查看全部案例<'),
    ('>Learn More \\u2192<', '>了解更多 \\u2192<'),
    ('>Learn more \\u2192<', '>了解更多 \\u2192<'),
    ('>SEND<', '>发送<'),
    ('>Send Message<', '>发送消息<'),

    # Section headings
    ('Next Gen. Industrial Partner', '新一代工业合作伙伴'),
    ('About SURIOTA', '关于 SURIOTA'),
    ('Get in Touch with SURIOTA', '联系 SURIOTA'),
    ('Get in Touch', '联系我们'),

    # Common phrases (long → short)
    ('SURIOTA</strong> is a technology company specializing in <strong>Industrial IoT &amp; System Integration</strong>',
     'SURIOTA</strong> 是专注于<strong>工业物联网与系统集成</strong>的科技公司'),
    ('SURIOTA</strong> is a technology company specializing in <strong>Industrial IoT & System Integration</strong>',
     'SURIOTA</strong> 是专注于<strong>工业物联网与系统集成</strong>的科技公司'),
    ('SURIOTA is a technology company specializing in Industrial IoT &amp; System Integration', 'SURIOTA 是专注于工业物联网与系统集成的科技公司'),
    ('SURIOTA is a technology company specializing in Industrial IoT & System Integration', 'SURIOTA 是专注于工业物联网与系统集成的科技公司'),
    # CAPABILITIES eyebrow
    ('>CAPABILITIES<', '>核心能力<'),
    ('>OUR PROCESS<', '>我们的流程<'),
    ('>CASE STUDY<', '>案例研究<'),
    ('>OUR APPROACH<', '>我们的方法<'),
    ('>OUR PRINCIPLES<', '>我们的原则<'),
    ('>OUR TEAM<', '>我们的团队<'),
    ('>OUR HISTORY<', '>我们的历史<'),
    ('>WHY IT MATTERS<', '>为何重要<'),
    ('>OUR EXPERTISE<', '>我们的专长<'),
    ('>KEY CAPABILITIES<', '>核心能力<'),
    ('>OUR EXPERIENCE<', '>我们的经验<'),
    ('>BUILT TO LAST<', '>持久耐用<'),
    ('>SPECIFICATIONS<', '>技术规格<'),
    ('>WHY SURIOTA HARDWARE<', '>为何选择 SURIOTA 硬件<'),
    ('>HOW IT WORKS<', '>工作原理<'),
    ('>READY TO DEPLOY<', '>即刻部署<'),
    ('>GET A QUOTE<', '>获取报价<'),
    ('>RELATED INSIGHTS<', '>相关洞察<'),
    ('>RELATED PRODUCTS<', '>相关产品<'),
    ('>IN THIS PAGE<', '>本页目录<'),
    ('>ON THIS PAGE<', '>本页目录<'),
    ('>VISION<', '>愿景<'),
    ('>MISSION<', '>使命<'),
    ('>VALUES<', '>价值观<'),
    ('headquartered in Batam, Riau Islands', '总部位于印度尼西亚廖内群岛巴淡岛'),
    ('Since January 2023, we have delivered', '自 2023 年 1 月以来,我们已交付'),
    ('industrial projects', '个工业项目'),
    ('from Modbus gateways to complete IoT platforms', '从 Modbus 网关到完整的物联网平台'),
    ('across manufacturing, energy, logistics, and maritime sectors', '服务于制造、能源、物流和海事行业'),
    ('With our commitment to the highest technical standards', '凭借对最高技术标准的承诺'),
    ('SURIOTA is a trusted partner in improving efficiency, productivity, and business sustainability', 'SURIOTA 是值得信赖的合作伙伴,助力提升效率、生产力和业务可持续性'),
    ('for clients across Indonesia', '服务于印尼全境客户'),

    # Service card titles (HTML)
    ('>IoT &amp; System Integration<', '>物联网与系统集成<'),
    ('>IoT & System Integration<', '>物联网与系统集成<'),
    ('>AI &amp; Data Analytics<', '>人工智能与数据分析<'),
    ('>AI & Data Analytics<', '>人工智能与数据分析<'),
    ('>Software as a Service<', '>软件即服务<'),
    ('>Automation &amp; Renewable Energy<', '>自动化与可再生能源<'),
    ('>Automation & Renewable Energy<', '>自动化与可再生能源<'),
    ('>Digital Consulting<', '>数字化咨询<'),

    # Common card body
    ('End-to-end Industrial IoT', '端到端工业物联网'),
    ('Modbus gateway, MQTT', 'Modbus 网关、MQTT'),
    ('edge computing, SCADA', '边缘计算、SCADA'),
    ('sensor-to-cloud pipelines', '传感器到云端数据管道'),
    ('with IEC 62443 security', '符合 IEC 62443 安全标准'),
    ('for manufacturing, oil &amp; gas, and maritime operations', '适用于制造业、石油天然气及海事运营'),
    ('for manufacturing, oil & gas, and maritime operations', '适用于制造业、石油天然气及海事运营'),
    ('Predictive maintenance, OEE dashboards', '预测性维护、OEE 仪表盘'),
    ('computer-vision QC, and real-time operational intelligence', '计算机视觉质检及实时运营洞察'),
    ('Turning raw machine data into actionable plant-floor decisions', '将原始机器数据转化为可执行的车间决策'),
    ('SURGE multi-tenant IoT platform', 'SURGE 多租户物联网平台'),
    ('Energy Mapping (kWh, power factor)', '能源监测(千瓦时、功率因数)'),
    ('Water Analytic (KLHK SPARING compliance)', '水质分析(KLHK SPARING 合规)'),
    ('Vessel Tracking (fleet + fuel monitoring)', '船舶追踪(船队+燃油监控)'),
    ('PLC integration, SCADA modernization', 'PLC 集成、SCADA 现代化升级'),
    ('Solar PV PLTS design, hybrid PLTS-PLTB systems', '太阳能光伏 PLTS 设计、PLTS-PLTB 混合系统'),
    ('and smart street light (PJU)', '及智能路灯(PJU)'),
    ('Turnkey industrial energy transition', '工业能源转型一站式方案'),
    ('Industry 4.0 roadmap', '工业 4.0 路线图'),
    ('OT/IT convergence assessment', 'OT/IT 融合评估'),
    ('IIoT readiness audit', 'IIoT 准备度审计'),
    ('SCADA modernization, and cloud migration strategy', 'SCADA 现代化与云迁移战略'),
    ('for Indonesian manufacturers', '专为印尼制造业打造'),

    # Common UI labels
    ('>Home<', '>首页<'),
    ('>SEND<', '>发送<'),
    ('>Year<', '>年<'),
    ('>Years<', '>年<'),
    ('>YEAR<', '>年<'),
    ('>YEARS<', '>年<'),
    ('>PROJECT<', '>项目<'),
    ('>PROJECTS<', '>项目<'),
    ('>CLIENT<', '>客户<'),
    ('>CLIENTS<', '>客户<'),
    ('>SERVICES<', '>服务<'),
    ('>NO<', '>序号<'),

    # Common technical terms in body
    ('Manufacturing', '制造业'),
    ('Food &amp; Beverage', '食品饮料'),
    ('Food & Beverage', '食品饮料'),
    ('Pharmaceutical', '制药'),
    ('Logistics &amp; Warehousing', '物流与仓储'),
    ('Logistics & Warehousing', '物流与仓储'),
    ('Power &amp; Energy', '电力能源'),
    ('Power & Energy', '电力能源'),
    ('Water Utilities', '水务公用事业'),
    ('Mining &amp; Quarry', '矿业'),
    ('Mining & Quarry', '矿业'),
    ('Maritime &amp; Port', '海事与港口'),
    ('Maritime & Port', '海事与港口'),
    ('Maritime &amp; Shipyard', '海事与船厂'),
    ('Maritime & Shipyard', '海事与船厂'),
    ('Commercial Buildings', '商业建筑'),
    ('Hospitality &amp; Tourism', '酒店与旅游'),
    ('Hospitality & Tourism', '酒店与旅游'),
    ('Apartments &amp; Kos', '公寓与宿舍'),
    ('Apartments & Kos', '公寓与宿舍'),
    ('Retail Chains', '连锁零售'),
    ('Healthcare Facilities', '医疗设施'),
    ('Industrial Plants', '工业厂区'),
    ('Government Offices', '政府办公'),
    ('Hospitality', '酒店业'),
    ('Data Centers', '数据中心'),
    ('Government &amp; Public', '政府与公共'),
    ('Government & Public', '政府与公共'),
    ('Residential Estates', '住宅小区'),
    ('Agriculture &amp; Aqua', '农业与水产'),
    ('Agriculture & Aqua', '农业与水产'),
]

def health_check(verbose=False):
    try:
        for u in ['https://suriota.com/wp-json/', 'https://suriota.com/', 'https://suriota.com/id/beranda/']:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
            if r.status >= 500:
                if verbose: print(f'❌ {u} status={r.status}')
                return False
        return True
    except Exception as e:
        if verbose: print(f'❌ {e}')
        return False

def fetch_page(pid):
    """Fetch page Elementor data + meta."""
    r = urllib.request.urlopen(
        urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta,title,template', headers=HDRS),
        timeout=30
    )
    return json.loads(r.read())

def apply_translations(content, translations):
    """Apply find-replace translations to content."""
    new = content
    cnt = 0
    for old, new_str in translations:
        c = new.count(old)
        if c > 0:
            new = new.replace(old, new_str)
            cnt += c
    return new, cnt

def create_zh_page(en_pid, zh_slug, zh_title, extra_translations=None):
    """Create ZH variant of EN page."""
    # Pre-check
    if not health_check():
        print('🛑 Health check failed before start')
        return None

    # Fetch EN
    d = fetch_page(en_pid)
    ed = d.get('meta', {}).get('_elementor_data', '')
    if isinstance(ed, list): ed = json.dumps(ed)
    ps = d.get('meta', {}).get('_elementor_page_settings', {})

    # Apply master + extra translations
    translations = MASTER_TRANSLATIONS + (extra_translations or [])
    new_ed, n = apply_translations(ed, translations)
    print(f'  Applied {n} master + extra translations')

    # Also translate custom_css if exists
    css = ps.get('custom_css', '') if isinstance(ps, dict) else ''
    # custom_css we don't translate (selectors are class names)

    # Create page
    payload = {
        'title': zh_title,
        'slug': zh_slug,
        'status': 'publish',
        'parent': 0,
        'template': d.get('template', ''),
        'meta': {
            '_elementor_data': new_ed,
            '_elementor_page_settings': ps if isinstance(ps, dict) else {},
            '_elementor_edit_mode': 'builder',
            '_elementor_template_type': 'wp-page',
            '_wp_page_template': d.get('template', 'default'),
        }
    }
    try:
        resp = urllib.request.urlopen(
            urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages', data=json.dumps(payload).encode(), method='POST', headers=HDRS),
            timeout=60
        ).read()
        zh = json.loads(resp)
        zh_id = zh['id']
        print(f'  ✅ Created ZH ID:{zh_id} link={zh["link"]}')
    except Exception as e:
        print(f'  ❌ Create failed: {e}')
        return None

    # Post-check
    time.sleep(2)
    if not health_check():
        print(f'  🛑 SITE DOWN after creating {zh_id}! Halt.')
        return None
    return zh_id

if __name__ == '__main__':
    print('Health check:', health_check(verbose=True))
    print(f'ZH term_id: {ZH_TERM_ID}')
