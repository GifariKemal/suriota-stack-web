"""ZH polish v3 — fix ghost redirect + remaining body content."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# === STEP 1: Remove /modbus-gateway/ from ghost redirect maps ===
# Snippet 5185 - SX / Ghost Slug Redirects
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5185?context=edit', headers=HDRS), timeout=30)
d = json.loads(r.read())
code = d.get('meta',{}).get('_elementor_code','')
print(f'Snippet 5185 ({len(code)} chars)')
new_code = code.replace(
    "'/modbus-gateway/':'/suriota-modbus-gateway/',",
    ""
).replace(
    "'/modbus-gateway/': '/suriota-modbus-gateway/',",
    ""
)
if new_code != code:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5185', data=json.dumps({'meta':{'_elementor_code':new_code}}).encode(), method='POST', headers=HDRS), timeout=30).read()
    print('  ✅ 5185: removed /modbus-gateway/ redirect')
else:
    print('  ⚠️ 5185: pattern not found')

# Snippet 5153 - Emergency Header-Footer
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5153?context=edit', headers=HDRS), timeout=30)
d = json.loads(r.read())
code = d.get('meta',{}).get('_elementor_code','')
print(f'Snippet 5153 ({len(code)} chars)')
patterns_to_remove = [
    "'/modbus-gateway/':'/suriota-modbus-gateway/',",
    "'/modbus-gateway':'/suriota-modbus-gateway/',",
    "'/modbus-gateway/': '/suriota-modbus-gateway/',",
]
new_code = code
removed = 0
for p in patterns_to_remove:
    if p in new_code:
        new_code = new_code.replace(p, '')
        removed += 1
        print(f"  removed: {p}")
if new_code != code:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5153', data=json.dumps({'meta':{'_elementor_code':new_code}}).encode(), method='POST', headers=HDRS), timeout=30).read()
    print(f'  ✅ 5153: removed {removed} redirect patterns')
else:
    print('  ⚠️ 5153: no pattern matched')

# === STEP 2: Fix remaining body chunks (with HTML tag boundaries) ===
PAGE_FIXES = {
    # WT (5457) - apostrophe is regular ', not \u2019
    5457: [
        ("Our long-term partnership with <strong>PDAM Tirta Kepri</strong> proves SURIOTA's competence in managing city-scale water infrastructure - from WTP, WWTP, to KLHK-integrated SPARING monitoring systems.",
         "我们与<strong>PDAM Tirta Kepri</strong>的长期合作证明了 SURIOTA 在管理城市规模水基础设施方面的能力 — 从 WTP、WWTP 到 KLHK 集成的 SPARING 监测系统。"),
        # Storage uses escaped slash format
        ("Our long-term partnership with <strong>PDAM Tirta Kepri<\\/strong> proves SURIOTA's competence in managing city-scale water infrastructure - from WTP, WWTP, to KLHK-integrated SPARING monitoring systems.",
         "我们与<strong>PDAM Tirta Kepri<\\/strong>的长期合作证明了 SURIOTA 在管理城市规模水基础设施方面的能力 — 从 WTP、WWTP 到 KLHK 集成的 SPARING 监测系统。"),
    ],
    # SURGE-W (5460) - has <strong> in middle
    5460: [
        ("<strong>Difficulty ensuring compliance</strong> with quality standards set by the government (like KLHK) and international bodies.",
         "<strong>难以确保合规</strong>满足政府(如 KLHK)及国际机构设定的质量标准。"),
        ("<strong>Difficulty ensuring compliance<\\/strong> with quality standards set by the government (like KLHK) and international bodies.",
         "<strong>难以确保合规<\\/strong>满足政府(如 KLHK)及国际机构设定的质量标准。"),
        ("The risk of environmental pollution",
         "环境污染风险"),
    ],
    # PM1611 (5463) - has <strong> in middle
    5463: [
        ("Review up to <strong>6 days of detailed energy usage</strong> per tenant. Identify abnormal consumption and resolve disputes with data.",
         "查看每个租户最多 <strong>6 天的详细能耗记录</strong>。识别异常消耗并通过数据解决争议。"),
        ("Review up to <strong>6 days of detailed energy usage<\\/strong> per tenant. Identify abnormal consumption and resolve disputes with data.",
         "查看每个租户最多 <strong>6 天的详细能耗记录<\\/strong>。识别异常消耗并通过数据解决争议。"),
    ],
    # DC (5470)
    5470: [
        ("We help you pick the right Industry 4.0 use cases, sequence them by <strong>ROI and risk</strong>, and budget realistically.",
         "我们帮助您选择正确的工业 4.0 用例,按 <strong>ROI 和风险</strong>排序,并制定切合实际的预算。"),
        ("We help you pick the right Industry 4.0 use cases, sequence them by <strong>ROI and risk<\\/strong>, and budget realistically.",
         "我们帮助您选择正确的工业 4.0 用例,按 <strong>ROI 和风险<\\/strong>排序,并制定切合实际的预算。"),
        ("Compliance-aware: KLHK, SNI, IEC, PUIL, OJK fintech",
         "合规导向:KLHK、SNI、IEC、PUIL、OJK 金融科技"),
    ],
    # MGATE (5456) - the intro paragraph
    5456: [
        ("The Suriota Modbus 网关 IIoT is an industrial-standard gateway solution designed to efficiently bridge Modbus-based automation systems with Internet of Things (IoT) ecosystems.",
         "Suriota Modbus 网关 IIoT 是工业标准的网关解决方案,旨在高效地将基于 Modbus 的自动化系统与物联网(IoT)生态系统桥接。"),
        ("This device converts data from industrial assets such as sensors, meters, and PLCs into a unified format",
         "该设备将工业资产(如传感器、计量器和 PLC)的数据转换为统一格式"),
        ("Suriota Modbus 网关 IIoT", "Suriota Modbus 网关 IIoT"),  # no-op placeholder
    ],
}

print('\n=== Fixing body chunks ===')
total = 0
for pid, pairs in PAGE_FIXES.items():
    r = urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS), timeout=30)
    d = json.loads(r.read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): continue
    new_ed = ed
    page_changes = 0
    for old, new in pairs:
        if old == new: continue
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            page_changes += c
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  {pid}: +{page_changes}')
        total += page_changes
    else:
        print(f'  {pid}: 0')

print(f'\nTotal body: {total}')

# Also need to fix MGATE eyebrows "KEY FEATURES" (which is stored as KEY FEATURES uppercase, not Key Features)
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5456?context=edit&_fields=meta', headers=HDRS), timeout=30)
d = json.loads(r.read())
ed = d.get('meta',{}).get('_elementor_data','')
if isinstance(ed, list): ed = json.dumps(ed)
new_ed = ed
extra_eyebrow_fixes = [
    ('>KEY FEATURES<', '>核心功能<'),
    ('>APPLICATIONS<', '>应用场景<'),
]
ch = 0
for old, new in extra_eyebrow_fixes:
    c = new_ed.count(old)
    if c > 0:
        new_ed = new_ed.replace(old, new)
        ch += c
if new_ed != ed:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5456', data=json.dumps({'meta':{'_elementor_data':new_ed}}).encode(), method='POST', headers=HDRS), timeout=30).read()
    print(f'MGATE all-caps eyebrows: +{ch}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')

time.sleep(2)
for u in ['https://suriota.com/', 'https://suriota.com/modbus-gateway/', 'https://suriota.com/shouye/']:
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
    print(f'  {u}: {r.status}')
