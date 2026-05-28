"""
Auto-translate EN/ID text nodes in HTML blocks using dictionary mapping.
Updates translations/extract.json in-place.
"""
import json, re
from bs4 import BeautifulSoup, NavigableString

# Load extract.json
with open('translations/extract.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Translation dictionary: original EN/ID phrase -> ZH translation
# Order matters: longer phrases first to avoid partial matches
DICT = {
    # CTAs & Headers
    "Free Consultation": "免费咨询",
    "Request Demo": "预约演示",
    "Get Started": "立即开始",
    "Book a 30-minute SURGE demo": "预约30分钟SURGE演示",
    "See SURGE Live": "观看SURGE实时演示",
    "Ready to start your Industrial IoT project?": "准备好开始您的工业物联网项目了吗？",
    "Ready to integrate your systems?": "准备好集成您的系统了吗？",
    "Ready to plan your digital roadmap?": "准备好规划您的数字路线图了吗？",
    "Ready to deploy industrial AI?": "准备好部署工业人工智能了吗？",
    "Ready to build your KPI cockpit?": "准备好构建您的KPI驾驶舱了吗？",
    "Related Portfolio Projects": "相关项目案例",
    "No obligation": "无义务",
    "Response within 24h": "24小时内响应",
    "Batam-based engineering team": "巴淡岛工程团队",

    # Section titles
    "Our IoT capabilities": "我们的物联网能力",
    "Our integration capabilities": "我们的集成能力",
    "Our consulting capabilities": "我们的咨询能力",
    "Our AI capabilities": "我们的人工智能能力",
    "Our analytics capabilities": "我们的数据分析能力",
    "What SURGE delivers": "SURGE 提供的功能",
    "Our IoT delivery workflow": "我们的物联网交付流程",
    "Our integration delivery workflow": "我们的集成交付流程",
    "Our consulting workflow": "我们的咨询流程",
    "Our AI delivery workflow": "我们的人工智能交付流程",
    "Our analytics workflow": "我们的数据分析工作流程",
    "SURGE onboarding workflow": "SURGE 上线流程",
    "Why choose SURIOTA": "为何选择 SURIOTA",
    "Built by engineers, for engineers": "由工程师打造，为工程师服务",
    "One unified data fabric across your stack": "跨技术栈的统一数据架构",
    "Integration without rip-and-replace": "无需推倒重来的集成",
    "Digital strategy that ships, by engineers who build": "由实战工程师打造的数字化战略",
    "AI that ships to production, not just demo": "可投产的人工智能，不只是演示",
    "From raw data to operational decisions": "从原始数据到运营决策",
    "SURGE - one platform, three industrial verticals": "SURGE - 一个平台，三大工业垂直领域",
    "Built for Indonesian industrial operations": "为印尼工业运营而生",

    # Workflow steps
    "Discovery": "需求调研",
    "Architecture": "架构设计",
    "Proof of Concept": "概念验证",
    "Roll-out": "全面部署",
    "Operate": "运营维护",
    "System inventory": "系统盘点",
    "Target architecture": "目标架构",
    "Build & test": "开发与测试",
    "Cutover": "切换上线",
    "Operate & evolve": "运营与优化",
    "Listen": "倾听",
    "Assess": "评估",
    "Ideate": "构思",
    "Plan": "规划",
    "Hand off (or build)": "移交（或承建）",
    "Use-case scoping": "用例范围界定",
    "Data audit": "数据审计",
    "Model development": "模型开发",
    "Deploy & integrate": "部署与集成",
    "Operate & retrain": "运营与再训练",
    "KPI definition": "KPI 定义",
    "Data plumbing": "数据管道",
    "Dashboard design": "仪表盘设计",
    "Train & launch": "培训与上线",
    "Iterate": "迭代优化",
    "Demo": "演示",
    "Trial": "试用",
    "Activate": "激活",
    "Scale": "扩展",
    "Optimise": "优化",

    # Feature titles
    "Quick to deploy": "快速部署",
    "Indonesia-hosted": "印尼本地托管",
    "Pay as you grow": "按需付费，随增长扩展",
    "White-label option": "白标选项",

    # Common phrases
    "We work across the stack": "我们覆盖全技术栈",
    "Advice from engineers who deliver": "来自实战工程师的建议",
    "ROI-first thinking": "ROI 优先思维",
    "Field-tested": "经过现场验证",
    "Vendor-neutral": "厂商中立",
    "Build-ready": "可立即实施",
    "Edge-capable,": "支持边缘部署，",
    "retrainable, and governed": "可再训练且受治理",
    "AI that lives beyond the demo": "超越演示的人工智能",
    "Production-ready": "生产就绪",
    "Edge-capable": "支持边缘部署",
    "ROI-grounded": "以 ROI 为基础",
    "Data sovereignty": "数据主权",
    "Dashboards people actually open": "人们真正会打开的仪表盘",
    "Operator-grade UX": "操作员级用户体验",
    "KPI to action": "KPI 到行动",
    "Unified data model": "统一数据模型",
    "Compliance-ready": "合规就绪",
    "Three flagship modules ship today:": "三大旗舰模块现已上线：",

    # Industry chips
    "Energy & Utilities": "能源与公用事业",
    "Water Treatment": "水处理",
    "Renewable Energy": "可再生能源",
    "Smart Building": "智能建筑",
    "Oil & Gas": "石油与天然气",
    "Power Generation": "发电",
    "Maritime": "海事",
    "Mining": "矿业",
    "FMCG": "快消品",
    "Logistics": "物流",
    "Construction": "建筑",
    "Smart City": "智慧城市",
    "Government": "政府",
    "Healthcare": "医疗健康",
    "Retail": "零售",
    "Finance": "金融",
    "Energy Companies": "能源公司",
    "Maritime & Logistics": "海事与物流",
    "Public Sector": "公共部门",

    # Stats labels
    "Deployments": "部署项目",
    "Protocols": "协议",
    "Security": "安全",
    "Multi-vendor": "多厂商",
    "Stack": "技术栈",
    "APIs": "接口",
    "Stacks": "技术栈",
    "SLA Uptime": "SLA 正常运行时间",
    "Multi-tenant": "多租户",
    "Architecture": "架构",
    "Indonesia": "印尼",
    "Hosted": "托管",

    # Misc
    "Industrial IoT, built for Indonesian production environments": "为印尼生产环境打造的工业物联网",
    "We work across": "我们覆盖",
    "The result: production KPIs, maintenance schedules, energy bills, and customer orders in one view.": "结果：生产KPI、维护计划、能源账单和客户订单一览无遗。",
    "Protocol-agnostic": "协议无关",
    "Phased delivery": "分阶段交付",
    "Start with high-value integrations; expand later. No big-bang risk, measurable wins at every stage.": "从高价值集成开始；后续扩展。无大爆炸风险，每个阶段都有可衡量的成果。",
    "Documented & owned": "文档化且自有",
    "SURIOTA guarantees secure, reliable, and observable telemetry.": "SURIOTA 确保遥测数据安全、可靠且可观测。",
    "IoT systems running in production across manufacturing, energy, maritime, and utilities since 2023.": "自2023年以来，物联网系统已在制造业、能源、海事和公用事业领域投入生产运行。",
    "From sensor selection to dashboard delivery - one accountable partner, no finger-pointing.": "从传感器选型到仪表盘交付 - 一个负责任的合作伙伴，无需推诿扯皮。",
    "TLS, certificate-based device auth, signed firmware, isolated network segments per IEC 62443.": "基于IEC 62443的TLS、证书设备认证、签名固件、隔离网络段。",
    "SNI, IEC, PUIL, KLHK compliance built-in. Local SLA, on-site team in Batam, Bahasa Indonesia support.": "内置SNI、IEC、PUIL、KLHK合规。本地SLA，巴淡岛现场团队，印尼语支持。",
    "Reference designs covering edge, network, security, and cloud layers. Sized for your scale and compliance needs.": "涵盖边缘、网络、安全和云层的参考设计。根据您的规模和合规需求量身定制。",
    "Gateway and PLC-edge deployments with local data preprocessing, store-and-forward, and offline resilience.": "网关和PLC边缘部署，具备本地数据预处理、存储转发和离线恢复能力。",
    "Fleet provisioning, OTA firmware updates, certificate rotation, telemetry observability across thousands of nodes.": "数千个节点的车队配置、OTA固件更新、证书轮换、遥测可观测性。",
    "Threat modelling, zero-trust device identity, network segmentation, security monitoring aligned to IEC 62443.": "威胁建模、零信任设备身份、网络分段、符合IEC 62443的安全监控。",
    "SURGE platform deployment or integration with AWS IoT, Azure IoT Hub, Google Cloud IoT with dashboards and alerts.": "SURGE平台部署或与AWS IoT、Azure IoT Hub、Google Cloud IoT集成，附带仪表盘和警报。",
    "Site walk, asset inventory, current data flows, business objectives.": "现场考察、资产盘点、当前数据流、业务目标。",
    "Solution design, BoM, security model, cost estimate.": "方案设计、物料清单、安全模型、成本估算。",
    "Pilot on a representative subset to validate assumptions before scale.": "在代表性子集上进行试点，在规模扩展前验证假设。",
    "Full deployment with commissioning, training, and runbook handover.": "全面部署，包含调试、培训和运行手册移交。",
    "SLA-backed support, observability, capacity planning, continuous improvement.": "SLA支持的可观测性、容量规划、持续改进。",
    "Catalogue current systems, data sources, owners, and integration pain points.": "盘点当前系统、数据源、负责人和集成痛点。",
    "Design the unified data model, integration patterns, security boundaries.": "设计统一数据模型、集成模式、安全边界。",
    "Implement adapters and APIs with automated test coverage and observability.": "实施适配器和API，具备自动化测试覆盖和可观测性。",
    "Phased go-live with rollback plan; parallel run before deprecating old paths.": "分阶段上线并附带回滚计划；在弃用旧路径前并行运行。",
    "SLA-backed support, schema versioning, continuous improvements.": "SLA支持、模式版本控制、持续改进。",
    "Interviews with leaders and operators - surface pain, ambition, constraints.": "与领导者和操作员访谈 - 发现痛点、抱负和约束。",
    "Current-state diagnostic across people, process, technology, data.": "针对人员、流程、技术、数据的现状诊断。",
    "Long-list of use cases; score by value, feasibility, urgency.": "用例长清单；按价值、可行性、紧迫性评分。",
    "Roadmap, budget, governance, KPIs. Defend it to your CFO.": "路线图、预算、治理、KPI。向您的CFO论证。",
    "Pick the highest-ROI AI use case grounded in data availability and operational constraints.": "选择基于数据可用性和运营约束的最高ROI人工智能用例。",
    "Inventory data sources, quality, labels, gaps. Define collection plan if data is thin.": "盘点数据源、质量、标签、差距。如果数据不足，定义收集计划。",
    "Baseline first, then iterate. Cross-validation, hyper-parameter search, fairness checks.": "先建立基线，再迭代。交叉验证、超参数搜索、公平性检查。",
    "Edge or cloud inference, API, dashboard, alerts, human-in-the-loop where appropriate.": "边缘或云端推理、API、仪表盘、警报、适当的人工介入。",
    "Drift monitoring, retraining triggers, A/B tests, governance, value reporting.": "漂移监控、再训练触发器、A/B测试、治理、价值报告。",
    "Co-create the metrics that matter, who owns each, what target counts as success.": "共创关键指标，明确负责人，定义成功目标。",
    "Connect sources, model the schema, build pipelines, test data quality.": "连接数据源、建模模式、构建管道、测试数据质量。",
    "Wireframe with users, iterate on real data, tune for fast load and clarity.": "与用户一起绘制线框图，基于真实数据迭代，优化加载速度和清晰度。",
    "Onboard operators and analysts; document drill paths and alert routes.": "培训操作员和分析师；记录钻取路径和警报路由。",
    "Monthly review of usage, retire dead metrics, add new use cases, evolve schema.": "月度审查使用情况，淘汰无效指标，添加新用例，演进模式。",
    "Tiered subscription based on assets, users, and modules. Annual commitment with discount.": "基于资产、用户和模块的分层订阅。年度承诺享折扣。",
    "Indonesian cloud regions (AWS Jakarta, Alibaba Indonesia, or private Indonesian data centre).": "印尼云区域（AWS雅加达、阿里云印尼或印尼私有数据中心）。",
    "Standard tier: 99.5% uptime. Enterprise: 99.95% with 1-hour incident response. Custom SLA available.": "标准版：99.5%正常运行时间。企业版：99.95%并附带1小时事件响应。可提供定制SLA。",
    "Yes. White-label tenancy with custom domain, brand colours, logo. Designed for system integrators and OEMs.": "是的。白标租户支持自定义域名、品牌色、Logo。专为系统集成商和OEM设计。",
    "Two options: self-managed Kubernetes cluster (we provide Helm charts), or managed hosting by SURIOTA.": "两种选择：自管Kubernetes集群（我们提供Helm图表），或由SURIOTA托管。",
    "Models ship with monitoring, drift detection, retraining pipelines, rollback. No black-box demos.": "模型附带监控、漂移检测、再训练管道、回滚。无黑盒演示。",
    "Every AI use case ships with measured baseline, target, and post-deployment value capture.": "每个人工智能用例都附带测量的基线、目标和部署后价值捕获。",
    "Train and run on your infrastructure if needed. Your data never leaves your control.": "如需可在您的基础设施上训练和运行。您的数据永远不会离开您的控制。",
    "You own the trained model and the data. We license MLOps tooling. On termination, full export.": "您拥有训练好的模型和数据。我们授权MLOps工具。终止时，完整导出。",
    "Pre-deployment baseline, success criteria signed off before launch, then quarterly business reviews.": "部署前基线、启动前签署的成功标准，然后季度业务回顾。",
    "We use task-specific models (not general-purpose LLMs) for industrial use cases, with validation and human-in-the-loop.": "我们对工业用例使用任务专用模型（非通用LLM），并进行验证和人工介入。",
    "Specific. Named technologies, sized infrastructure, named teams, dated milestones, budget line items.": "具体的。指定技术、规模化的基础设施、指定团队、 dated里程碑、预算明细。",
    "Yes. We present the business case ourselves, including sensitivity analysis, to your board or investment committee.": "是的。我们亲自向您的董事会或投资委员会展示商业案例，包括敏感性分析。",
    "Yes. Standard NDAs are signed before any data or strategic discussion.": "是的。在任何数据或战略讨论前签署标准保密协议。",
    "Specific. Named technologies, sized infrastructure, named teams, dated milestones, budget line items.": "具体的。指定技术、规模化的基础设施、指定团队、 dated里程碑、预算明细。",
    "Reconciliation jobs, schema validation, dead-letter queues, and observability dashboards catch issues before they propagate.": "对账作业、模式验证、死信队列和可观测性仪表板在问题传播前捕获它们。",
    "Yes. Our integration architects have connected in-house systems built on Java, .NET, Python, PHP, and Go.": "是的。我们的集成架构师已连接基于Java、.NET、Python、PHP和Go构建的内部系统。",
    "We design parallel-run architectures. Old and new systems run side-by-side until you are confident to cut over.": "我们设计并行运行架构。新旧系统并排运行，直到您有信心切换。",
    "Yes. IAM, SSO, MFA, RBAC, and API gateway policies are part of every integration we deliver.": "是的。IAM、SSO、MFA、RBAC和API网关策略是我们交付的每个集成的组成部分。",
    "Both. Real-time for operational dashboards and alerts; batch for regulatory reporting and BI.": "两者都有。实时用于运营仪表盘和警报；批处理用于监管报告和商业智能。",
    "Bridge SCADA historians (OSIsoft PI, Wonderware, Ignition) to cloud, BI tools, and ERP.": "将SCADA历史数据库（OSIsoft PI、Wonderware、Ignition）桥接到云端、BI工具和ERP。",
    "Connect plant-floor data to SAP, Oracle, Microsoft Dynamics. Production orders in, actuals out.": "将车间数据连接到SAP、Oracle、Microsoft Dynamics。生产订单进，实际产出出。",
    "Secure DMZ design, identity federation, network segmentation between IT and OT zones.": "安全DMZ设计、身份联合、IT和OT区域之间的网络分段。",
    "Wrap legacy systems behind modern APIs. No need to rebuild a 20-year-old asset register.": "将遗留系统封装在现代API后面。无需重建已有20年历史的资产登记册。",
    "Custom REST and GraphQL APIs, gateway management, rate limiting, OAuth2 / OIDC auth.": "自定义REST和GraphQL API、网关管理、速率限制、OAuth2/OIDC认证。",
    "ETL/ELT pipelines (Kafka, Airflow, dbt), data quality checks, master data management.": "ETL/ELT管道（Kafka、Airflow、dbt）、数据质量检查、主数据管理。",
    "No vendor lock-in. We work with Siemens, Schneider, Rockwell, SAP, Oracle, Microsoft, and open-source stacks.": "无厂商锁定。我们与Siemens、Schneider、Rockwell、SAP、Oracle、Microsoft和开源技术栈合作。",
    "Define digital ambition, target operating model, and the use-case portfolio aligned to business strategy.": "定义数字化雄心、目标运营模式、与业务战略对齐的用例组合。",
    "Maturity diagnostic across data, automation, analytics, organisation, and culture.": "针对数据、自动化、分析、组织和文化的成熟度诊断。",
    "3-year phased roadmap with budget, vendor shortlist, risk register, and success metrics.": "三年分阶段路线图，包含预算、厂商候选名单、风险登记册和成功指标。",
    "Quantified business cases per use case: investment, payback, NPV, sensitivity analysis.": "每个用例的量化商业案例：投资、回报、NPV、敏感性分析。",
    "KLHK, SNI, IEC, PUIL, OJK fintech, BSSN cybersecurity - mapping requirements to implementation.": "KLHK、SNI、IEC、PUIL、OJK金融科技、BSSN网络安全 - 将需求映射到实施。",
    "Operator training plans, governance structures, communication, KPIs that drive adoption.": "操作员培训计划、治理结构、沟通、推动采用的KPI。",
    "Metabase, Grafana, Apache Superset, Power BI, Tableau, Looker. We pick based on your constraints and team skills.": "Metabase、Grafana、Apache Superset、Power BI、Tableau、Looker。我们根据您的约束和团队技能进行选择。",
    "Yes - our SURGE-Water Analytics module is built for this. Real-time effluent monitoring with KLHK-compliant auto-reporting.": "是的 - 我们的SURGE-Water Analytics模块专为这个打造。实时废水监控，符合KLHK的自动报告。",
    "Your choice: on-prem, AWS, Azure, GCP, or our private cloud in Indonesia. Time-series optimised.": "您的选择：本地、AWS、Azure、GCP或我们在印尼的私有云。针对时序优化。",
    "Pilot dashboards in 2-4 weeks. Full production roll-out in 6-12 weeks depending on data source complexity.": "试点仪表盘2-4周。全面生产部署6-12周，取决于数据源复杂度。",
    "Encryption in transit and at rest, RBAC, audit logs, single sign-on, GDPR/UU PDP compliance.": "传输和静态加密、RBAC、审计日志、单点登录、GDPR/UU PDP合规。",
    "Pilot deployments: 4-6 weeks. Full enterprise roll-outs: 3-9 months depending on scale and integration complexity.": "试点部署：4-6周。企业全面部署：3-9个月，取决于规模和集成复杂度。",
    "是。我们的 Modbus Gateway 系列将传统自动化(Modbus RTU/TCP)桥接到现代 IoT(MQTT)。我们支持 OPC UA、BACnet 和自定义协议。": "是。我们的 Modbus Gateway 系列将传统自动化（Modbus RTU/TCP）桥接到现代 IoT（MQTT）。我们支持 OPC UA、BACnet 和自定义协议。",
    "两种选项都可以。我们可以部署 SURGE 平台,或使用您现有的基础设施在 AWS、Azure 或 GCP 上构建。": "两种选项都可以。我们可以部署 SURGE 平台，或使用您现有的基础设施在 AWS、Azure 或 GCP 上构建。",
    "Per IEC 62443 - device-level certificates, mutual TLS, signed firmware, role-based access control, and network segmentation.": "依据 IEC 62443 - 设备级证书、双向TLS、签名固件、基于角色的访问控制和网络分段。",
    "SLA-backed tiers from break-fix to 24/7 monitoring including firmware updates, telemetry health checks, and incident response.": "从故障修复到24/7监控的SLA支持层级，包括固件更新、遥测健康检查和事件响应。",
    "SURIOTA builds analytics platforms that combine real-time plant data with business intelligence for operational decisions.": "SURIOTA 构建分析平台，将实时工厂数据与商业智能相结合，用于运营决策。",
    "We work across the stack: ETL/ELT pipelines, time-series databases, BI tools (Metabase, Grafana, Power BI), and regulatory reporting.": "我们覆盖全技术栈：ETL/ELT管道、时序数据库、BI工具（Metabase、Grafana、Power BI）和监管报告。",
    "Operator-grade UX, KPI-to-action mapping, audit-traceable exports.": "操作员级用户体验、KPI到行动映射、审计可追溯导出。",
    "Designed for plant operators, not just executives. Glanceable, alarmable, drillable.": "为工厂操作员设计，不仅仅是高管。一目了然、可报警、可钻取。",
    "Every metric ties to an action: who is alerted, what runbook applies, expected SLA.": "每个指标都关联一个行动：谁被警报、适用什么运行手册、预期SLA。",
    "Single canonical schema across plant, ERP, CRM - no contradictory numbers in different dashboards.": "跨工厂、ERP、CRM的单一规范模式 - 不同仪表盘中没有矛盾数字。",
    "KLHK SPARING, KEMENPERIN, OJK formats built-in. Audit logs, signed exports, retention policies.": "内置KLHK SPARING、KEMENPERIN、OJK格式。审计日志、签名导出、保留策略。",
    "Operational dashboards on Grafana, Metabase, Power BI. Sub-second refresh for time-critical processes.": "Grafana、Metabase、Power BI上的运营仪表盘。关键流程的亚秒级刷新。",
    "OEE, MTBF, MTTR, energy intensity, water quality, asset utilisation - with targets, trends, and alerts.": "OEE、MTBF、MTTR、能源强度、水质、资产利用率 - 附带目标、趋势和警报。",
    "KLHK SPARING (water effluent), KEMENPERIN, BPS, OJK, BSSN. Auto-generated, audit-traceable, scheduleable.": "KLHK SPARING（废水）、KEMENPERIN、BPS、OJK、BSSN。自动生成、审计可追溯、可定时。",
    "Forecasting, what-if simulation, root-cause analysis on operational and business data.": "对运营和业务数据进行预测、假设模拟、根因分析。",
    "Pipelines (Kafka, Airflow, dbt), data quality, schema evolution, time-series databases (TimescaleDB, InfluxDB).": "管道（Kafka、Airflow、dbt）、数据质量、模式演进、时序数据库（TimescaleDB、InfluxDB）。",
    "Self-service BI for analysts, semantic layer, governed access, scheduled distribution.": "分析师自助BI、语义层、受治理的访问、定时分发。",
    "Real-time energy monitoring across buildings, plants, feeders. Demand response, tariff optimisation, power-factor correction.": "跨建筑、工厂、馈线的实时能源监控。需求响应、电价优化、功率因数校正。",
    "Maritime fleet visibility - AIS, GPS, fuel, engine telemetry. Route optimisation, ETA prediction, regulatory reporting.": "海事船队可视化 - AIS、GPS、燃油、发动机遥测。航线优化、ETA预测、监管报告。",
    "PDAM & WTP monitoring. KLHK SPARING automated reporting. Leak detection, demand forecasting, tariff modelling.": "PDAM和WTP监控。KLHK SPARING自动报告。泄漏检测、需求预测、电价建模。",
    "Build your domain-specific SaaS on the SURGE platform. We handle multi-tenant, auth, billing, and scaling.": "在SURGE平台上构建您的领域专属SaaS。我们处理多租户、认证、计费和扩展。",
    "REST & GraphQL APIs, webhooks, MQTT ingestion, file imports. Open ecosystem.": "REST和GraphQL API、Webhook、MQTT接入、文件导入。开放生态。",
    "Re-brand SURGE for your customers. Dedicated tenants, custom domains, isolated backups.": "为您的客户重新品牌SURGE。专属租户、自定义域名、隔离备份。",
    "Tiered subscription signed; production tenant provisioned with SLA.": "签署分层订阅；生产租户附带SLA配置。",
    "Onboard more sites/users; configure custom dashboards, integrations, reports.": "接入更多站点/用户；配置自定义仪表盘、集成、报告。",
    "Quarterly reviews, new modules, feature requests, success metrics.": "季度回顾、新模块、功能需求、成功指标。",

    # SaaS specific
    "Data residency in Indonesia. UU PDP compliant. Latency optimised for SE Asia.": "数据驻留印尼。符合UU PDP。针对东南亚优化延迟。",
    "Tiered subscription - start with one site or 100 assets, scale to thousands without re-architecture.": "分层订阅 - 从一个站点或100个资产开始，无需重构即可扩展到数千个。",

    # Small page headings
    "Industrial 物联网": "工业物联网",
    "Industrial IoT & system integration - Modbus RTU/TCP to MQTT gateways, edge computing, AWS IoT Core & SURGE cloud dashboards for manufacturing, oil & gas, shipyard, water utilities & renewable energy across Indonesia.": "工业物联网与系统集成 - Modbus RTU/TCP 到 MQTT 网关、边缘计算、AWS IoT Core 和 SURGE 云端仪表盘，服务于印尼的制造业、石油天然气、船厂、水务公用事业和可再生能源。",
    "系统集成": "系统集成",
    "Bridge SCADA, ERP, MES, and IoT into a single source of truth. SURIOTA connects legacy and modern systems so your data flows without silos.": "将SCADA、ERP、MES和物联网整合为单一可信数据源。SURIOTA连接遗留和现代系统，让您的数据流动无孤岛。",
    "数字化咨询": "数字化咨询",
    "Digital transformation consulting - 工业 4.0 路线图, OT/IT convergence, IIoT 准备度审计, SCADA modernisation & cloud migration strategy 专为印尼制造业打造, energy & maritime operators.": "数字化转型咨询 - 工业4.0路线图、OT/IT融合、IIoT就绪度审计、SCADA现代化和云迁移策略，专为印尼制造业、能源和海事运营商打造。",
    "人工智能": "人工智能",
    "Production-grade AI for industrial use cases. Predictive maintenance, computer vision QC, anomaly detection — built on your data, deployed on your terms.": "工业级人工智能应用。预测性维护、计算机视觉质检、异常检测 - 基于您的数据，按您的条件部署。",
    "数据分析": "数据分析",
    "AI & industrial data analytics - predictive maintenance, OEE, energy optimisation, KPI dashboards & computer vision QC for manufacturing, oil & gas, mining, water utilities & logistics across Indonesia.": "AI与工业数据分析 - 预测性维护、OEE、能源优化、KPI仪表盘和计算机视觉质检，服务于印尼的制造业、石油天然气、矿业、水务公用事业和物流。",
    "软件即服务": "软件即服务",
    "SURGE SaaS platform - multi-tenant industrial IoT monitoring for energy (kWh, power factor), water (KLHK SPARING, pH/COD/TSS/NH3) & vessel tracking. 70% cheaper than ThingsBoard, made in Indonesia.": "SURGE SaaS平台 - 多租户工业物联网监控，覆盖能源（kWh、功率因数）、水务（KLHK SPARING、pH/COD/TSS/NH3）和船舶追踪。比ThingsBoard便宜70%，印尼制造。",

    # About page
    "新一代工业合作伙伴 | Industrial IoT & System Integration in Batam, Indonesia": "新一代工业合作伙伴 | 印尼巴淡岛工业物联网与系统集成",
    "Transforming Indonesia's industries through smart, connected end-to-end IoT, AI, and SaaS solutions.": "通过智能互联的端到端物联网、人工智能和SaaS解决方案，变革印尼工业。",
    "End-to-end solutions connecting hardware, software & cloud.": "连接硬件、软件和云端的端到端解决方案。",
    "Real-time monitoring & data-driven decisions to reduce downtime.": "实时监控和数据驱动决策，减少停机时间。",
    "Cross-sector partnerships: manufacturing, energy, logistics, maritime.": "跨行业合作伙伴关系：制造业、能源、物流、海事。",
    "Continuous expertise in IoT, AI, and emerging technologies.": "在物联网、人工智能和新兴技术方面的持续专业能力。",
    "Highest standards of integrity & professionalism.": "最高的诚信和专业标准。",
    "SURIOTA | 工业物联网与系统集成": "SURIOTA | 工业物联网与系统集成",
    "PT Surya Inovasi Prioritas (SURIOTA) is a technology company specializing in Industrial IoT Services and System Integration, 总部位于廖内群岛巴淡岛中心. Since January 2023,我们一直在设计和制造工业连接解决方案。从 Modbus 网关到完整的物联网平台。": "PT Surya Inovasi Prioritas (SURIOTA) 是一家专注于工业物联网服务和系统集成的科技公司，总部位于廖内群岛巴淡岛中心。自2023年1月以来，我们一直在设计和制造工业连接解决方案。从Modbus网关到完整的物联网平台。",
    "64+ 个工业项目 across manufacturing, energy, logistics, and maritime sectors. In-house products: SURGE IIoT platform (Energy Mapping, Water Analytic, Vessel Tracking), SRT-MGATE-1210 gateway, RS-485 SPD, ISO-M485, THM-30MD, PM1611-WD.": "64+个工业项目，涵盖制造业、能源、物流和海事领域。自研产品：SURGE IIoT平台（能源图谱、水质分析、船舶追踪）、SRT-MGATE-1210网关、RS-485 SPD、ISO-M485、THM-30MD、PM1611-WD。",
    "Independent · Self-funded · Integrity & Technical Excellence": "独立运营 · 自筹资金 · 诚信与技术卓越",
    "坚定的成果": "坚定的成果",
    "始终专注于最佳结果与既定目标。": "始终专注于最佳结果与既定目标。",
    "诚信创新": "诚信创新",
    "以诚信、伦理与责任进行创新。": "以诚信、伦理与责任进行创新。",
    "精准执行": "精准执行",
    "精准、纪律与高质量标准。": "精准、纪律与高质量标准。",
    "通过可靠建立信任": "通过可靠建立信任",
    "始终如一、可靠与承诺。": "始终如一、可靠与承诺。",
    "适应性成长": "适应性成长",
    "拥抱变化与持续改进。": "拥抱变化与持续改进。",
    "准备好与 SURIOTA 合作了吗？": "准备好与 SURIOTA 合作了吗？",
    "Discuss your engineering needs with the SURIOTA team. Response within 1 business day.": "与SURIOTA团队讨论您的工程需求。1个工作日内回复。",
    "下载 Company Profile": "下载公司介绍",
    "Chat via WhatsApp": "WhatsApp 咨询",
    "Free 咨询": "免费咨询",

    # Service page common
    "凭借 SURIOTA 自动化解决方案提升效率与生产力": "凭借 SURIOTA 自动化解决方案提升效率与生产力",
    "借助 SURIOTA 的工业电气系统优化您的业务": "借助 SURIOTA 的工业电气系统优化您的业务",
    "携手 SURIOTA 可再生能源方案，迈向更绿色的未来": "携手 SURIOTA 可再生能源方案，迈向更绿色的未来",
    "携手 SURIOTA 的纯净水处理方案，迈向可持续的未来": "携手 SURIOTA 的纯净水处理方案，迈向可持续的未来",
    "PLC、SCADA 与 IIoT 集成,基于 Modbus 网关,服务工业 4.0. 厂商中立的自动化方案,覆盖制造业、石油天然气、船厂、能源与公用事业": "PLC、SCADA 与 IIoT 集成，基于 Modbus 网关，服务工业 4.0。厂商中立的自动化方案，覆盖制造业、石油天然气、船厂、能源与公用事业。",
    "依据 SNI、IEC 与 PUIL 2011 进行配电盘安装、电力分配与调试。为印尼各地的石油天然气、船厂、制造业及商业建筑提供电气工程服务。": "依据 SNI、IEC 与 PUIL 2011 进行配电盘安装、电力分配与调试。为印尼各地的石油天然气、船厂、制造业及商业建筑提供电气工程服务。",
    "太阳能光伏 PLTS、PLTS-PLTB 混合系统与智能路灯(PJU),集成物联网能源监控. Feasibility study, design & installation for industries & commercial buildings across Indonesia": "太阳能光伏 PLTS、PLTS-PLTB 混合系统与智能路灯（PJU），集成物联网能源监控。为印尼各地的工业和商业建筑提供可行性研究、设计与安装。",
    "面向工业、PDAM 与供水公用事业，提供符合 KLHK SPARING 合规要求的 WTP、WWTP 与 IPAL 设计、安装及维护": "面向工业、PDAM 与供水公用事业，提供符合 KLHK SPARING 合规要求的 WTP、WWTP 与 IPAL 设计、安装及维护。",
    "免费咨询 →": "免费咨询 →",
    "我们服务的行业": "我们服务的行业",
    "为何选择 SURIOTA": "为何选择 SURIOTA",
    "我们的服务": "我们的服务",
    "常见问题": "常见问题",
    "下一步流程": "下一步流程",
    "From message to engagement — in 4 steps": "从留言到合作——仅需4步",

    # Contact page
    "联系方式": "联系方式",
    "联系 SURIOTA": "联系 SURIOTA",
    "与我们的工程师讨论工业物联网、系统集成或定制项目。工作日 24 小时内回复。": "与我们的工程师讨论工业物联网、系统集成或定制项目。工作日24小时内回复。",
    "发送消息": "发送消息",
    "姓名": "姓名",
    "邮箱": "邮箱",
    "电话": "电话",
    "项目类型": "项目类型",
    "留言内容": "留言内容",
    "发送": "发送",
    "办公地址": "办公地址",
    "印度尼西亚廖内群岛巴淡市中心 Jl. Legenda Malaka, Baloi Permai": "印度尼西亚廖内群岛巴淡市中心 Jl. Legenda Malaka, Baloi Permai",
    "工作时间": "工作时间",
    "周一至周五 09:00 – 18:00 WIB": "周一至周五 09:00 – 18:00 WIB",
    "周六 09:00 – 13:00 WIB": "周六 09:00 – 13:00 WIB",
    "联系电话": "联系电话",
    "WhatsApp": "WhatsApp",
    "电子邮箱": "电子邮箱",
    "社交媒体": "社交媒体",
    "步骤 01": "步骤 01",
    "步骤 02": "步骤 02",
    "步骤 03": "步骤 03",
    "步骤 04": "步骤 04",
    "咨询提交": "咨询提交",
    "需求评估": "需求评估",
    "方案设计": "方案设计",
    "项目启动": "项目启动",

    # Legal pages
    "法律信息": "法律信息",
    "隐私政策": "隐私政策",
    "服务条款": "服务条款",
    "PT Surya Inovasi Prioritas (SURIOTA) 如何收集、使用和保护您的个人数据。 This policy is aligned with Indonesia's Personal Data Protection Law (UU PDP No.27/2022) and the EU General Data Protection Regulation (GDPR).": "PT Surya Inovasi Prioritas (SURIOTA) 如何收集、使用和保护您的个人数据。本政策符合印度尼西亚《个人数据保护法》（UU PDP No.27/2022）和欧盟《通用数据保护条例》（GDPR）。",
    "The agreement that governs your use of the SURIOTA website, our products (SURGE platform, SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 Surge Protector), and our engineering services. Please read carefully.": "管辖您使用SURIOTA网站、我们的产品（SURGE平台、SRT-MGATE-1210、ISO-M485、THM-30MD、PM1611-WD、RS-485浪涌保护器）以及我们工程服务的协议。请仔细阅读。",
    "生效日期:": "生效日期：",
    "最后更新:": "最后更新：",
    "版本:": "版本：",
    "本页目录": "本页目录",
    "概述": "概述",
    "数据控制方": "数据控制方",
    "我们收集的信息": "我们收集的信息",
    "我们如何使用信息": "我们如何使用信息",
    "法律依据 (GDPR)": "法律依据 (GDPR)",
    "共享与披露": "共享与披露",
    "Cookies 与追踪": "Cookies 与追踪",
    "数据保留": "数据保留",
    "安全": "安全",
    "International Transfers": "国际传输",
    "您的权利": "您的权利",
    "Children's Privacy": "儿童隐私",
    "政策变更": "政策变更",
    "联系我们": "联系我们",
    "接受条款": "接受条款",
    "一般条款": "一般条款",
    "服务范围": "服务范围",
    "付款条款": "付款条款",
    "知识产权": "知识产权",
    "责任限制": "责任限制",
    "保密义务": "保密义务",
    "终止条款": "终止条款",
    "争议解决": "争议解决",
    "适用法律": "适用法律",

    # Portfolio page
    "项目案例": "项目案例",
    "项目档案": "项目档案",
    "Deployments": "部署项目",
    "年": "年",
    "Clients": "客户",
    "Services": "服务",
    "No Client Listed": "未列出客户",
    "View Details": "查看详情",
    "All Years": "所有年份",

    # Product pages
    "SURIOTA 模块 – Modbus 网关 IIoT": "SURIOTA 模块 – Modbus 网关 IIoT",
    "工业物联网": "工业物联网",
    "RS-485 隔离模块": "RS-485 隔离模块",
    "可靠的 RS-485 通信,加固隔离与浪涌保护": "可靠的 RS-485 通信，加固隔离与浪涌保护",
    "当您的运营依赖快速、稳定和安全的数据通信时,您无法承受停机或干扰。ISO-M485 系列专为工业级 RS-485 网络设计,提供高达 5kV 的光电隔离和强大的浪涌保护,确保在最严苛的环境中也能实现最高可靠性。": "当您的运营依赖快速、稳定和安全的数据通信时，您无法承受停机或干扰。ISO-M485 系列专为工业级 RS-485 网络设计，提供高达 5kV 的光电隔离和强大的浪涌保护，确保在最严苛的环境中也能实现最高可靠性。",
    "应用场景": "应用场景",
    "规格参数": "规格参数",
    "订购信息": "订购信息",
    "技术文档": "技术文档",
    "Elevate Your Industrial Connectivity with Suriota Modbus 网关": "使用 Suriota Modbus 网关提升您的工业连接能力",
    "Seamless Integration Between Automation Systems and Modern IoT Ecosystems": "自动化系统与现代物联网生态系统之间的无缝集成",

    # Second-pass fixes and remaining phrases
    "Related 案例 Projects": "相关项目案例",
    "印尼n National Standard": "印尼国家标准",
    "General 电气工程 Installation Requirements": "通用电气工程安装要求",
    "水处理 规划t": "水处理厂",
    "Waste 水处理 规划t": "污水处理厂",
    "维护服务 frequency depends on capacity and raw water conditions. Typically, routine inspections occur monthly, medium servicing every 3-6 months, and annual overhauls to ensure optimal performance.": "维护服务频率取决于处理能力和原水水质。通常，例行检查每月一次，中度保养每3-6个月一次，年度大修以确保最佳性能。",
    "Yes, SURGE is built with open 接口 that enable integration with ERP, SCADA 监控, or existing management software running in your facility.": "是的，SURGE 采用开放式接口，支持与 ERP、SCADA 监控或现有管理软件集成。",
    "Yes, SURIOTA serves engineering projects throughout the Riau Islands region and can discuss projects in other locations across 印尼. 联系 our team for free initial consultation.": "是的，SURIOTA 为廖内群岛地区提供工程服务，也可讨论印尼其他地区的项目。请联系我们的团队进行免费初步咨询。",
    "Yes, every PLTS system SURIOTA installs is equipped with IoT monitoring via the SURGE 能源 Mapping platform. You can monitor energy production, panel performance, and consumption in real-time through a web dashboard.": "是的，SURIOTA 安装的每个 PLTS 系统都配备通过 SURGE 能源 Mapping 平台的物联网监控。您可以通过 Web 仪表盘实时监控发电量、面板性能和消耗量。",
    "WTP (水处理 规划t) processes raw water into clean water for consumption or industrial use. WWTP (Waste 水处理 规划t) treats wastewater before environmental discharge, ensuring parameters meet regulatory standards.": "WTP（水处理厂）将原水净化为饮用水或工业用水。WWTP（污水处理厂）在环境排放前处理废水，确保参数符合监管标准。",
    "SURIOTA uses SNI (印尼国家标准), IEC (国际电工委员会), and PUIL (通用电气工程安装要求) standards for all electrical installation, panel assembly, and commissioning work.": "SURIOTA 对所有电气安装、配电盘组装和调试工作均采用 SNI（印尼国家标准）、IEC（国际电工委员会）和 PUIL（通用电气工程安装要求）标准。",
    "Transforming 印尼's industries through smart, connected end-to-end IoT, AI, and SaaS solutions.": "通过智能互联的端到端物联网、人工智能和SaaS解决方案，变革印尼工业。",
    "is a technology company specializing in Industrial IoT 服务 and System Integration": "是一家专注于工业物联网服务和系统集成的科技公司",
    "SURIOTA's team designs and implements automation systems from small to large scale using Siemens S7, Omron, Schneider, and IEC 61131-3 compliant microcontrollers.": "SURIOTA 团队使用西门子 S7、欧姆龙、施耐德和符合 IEC 61131-3 标准的微控制器，设计并实施从小型到大型的自动化系统。",
    "We integrate Siemens, Schneider, Mitsubishi, Omron, Allen-Bradley。": "我们集成西门子、施耐德、三菱、欧姆龙、罗克韦尔（Allen-Bradley）。",
    "Native integration with our SURGE platform. Energy mapping, vessel tracking, water analytics. No third-party gateway lock-in.": "与我们 SURGE 平台的原生集成。能源图谱、船舶追踪、水质分析。无第三方网关锁定。",
    "In-house SRT-MGATE-1210 Modbus Gateway bridges legacy RTU/TCP devices to modern MQTT/OPC UA cloud telemetry.": "自研 SRT-MGATE-1210 Modbus 网关将传统 RTU/TCP 设备桥接到现代 MQTT/OPC UA 云端遥测。",
    "Feasibility → design → wiring → PLC code → HMI/SCADA → commissioning → operator training. One accountable partner, one contract.": "可行性研究 → 设计 → 布线 → PLC 编程 → HMI/SCADA → 调试 → 操作员培训。一个负责任的合作伙伴，一份合同。",
    "OT/IT network segregation, firewall zones, role-based HMI access, and encrypted telemetry per IEC 62443. Reduce attack surface from day one.": "依据 IEC 62443 的 OT/IT 网络隔离、防火墙区域、基于角色的 HMI 访问和加密遥测。从第一天起减少攻击面。",
    "12-month warranty, indexed spare parts, annual SCADA backup, and remote diagnostics. We stay engaged long after go-live.": "12 个月质保、备件索引、年度 SCADA 备份和远程诊断。我们在上线后仍持续提供支持。",
    "SURGE 能源 Mapping – Monitoring HVAC": "SURGE 能源图谱 – HVAC 监控",
    "SURGE 能源 Mapping – Monitoring Panel Surya": "SURGE 能源图谱 – 太阳能面板监控",
    "SRT-MGATE-1210 Gateway – Integrasi Modbus ke MQTT": "SRT-MGATE-1210 网关 – Modbus 到 MQTT 集成",
    "SRT-MGATE-1210 Gateway – IIoT Water Quality Monitoring": "SRT-MGATE-1210 网关 – IIoT 水质监控",
    "WS 电气工程 Installation – PT Multi Mitra Guna": "WS 电气工程安装 – PT Multi Mitra Guna",
    "Hybrid PJU Menggunakan PLTS dan PLTB Berbasis IoT": "基于物联网的 PLTS 和 PLTB 混合智能路灯",
    "Water Quality Monitoring SPARING – PT Satya Samudera Abadi": "水质监控 SPARING – PT Satya Samudera Abadi",
    "IoT Monitoring Panel Surya – PT Mitra Multi Guna": "物联网太阳能面板监控 – PT Mitra Multi Guna",

    # Portfolio links
    "Modbus 网关 IIoT – Integrasi Sensor Water Quality": "Modbus 网关 IIoT – 传感器水质集成",
    "Control & Monitoring ATS Panel Surya Berbasis IoT": "基于物联网的太阳能ATS控制与监控面板",
    "Modul Absensi IoT – PT Sandifox": "物联网考勤模块 – PT Sandifox",
    "WS 电气工程 Installation – PT Sentra Gapura Inovasi": "WS 电气工程安装 – PT Sentra Gapura Inovasi",
    "电气工程 Wiring & Commissioning": "电气工程接线与调试",
    "SURGE 能源 Mapping – Monitoring & Management HVAC": "SURGE 能源图谱 – HVAC监控与管理",
    "SURGE 能源 Mapping – Monitoring Panel Surya": "SURGE 能源图谱 – 太阳能面板监控",

    # aria-labels
    "Order SRT-MGATE-1210 on Tokopedia": "在 Tokopedia 订购 SRT-MGATE-1210",
    "Order ISO-M485 on Tokopedia": "在 Tokopedia 订购 ISO-M485",
    "Chat SURIOTA via WhatsApp": "通过 WhatsApp 咨询 SURIOTA",
    "Free consultation via form": "通过表单免费咨询",
    "Chat on WhatsApp": "通过 WhatsApp 咨询",
    "Breadcrumb": "面包屑导航",
    "Table of contents": "目录",
    "IoT network illustration": "物联网网络示意图",
    "System integration illustration": "系统集成示意图",
    "Strategy roadmap illustration": "战略路线图示意图",
    "Neural network illustration": "神经网络示意图",
    "Analytics dashboard illustration": "分析仪表盘示意图",
    "SaaS cloud platform illustration": "SaaS 云平台示意图",

    # Breadcrumbs
    "Automation": "自动化",
    "Electrical": "电气工程",
    "Renewable Energy": "可再生能源",
    "Water Treatment": "水处理",
    "Contact Us": "联系我们",
    "About Us": "关于我们",
    "Portfolio": "项目案例",
    "Modbus Gateway": "Modbus 网关",

    # Product page - Modbus Gateway 5456
    "Why engineers choose SRT-MGATE-1210": "工程师选择 SRT-MGATE-1210 的理由",
    "Multi-Protocol Bridge": "多协议桥接",
    "Modbus RTU (RS-485) ↔ Modbus TCP/IP ↔ MQTT ↔ HTTP/REST": "Modbus RTU（RS-485）↔ Modbus TCP/IP ↔ MQTT ↔ HTTP/REST",
    ". No-code register mapping, JSON/custom topic output.": "。无需代码的寄存器映射，JSON/自定义主题输出。",
    "Dual Network Failover": "双网络故障切换",
    "WiFi 2.4 GHz (802.11 b/g/n) + Ethernet 10/100 with": "WiFi 2.4 GHz（802.11 b/g/n）+ 以太网 10/100，具备",
    "auto-failover": "自动故障切换",
    ". Optional PoE (IEEE 802.3af/at) on select versions.": "。特定版本可选 PoE（IEEE 802.3af/at）。",
    "Industrial-Grade Hardware": "工业级硬件",
    "operating range, 2kV isolation on RS-485, dual 12-48VDC redundant inputs. Built for harsh environmen": "工作范围，RS-485 具备 2kV 隔离，双 12-48VDC 冗余输入。为恶劣环境而生",
    "Mobile BLE Configuration": "移动蓝牙配置",
    "Configure via": "通过",
    "Suriota Config app": "Suriota Config 应用",
    "(Android/iOS) over BLE 5.0, up to 50m range. No PC, no cables, no Telnet required.": "（安卓/iOS）通过 BLE 5.0 配置，最远 50 米范围。无需电脑、线缆或 Telnet。",
    "Cloud-Agnostic Integration": "云无关集成",
    "AWS IoT, Azure IoT Hub, Google Cloud, ThingsBoard": "AWS IoT、Azure IoT Hub、Google Cloud、ThingsBoard",
    ", and on-premises MQTT brokers. No vendor lock-in.": "和本地 MQTT 代理。无厂商锁定。",
    "Secure Local Data Logging": "安全本地数据记录",
    "MicroSD slot for": "MicroSD 卡槽用于",
    "CSV/JSON local logging": "CSV/JSON 本地日志记录",
    "during outages. TLS/SSL encryption and firewall rules ensure end-to-end security.": "在断网期间。TLS/SSL 加密和防火墙规则确保端到端安全。",
    "Order on Tokopedia": "在 Tokopedia 订购",
    "Download Datasheet": "下载数据手册",
    "WiFi 2.4 GHz (802.11 b/g/n), Bluetooth 5.0 (BLE) up to 50m LOS": "WiFi 2.4 GHz（802.11 b/g/n），蓝牙 5.0（BLE）最远 50 米视距",
    "2× Isolated RS-485 (up to 32 devices per port), 1× RJ45 Ethernet 10/100 Mbps": "2× 隔离 RS-485（每端口最多 32 台设备），1× RJ45 以太网 10/100 Mbps",
    "Dual DC 12-48VDC inputs for redundancy, PoE (IEEE 802.3af/at) option on specific versions": "双路 DC 12-48VDC 冗余输入，特定版本可选 PoE（IEEE 802.3af/at）",
    "MQTT (ISO/IEC 20922), HTTP/HTTPS, REST API": "MQTT（ISO/IEC 20922），HTTP/HTTPS，REST API",
    "太阳能光伏 PLTS、PLTS-PLTB 混合系统与智能路灯(PJU),集成物联网能源监控. Feasibility study, design & installation for industries & commercial buildings across Indonesia": "太阳能光伏 PLTS、PLTS-PLTB 混合系统与智能路灯（PJU），集成物联网能源监控。为印尼各地的工业和商业建筑提供可行性研究、设计与安装。",
    "Solar PV & hybrid renewable energy across 印尼": "覆盖印尼的太阳能光伏与混合可再生能源",

    # Product page - ISO-M485 5461
    "Why engineers choose ISO-M485": "工程师选择 ISO-M485 的理由",
    "2.5kV Optical Isolation": "2.5kV 光电隔离",
    "Optocoupler isolation": "光耦隔离",
    "between RS-485 ports protects upstream PLC/SCADA from ground loops and field-side faults.": "跨 RS-485 端口保护上游 PLC/SCADA 免受接地回路和现场侧故障影响。",
    "Built-in Surge Protection": "内置浪涌保护",
    "TVS diodes + gas discharge tubes": "TVS 二极管 + 气体放电管",
    "guard against lightning-induced and switching transients on outdoor cables.": "防护户外电缆上的雷击和开关瞬态。",
    "256 Devices Per Bus": "每总线 256 台设备",
    "Extended driver capacity supports up to": "扩展驱动能力支持最多",
    "256 nodes per segment": "每段 256 个节点",
    ". Auto direction control simplifies wiring.": "。自动方向控制简化布线。",
    "Industrial Temp Range": "工业温度范围",
    "operation. DIN rail mountable. Rated for continuous operation in harsh field cabinets.": "工作。DIN 导轨安装。适用于恶劣现场机柜的连续运行。",
    "Flexible Wide Power Input": "灵活宽压输入",
    "7-15VDC or 9-24VDC": "7-15VDC 或 9-24VDC",
    "supply variants for easy integration with industrial 12V or 24V control panels.": "供电版本，便于与工业 12V 或 24V 控制面板集成。",
    "High-Speed Data Rate": "高速数据速率",
    "data rate (within distance limits) for high-throughput SCADA and PLC networks.": "数据速率（在距离限制内），适用于高吞吐量 SCADA 和 PLC 网络。",

    # Common schema/org text
    "Technology company specializing in Industrial IoT & System Integration in Batam, Riau Islands. Founded January 2023 by Gifari Kemal Suryo. 64+ 个工业项目, 6 in-house products, 5 core services.": "总部位于廖内群岛巴淡岛、专注于工业物联网与系统集成的科技公司。由 Gifari Kemal Suryo 于2023年1月创立。64+个工业项目，6个自研产品，5项核心服务。",
    "端到端工业物联网 architecture, edge computing, protocol translation, device management, IoT security, and cloud dashboards for manufacturing, energy, maritime, and utilities.": "面向制造业、能源、海事和公用事业的端到端工业物联网架构、边缘计算、协议转换、设备管理、物联网安全和云仪表盘。",

    # About page remaining EN
    "Transforming 印尼's industries through smart, connected end-to-end IoT, AI, and SaaS solutions.": "通过智能互联的端到端物联网、人工智能和SaaS解决方案，变革印尼工业。",
    "PT Surya Inovasi Prioritas (SURIOTA) is a technology company specializing in Industrial IoT Services and System Integration": "PT Surya Inovasi Prioritas (SURIOTA) 是一家专注于工业物联网服务和系统集成的科技公司",
    "总部位于印度尼西亚巴淡岛廖内群岛。自2023年1月以来，": "总部位于印度尼西亚巴淡岛廖内群岛。自2023年1月以来，",

    # Electrical page remaining EN
    "Industrial electrical engineering across 印尼": "覆盖印尼的工业电气工程",
    "SURIOTA's experienced engineering team has handled various electrical installation and maintenance projects across 印尼.": "SURIOTA 经验丰富的工程团队已在印尼各地完成了各种电气安装和维护项目。",
    "Compliant, IoT-enabled electrical engineering": "合规、支持物联网的电气工程",
    "01  Compliance &amp; Standards  All installation, panel building, and commissioning follow  SNI, IEC, and PUIL 2011 . Documented test reports and compliance certificates provided.": "01 合规与标准 所有安装、配电盘组装和调试均遵循 SNI、IEC 和 PUIL 2011 标准。提供完整的测试报告和合规证书。",
    "64+ projects delivered since 2023 across manufacturing, oil &amp; gas, maritime, and commercial sectors in Batam, Riau, and beyond.": "自2023年以来，已在巴淡岛、廖内群岛及其他地区的制造业、石油天然气、海事和商业领域交付64+个项目。",
    "Multi-skilled team with rapid mobilization across Sumatera, Java, Kalimantan . Maintenance contracts available.": "多技能团队，可快速 mobilize 至苏门答腊、爪哇、加里曼丹。提供维护合同。",
    "05  Safety-First Workflow  Every project follows documented risk assessments, lockout/tagout procedures, and PPE protocols. Zero-compromise safety culture.": "05 安全第一工作流程 每个项目均遵循文件化的风险评估、上锁/挂牌程序和个人防护装备规程。零妥协的安全文化。",
    "01   Design &amp; Installation  ": "01 设计与安装 ",
    "Design and installation of power distribution systems, distribution panels, cables, and industrial wiring harnesses per SNI and IEC standards.": "依据 SNI 和 IEC 标准进行配电系统、配电盘、电缆和工业线束的设计与安装。",
    "02   Testing &amp; Commissioning  ": "02 测试与调试 ",
    "Insulation resistance, continuity, ground resistance, and load testing to ensure safe installation before operation.": "绝缘电阻、导通性、接地电阻和负载测试，确保运行前的安装安全。",
    "03   Maintenance &amp; Repair  ": "03 维护与维修 ",
    "Periodic maintenance, troubleshooting, motor rewinding, and component replacement to maintain electrical system reliability.": "定期维护、故障排除、电机重绕和部件更换，以保持电气系统的可靠性。",
    "04   IoT Monitoring Integration  ": "04 物联网监控集成 ",
    "Integration with SURGE platform for real-time energy monitoring, predictive maintenance alerts, and dashboard analytics.": "与 SURGE 平台集成，实现实时能源监控、预测性维护警报和仪表盘分析。",
    "SURIOTA uses SNI (印尼国家标准), IEC (International Electrotechnical Commission), and PUIL (通用电气工程安装要求) standards in every installation, ensuring full safety and regulatory compliance.": "SURIOTA 在所有安装中均采用 SNI（印尼国家标准）、IEC（国际电工委员会）和 PUIL（通用电气工程安装要求）标准，确保完全符合安全和监管要求。",
    "2 年": "2年",
    "06  years": "06 年",
    "06  年": "06 年",

    # Automation page remaining EN
    "Industrial automation and IIoT integration for manufacturing, oil &amp; gas, shipyard, and energy sectors across 印尼": "面向印尼制造业、石油天然气、船厂和能源领域的工业自动化与 IIoT 集成",
    "SURIOTA designs and implements automation systems from small to large scale using Siemens S7, Omron, Schneider, and IEC 61131-3 compliant controllers.": "SURIOTA 使用西门子 S7、欧姆龙、施耐德和符合 IEC 61131-3 标准的控制器，设计并实施从小型到大型的自动化系统。",
    "PLC, SCADA &amp; IIoT integration, powered by Modbus Gateway, for Industry 4.0. Vendor-neutral automation for manufacturing, oil &amp; gas, shipyard, energy &amp; utilities": "基于 Modbus 网关的 PLC、SCADA 与 IIoT 集成，服务工业 4.0。厂商中立的自动化方案，覆盖制造业、石油天然气、船厂、能源与公用事业",
    "01  PLC &amp; SCADA Programming  ": "01 PLC 与 SCADA 编程 ",
    "02  HMI Development  ": "02 HMI 开发 ",
    "03  IIoT Integration  ": "03 IIoT 集成 ",
    "04  Preventive Maintenance  ": "04 预防性维护 ",

    # Renewable page remaining EN
    "Solar PV PLTS, hybrid PLTS-PLTB, and smart street lighting (PJU) with IoT energy monitoring. Feasibility study, design &amp; installation for industries &amp; commercial buildings across 印尼": "太阳能光伏 PLTS、PLTS-PLTB 混合系统和智能路灯（PJU），集成物联网能源监控。为印尼各地的工业和商业建筑提供可行性研究、设计与安装。",
    "Hybrid Off-Grid, IoT Energy Monitoring": "混合离网，物联网能源监控",
    "On/Off-Grid Hybrid": "并网/离网混合",
    "Feasibility Study": "可行性研究",
    "Feasibility-First Approach": "可行性优先方法",
    "IoT Hybrid": "物联网混合",
    "IoT Monitoring": "物联网监控",
    "PJU PLTS": "PJU PLTS",
    "PJU PLTS-PLTB": "PJU PLTS-PLTB",
    "Solar PV, PLTS, PLTB Hybrid": "太阳能光伏、PLTS、PLTB 混合",
    "Solar PV, Wind, Hybrid Systems Batam": "太阳能光伏、风力、混合系统 巴淡岛",
    "Monitoring SURGE Energy": "监控 SURGE 能源",
    "Off-Grid Hybrid PJU IoT Hybrid ROI Feasibility Study": "离网混合 PJU 物联网混合 ROI 可行性研究",

    # Water page remaining EN
    "WTP, WWTP &amp; IPAL design, installation &amp; maintenance for industrial, PDAM &amp; water utilities with KLHK SPARING compliance and real-time IoT monitoring (pH, COD, TSS, NH₃).": "面向工业、PDAM 与供水公用事业，提供符合 KLHK SPARING 合规要求的 WTP、WWTP 与 IPAL 设计、安装及维护，并配备实时物联网监测（pH、COD、TSS、NH₃）。",

    # Portfolio page remaining EN
    "SURIOTA Project Portfolio": "SURIOTA 项目案例",
    "Browse our completed industrial IoT, automation, electrical engineering, and renewable energy projects across 印尼.": "浏览我们在印尼各地完成的工业物联网、自动化、电气工程和可再生能源项目。",

    # Modbus Gateway page remaining EN
    "Where SRT-MGATE-1210 is deployed": "SRT-MGATE-1210 部署场景",
    "SRT-MGATE-1210 | Frequently Asked Questions": "SRT-MGATE-1210 | 常见问题",
    "What protocols does the Modbus 网关 support?": "Modbus 网关支持哪些协议？",
    "SRT-MGATE-1210 supports Modbus RTU (RS-485), Modbus TCP/IP, MQTT (ISO/IEC 20922), HTTP/HTTPS, and REST API. Custom protocol adapters available on request.": "SRT-MGATE-1210 支持 Modbus RTU（RS-485）、Modbus TCP/IP、MQTT（ISO/IEC 20922）、HTTP/HTTPS 和 REST API。可根据要求提供自定义协议适配器。",
    "Ready to bridge your industrial assets to IoT?": "准备好将您的工业资产桥接到物联网了吗？",
    "Request a quote, RFQ, or on-site technical demo. Our engineering team will provide sample register-mapping configurations for your existing equipment within 24 hours.": "请求报价、询价单或现场技术演示。我们的工程团队将在24小时内为您现有设备提供示例寄存器映射配置。",
    "Request Quote": "请求报价",
    "Sample config included": "包含示例配置",
    "Bulk pricing available": "提供批量定价",

    # ISO-M485 page remaining EN
    "ISO-M485 部署应用": "ISO-M485 部署应用",
    "When your operations depend on fast, stable, and secure data communication, you cannot afford downtime or interference. The ISO-M485 series is designed for industrial-grade RS-485 connectivity with built-in galvanic isolation and robust surge protection, ensuring maximum reliability in the most demanding environments.": "当您的运营依赖快速、稳定和安全的数据通信时，您无法承受停机或干扰。ISO-M485 系列专为工业级 RS-485 连接而设计，内置光电隔离和强大的浪涌保护，确保在最严苛的环境中也能实现最高可靠性。",
    "ISO-M485 | Frequently Asked Questions": "ISO-M485 | 常见问题",
    "What isolation voltage does ISO-M485 provide?": "ISO-M485 提供多大的隔离电压？",
    "RS-485 port-to-port 2.5kV optocoupler isolation protects upstream PLC/SCADA equipment from ground loops, common-mode noise, and field-side faults. Electrical isolation prevents damaging currents from propagating to your control room.": "RS-485 端口之间的 2.5kV 光耦隔离可保护上游 PLC/SCADA 设备免受地环路、共模噪声和现场故障影响。电气隔离可防止损坏电流传导至您的控制室。",
    "Ready to harden your RS-485 network?": "准备好加固您的 RS-485 网络了吗？",
    "Request a quote or technical sample. Our team will provide wiring diagrams and isolation topology recommendations within 24 hours.": "请求报价或技术样品。我们的团队将在24小时内提供接线图和隔离拓扑建议。",
    "Wiring diagram": "接线图",

    # SaaS page remaining EN
    "SaaS - Suriota": "SaaS - SURIOTA",
    "Data residency guaranteed by contract": "数据驻留通过合同保障",
    "for system integrators and regional partners": "面向系统集成商和区域合作伙伴",
    "n cloud regions for data residency": "云区域确保数据驻留",
    "n cloud regions": "云区域",
    "Kubernetes Helm chart": "Kubernetes Helm 图表",

    # Modbus Gateway page remaining EN
    "SSL certificates from your phone": "通过手机管理 SSL 证书",
    "oors, and maritime installations": "门和海上设施",
    "Converts Modbus RTU": "转换 Modbus RTU",
    "Connects to AWS IoT": "连接 AWS IoT",

    # Consulting page remaining EN
    "Focus ROI-First Method": "聚焦 ROI 优先方法",
    "and BSSN cybersecurity guidance built into every roadmap": "每个路线图都内置 BSSN 网络安全指导",
    "Benchmark vs peers": "与同行基准对比",
    "Power Calculations Site": "功率计算现场",
    "D Drawing": "D 绘图",
    "D Splingker P": "D 喷头 P",
    "ROADMAP ROI Q": "路线图 ROI 季度",
    "Compliance Advisory": "合规咨询",
    "PT Darmawan SLD": "PT Darmawan 单线图",
    "PT Koltiva Maintenance WTP": "PT Koltiva WTP 维护",

    # Analytics page remaining EN
    "and regulatory reporting": "以及合规报告",
    "BI Tools SURIOTA": "BI 工具 SURIOTA",
    "Real-time Dashboards Grafana": "实时仪表板 Grafana",
    "Regulatory Reporting KLHK SPARING": "合规报告 KLHK SPARING",
    "pH, Temp, Humidity": "pH、温度、湿度",
    "vs last week MON TUE WED THU FRI": "对比上周 周一 周二 周三 周四 周五",

    # AI page remaining EN
    "n on your data, and deploy with rollback and monitoring": "在您数据上训练，并带回滚和监控部署",
    "tation Monitoring LIFA": "监测 LIFA",
    "Temp Monitoring AI": "温度监测 AI",

    # IoT page remaining EN
    "m or your preferred cloud": "m 或您首选的云",
    "tation Soil Monitoring IoT": "土壤监测物联网",
    "Protocol Translation Modbus RTU": "协议转换 Modbus RTU",

    # Electrical page remaining EN
    "Safety-First Workflow": "安全第一工作流",
    "HSE-driven procedures": "HSE 驱动程序",
    "with rapid mobilization across": "快速动员覆盖",
    "Berita Acara Serah Terima": "交接会议纪要",

    # Integration page remaining EN
    "IIoT -- Sensor Integration": "IIoT 传感器集成",
    "PT Koltiva Maintenance WTP": "PT Koltiva WTP 维护",

    # Water page remaining EN
    "and installing units": "安装单元",

    # About page remaining EN
    "across manufacturing , energy": "覆盖制造业、能源",

    # Automation page remaining EN
    "SCADA We integrate": "SCADA 我们集成",

    # Renewable page remaining EN
    "Monitoring SURGE Energy": "监控 SURGE 能源",
    "Off-Grid Hybrid PJU IoT Hybrid ROI Feasibility Study": "离网混合 PJU IoT 混合 ROI 可行性研究",

    # Portfolio page remaining EN
    "PT Tri Hexa Inovasi SURGE": "PT Tri Hexa Inovasi SURGE",
    "PT Techno Mandiri Anak Negeri SURIOTA Modbus": "PT Techno Mandiri Anak Negeri SURIOTA Modbus",
    "Madani SURGE Energy Mapping": "Madani SURGE 能源映射",
    "Personal Smart NPK": "个人智能 NPK",
    "tation Soil Monitoring IoT System": "土壤监测物联网系统",
    "PT Koltiva Procurement Module": "PT Koltiva 采购模块",
    "Personal Mini Pertamina": "个人迷你 Pertamina",
    "Personal School Website": "个人学校网站",
    "Personal LIFA Programming": "个人 LIFA 编程",
    "WTP Maintenance": "WTP 维护",
    "Site 规划": "现场规划",
    "Digital Stamp": "数字印章",
    "Webmail Maintenance": "邮件维护",
    "电气工程 Testing": "电气工程测试",
    "Load Suppression": "负载抑制",
    "电气工程 Power Calculations": "电气工程功率计算",
    "CAD Design - POS 安全 Canopy": "CAD 设计 - POS 安全顶棚",
    "CAD Design - 水处理": "CAD 设计 - 水处理",
    "CAD Design - 废物处理场": "CAD 设计 - 废物处理场",
    "工程计算烟雾探测器": "工程计算烟雾探测器",
    "工程计算流量": "工程计算流量",
    "SLD烟雾探测器": "SLD 烟雾探测器",
    "2D 喷头 P&ID": "2D 喷头 P&ID",
    "设置以太网通讯打印": "设置以太网通讯打印",
    "蒲莱河 75kW 离心泵重绕": "蒲莱河 75kW 离心泵重绕",
    "双溪蒲莱水库缺相保护及避雷器": "双溪蒲莱水库缺相保护及避雷器",
    "SPARING 传感器的更换和维修": "SPARING 传感器的更换和维修",
    "节约污水处理厂维护": "节约污水处理厂维护",
    "45kW潜水卫星泵复卷": "45kW 潜水卫星泵复卷",
    "物联网考勤模块": "物联网考勤模块",
    "基于物联网的混合街道照明（太阳能光伏+风力涡轮机）": "基于物联网的混合街道照明（太阳能光伏+风力涡轮机）",
    "设置发电机组 DSE-5520": "设置发电机组 DSE-5520",
    "发电机组传感器采购": "发电机组传感器采购",
    "电气工程接线与调试": "电气工程接线与调试",
    "YOLO 物体检测人工智能": "YOLO 物体检测人工智能",
    "物联网机器人坦克原型": "物联网机器人坦克原型",
    "基于 IoT 和 LabVIEW 的水位系统": "基于 IoT 和 LabVIEW 的水位系统",
    "RGB、CMYK 和 HSL 颜色检测程序": "RGB、CMYK 和 HSL 颜色检测程序",
    "物体形状检测程序": "物体形状检测程序",
    "MnS标志设计": "MnS 标志设计",
    "安顺贴纸设计": "安顺贴纸设计",
    "婚礼请柬硬拷贝": "婚礼请柬硬拷贝",
    "基于物联网的自动微型电容器组系统": "基于物联网的自动微型电容器组系统",
    "基于物联网的鱼饲料控制和监测": "基于物联网的鱼饲料控制和监测",
    "基于物联网的太阳能电池板 ATS 控制和监测": "基于物联网的太阳能电池板 ATS 控制和监测",
    "Jamu 标志与产品设计": "Jamu 标志与产品设计",
    "公司产品徽标、图标和 PrintUP 设计": "公司产品徽标、图标和 PrintUP 设计",
    "物联网机器人坦克原型": "物联网机器人坦克原型",
    "规划pH、温度、湿度监测和土壤控制物联网系统": "规划 pH、温度、湿度监测和土壤控制物联网系统",
}


def _normalize_text(text):
    """Normalize typographic quotes to ASCII for consistent matching."""
    return (text
            .replace('\u2019', "'")   # right single quotation mark
            .replace('\u2018', "'")   # left single quotation mark
            .replace('\u201c', '"')   # left double quotation mark
            .replace('\u201d', '"')   # right double quotation mark
            .replace('\u2013', '-')   # en dash
            .replace('\u2014', '--')) # em dash

# Normalize DICT keys once at module level
_NORM_DICT = {_normalize_text(k): v for k, v in DICT.items()}

def translate_html(html, page_id=None):
    modified = False

    # First pass: raw string replacement on normalized HTML (handles keys spanning tags)
    new_html = _normalize_text(html)
    for en, zh in sorted(_NORM_DICT.items(), key=lambda x: -len(x[0])):
        if en in new_html:
            new_html = new_html.replace(en, zh)
            modified = True

    # Second pass: BeautifulSoup for text nodes not caught above
    soup = BeautifulSoup(new_html, 'html.parser')

    for node in soup.find_all(string=True):
        if isinstance(node, NavigableString):
            text = str(node)
            # Skip style/script content
            if node.parent and node.parent.name in ['style', 'script']:
                continue

            new_text = _normalize_text(text)
            # Replace using dictionary (longest first)
            for en, zh in sorted(_NORM_DICT.items(), key=lambda x: -len(x[0])):
                if en in new_text:
                    new_text = new_text.replace(en, zh)
                    modified = True

            if new_text != text:
                node.replace_with(new_text)

    # Translate aria-label and alt attributes
    for tag in soup.find_all():
        for attr in ['aria-label', 'alt']:
            if tag.has_attr(attr):
                val = tag[attr]
                new_val = _normalize_text(val)
                for en, zh in sorted(_NORM_DICT.items(), key=lambda x: -len(x[0])):
                    if en in new_val:
                        new_val = new_val.replace(en, zh)
                        modified = True
                if new_val != val:
                    tag[attr] = new_val

    return str(soup), modified

def translate_plain(text, page_id=None):
    new_text = _normalize_text(text)
    for en, zh in sorted(_NORM_DICT.items(), key=lambda x: -len(x[0])):
        if en in new_text:
            new_text = new_text.replace(en, zh)
    return new_text

# Process all entries
count = 0
for item in data:
    original = item['original']
    widget = item['widget_type']

    # Use existing translated as base if available and different from original
    base = item.get('translated') if item.get('translated') and item.get('translated') != original else original

    if widget in ('html', 'text-editor'):
        translated, modified = translate_html(base, item['page_id'])
        if modified:
            item['translated'] = translated
            count += 1
    else:
        translated = translate_plain(base, item['page_id'])
        if translated != base:
            item['translated'] = translated
            count += 1

# Save
with open('translations/extract.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Translated {count} / {len(data)} fields')

# Print untranslated fields
print('\nUntranslated fields:')
for item in data:
    if not item.get('translated'):
        preview = item['original'][:80].replace('\n', ' ')
        print(f"  Page {item['page_id']} [{item['widget_type']}] {preview}...")
