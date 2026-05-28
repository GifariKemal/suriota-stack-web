import json, re

with open('translations/extract.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ARIA_DICT = {
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
    "Order SRT-MGATE-1210 on Tokopedia": "在 Tokopedia 订购 SRT-MGATE-1210",
    "Order ISO-M485 on Tokopedia": "在 Tokopedia 订购 ISO-M485",
}

count = 0
for item in data:
    if item['widget_type'] not in ('html', 'text-editor'):
        continue

    text = item.get('translated') or item['original']
    modified = False

    for en, zh in ARIA_DICT.items():
        # Replace aria-label values
        pattern = f'aria-label="{en}"'
        replacement = f'aria-label="{zh}"'
        if pattern in text:
            text = text.replace(pattern, replacement)
            modified = True
        # Also handle single-quoted versions
        pattern2 = f"aria-label='{en}'"
        replacement2 = f"aria-label='{zh}'"
        if pattern2 in text:
            text = text.replace(pattern2, replacement2)
            modified = True

    if modified:
        item['translated'] = text
        count += 1

with open('translations/extract.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Updated aria-labels in {count} fields')
