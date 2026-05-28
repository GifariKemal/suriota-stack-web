"""Phase 5: AIOSEO description backfill — 13 ZH + 7 EN/ID legal/contact pages."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
AIOSEO = "https://suriota.com/wp-json/aioseo/v1/post"

descriptions = [
    # ZH pages (11 missing + 2 with title fix from Phase 2)
    (5467, "fuwu-tiaokuan",          "SURIOTA 服务条款 — 使用 suriota.com 网站、咨询服务、产品销售与技术支持的法律条款。包含责任范围、知识产权、付款条件与争议解决，适用于印尼客户。"),
    (5465, "lianxi",                  "联系 SURIOTA — 巴淡岛工业 IoT、Modbus 网关、SCADA 自动化与 SaaS 监控团队。咨询、报价、技术支持。WhatsApp、邮件、办公地址。"),
    (5464, "rs-485-spd",              "RS-485 浪涌保护器 SPD-T485-105 — 工业级 Modbus、串行通信线路雷击与瞬态电压保护。10kA 通流容量，IP67 防护，DIN 导轨安装。"),
    (5463, "pm1611-wd-2",             "PM1611-WD 多功能数字电表 — 三相电流、电压、功率、能量、谐波监测。Modbus RTU/TCP 通信，DIN 导轨安装，适用于配电、能源管理与 IoT 监控。"),
    (5462, "thm-30md-2",              "THM-30MD 温湿度变送器 — 工业级温度湿度传感器，Modbus RTU 输出，IP65 防护，适用于配电柜、暖通空调、洁净室、农业大棚监控。"),
    (5461, "iso-m485",                "ISO-M485 系列 — RS-485 信号隔离器与中继器。光电隔离 2500V，支持 Modbus 协议透传，扩展通信距离到 1200m，多机串联组网。"),
    (5460, "surge-water-analytic-2",  "SURGE-Water Analytic — 印尼 KLHK SPARING 合规废水监测云平台。pH、TSS、COD、流量实时监测、自动报警、政府数据上报。"),
    (5459, "surge-vessel-tracking-2", "SURGE-Vessel Tracking — 船队 GPS 追踪、燃油消耗、引擎状态、航行历史。海洋物流公司多船队多港口实时监控仪表板。"),
    (5458, "surge-energy-mapping-2",  "SURGE-Energy Mapping — 能源数据可视化平台。kWh、功率因数、CO2 排放、多场地能源效率对标，符合 ISO 50001 能源管理体系。"),
    (5456, "modbus-gateway",          "SRT-MGATE-1210 工业 Modbus 网关 — RTU/TCP 转 MQTT/SaaS。ESP32 双核、DIN 导轨安装、4G/Wi-Fi 双连接，桥接 PLC、电表、传感器到云端。"),
    (5455, "wastewater-logger",       "Wastewater Logger V.3 — 印尼 KLHK SPARING 合规废水监测数据采集器。pH、TSS、COD、流量、温度多参数采集，4G 自动上报政府平台。"),
    (5541, "shixi-jihua",             "SURIOTA 实习计划 — 工业物联网、SCADA 自动化、嵌入式硬件、Web 开发与商业分析方向。巴淡岛与雅加达办公室招收学生与应届毕业生。"),
    (5454, "anli",                    "SURIOTA 项目案例 — 巴淡岛工业 IoT、SCADA、自动化、能源管理、水处理解决方案部署案例。涵盖制造、海事、油气、政府项目 64+ 项。"),
    # ID pages
    (5378, "kontak",                  "Hubungi SURIOTA Batam — tim Industrial IoT, Modbus Gateway, SCADA & SaaS monitoring. Konsultasi, quotation, technical support. WhatsApp, email, alamat kantor."),
    (5379, "kebijakan-privasi",       "Kebijakan Privasi SURIOTA — cara kami mengumpulkan, menggunakan, menyimpan, dan melindungi data pribadi pengunjung suriota.com. Sesuai regulasi data Indonesia."),
    (5380, "syarat-layanan",          "Syarat & Ketentuan Layanan SURIOTA — ketentuan hukum penggunaan website, jasa konsultasi, penjualan produk & dukungan teknis untuk klien di Indonesia."),
    # EN pages
    (4983, "contact",                 "Contact SURIOTA Batam — Industrial IoT, Modbus Gateway, SCADA & SaaS monitoring team. Consultation, quotation, technical support. WhatsApp, email, office address."),
    (4985, "privacy-policy",          "SURIOTA Privacy Policy — how we collect, use, store, and protect personal data from visitors of suriota.com. Compliant with Indonesian data protection regulations."),
    (4987, "terms-of-service",        "SURIOTA Terms of Service — legal terms governing the use of suriota.com, consulting services, product sales, and technical support for Indonesia-based clients."),
    (5014, "sitemap",                 "SURIOTA Sitemap — full directory of all pages on suriota.com. Browse industrial IoT pillars, products, articles, portfolio, and corporate pages."),
]

ok = 0
fail = 0
for pid, slug, desc in descriptions:
    payload = {"id": pid, "description": desc}
    r = requests.post(AIOSEO, auth=AUTH, json=payload, timeout=30)
    status = "[+]" if r.status_code == 200 else "[!]"
    print(f"  {status} {r.status_code} id={pid:5d}  slug={slug:30s}  len={len(desc):3d}")
    if r.status_code == 200:
        ok += 1
    else:
        fail += 1
        print(f"       body: {r.text[:200]}")
print(f"\n=== Summary: {ok} OK, {fail} FAIL, total {len(descriptions)} ===")
