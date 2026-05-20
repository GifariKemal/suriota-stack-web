# SURIOTA Chinese (Simplified) Translation Brief — v2 HARDENED

**Target executor:** Kimi CLI (or any code-capable AI agent)
**Project:** Add Simplified Chinese (zh-CN) as 3rd language to suriota.com
**Status of EN + ID:** ✅ Complete, **DO NOT MODIFY UNDER ANY CIRCUMSTANCES**
**Brief version:** 2.0 (hardened after v1 caused site outage)
**Date:** 2026-05-20

---

## 🚨 ABSOLUTE PROHIBITIONS — VIOLATION CAUSES SITE OUTAGE 🚨

Brief v1 caused a WordPress fatal error because the executor (Kimi) tried to use Code Snippets plugin PHP. **DO NOT REPEAT.** Hard rules:

| ❌ NEVER DO | Why |
|---|---|
| **NEVER activate "Code Snippets" plugin** | It is currently deactivated for a reason. Activating + running any PHP causes WP fatal error → site 500. Recovery requires admin email link. |
| **NEVER write or execute PHP code** | All work must go through WordPress REST API only |
| **NEVER POST to `/wp-json/code-snippets/...`** | Same plugin, same outage risk |
| **NEVER modify existing EN/ID pages, posts, or snippets** | Only CREATE new ZH pages and (where explicitly allowed) update snippet 5447 |
| **NEVER modify pages: 12, 29, 35, 37, 39, 839, 929, 934, 945, 1127, 1542, 1546, 1547, 1740-1742, 1765** (all EN pages) | Production EN content |
| **NEVER modify pages: 5273-5295, 5378-5382** (all ID pages) | Production ID content |
| **NEVER modify posts (articles)** | 64 articles stay as-is |
| **NEVER modify existing elementor_snippet IDs: 4332, 4374, 4604, 5153, 5180-5188, 5190-5192, 5261, 5411, 5184** | Production design system |
| **NEVER touch the Default Kit (post 5)** | Sitewide design system |
| **NEVER bulk-edit > 5 things without health check** | Health check defined in Section 11 |

**The ONLY existing snippet you may modify: ID 5447** (Nav Header swap). Brief v1 already added ZH support — DO NOT change it.

---

## 0. EXECUTION SAFETY PROTOCOL (FOLLOW EVERY STEP)

### Health check (run after EVERY page creation, snippet update, or bulk change)
```python
import urllib.request, time
def health_check():
    try:
        r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/', headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
        if r.status != 200:
            raise Exception(f'REST returned {r.status}')
        # Test EN home
        r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/', headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
        if r.status != 200:
            raise Exception(f'EN home returned {r.status}')
        # Test ID home
        r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/beranda/', headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
        if r.status != 200:
            raise Exception(f'ID home returned {r.status}')
        return True
    except Exception as e:
        print(f'❌ HEALTH CHECK FAILED: {e}')
        return False

# Use after every change:
if not health_check():
    print('🛑 STOP. Site is down. Do NOT make any more changes.')
    print('Required actions:')
    print('1. Tell user to check WP admin email for recovery link')
    print('2. Wait for user confirmation site is back')
    print('3. Identify which change caused outage; revert it')
    import sys; sys.exit(1)
```

### Failure mode protocol
- Site returns 500: **STOP IMMEDIATELY.** Notify user. Wait for recovery confirmation.
- REST returns 401/403: Auth issue. Stop. Verify credentials.
- REST returns 404 on `/pll/v1/...`: Polylang language not added yet. See Section 3.
- Any unexpected error: STOP. Diagnose before continuing.

### Token budget management
Each page creation = ~1 GET + 1 POST + 1 health check = ~3 requests. Total for 25 ZH pages ≈ 75 requests + 25 health checks. Avoid retrying loops.

---

## 1. WHY SIMPLIFIED CHINESE

Research-backed decision (target: mainland China B2B industrial IoT buyers):
- Simplified script — 1.4B mainland speakers
- WordPress locale: `zh_CN`
- Polylang code: `zh`
- HTML lang: `zh-CN`
- Baidu (60% China search) favors Simplified

Out of scope: Traditional Chinese (zh-TW, zh-HK). Can be added later as separate Polylang locale.

---

## 2. AUTHENTICATION

### Endpoint base
```
https://suriota.com/wp-json/
```

### Auth header (WordPress Application Password)
```
User: admin
App password: hCYK JqF1 khdB WDzI LQdQ WEBr
```

```python
import base64
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
```

### Site status (as of 2026-05-20)
- ✅ Site UP, REST 200
- ✅ Polylang installed, EN + ID active
- ❌ ZH not added yet (manual step — see Section 3)
- ✅ Elementor snippet 5447 already has ZH map (do not modify)
- ⛔ Code Snippets plugin DEACTIVATED — leave it that way

---

## 3. MANDATORY MANUAL USER STEPS (DO BEFORE RUNNING SCRIPTS)

The following CANNOT be done via REST. Ask the user (Gifari) to complete these steps in WordPress admin first, then notify you when done.

### 3.1 Add ZH language to Polylang
**User action required:**
1. Login to https://suriota.com/wp-admin/
2. Navigate to **Languages → Languages**
3. Click **Add new language**
4. From dropdown: select `中文 (zh)` or manually enter:
   - Name: `中文`
   - Locale: `zh_CN`
   - Language code (slug): `zh`
   - Text direction: LTR
   - Flag: 🇨🇳 China
   - Order: `3`
5. Click **Add language**

### 3.2 Verify (run after user confirms step 3.1)
```python
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/pll/v1/languages', headers=HDRS), timeout=15)
langs = json.loads(r.read())
zh = next((l for l in langs if l['slug'] == 'zh'), None)
if not zh:
    print('🛑 ZH language not found. Ask user to complete Section 3.1 first.')
    sys.exit(1)
print(f'✅ ZH language active: term_id={zh["term_id"]}, locale={zh["locale"]}')
ZH_TERM_ID = zh['term_id']  # save this for later
```

### 3.3 (Optional but recommended) Hreflang setup
**User action:**
1. **Languages → Settings → Hreflang**: enable "Generate hreflang HTML tags"
2. Save

### 3.4 Set ZH URL pattern
**User action:**
1. **Languages → Settings → URL modifications**
2. Confirm "The language is set from the directory name in pretty permalinks" is selected (matches existing `/id/` pattern)
3. ZH pages will live at `/zh/{slug}/`

---

## 4. DESIGN SYSTEM (READ-ONLY — DO NOT CHANGE)

### 4.1 Typography (loaded by elementor_snippet 5411 — DO NOT MODIFY)
```css
font-family: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif;
font-family: 'Geist Mono', ui-monospace, monospace;
```

### 4.2 Color tokens (USE EXACT VALUES)
| Token | Value |
|---|---|
| `--sx-accent` | `#0E3942` |
| `--sx-amber` | `#C8851F` |
| `--sx-ink` | `#0F1A1F` |
| `--sx-mute` | `#5B6F75` |
| `--sx-line` | `#E8ECEE` |
| `--sx-surface` | `#FAFBFC` |
| `--sx-success` | `#3C7D47` |

### 4.3 Type sizes (preserve when copying EN page structure)
- h1 (hero): 42–80px clamp
- h2 (section): 24–32px
- h3 (subsection/card): 18px
- body / p: 15–16px
- `.sx-eyebrow`: 12px Geist Mono uppercase letter-spacing 0.08em
- `.sx-brand-name`: 16px Geist 600 mixed-case

### 4.4 Container widths
- `.sx-inner` (general): 1180px
- `.sx-whyus-inner` (trust cards): 1080px
- `.sx-industries-inner` (industry tags): 960px

---

## 5. TRANSLATION GLOSSARY (USE EXACTLY)

### 5.1 NEVER translate (keep as-is in ZH content)
- SURIOTA, PT Surya Inovasi Prioritas (on first mention in About page only, add `/苏里奥塔` in parentheses)
- SURGE, SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytic
- Product SKUs: SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 SPD, Wastewater Logger
- Protocols: Modbus, RTU, TCP, MQTT, OPC UA, RS-485, RS-232, PLC, SCADA, HMI, ERP, IIoT, IoT
- Standards/orgs: KLHK, SPARING, BAST, PUIL, IEC, SNI, GDPR, UU PDP, BANI
- Brand assets: WhatsApp, Tokopedia
- Numeric values: 64+, 24 hours, 99.9% — keep Arabic numerals

### 5.2 Core terminology (research-verified from Chinese B2B IoT sites)

| EN | ZH Simplified |
|---|---|
| Industrial IoT / IIoT | 工业物联网 |
| Internet of Things | 物联网 |
| System Integration | 系统集成 |
| Automation | 自动化 |
| Renewable Energy | 可再生能源 |
| Water Treatment | 水处理 |
| Electrical Engineering | 电气工程 |
| Data Analytics | 数据分析 |
| Digital Consulting | 数字化咨询 |
| Artificial Intelligence | 人工智能 |
| Software as a Service | 软件即服务 (use "SaaS" in titles) |
| Gateway | 网关 |
| Modbus Gateway | Modbus 网关 |
| Sensor | 传感器 |
| Dashboard | 仪表盘 |
| Real-time monitoring | 实时监控 |
| Edge computing | 边缘计算 |
| Predictive maintenance | 预测性维护 |
| Smart manufacturing | 智能制造 |
| Cloud platform | 云平台 |
| Industry 4.0 | 工业4.0 |
| Power monitoring | 电力监控 |
| Energy mapping | 能源监测 |
| Vessel tracking | 船舶追踪 |
| Water analytic | 水质分析 |
| Compliance | 合规 |
| Engineering | 工程 |
| Consulting | 咨询 |
| Service | 服务 |
| Product | 产品 |
| Project | 项目 |
| Client / Customer | 客户 |
| Engineer | 工程师 |
| Industry | 行业 |
| Manufacturing | 制造业 |
| Oil & Gas | 石油和天然气 |
| Maritime | 海事 |
| Utilities | 公共事业 |
| Mining | 矿业 |
| Power & Energy | 电力能源 |
| Pharmaceutical | 制药 |
| Food & Beverage | 食品饮料 |
| Logistics & Warehousing | 物流与仓储 |

### 5.3 Eyebrow translations (preserve uppercase style)

| EN eyebrow | ZH |
|---|---|
| FAQ | 常见问题 |
| KEY FEATURES | 核心功能 |
| WHY SURIOTA | 为何选择 SURIOTA |
| WHAT WE DELIVER | 我们交付什么 |
| HOW WE WORK | 我们的工作方式 |
| APPLICATIONS | 应用场景 |
| BUILT FOR | 专为...打造 |
| INDUSTRIES WE SERVE | 我们服务的行业 |
| INDUSTRIES WE AUTOMATE | 我们自动化的行业 |
| INDUSTRIES WE POWER | 我们供能的行业 |
| WHY SURGE | 为何选择 SURGE |
| CONTACT | 联系方式 |
| START A CONVERSATION | 开始对话 |
| WHAT HAPPENS NEXT | 下一步流程 |
| READY TO START? | 准备开始？ |
| LEGAL | 法律信息 |
| ABOUT US | 关于我们 |
| OUR SERVICES / OUR 5 CORE SERVICES | 我们的服务 / 五大核心服务 |
| SAAS · ENERGY MONITORING | SAAS · 能源监控 |
| RS-485 ISOLATION MODULE | RS-485 隔离模块 |
| INDUSTRIAL IOT GATEWAY | 工业物联网网关 |

### 5.4 Navigation labels (already in snippet 5447)

| EN | ZH |
|---|---|
| About Us | 关于我们 |
| Portfolio | 案例 |
| Internship | 实习计划 |
| Our Services | 我们的服务 |
| Product | 产品 |
| Home (breadcrumb) | 首页 |
| Contact | 联系我们 |
| Privacy Policy | 隐私政策 |
| Terms of Service | 服务条款 |
| Automation | 自动化 |
| Electrical | 电气工程 |
| Water Treatment | 水处理 |
| Renewable Energy | 可再生能源 |
| System Integration | 系统集成 |

### 5.5 CTA buttons

| EN | ZH |
|---|---|
| Free Consultation → | 免费咨询 → |
| Request Free Demo → | 申请免费演示 → |
| Request Quote → | 申请报价 → |
| Message on WhatsApp | WhatsApp 联系 |
| Email admin@suriota.com | 邮箱 admin@suriota.com |
| View All Portfolio | 查看全部案例 |
| Download Company Profile | 下载公司简介 |
| SEND | 发送 |
| Learn more → | 了解更多 → |

### 5.6 Common UI labels

| EN | ZH |
|---|---|
| Year(s) | 年 |
| Projects | 项目 |
| Clients | 客户 |
| Services | 服务 |
| within 24 hours | 24小时内 |
| Mon–Fri · 09:00–18:00 WIB | 周一至周五 · 09:00–18:00 WIB |
| Fastest response | 最快响应 |
| Direct chat | 直接聊天 |

### 5.7 Voice & tone
- **Professional, technical, B2B-direct.** Industrial buyers want specs and ROI.
- **Use 我们 (women, "we") and 您 (nin, formal "you").** Never 你 (casual).
- **Mixed-language okay for technical specs:** "支持 Modbus RTU / TCP 协议" preferred over forced all-ZH.
- **Keep brand names English in body** ("SURGE platform", not "SURGE 平台" except where naturally needed).

---

## 6. PAGE INVENTORY

Run this first to get current EN page IDs (these may differ from documented):

```python
import urllib.request, base64, json
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0'}
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?per_page=100&_fields=id,slug,title,link', headers=HDRS), timeout=30)
pages = json.loads(r.read())
en_pages = [p for p in pages if '/id/' not in p['link'] and '/zh/' not in p['link']]
for p in sorted(en_pages, key=lambda x: x['id']):
    print(f"{p['id']:5d} {p['slug']:35s} {p['link']}")
```

### Target ZH page slugs (proposed)

| EN slug | ZH slug | Notes |
|---|---|---|
| `/` (home) | `/zh/shouye/` | use `?slug=shouye` |
| `about/` | `zh/guanyu-women/` | |
| `portfolio/` | `zh/anli/` | "case studies" feel |
| `contact/` | `zh/lianxi/` | |
| `automation/` | `zh/zidonghua/` | |
| `electrical/` | `zh/dianqi-gongcheng/` | |
| `renewable-energy/` | `zh/kezaisheng-nengyuan/` | |
| `internet-of-things/` | `zh/iot/` | |
| `water-treatment/` | `zh/shuichuli/` | |
| `data-analytics/` | `zh/shujufenxi/` | |
| `digital-consulting/` | `zh/shuzihua-zixun/` | |
| `artificial-intelligence/` | `zh/rengong-zhineng/` | |
| `system-integration/` | `zh/xitong-jicheng/` | |
| `saas/` | `zh/saas/` | |
| `surge-energy-mapping/` | `zh/surge-energy-mapping/` | product name |
| `surge-vessel-tracking/` | `zh/surge-vessel-tracking/` | product name |
| `surge-water-analytic/` | `zh/surge-water-analytic/` | product name |
| `suriota-modbus-gateway/` | `zh/modbus-gateway/` | |
| `iso-m485-series/` | `zh/iso-m485/` | |
| `pm1611-wd/` | `zh/pm1611-wd/` | |
| `thm-30md/` | `zh/thm-30md/` | |
| `rs-485-surge-protector/` | `zh/rs-485-spd/` | |
| `waste-water-logger/` | `zh/wastewater-logger/` | |
| `privacy-policy/` | `zh/yinsi-zhengce/` | |
| `terms-of-service/` | `zh/fuwu-tiaokuan/` | |

Skip: portfolio articles (64 posts), Internship page (low priority).

---

## 7. ZH PAGE CREATION WORKFLOW (REST ONLY)

### 7.1 Workflow per page

```python
import urllib.request, base64, json, time, sys

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

EN_PAGE_ID = 29  # About — fetch live IDs via Section 6 script
ZH_SLUG = 'guanyu-women'
ZH_TITLE = '关于 SURIOTA'

def health_check():
    try:
        for u in ['https://suriota.com/wp-json/', 'https://suriota.com/', 'https://suriota.com/id/beranda/']:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
            if r.status >= 500:
                return False
        return True
    except: return False

# Pre-check
if not health_check():
    print('🛑 Health check failed BEFORE start. Halt.')
    sys.exit(1)

# 1) Fetch EN page Elementor data
r = urllib.request.urlopen(
    urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{EN_PAGE_ID}?context=edit&_fields=meta,title,content,template', headers=HDRS),
    timeout=30
)
d = json.loads(r.read())
ed = d.get('meta', {}).get('_elementor_data', '')
if isinstance(ed, list): ed = json.dumps(ed)
ps = d.get('meta', {}).get('_elementor_page_settings', {})

# 2) Apply translations (build full mapping from glossary + page-specific terms)
TRANSLATIONS = [
    # Hero
    ('About SURIOTA', '关于 SURIOTA'),
    # Eyebrows
    ('>ABOUT US<', '>关于我们<'),
    ('>VISION<', '>愿景<'),
    ('>MISSION<', '>使命<'),
    # body content (long sentences here)
    # ...
]
new_ed = ed
for old, new in TRANSLATIONS:
    new_ed = new_ed.replace(old, new)

# 3) Create new ZH page via REST POST
payload = {
    'title': ZH_TITLE,
    'slug': ZH_SLUG,
    'status': 'publish',
    'parent': 0,
    'template': d.get('template', ''),
    'meta': {
        '_elementor_data': new_ed,
        '_elementor_page_settings': ps,
        '_elementor_edit_mode': 'builder',
        '_elementor_template_type': 'wp-page',
        '_wp_page_template': d.get('template', 'default'),
    }
}
try:
    resp = urllib.request.urlopen(
        urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages', data=json.dumps(payload).encode(), method='POST', headers=HDRS),
        timeout=30
    ).read()
    zh_page = json.loads(resp)
    zh_id = zh_page['id']
    print(f'✅ Created ZH page ID:{zh_id}, slug={zh_page["slug"]}, link={zh_page["link"]}')
except Exception as e:
    print(f'❌ Create failed: {e}')
    sys.exit(1)

# 4) Post-creation health check
time.sleep(2)
if not health_check():
    print(f'🛑 Site went down after creating page {zh_id}. STOP.')
    sys.exit(1)
print('✅ Health check OK')

# 5) Language assignment — try multiple approaches in order:
# Approach A: standard WP taxonomy POST
try:
    # NOTE: requires ZH_TERM_ID from Section 3.2
    ZH_TERM_ID = None  # set from Section 3.2 verification
    if ZH_TERM_ID:
        payload2 = json.dumps({'language': [ZH_TERM_ID]}).encode()
        urllib.request.urlopen(
            urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{zh_id}', data=payload2, method='POST', headers=HDRS),
            timeout=15
        ).read()
        print(f'✅ Set language taxonomy via WP REST')
except Exception as e:
    print(f'⚠️ Language assignment failed: {e}')
    print(f'   Page {zh_id} created without language tag.')
    print(f'   USER ACTION: in WP admin → Pages → edit page {zh_id} → set language to 中文 manually')
```

### 7.2 If language assignment via REST fails (likely with Polylang free)

**DO NOT try to fix via PHP snippet.** Instead:

1. Continue creating all ZH pages without language tag
2. At the end, output a manual checklist for the user:

```
=== MANUAL POLYLANG LINKING REQUIRED ===
Please go to WP admin → Pages, find each ZH page below,
edit it, and set:
- Language: 中文 (zh)
- Translations: link to EN sibling + ID sibling

ZH pages created (need manual link):
  ID 9001 / zh/shouye/      → link to EN ID 12 + ID 5273
  ID 9002 / zh/guanyu-women/ → link to EN ID 29 + ID 5274
  ID 9003 / zh/anli/        → link to EN ID 839 + ID 5275
  ...etc
```

3. User does manual linking (5-10 min total). Brief done.

---

## 8. RULE: 64 PORTFOLIO ARTICLES STAY UNTRANSLATED

- Article post bodies (post type `post`, IDs 1925, 2201-2266, etc.) **remain in their existing language** (EN/mixed)
- ZH portfolio archive page (`/zh/anli/`) has ZH UI labels but article rows still show original EN titles
- Article URLs accessed from ZH context redirect to EN URL (`/article-slug/` not `/zh/article-slug/`) — this is acceptable, no fix needed
- Related-articles widgets on ZH pages: translate widget label ("RELATED INSIGHTS" → "相关文章") but leave post titles untouched

**Why:** translating 64 long technical articles is high-effort and low-ROI for B2B Chinese audience who prefers short product pages anyway.

---

## 9. NAVIGATION (DO NOT MODIFY)

Snippet 5447 already includes ZH map (verified). It auto-detects `<html lang="zh-CN">` or `/zh/` URL prefix and swaps nav labels. **DO NOT change snippet 5447 — it works.**

If ZH nav labels aren't appearing on your new ZH page:
1. Verify the page outputs `<html lang="zh-CN">` (Polylang sets this automatically when language tag is set)
2. If still in `id-ID` lang, the Polylang language tag is missing — see Section 7.2 manual fix

---

## 10. EXECUTION ORDER

1. **VERIFY site is up** — run health_check before anything
2. **Confirm with user** that they've completed Section 3 (added ZH language in WP admin)
3. **Verify ZH language exists** via REST (Section 3.2)
4. **Fetch live EN page IDs** (Section 6 script)
5. **Create ZH Home** (`/zh/shouye/`) — use as template/learning
6. **Health check** ✓
7. **Create ZH About** + **ZH Contact**
8. **Health check** ✓
9. **Create ZH Service pages** (9 pages: Automation, Electrical, RE, IoT, WT, DA, DC, AI, SysInt, SaaS) — health check after each 2 pages
10. **Create ZH Product pages** (9 pages) — health check after each 2 pages
11. **Create ZH Privacy + Terms** (2 pages)
12. **Final audit** (Section 11)
13. **Output manual linking checklist** for user

---

## 11. VERIFICATION AUDIT

### 11.1 After all pages created, run this:

```python
import urllib.request, base64, json, time, sys

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0'}

# 1) List all ZH pages
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?per_page=100&_fields=id,slug,title,link', headers=HDRS), timeout=30)
pages = json.loads(r.read())
zh_pages = [p for p in pages if '/zh/' in p.get('link','')]
print(f'Total ZH pages: {len(zh_pages)}')

# 2) HTTP status check for each
for p in zh_pages:
    try:
        r = urllib.request.urlopen(urllib.request.Request(p['link'], headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
        body = r.read().decode('utf-8', errors='replace')
        has_zh_lang = 'lang="zh-CN"' in body or 'lang="zh"' in body
        has_geist = 'Geist' in body
        print(f'  {p["id"]:5d} {p["slug"]:30s} HTTP={r.status} zh-lang={has_zh_lang} geist={has_geist}')
    except Exception as e:
        print(f'  {p["id"]} {p["slug"]} ERR: {e}')

# 3) Final site health
if not health_check():
    print('❌ Site is down. Investigate.')
else:
    print('✅ Site healthy. ZH rollout complete.')
```

### 11.2 Browser visual check (recommend Playwright)

```python
import asyncio
from playwright.async_api import async_playwright

ZH_URLS = ['https://suriota.com/zh/', 'https://suriota.com/zh/guanyu-women/', ...]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        for url in ZH_URLS:
            page = await b.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(1500)
            body = await page.evaluate('document.body.innerText.slice(0, 500)')
            font = await page.evaluate('getComputedStyle(document.body).fontFamily.split(",")[0]')
            print(f'{url}\n  font={font}\n  preview: {body[:200]}\n')
            await page.close()
        await b.close()
asyncio.run(main())
```

---

## 12. ROLLBACK PROTOCOL

If anything breaks:

### Site returns 500 after ZH page creation:
1. **STOP immediately.** Do not create more pages.
2. Identify the last-created ZH page ID
3. Delete it: `DELETE /wp-json/wp/v2/pages/{id}?force=true`
4. Health check
5. If still 500 — user must access WP admin recovery mode (check email)

### Bulk delete all ZH pages (nuclear option):
```python
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?per_page=100&_fields=id,link', headers=HDRS), timeout=30)
pages = json.loads(r.read())
zh_ids = [p['id'] for p in pages if '/zh/' in p.get('link','')]
for pid in zh_ids:
    try:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?force=true', method='DELETE', headers=HDRS), timeout=30).read()
        print(f'Deleted {pid}')
    except: pass
```

### Snippet 5447 broken (nav swap not working):
- **DO NOT** modify 5447 to fix. Instead delete the symptoms and ask user.
- Backup of 5447 v1 content is stored in this repo's git history (commit `0e8daf8`).

---

## 13. REFERENCE GLOSSARY (FROM EARLIER SESSION)

The full glossary of all 22 unique eyebrows, 50+ technical terms, brand voice rules, and design tokens is preserved at git commit `0e8daf8` in `_KIMI_CN_BRIEF.md` v1. Sections 5.1-5.7 above contain the essential subset needed for ZH execution.

If you need additional ID translation examples, fetch:
```python
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5274?context=edit&_fields=meta', headers=HDRS), timeout=30)
# Compare EN ID 29 with ID ID 5274 to see translation pattern
```

---

## 14. SUPPORT

If unclear or stuck:
- **STOP making changes**
- Run health_check
- Report status to user (Gifari): gheryanto@calx.sa / WhatsApp +62 858-3567-2476
- Specifically describe: what step you were on, what error, what last change was

---

## 15. SUCCESS CRITERIA

Brief is complete when:
- ✅ ~25 ZH pages live at `/zh/...`
- ✅ Each ZH page passes Section 11.1 audit (HTTP 200, Geist font, zh-lang attr)
- ✅ Polylang switcher shows EN | ID | ZH on every page
- ✅ Nav header swaps to Chinese on ZH pages
- ✅ Zero modifications to existing EN/ID content
- ✅ 64 articles untouched
- ✅ Site never went 500 during rollout
- ✅ Code Snippets plugin still DEACTIVATED

**Site MUST remain up at all times.** If you cannot achieve a step without breaking the site, **skip that step and document it for manual user completion** instead.

---

**END OF BRIEF v2.**

This is a SAFER version. Token-efficient, REST-only, no PHP risks. Polylang language assignment may fall back to manual user step — that's intentional and acceptable.
