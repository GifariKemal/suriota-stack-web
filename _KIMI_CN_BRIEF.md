# SURIOTA Website — Chinese (Simplified) Translation Brief

**Target executor:** Kimi CLI (or any code-capable AI agent)
**Project:** Add Simplified Chinese (zh-CN / `zh`) as 3rd language on suriota.com
**Status of EN + ID:** ✅ Complete, DO NOT MODIFY
**Date:** 2026-05-20

---

## 0. CRITICAL RULES — READ FIRST

1. **DO NOT modify any EN or ID content.** They are production-ready. Your job is **additive only** (create ZH variants).
2. **Target language: Simplified Chinese (zh-CN)** — for mainland China audience. NOT Traditional.
3. **Skip 64 portfolio articles.** They stay as-is. Article post links in ZH menu/related sections may stay EN URLs; only translate UI labels around them.
4. **Reuse the existing design system** — Geist font, brand colors, eyebrow taxonomy, card patterns, etc. NEVER swap design tokens.
5. **Polylang plugin** handles translations. Each EN page already has an ID translation linked via Polylang. You will add a third (ZH) translation.
6. **Always verify after each step.** Re-fetch via REST after POST. Browser-test with Playwright.
7. **Cache strategy:** After bulk edits, hit `/wp-json/elementor/v1/cache` DELETE, then warm cache by visiting key pages.

---

## 1. WHY SIMPLIFIED CHINESE (RESEARCH-BACKED)

| Factor | Decision |
|---|---|
| **Audience** | Mainland China B2B industrial IoT buyers, OEMs, system integrators |
| **Script** | Simplified (zh-CN) — used by 1.4B mainland speakers; Baidu favors zh-CN content |
| **Locale** | `zh_CN` (WordPress locale) |
| **Polylang code** | `zh` or `zh-cn` (see Section 4 for setup) |
| **HTML lang attr** | `zh-CN` |
| **Hreflang** | `zh-CN` |

Reasoning (from research):
- Mainland China users expect Simplified — Traditional is for Taiwan/Hong Kong only
- Baidu (60%+ search share in China) heavily favors Simplified content
- SURIOTA's products (Modbus gateways, IoT sensors) target mainland manufacturing/industrial market

**For multi-region China later:** add `zh-tw` (Traditional) as separate Polylang locale. Out of scope for this brief.

---

## 2. AUTHENTICATION & ENDPOINTS

### WP REST API base
```
https://suriota.com/wp-json/
```

### Auth (Application Password — Basic auth)
```
User: admin
App password: hCYK JqF1 khdB WDzI LQdQ WEBr
```
Python:
```python
import base64
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
```

### Key endpoints
| Endpoint | Use |
|---|---|
| `GET /wp/v2/pages?per_page=100&context=edit&_fields=id,title,meta` | List all pages |
| `GET /wp/v2/pages/{id}?context=edit&_fields=meta` | Get page Elementor data |
| `POST /wp/v2/pages/{id}` | Update page meta (Elementor data, custom_css) |
| `POST /wp/v2/pages` | Create new page |
| `GET /wp/v2/elementor_snippet` | Elementor Custom Code snippets (READ ONLY for ZH; do not modify existing) |
| `POST /wp/v2/elementor_snippet` | Create new ZH-specific snippet |
| `POST /wp/v2/elementor_snippet/{id}` | Update existing snippet (only ID:5447 nav swap needs ZH map added) |
| `DELETE /wp-json/elementor/v1/cache` | Clear Elementor render cache |

---

## 3. DESIGN SYSTEM (UNCHANGED — REUSE EXACTLY)

### 3.1 Typography (Geist family — loaded via elementor_snippet 5411)
```css
font-family: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif;
font-family: 'Geist Mono', ui-monospace, monospace;
```
**Google Fonts URL** (already in 5411 — do not duplicate):
```
https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap
```

### 3.2 Color tokens
| Token | Value | Use |
|---|---|---|
| `--sx-accent` | `#0E3942` | Headings, primary text |
| `--sx-amber` / `--sx-amber-accent` | `#C8851F` | Eyebrow numbers, highlights |
| `--sx-ink` | `#0F1A1F` | Body text |
| `--sx-mute` | `#5B6F75` | Secondary text |
| `--sx-line` | `#E8ECEE` | Borders |
| `--sx-surface` | `#FAFBFC` | Card backgrounds |
| `--sx-success` | `#3C7D47` | Success/eco accents |
| White soft | `rgba(255,255,255,0.86)` | Text on dark hero |
| White muted | `rgba(255,255,255,0.7)` | Tertiary on dark |

### 3.3 Typography sizes
| Element | Size |
|---|---|
| h1 (hero) | 42–80px clamp |
| h2 (section) | 24–32px |
| h3 (subsection) | 18px standard, 18px card title (`.sx-whyus-h3`, `.about-service-card h3`) |
| body / p | 15–16px |
| li | 14.5–16px |
| `.sx-eyebrow` | 12px Geist Mono uppercase letter-spacing 0.08em |
| `.sx-brand-name` | 16px Geist 600 mixed-case (used for "PT Surya Inovasi Prioritas") |

### 3.4 Container widths
| Selector | Max-width |
|---|---|
| `.sx-inner` (general) | 1180px |
| `.sx-whyus-inner` (trust cards) | 1080px |
| `.sx-industries-inner` (industry tags) | 960px |

### 3.5 Eyebrow taxonomy (DO NOT INVENT new ones — translate from this list)

EN eyebrows used sitewide (24 unique):

| EN eyebrow | ZH translation | Context |
|---|---|---|
| FAQ | 常见问题 / FAQ | FAQ section (FAQ universal accepted in CN B2B too) |
| KEY FEATURES | 核心功能 | Product features |
| WHY SURIOTA | 为何选择 SURIOTA | Trust cards |
| WHY CHOOSE SURIOTA | 为何选择 SURIOTA | Comparison |
| WHAT WE DELIVER | 我们交付什么 | Service deliverables |
| HOW WE WORK | 我们的工作方式 | Process section |
| APPLICATIONS | 应用场景 | Use cases |
| BUILT FOR | 专为...打造 | Target audience |
| INDUSTRIES WE SERVE | 我们服务的行业 | Industries |
| INDUSTRIES WE AUTOMATE | 我们自动化的行业 | Automation page |
| INDUSTRIES WE POWER | 我们供能的行业 | Renewable Energy |
| WHY SURGE | 为何选择 SURGE | SaaS page |
| CONTACT | 联系方式 | Contact page |
| START A CONVERSATION | 开始对话 | Contact form |
| WHAT HAPPENS NEXT | 下一步流程 | Onboarding |
| READY TO START? | 准备开始？ | CTA |
| LEGAL | 法律信息 | Privacy/Terms |
| ABOUT US | 关于我们 | About page |
| OUR SERVICES / OUR 5 CORE SERVICES | 我们的服务 / 五大核心服务 | Service cards |
| SAAS · ENERGY MONITORING | SAAS · 能源监控 | SURGE-E |
| RS-485 ISOLATION MODULE | RS-485 隔离模块 | ISO-M485 |
| INDUSTRIAL IOT GATEWAY | 工业物联网网关 | MGATE |

### 3.6 Patterns / class names (use exactly, do not invent variants)
- Hero: `<section class="sx-hero"><div class="sx-inner"><p class="sx-eyebrow">EYEBROW</p><h1 class="sx-hero-h1">Title</h1><p class="sx-hero-sub">subtitle</p>...`
- Trust card grid: `.sx-whyus` > `.sx-whyus-inner` > `.sx-whyus-grid` > `.sx-whyus-card` (each card has `.sx-whyus-num` + `<h3 class="sx-whyus-h3">` + `<p class="sx-whyus-desc">`)
- Industries tags: `.sx-industries` > `.sx-industries-inner` > tags
- CTA: `<a class="sx-cta-final-btn sx-cta-final-btn--primary">咨询免费 →</a>` + `--wa` variant for WhatsApp

---

## 4. POLYLANG ZH SETUP (FIRST TASK)

### 4.1 Add Chinese language to Polylang
WordPress admin → **Languages → Languages** → **Add new language**
- **Choose a language:** Select `中文 (zh-CN)` from dropdown (auto-fills locale `zh_CN`)
- **Name:** 中文
- **Locale:** `zh_CN`
- **Language code:** `zh` (or `zh-cn` if conflict)
- **Text direction:** LTR
- **Flag:** China
- **Order:** 3 (after EN=1, ID=2)

### 4.2 Verify via REST
```bash
curl -X GET "https://suriota.com/wp-json/pll/v1/languages" -H "Authorization: Basic $AUTH"
```
Should return array including `{"slug":"zh","locale":"zh_CN", ...}`.

### 4.3 Configure URL pattern
Languages → Settings → URL modifications:
- **Choose URL pattern:** "The language is set from the directory name in pretty permalinks" (matches existing `/id/` pattern)
- Result: ZH pages live at `https://suriota.com/zh/...`

### 4.4 Translation Strings (admin Strings)
After language added, Polylang exposes a "Strings translations" page. Translate site identity strings (title, tagline) — but most page content is done per-page.

---

## 5. CONTENT TRANSLATION GLOSSARY

### 5.1 Brand & company terms (DO NOT TRANSLATE — keep as-is)
- SURIOTA, PT Surya Inovasi Prioritas (use both English brand name + add `/苏里奥塔` parenthetical only on About page first mention)
- SURGE, SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytic, SURGE-Energy
- Product SKUs: SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 SPD, Wastewater Logger
- Technical protocols: Modbus, RTU, TCP, MQTT, OPC UA, RS-485, RS-232, PLC, SCADA, HMI, ERP, IIoT, IoT, BANI (legal), KLHK, SPARING, BAST, PUIL, IEC, SNI, GDPR, UU PDP
- "Industry 4.0" → 工业4.0
- WhatsApp, Tokopedia (kept)

### 5.2 Core terminology table (verified from Chinese B2B IoT sites)

| EN | Bahasa (existing) | ZH Simplified | Notes |
|---|---|---|---|
| Industrial IoT / IIoT | IoT Industri | 工业物联网 | wù lián wǎng |
| System Integration | Integrasi Sistem | 系统集成 | |
| Automation | Otomasi | 自动化 | |
| Renewable Energy | Energi Terbarukan | 可再生能源 | |
| Water Treatment | Water Treatment | 水处理 | |
| Electrical | Electrical | 电气工程 | for "Electrical Engineering" |
| Data Analytics | Data Analytics | 数据分析 | |
| Digital Consulting | Digital Consulting | 数字化咨询 | |
| Artificial Intelligence / AI | AI | 人工智能 | |
| SaaS / Software as a Service | SaaS | 软件即服务 / SaaS | keep SaaS in title |
| Gateway | Gateway | 网关 | |
| Sensor | Sensor | 传感器 | |
| Dashboard | Dashboard | 仪表盘 | |
| Real-time monitoring | Monitoring real-time | 实时监控 | |
| Edge computing | Edge computing | 边缘计算 | |
| Predictive maintenance | Predictive maintenance | 预测性维护 | |
| Smart manufacturing | Smart manufacturing | 智能制造 | |
| Cloud platform | Cloud platform | 云平台 | |
| Modbus gateway | Modbus Gateway | Modbus 网关 | |
| Power monitoring | Power monitoring | 电力监控 | |
| Energy mapping | Energy mapping | 能源映射 / 能源监测 | for SURGE-Energy |
| Vessel tracking | Vessel tracking | 船舶追踪 / 船舶定位 | for SURGE-V |
| Water analytic | Water Analytic | 水质分析 | for SURGE-W |
| Compliance | Compliance | 合规 | |
| Engineering | Engineering | 工程 | |
| Consulting | Konsultasi | 咨询 | |
| Service | Layanan | 服务 | |
| Product | Produk | 产品 | |
| Project | Proyek | 项目 | |
| Client | Klien | 客户 | |
| Customer | Pelanggan | 客户 | same as klien |
| Engineer | Engineer | 工程师 | |
| Industry | Industri | 行业 | |
| Manufacturing | Manufaktur | 制造业 | |
| Oil & Gas | Oil & Gas | 石油和天然气 | |
| Maritime | Maritim | 海事 | |
| Utilities | Utilitas | 公共事业 / 公用事业 | |
| Mining | Mining | 矿业 | |
| Power & Energy | Power & Energy | 电力能源 | |
| Pharmaceutical | Pharmaceutical | 制药 | |
| Food & Beverage | Food & Beverage | 食品饮料 | |
| Logistics & Warehousing | Logistics & Warehousing | 物流与仓储 | |

### 5.3 Navigation labels

| EN | ID (existing) | ZH | Notes |
|---|---|---|---|
| About Us | Tentang Kami | 关于我们 | |
| Portfolio | Portfolio | 案例 | "case studies" feel; or 项目案例 |
| Internship | Magang | 实习计划 | |
| Our Services | Layanan Kami | 我们的服务 | |
| Product | Produk | 产品 | |
| Home (breadcrumb) | Beranda | 首页 | |
| Contact | Kontak | 联系我们 | for nav |
| Privacy Policy | Kebijakan Privasi | 隐私政策 | |
| Terms of Service | Syarat Layanan | 服务条款 | |

### 5.4 Call-to-action labels

| EN | ID | ZH |
|---|---|---|
| Free Consultation → | Konsultasi Gratis → | 免费咨询 → |
| Request Free Demo → | Minta Demo Gratis → | 申请免费演示 → |
| Request Quote → | Minta Penawaran → | 申请报价 → |
| Message on WhatsApp | Pesan on WhatsApp | WhatsApp 联系 |
| Email admin@suriota.com | Email admin@suriota.com | 邮箱 admin@suriota.com |
| View All Portfolio | Lihat Semua Portfolio | 查看全部案例 |
| Download Company Profile | Unduh Company Profile | 下载公司简介 |
| SEND | KIRIM | 发送 |
| Learn more → | Pelajari selengkapnya → | 了解更多 → |

### 5.5 Common UI labels

| EN | ID | ZH |
|---|---|---|
| Year(s) | Tahun | 年 |
| Projects | Proyek | 项目 |
| Clients | Klien | 客户 |
| Services | Layanan | 服务 |
| within 24 hours | dalam 24 jam | 24小时内 |
| Mon–Fri · 09:00–18:00 WIB | Sen–Jum · 09:00–18:00 WIB | 周一至周五 · 09:00–18:00 WIB |
| Fastest response | Respons tercepat | 最快响应 |
| Direct chat | Chat langsung | 直接聊天 |

### 5.6 Voice & tone (for body content translation)
- **Professional, technical, direct.** Avoid marketing fluff. B2B industrial buyers want specs, ROI, capabilities.
- **Use 我们 (women, "we") and 您 (nin, formal "you").** Avoid casual 你 (ni).
- **Numbers kept in Arabic** (64+, 1.4M, etc.). Don't write 六十四.
- **Long English brand names stay English** in body text. Add ZH translation parenthetical only on first occurrence in About page.
- **Mixed-language okay for technical specs:** "支持 Modbus RTU / TCP 协议" is preferable to forcing all-ZH.

---

## 6. PAGE-BY-PAGE EXECUTION PLAN

### 6.1 Page inventory (54 pages — Polylang already links EN ↔ ID)

| EN slug | EN ID | ID slug | ID ID | ZH slug (proposed) | Notes |
|---|---|---|---|---|---|
| / | 12 | id/beranda/ | 5273 | zh/shouye/ | Home |
| about/ | 29 | id/tentang-kami/ | 5274 | zh/guanyu-women/ | About |
| portfolio/ | 839 | id/portfolio-id/ | 5275 | zh/anli/ | Portfolio |
| contact/ | 1547 | id/kontak/ | 5378 | zh/lianxi/ | Contact |
| automation/ | 35 | id/automation-id/ | 5282 | zh/zidonghua/ | Service |
| electrical/ | 37 | id/electrical-id/ | 5281 | zh/dianqi-gongcheng/ | Service |
| renewable-energy/ | 39 | id/renewable-energy-id/ | 5283 | zh/kezaisheng-nengyuan/ | Service |
| internet-of-things/ | 5029 | id/internet-of-things-id/ | 5284 | zh/iot/ | Service |
| water-treatment/ | 945 | id/water-treatment-id/ | 5277 | zh/shuichuli/ | Service |
| data-analytics/ | 5037 | id/data-analytics-id/ | 5285 | zh/shujufenxi/ | Service |
| digital-consulting/ | 5033 | id/digital-consulting-id/ | 5286 | zh/shuzihua-zixun/ | Service |
| artificial-intelligence/ | 5035 | id/artificial-intelligence-id/ | 5285 | zh/rengong-zhineng/ | Service |
| system-integration/ | 5031 | id/system-integration-id/ | 5382 | zh/xitong-jicheng/ | Service |
| saas/ | 5039 | id/saas-id/ | 5278 | zh/saas/ | SaaS |
| surge-energy-mapping/ | 1542 | id/surge-energy-mapping-id/ | 5288 | zh/surge-energy-mapping/ | Product |
| surge-vessel-tracking/ | 1546 | id/surge-vessel-tracking-id/ | 5289 | zh/surge-vessel-tracking/ | Product |
| surge-water-analytic/ | 1547 | id/surge-water-analytic-id/ | 5290 | zh/surge-water-analytic/ | Product |
| suriota-modbus-gateway/ | 934 | id/suriota-modbus-gateway-id/ | 5287 | zh/modbus-gateway/ | Product |
| iso-m485-series/ | 1740 | id/iso-m485-series-id/ | 5291 | zh/iso-m485/ | Product |
| pm1611-wd/ | 1742 | id/pm1611-wd-id/ | 5293 | zh/pm1611-wd/ | Product |
| thm-30md/ | 1741 | id/thm-30md-id/ | 5292 | zh/thm-30md/ | Product |
| rs-485-surge-protector/ | 1765 | id/rs-485-surge-protector-id/ | 5294 | zh/rs-485-surge-protector/ | Product |
| waste-water-logger/ | 929 | id/waste-water-logger-id/ | 5295 | zh/wastewater-logger/ | Product |
| privacy-policy/ | 1127 (or check) | id/kebijakan-privasi/ | 5379 | zh/yinsi-zhengce/ | Legal |
| terms-of-service/ | 1127 (or check) | id/syarat-layanan/ | 5380 | zh/fuwu-tiaokuan/ | Legal |
| (internship) | 1127 | id/magang-srt-team/ | 5276 | zh/shixi/ | Internship |
| (articles listing) | 5260 | id/artikel-id/ | 5279 | (skip — see Section 7) | Article archive |

**To fetch live IDs:** `GET /wp/v2/pages?per_page=100&context=edit&_fields=id,slug,title,link`

### 6.2 Workflow per page (use this script template)

```python
"""Create ZH variant of an existing page (copy from EN, translate, link via Polylang)."""
import urllib.request, base64, json, time

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

EN_PAGE_ID = 29       # About page (EN)
ZH_SLUG = 'guanyu-women'
ZH_TITLE = '关于 SURIOTA'

# 1) Fetch EN page Elementor data
r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{EN_PAGE_ID}?context=edit&_fields=meta,title,content', headers=HDRS)
d = json.loads(urllib.request.urlopen(r, timeout=30).read())
ed = d.get('meta', {}).get('_elementor_data', '')
if isinstance(ed, list): ed = json.dumps(ed)
ps = d.get('meta', {}).get('_elementor_page_settings', {})

# 2) Apply translations using glossary (extend with page-specific terms)
TRANSLATIONS = [
    # Hero
    ('About SURIOTA', '关于 SURIOTA'),
    ('Next Gen. Industrial Partner | Industrial IoT & System Integration in Batam, Indonesia',
     '新一代工业合作伙伴 | 印尼巴淡岛工业物联网与系统集成'),
    # Section eyebrows
    ('>ABOUT US<', '>关于我们<'),
    ('>VISION<', '>愿景<'),
    ('>MISSION<', '>使命<'),
    # H2/H3 ...
    # Body paragraphs ...
]
new_ed = ed
for old, new in TRANSLATIONS:
    new_ed = new_ed.replace(old, new)

# 3) Create new ZH page
payload = {
    'title': ZH_TITLE,
    'slug': ZH_SLUG,
    'status': 'publish',
    'parent': 0,
    'meta': {
        '_elementor_data': new_ed,
        '_elementor_page_settings': ps,
        '_elementor_edit_mode': 'builder',
        '_elementor_template_type': 'wp-page',
        '_wp_page_template': d.get('template', 'default'),
    }
}
resp = urllib.request.urlopen(
    urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages', data=json.dumps(payload).encode(), method='POST', headers=HDRS),
    timeout=30
).read()
zh_page = json.loads(resp)
zh_id = zh_page['id']
print(f'Created ZH page ID: {zh_id}')

# 4) Set Polylang language to 'zh' (via Polylang REST or pll_set_language meta)
# Polylang stores language in taxonomy `language` (term)
# Easiest: use Polylang REST API endpoint:
pll_payload = {'language': 'zh'}
urllib.request.urlopen(
    urllib.request.Request(f'https://suriota.com/wp-json/pll/v1/posts/{zh_id}', data=json.dumps(pll_payload).encode(), method='POST', headers=HDRS),
    timeout=30
).read()

# 5) Link ZH ↔ EN ↔ ID as translation siblings via Polylang
# Use Polylang's `translations` field
link_payload = {'translations': {'en': EN_PAGE_ID, 'id': 5274, 'zh': zh_id}}  # adapt IDs
urllib.request.urlopen(
    urllib.request.Request(f'https://suriota.com/wp-json/pll/v1/posts/{zh_id}', data=json.dumps(link_payload).encode(), method='POST', headers=HDRS),
    timeout=30
).read()

# 6) Clear Elementor cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)

# 7) Verify by fetching new page
urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/zh/{ZH_SLUG}/?nc={int(time.time())}', headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()
print('Done')
```

**Note:** Polylang REST API endpoint (`/wp-json/pll/v1/posts/{id}`) may or may not exist depending on Polylang Pro vs free. If not available:
- Fallback: set the language taxonomy term via standard WP REST: `POST /wp/v2/pages/{id}` with `{"language":["zh"]}` in payload
- If that doesn't work either: use a one-time `code_snippets` PHP snippet to call `pll_set_post_language($id, 'zh')` and `pll_save_post_translations(['en'=>$en_id, 'id'=>$id_id, 'zh'=>$zh_id])`. ⚠️ Code Snippets plugin currently DEACTIVATED — see Section 9 for safe activation.

---

## 7. RULE: SKIP 64 PORTFOLIO ARTICLES (POSTS)

64 portfolio posts (`/wp-json/wp/v2/posts` — IDs 2266, 2253, 2246, etc.) stay in their current language form. **DO NOT translate posts.**

### 7.1 What ZH user sees on articles
- ZH visitor lands on `/zh/anli/` (Portfolio listing) sees ZH UI labels (PROJECT, CLIENT, YEAR → 项目/客户/年)
- Clicking any article row → opens original EN URL `/jasa-maintenance-webmail.../` (the article post itself)
- **Acceptable** — article body stays EN. This is documented expected behavior.

### 7.2 Article archive page UI (ID `5260` / slug `artikel-id`)
- Listing page UI can have ZH variant if desired (e.g., `/zh/wenzhang/` with "INSIGHTS" eyebrow = 洞察)
- But **article post bodies themselves are NOT translated**

### 7.3 Related posts widget on ZH pages
- If a ZH page has a "Related Articles" / "Wawasan SURIOTA" / "INSIGHTS" widget that lists post titles, leave post titles in original language (EN/ID)
- ONLY translate the widget's eyebrow label and "Read more →" link text to ZH

---

## 8. NAVIGATION HEADER ZH SUPPORT

Existing JS swap (elementor_snippet ID:5447) handles EN → ID. Extend to handle ZH.

### 8.1 Update snippet 5447 — add ZH map

```python
import urllib.request, base64, json

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

NEW_JS = '''<script id="sx-nav-id-swap">
(function(){
  var lang = document.documentElement.lang || '';
  var isID = lang === "id" || lang === "id-ID" || location.pathname.indexOf("/id/") === 0;
  var isZH = lang === "zh" || lang === "zh-CN" || lang === "zh_CN" || location.pathname.indexOf("/zh/") === 0;
  if (!isID && !isZH) return;

  var maps = {
    id: {
      "About Us": "Tentang Kami",
      "Internship": "Magang",
      "Our Services": "Layanan Kami",
      "Automation": "Otomasi",
      "Renewable Energy": "Energi Terbarukan",
      "System Integration": "Integrasi Sistem",
      "Product": "Produk"
    },
    zh: {
      "About Us": "关于我们",
      "Portfolio": "案例",
      "Internship": "实习计划",
      "Our Services": "我们的服务",
      "Automation": "自动化",
      "Electrical": "电气工程",
      "Water Treatment": "水处理",
      "Renewable Energy": "可再生能源",
      "Internet of Things": "物联网",
      "System Integration": "系统集成",
      "Digital Consulting": "数字化咨询",
      "Artificial Intelligence": "人工智能",
      "Data Analytics": "数据分析",
      "Software as a Service": "软件即服务",
      "Product": "产品",
      "Modbus Gateway IIoT": "Modbus 网关 IIoT",
      "Waste Water Logger": "废水记录仪",
      "ISO-M485 SERIES": "ISO-M485 系列",
      "PM1611-WD": "PM1611-WD",
      "THM-30MD": "THM-30MD",
      "RS-485 Surge Protector": "RS-485 浪涌保护器"
    }
  };
  var map = isZH ? maps.zh : maps.id;

  function applySwap(root) {
    if (!root) return;
    var selectors = "header a, nav a, .elementor-nav-menu a, .menu-item > a, .sx-hf-v5-nav a, .sx-hf-v5-mobile a, .sx-emergency-hf a, .sx-hf-v5-dropbtn, header h4, header button, header .sx-hf-v5-mobile h4";
    var elements = root.querySelectorAll ? root.querySelectorAll(selectors) : [];
    elements.forEach(function(el){
      el.childNodes.forEach(function(n){
        if (n.nodeType === 3) {
          var txt = n.textContent.trim();
          if (map[txt]) n.textContent = n.textContent.replace(txt, map[txt]);
        }
      });
      el.querySelectorAll("span").forEach(function(sp){
        var txt = sp.textContent.trim();
        if (map[txt] && sp.children.length === 0) sp.textContent = map[txt];
      });
    });
  }

  function init() {
    if (!document.body) { setTimeout(init, 50); return; }
    applySwap(document);
    var header = document.querySelector("header") || document.querySelector(".sx-hf-v5-nav");
    if (header) {
      try {
        var mo = new MutationObserver(function(muts){
          muts.forEach(function(m){ if (m.addedNodes.length) applySwap(m.target); });
        });
        mo.observe(header, {childList:true, subtree:true});
        setTimeout(function(){ mo.disconnect(); }, 5000);
      } catch(e) {}
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>'''

payload = {'meta': {'_elementor_code': NEW_JS}}
urllib.request.urlopen(
    urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5447', data=json.dumps(payload).encode(), method='POST', headers=HDRS),
    timeout=30
).read()
print('Snippet 5447 updated with ZH support')
```

### 8.2 Language switcher
The site uses Polylang's built-in switcher. Once `zh` language is added (Section 4), switcher dropdown auto-includes "中文". Verify by checking the EN/ID dropdown in header — should now show third option "ZH" or "中文".

---

## 9. SAFE USE OF CODE SNIPPETS PLUGIN

**Code Snippets plugin is currently DEACTIVATED** because a bad PHP snippet broke the site previously. Plugin path: `code-snippets-test/code-snippets`.

### Safe re-activation procedure (only if Polylang REST is insufficient)
1. WP admin → Plugins → Activate **Code Snippets**
2. Test admin still loads
3. Add snippet via WP admin UI ONLY (not REST POST) — use the editor's syntax check
4. Use **wrapped hook approach** ONLY:
   ```php
   add_action('init', function() {
       if (!function_exists('pll_set_post_language')) return;
       // your code here
   }, 99);
   ```
5. **NEVER use top-level eager calls** like `\Elementor\Plugin::instance()` outside a hook — that broke the site before
6. Use snippet **scope = "Run on snippet activation only"** for one-shot Polylang language assignments

### Snippet template for Polylang bulk assignment (if REST doesn't work)
```php
add_action('init', function() {
    if (!function_exists('pll_set_post_language') || !function_exists('pll_save_post_translations')) return;
    if (get_option('sx_zh_pll_done')) return;

    $pairs = [
        // ['en_id' => 29, 'id_id' => 5274, 'zh_id' => 9001],
        // ['en_id' => 12, 'id_id' => 5273, 'zh_id' => 9002],
    ];
    foreach ($pairs as $p) {
        pll_set_post_language($p['zh_id'], 'zh');
        pll_save_post_translations([
            'en' => $p['en_id'],
            'id' => $p['id_id'],
            'zh' => $p['zh_id'],
        ]);
    }
    update_option('sx_zh_pll_done', 1);
}, 99);
```
After it runs once, **deactivate the snippet** immediately to avoid re-runs.

---

## 10. VERIFICATION & AUDIT

### 10.1 Per-page checklist (run after each page creation)
- [ ] Page loads at `https://suriota.com/zh/{slug}/` (HTTP 200)
- [ ] `<html lang="zh-CN">` in source
- [ ] All visible text in Simplified Chinese (no English chunks except technical terms in glossary)
- [ ] Geist font renders (no font fallback)
- [ ] Hero pattern matches EN/ID layout (eyebrow + h1 + subtitle + CTA)
- [ ] Card titles 18px Geist 600
- [ ] CTAs use ZH labels (免费咨询 →)
- [ ] Polylang language switcher shows EN | ID | ZH and links work bidirectionally

### 10.2 Sitewide audit (after all pages done)
Run this Python script:
```python
import asyncio, time
from playwright.async_api import async_playwright

ZH_PAGES = [
    'https://suriota.com/zh/',
    'https://suriota.com/zh/guanyu-women/',
    'https://suriota.com/zh/anli/',
    # ... all ZH URLs
]

EN_HEAVY_PHRASES = ['the ', 'and ', 'for ', 'with ', 'you ', 'will ', 'our ', 'we ', 'is ', 'are ']

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        for url in ZH_PAGES:
            page = await b.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(1500)
            body = await page.evaluate('document.body.innerText')
            en_count = sum(1 for w in EN_HEAVY_PHRASES if ' '+w in ' '+body.lower())
            font = await page.evaluate('getComputedStyle(document.body).fontFamily.split(",")[0]')
            print(f'{url}: EN markers={en_count}, font={font}')
            await page.close()
        await b.close()

asyncio.run(main())
```

### 10.3 SEO checklist
- Each ZH page has `<link rel="alternate" hreflang="zh-CN" href="...">` + reciprocal hreflang to EN + ID
- Polylang auto-injects hreflang if "Hreflang" option enabled in Languages → Settings
- AIOSEO (or whichever SEO plugin) per-page meta title/description in ZH:
  - **Title pattern:** `{Page Title} | SURIOTA — 工业物联网与系统集成`
  - **Description:** 155 chars in ZH summarizing page benefit + CTA

---

## 11. HOMEPAGE TRANSLATION (REFERENCE EXAMPLE)

### Source (EN Home — page 12)
```
Hero eyebrow: PT Surya Inovasi Prioritas
H1: Next Gen. Industrial Partner
Subtitle: SURIOTA is a technology company specializing in Industrial IoT & System Integration, headquartered in Batam, Riau Islands. Since January 2023, we have delivered 64+ industrial projects – from Modbus gateways to complete IoT platforms across manufacturing, energy, logistics, and maritime sectors.
Eyebrow: OUR 5 CORE SERVICES
Card 01: IoT & System Integration
Card 02: AI & Data Analytics
Card 03: Software as a Service
Card 04: Automation & Renewable Energy
Card 05: Digital Consulting
Trust: With our commitment to the highest technical standards, SURIOTA is a trusted partner in improving efficiency, productivity, and business sustainability for clients across Indonesia.
CTA: Free Consultation →
```

### Target ZH Home (proposed)
```
Hero eyebrow: PT Surya Inovasi Prioritas
H1: 新一代工业合作伙伴
Subtitle: SURIOTA 是一家专注于工业物联网与系统集成的技术公司,总部位于印度尼西亚廖内群岛巴淡岛。自 2023 年 1 月以来,我们已交付 64+ 工业项目——从 Modbus 网关到完整 IoT 平台,服务于制造、能源、物流和海事行业。
Eyebrow: 五大核心服务
Card 01: 物联网与系统集成
Card 02: 人工智能与数据分析
Card 03: 软件即服务
Card 04: 自动化与可再生能源
Card 05: 数字化咨询
Trust: 凭借对最高技术标准的承诺,SURIOTA 是印尼客户值得信赖的合作伙伴,助力提升效率、生产力和业务可持续性。
CTA: 免费咨询 →
```

Use this as the structural reference — every other page follows the same pattern (replace content, keep classes/widgets).

---

## 12. EXECUTION ORDER (RECOMMENDED)

1. **Polylang ZH setup** (Section 4) — must be done first, in WP admin
2. **Update nav swap snippet 5447** (Section 8) — adds ZH map; safe to do via REST
3. **Create ZH Home** (`/zh/`) — use as template/reference for other pages
4. **Create ZH About** + **ZH Contact** — high-priority pages
5. **Create ZH Service pages** (9 pages: Automation, Electrical, RE, IoT, WT, DA, DC, AI, SysInt, SaaS)
6. **Create ZH Product pages** (9 pages: MGATE, ISO-M485, PM1611, THM-30MD, SPD-T485, WW Logger, SURGE-E, SURGE-V, SURGE-W)
7. **Create ZH Portfolio archive** (links to EN posts — see Section 7)
8. **Create ZH Privacy + Terms** (legal — use existing EN/ID structure)
9. **Audit + cache warm** (Section 10)

After each page: link Polylang translations (Section 6.2 step 5).

---

## 13. ROLLBACK STRATEGY

If something breaks:
1. **Don't panic.** Each ZH page is a NEW post — deleting it doesn't affect EN/ID.
2. **Bulk delete ZH pages via REST:** `DELETE /wp-json/wp/v2/pages/{id}?force=true`
3. **Snippet 5447 rollback:** before updating, fetch and save its current `_elementor_code` content. If new version breaks JS, POST back the old content.
4. **Polylang language removal:** WP admin → Languages → Languages → delete 中文 entry. ALL ZH page-language assignments will be lost (pages will become "no language"), but content stays.

---

## 14. SUPPORT REFERENCES

- Polylang docs: https://polylang.pro/documentation/
- Polylang Chinese setup: https://wordpress.org/support/topic/polylang-zh_cn-zh_hk-and-zh_tw/
- WP REST API: https://developer.wordpress.org/rest-api/
- Elementor page settings via REST: stored in `meta._elementor_data` as JSON string
- Geist font: https://vercel.com/font

---

## 15. CONTACT (if Kimi needs to ask Gifari for clarification)

- Email: gheryanto@calx.sa / guntur.kh@gmail.com
- WhatsApp: +62 858-3567-2476
- Project owner: Gifari Kemal Suryo, CEO PT Surya Inovasi Prioritas

---

**END OF BRIEF.** This document is self-contained — Kimi should be able to execute the full ZH rollout using only this file + WP REST credentials.

Output expected:
- 25+ new ZH pages live at `/zh/...`
- Polylang language switcher shows EN | ID | ZH
- Nav header swaps to Chinese on ZH pages
- All Geist font, brand colors preserved
- Zero modifications to existing EN/ID content
- 64 portfolio articles untouched
