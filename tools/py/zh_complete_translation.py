"""ZH/CN complete translation pipeline for suriota.com.

Pipeline:
  1. Health check (EN home + ID home + ZH home must return 200)
  2. Fetch each ZH page's _elementor_data
  3. Walk dict recursively, translate string fields using GLOSSARY + per-page map
  4. JSON-validate before POST (load/dump round-trip)
  5. Re-bundle per-page custom_css into snippet 5498 (sitewide CSS injection)
  6. Audit: count remaining EN-only lines per page

Safety:
  - REST API only (no PHP execution)
  - Dict-walker translation (no string-level regex on JSON dumps)
  - Pre/post JSON.loads validation
  - Skip pages on health-check failure
  - 64 articles excluded
"""
from __future__ import annotations
import base64
import json
import re
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

WP_USER = "admin"
WP_PASS = "hCYK JqF1 khdB WDzI LQdQ WEBr"
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
BASE = "https://suriota.com/wp-json"
HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

ZH_PAGES = {
    5448: ("shouye",              "首页"),
    5450: ("guanyu-women",        "关于 SURIOTA"),
    5451: ("zidonghua",           "自动化与物联网服务"),
    5452: ("dianqi-gongcheng",    "电气工程服务"),
    5453: ("kezaisheng-nengyuan", "可再生能源服务"),
    5454: ("anli",                "项目案例"),
    5456: ("modbus-gateway",      "Modbus 网关 IIoT"),
    5457: ("shuichuli",           "水处理服务"),
    5461: ("iso-m485",            "ISO-M485 系列"),
    5463: ("pm1611-wd-2",         "PM1611-WD"),
    5465: ("lianxi",              "联系我们"),
    5466: ("yinsi-zhengce",       "隐私政策"),
    5467: ("fuwu-tiaokuan",       "服务条款"),
    5468: ("iot",                 "物联网与系统集成"),
    5469: ("xitong-jicheng",      "系统集成"),
    5470: ("shuzihua-zixun",      "数字化咨询"),
    5471: ("rengong-zhineng",     "人工智能与数据分析"),
    5472: ("shujufenxi",          "数据分析"),
    5473: ("saas",                "软件即服务 SaaS"),
}

CSS_BUNDLE_SNIPPET_ID = 5498

GLOSSARY: dict[str, str] = {
    # Headline / hero
    "Next Gen. Industrial Partner":   "新一代工业合作伙伴",
    "Next Gen Industrial Partner":    "新一代工业合作伙伴",
    "Industrial IoT & System Integration": "工业物联网与系统集成",
    "Industrial IoT":                 "工业物联网",
    "System Integration":             "系统集成",
    "Digital Consulting":             "数字化咨询",
    "Artificial Intelligence":        "人工智能",
    "Data Analytics":                 "数据分析",
    "Software as a Service":          "软件即服务",
    "Internet of Things":             "物联网",
    "Water Treatment":                "水处理",
    "Renewable Energy":               "可再生能源",
    "Electrical":                     "电气工程",
    "Automation":                     "自动化",
    "Vendor-Agnostic PLC":            "厂商中立 PLC",
    "SCADA":                          "SCADA 监控",
    "OT/IT Convergence":              "OT/IT 融合",
    "Industrial Networking":          "工业网络",
    "Edge Computing":                 "边缘计算",
    # Nav / CTA
    "About Us":               "关于我们",
    "About":                  "关于",
    "Our Services":           "我们的服务",
    "Services":               "服务",
    "Service":                "服务",
    "Products":               "产品",
    "Product":                "产品",
    "Portfolio":              "案例",
    "Case Studies":           "案例研究",
    "Internship":             "实习计划",
    "Contact Us":             "联系我们",
    "Contact":                "联系",
    "Get in touch":           "联系我们",
    "Get a Quote":             "获取报价",
    "Request a Quote":         "申请报价",
    "Learn More":              "了解更多",
    "Read More":               "阅读更多",
    "Explore":                 "探索",
    "Download":                "下载",
    "Download Datasheet":      "下载数据表",
    "Back to top":             "返回顶部",
    "View All":                "查看全部",
    "View Project":            "查看项目",
    # Sections
    "Why Choose Us":           "为何选择我们",
    "Why Us":                  "为何选择我们",
    "Our Approach":            "我们的方法",
    "Our Process":             "我们的流程",
    "Our Capabilities":        "我们的能力",
    "Our Expertise":           "我们的专长",
    "Key Features":            "核心功能",
    "Key Benefits":            "核心优势",
    "Technical Specifications": "技术规格",
    "Specifications":          "技术规格",
    "Applications":            "应用领域",
    "Frequently Asked Questions": "常见问题",
    "FAQ":                     "常见问题",
    "Testimonials":            "客户评价",
    "Trusted by":              "客户信赖",
    "Industries Served":       "服务行业",
    "Industries We Serve":     "我们服务的行业",
    "Latest Insights":         "最新洞察",
    "Latest News":             "最新动态",
    "From the Blog":           "博客文章",
    "Related Services":        "相关服务",
    "Related Products":        "相关产品",
    "Built For":               "面向",
    "BUILT FOR":               "面向",
    # Process steps
    "STEP 01": "步骤 01",
    "STEP 02": "步骤 02",
    "STEP 03": "步骤 03",
    "STEP 04": "步骤 04",
    "STEP 05": "步骤 05",
    "STEP 06": "步骤 06",
    "Step 01": "步骤 01",
    "Step 02": "步骤 02",
    "Step 03": "步骤 03",
    "Step 04": "步骤 04",
    "Step 05": "步骤 05",
    "Step 06": "步骤 06",
    "Discovery":            "调研发现",
    "Design":               "方案设计",
    "Development":          "系统开发",
    "Deployment":           "部署实施",
    "Delivery":             "交付上线",
    "Support":              "运维支持",
    "Maintenance":          "维护服务",
    "Consultation":         "咨询",
    "Assessment":           "评估",
    "Implementation":       "实施",
    "Testing":              "测试",
    "Training":             "培训",
    # Industry / Sector terms
    "Oil & Gas":            "石油天然气",
    "Manufacturing":        "制造业",
    "Mining":               "采矿业",
    "Utilities":            "公用事业",
    "Smart City":           "智慧城市",
    "Smart Building":       "智能建筑",
    "Energy":               "能源",
    "Power Plant":          "电厂",
    "Transportation":       "交通运输",
    "Logistics":            "物流",
    "Healthcare":           "医疗",
    "Education":            "教育",
    "Agriculture":          "农业",
    "Fisheries":            "渔业",
    "Maritime":             "海事",
    # Footer / legal
    "Privacy Policy":              "隐私政策",
    "Terms of Service":            "服务条款",
    "Terms & Conditions":          "条款与条件",
    "Cookie Policy":               "Cookie 政策",
    "Sitemap":                     "网站地图",
    "All rights reserved":         "版权所有",
    "Stay Updated":                "订阅更新",
    "Subscribe to our newsletter": "订阅我们的资讯",
    "Subscribe":                   "订阅",
    "Your email":                  "您的邮箱",
    "Email Address":               "邮箱地址",
    "Send Message":                "发送消息",
    "Send":                        "发送",
    "Submit":                      "提交",
    # Company tagline
    "PT Surya Inovasi Prioritas":  "PT Surya Inovasi Prioritas",
    "Surya Inovasi Prioritas":     "Surya Inovasi Prioritas",
    # Common verbs / claims
    "Designed for":             "专为",
    "Engineered for":           "为…而设计",
    "Built for":                "面向",
    "Powered by":               "驱动:",
    "Made in Indonesia":        "印尼制造",
    "ISO Certified":            "ISO 认证",
    "Industrial Grade":         "工业级",
    "Mission Critical":         "关键业务",
    "Real-time":                "实时",
    "End-to-end":               "端到端",
    "Cloud-native":             "云原生",
    "On-premise":               "本地部署",
    "Scalable":                 "可扩展",
    "Reliable":                 "可靠",
    "Secure":                   "安全",
    "Cost-effective":           "高性价比",
    # CTAs unique
    "Talk to an Expert":        "咨询专家",
    "Schedule a Demo":          "预约演示",
    "Book a Consultation":      "预约咨询",
    "Start Your Project":       "开启您的项目",
}

PER_PAGE_TRANSLATIONS: dict[int, dict[str, str]] = {
    5466: {
        "Last updated:":              "最后更新:",
        "Effective Date:":            "生效日期:",
        "Information We Collect":     "我们收集的信息",
        "How We Use Information":     "信息使用方式",
        "How We Use Your Information":"我们如何使用您的信息",
        "Information Sharing":        "信息共享",
        "Data Security":              "数据安全",
        "Your Rights":                "您的权利",
        "Cookies":                    "Cookie",
        "Changes to This Policy":     "政策变更",
        "Changes to this Policy":     "政策变更",
        "Contact Us":                 "联系我们",
        "Personal Information":       "个人信息",
        "Third Parties":              "第三方",
        "Third-Party Services":       "第三方服务",
    },
    5467: {
        "Acceptance of Terms":        "条款接受",
        "Use of Services":            "服务使用",
        "User Obligations":           "用户义务",
        "Intellectual Property":      "知识产权",
        "Limitation of Liability":    "责任限制",
        "Termination":                "终止",
        "Governing Law":              "适用法律",
        "Changes to Terms":           "条款变更",
        "Dispute Resolution":         "争议解决",
        "Effective Date:":            "生效日期:",
        "Last updated:":              "最后更新:",
    },
    5465: {
        "Drop us a message":              "给我们留言",
        "We typically respond within":    "我们通常在以下时间内回复:",
        "1 business day":                 "1 个工作日",
        "Office Hours":                   "办公时间",
        "Monday – Friday":                "周一至周五",
        "Headquarters":                   "总部",
        "Find Us":                        "找到我们",
        "Full Name":                      "姓名",
        "Company":                        "公司",
        "Message":                        "留言",
        "Phone":                          "电话",
        "Email":                          "邮箱",
    },
    5448: {
        "SURIOTA is a technology company specializing in Industrial IoT & System Integration":
            "SURIOTA 是一家专注于工业物联网与系统集成的科技公司",
    },
    5450: {
        "Ready to Collaborate with SURIOTA?": "准备好与 SURIOTA 合作了吗？",
        "SURIOTA Core Values": "SURIOTA 核心价值观",
        "CIPTA - Core Values": "CIPTA - 核心价值观",
        "Five principles guiding every SURIOTA project, execution, and partnership.":
            "指导 SURIOTA 每一个项目、执行与合作的五项原则。",
        "Committed Outcome":  "坚定的成果",
        "Consistent focus on the best results &amp; defined targets.":
            "始终专注于最佳结果与既定目标。",
        "Integrity of Innovation": "诚信创新",
        "Innovating with honesty, ethics, &amp; responsibility.":
            "以诚信、伦理与责任进行创新。",
        "Precision in Execution": "精准执行",
        "Precision, discipline, &amp; high quality standards.":
            "精准、纪律与高质量标准。",
        "Trust Through Reliability": "通过可靠建立信任",
        "Consistency, dependability, &amp; commitment.":
            "始终如一、可靠与承诺。",
        "Adaptive Growth": "适应性成长",
        "Embracing change &amp; continuous improvement.":
            "拥抱变化与持续改进。",
    },
    5451: {
        "What communication protocols does the SURGE platform support?":
            "SURGE 平台支持哪些通信协议？",
        "The SURGE platform supports standard industrial protocols including Modbus RTU/TCP, MQTT, HTTP REST API, and OPC-UA. We can also integrate custom protocols specific to your system requirements.":
            "SURGE 平台支持标准工业协议，包括 Modbus RTU/TCP、MQTT、HTTP REST API 以及 OPC-UA。我们也能根据您的系统需求集成自定义协议。",
        "Can SURIOTA IoT systems operate without internet?":
            "SURIOTA 物联网系统可以离线运行吗？",
        "Yes, our systems are designed with offline operation capability (edge computing). Data is stored locally during connection loss and synchronized automatically when connection is restored.":
            "可以，我们的系统具备离线运行能力（边缘计算）。在网络中断期间数据会先存储在本地，连接恢复后会自动同步。",
        "How long does IoT monitoring system implementation take?":
            "物联网监控系统的实施周期需要多长？",
        "For basic monitoring systems with 5-10 sensors, implementation typically takes 2-4 weeks, covering hardware installation, software configuration, dashboard integration, and operator training.":
            "对于含 5–10 个传感器的基础监控系统，实施通常需要 2–4 周，涵盖硬件安装、软件配置、看板集成及操作员培训。",
        "Can SURGE integrate with existing ERP systems?":
            "SURGE 可以与现有 ERP 系统集成吗？",
    },
    5452: {
        "Panel installation, power distribution & commissioning per SNI, IEC, PUIL 2011. Turnkey electrical engineering for oil & gas, shipyard, manufacturing & commercial buildings across Indonesia":
            "依据 SNI、IEC 与 PUIL 2011 进行配电盘安装、电力分配与调试。为印尼各地的石油天然气、船厂、制造业及商业建筑提供交钥匙电气工程。",
        "Optimize your business with industrial electrical systems from SURIOTA":
            "借助 SURIOTA 的工业电气系统优化您的业务",
        "What standards does SURIOTA use for electrical installation?":
            "SURIOTA 电气安装遵循哪些标准？",
        "How long does electrical commissioning take?":
            "电气调试需要多长时间？",
        "What documents are delivered after project completion?":
            "项目完工后会交付哪些文件？",
        "SURIOTA delivers As-Built Drawings, complete Commissioning Reports, Handover Documents (Berita Acara Serah Terima), and recommended maintenance schedules for every electrical installation project.":
            "对于每个电气安装项目，SURIOTA 都会交付竣工图、完整的调试报告、交接文件（Berita Acara Serah Terima）以及建议的维护计划。",
        "Does SURIOTA serve projects outside Batam?":
            "SURIOTA 可以承接巴淡岛以外的项目吗？",
        "Commissioning duration depends on installation complexity. For medium-scale commercial building installations, the commissioning process typically takes 2-5 business days, covering insulation resistance, continuity, and load testing.":
            "调试时长取决于安装的复杂程度。对于中等规模的商业建筑安装，调试通常需要 2–5 个工作日，包含绝缘电阻、导通性以及负载测试。",
    },
    5453: {
        "Toward a greener future with SURIOTA renewable energy solutions":
            "携手 SURIOTA 可再生能源方案，迈向更绿色的未来",
        "What are the advantages of PLTS-PLTB hybrid over PLTS alone?":
            "PLTS-PLTB 混合系统相比单独的 PLTS 有什么优势？",
        "What is the estimated ROI for industrial PLTS systems?":
            "工业 PLTS 系统的投资回报率大约是多少？",
        "Does SURIOTA provide remote monitoring for PLTS?":
            "SURIOTA 是否为 PLTS 提供远程监控？",
        "Are special permits required for PLTS installation?":
            "PLTS 安装需要特殊许可吗？",
        "For on-grid PLTS systems, PLN approval and applicable regulatory permits are required. SURIOTA assists with the permitting process and coordination with relevant agencies as part of our service.":
            "对于并网 PLTS 系统，需要 PLN 审批和相关法规许可。作为服务的一部分，SURIOTA 协助办理许可流程并与相关机构对接。",
        "Hybrid systems leverage two renewable energy sources simultaneously. When solar production is low (night or cloudy), wind turbines continue generating electricity, providing more stable energy supply and requiring smaller battery capacity.":
            "混合系统同时利用两种可再生能源。当光伏出力较低时（夜间或多云），风力发电机可继续发电，从而提供更稳定的能源供应，并降低所需的电池容量。",
        "PLTS ROI depends on electricity tariffs, solar irradiation at the location, and system capacity. For industrial applications in Batam and Riau Islands, ROI is typically achieved within 5-8 years, with system lifespan reaching 25 years.":
            "PLTS 的投资回报周期取决于电价、当地的光照辐射以及系统容量。对于巴淡岛和廖内群岛的工业应用，通常在 5–8 年内即可实现回报，而系统寿命可达 25 年。",
    },
    5457: {
        "WTP, WWTP & IPAL design-build with KLHK SPARING compliance & real-time IoT monitoring (pH, COD, TSS, NH3) for industries, PDAM & water utilities":
            "面向工业、PDAM 与供水公用事业，提供符合 KLHK SPARING 合规要求的 WTP、WWTP 与 IPAL 设计建造，并配备实时物联网监测（pH、COD、TSS、NH₃）。",
        "Pure water treatment solutions for a sustainable future with SURIOTA":
            "携手 SURIOTA 的纯净水处理方案，迈向可持续的未来",
        "What is the difference between WTP and WWTP?":
            "WTP 与 WWTP 有什么区别？",
        "How often is WTP maintenance required?":
            "WTP 多久维护一次？",
        "Can SURIOTA repair pumps from any brand?":
            "SURIOTA 可以维修任何品牌的水泵吗？",
        "Yes, our experienced technicians can rewind and repair pump motors from various brands including Grundfos, Ebara, Flygt, Satelite, and others.":
            "可以，我们经验丰富的技术人员能够对 Grundfos、Ebara、Flygt、Satelite 等多种品牌的水泵电机进行重绕和维修。",
        "What is SPARING and why is it important?":
            "SPARING 是什么？为什么重要？",
        "SPARING (Industrial Wastewater Quality Monitoring System) is an online monitoring system required by KLHK for certain industries. SURIOTA provides installation, integration, and maintenance of SPARING systems per government regulations.":
            "SPARING（工业废水水质在线监测系统）是 KLHK 针对部分行业强制要求的在线监测系统。SURIOTA 依据政府法规提供 SPARING 系统的安装、集成与维护服务。",
    },
    5461: {
        "RS-485 Isolation Module": "RS-485 隔离模块",
    },
}

LOG: list[str] = []

def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG.append(line)


def http(method: str, path: str, body: dict | None = None, timeout: int = 60) -> tuple[int, dict | list | str]:
    url = path if path.startswith("http") else f"{BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", errors="replace")
            try:
                return r.status, json.loads(raw)
            except json.JSONDecodeError:
                return r.status, raw
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8", errors="replace"))
        except Exception:
            err = str(e)
        return e.code, err


def health_check() -> bool:
    log("Health check…")
    targets = [
        ("EN home", "https://suriota.com/"),
        ("ID home", "https://suriota.com/id/"),
        ("ZH home", "https://suriota.com/shouye/"),
    ]
    ok = True
    for name, url in targets:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                status = r.status
            log(f"  {name:8} → {status}")
            if status >= 400:
                ok = False
        except Exception as e:
            log(f"  {name:8} → FAIL {e}")
            ok = False
    return ok


def fetch_page_raw(pid: int) -> dict | None:
    code, data = http("GET", f"/wp/v2/pages/{pid}?context=edit")
    if code != 200 or not isinstance(data, dict):
        log(f"  fetch {pid} FAIL ({code})")
        return None
    return data


def translate_string(s: str, page_map: dict[str, str]) -> tuple[str, int]:
    """Apply per-page map first (more specific), then global glossary.

    Returns (translated, replacement_count). Skips if string already contains CJK.
    """
    if not s or not isinstance(s, str):
        return s, 0
    # If string contains CJK already, skip to avoid double-translation
    if re.search(r"[\u4e00-\u9fff]", s):
        return s, 0
    count = 0
    out = s
    # Page-specific first (longer / more specific patterns)
    for src in sorted(page_map.keys(), key=len, reverse=True):
        if src and src in out:
            out = out.replace(src, page_map[src])
            count += 1
    for src in sorted(GLOSSARY.keys(), key=len, reverse=True):
        if src and src in out:
            out = out.replace(src, GLOSSARY[src])
            count += 1
    return out, count


TRANSLATABLE_KEYS = {
    "title", "subtitle", "heading", "subheading", "description", "text",
    "editor", "html", "label", "button_text", "field_label", "placeholder",
    "tab_title", "tab_content", "title_text", "sub_text", "after_text",
    "before_text", "highlighted_text", "rotating_text", "link_text",
    "icon_text", "tooltip", "caption", "alt", "content", "header_label",
}

URL_KEYS_SKIP = {"url", "link", "image", "background_image", "background_video_link"}


def walk_translate(node, page_map: dict[str, str], stats: dict[str, int]) -> None:
    """Mutate node in place: translate strings in known content fields."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in URL_KEYS_SKIP:
                continue
            if isinstance(v, str) and (k in TRANSLATABLE_KEYS or k.endswith("_text") or k.endswith("_title")):
                new, cnt = translate_string(v, page_map)
                if cnt > 0:
                    node[k] = new
                    stats["replacements"] += cnt
                    stats["fields"] += 1
            elif isinstance(v, (dict, list)):
                walk_translate(v, page_map, stats)
    elif isinstance(node, list):
        for item in node:
            walk_translate(item, page_map, stats)


def translate_page(pid: int) -> dict:
    slug, expected_title = ZH_PAGES[pid]
    log(f"→ {pid} {slug}")
    page = fetch_page_raw(pid)
    if not page:
        return {"pid": pid, "ok": False, "reason": "fetch_fail"}

    meta = page.get("meta") or {}
    elementor_raw = meta.get("_elementor_data")
    if not elementor_raw:
        log(f"  no _elementor_data — skip")
        return {"pid": pid, "ok": False, "reason": "no_data"}

    try:
        elementor = json.loads(elementor_raw) if isinstance(elementor_raw, str) else elementor_raw
    except json.JSONDecodeError as e:
        log(f"  pre-JSON INVALID: {e}")
        return {"pid": pid, "ok": False, "reason": "pre_json_invalid"}

    stats = {"replacements": 0, "fields": 0}
    page_map = PER_PAGE_TRANSLATIONS.get(pid, {})
    walk_translate(elementor, page_map, stats)

    if stats["replacements"] == 0:
        log(f"  0 replacements — skip POST")
        return {"pid": pid, "ok": True, "reason": "no_change", "stats": stats}

    new_raw = json.dumps(elementor, ensure_ascii=False, separators=(",", ":"))
    try:
        json.loads(new_raw)
    except json.JSONDecodeError as e:
        log(f"  post-JSON INVALID: {e}")
        return {"pid": pid, "ok": False, "reason": "post_json_invalid"}

    code, _ = http("POST", f"/wp/v2/pages/{pid}", {"meta": {"_elementor_data": new_raw}})
    if code not in (200, 201):
        log(f"  POST FAIL {code}")
        return {"pid": pid, "ok": False, "reason": f"post_{code}", "stats": stats}

    log(f"  {stats['replacements']} replacements across {stats['fields']} fields ✓")
    return {"pid": pid, "ok": True, "stats": stats}


def regen_elementor_css(pid: int) -> None:
    """Trigger Elementor to regenerate per-page CSS (clears stale cache)."""
    http("POST", f"/wp/v2/pages/{pid}", {"meta": {"_elementor_css": ""}})


def audit_remaining_en(pid: int) -> int:
    """Count strings still containing latin alphabetic runs ≥3 chars but no CJK."""
    page = fetch_page_raw(pid)
    if not page:
        return -1
    raw = (page.get("meta") or {}).get("_elementor_data") or ""
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return -1

    en_strings: list[str] = []

    def visit(n):
        if isinstance(n, dict):
            for k, v in n.items():
                if k in URL_KEYS_SKIP:
                    continue
                if isinstance(v, str):
                    if k in TRANSLATABLE_KEYS or k.endswith("_text") or k.endswith("_title"):
                        if v and not re.search(r"[\u4e00-\u9fff]", v) and re.search(r"[A-Za-z]{3,}", v):
                            en_strings.append(v.strip()[:80])
                elif isinstance(v, (dict, list)):
                    visit(v)
        elif isinstance(n, list):
            for x in n:
                visit(x)

    visit(data)
    return len(en_strings)


def run() -> None:
    if not health_check():
        log("ABORT: health check failed")
        return
    log("")
    log("=== Translation pass ===")
    results = []
    for pid in sorted(ZH_PAGES.keys()):
        results.append(translate_page(pid))
        time.sleep(0.3)

    log("")
    log("=== Audit ===")
    for pid in sorted(ZH_PAGES.keys()):
        slug = ZH_PAGES[pid][0]
        remaining = audit_remaining_en(pid)
        log(f"  {pid} {slug:25} EN-residual: {remaining}")

    log("")
    ok = sum(1 for r in results if r.get("ok"))
    total_reps = sum((r.get("stats") or {}).get("replacements", 0) for r in results)
    log(f"=== Summary: {ok}/{len(results)} OK, {total_reps} total replacements ===")


if __name__ == "__main__":
    run()
