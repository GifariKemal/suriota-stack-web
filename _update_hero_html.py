"""Update sx-hero-sub paragraph on 4 service pages with Tier-2 industry + Tier-3 keywords.
Each page = get full HTML, regex-replace just the hero-sub <p>, push back.
"""
import json, urllib.request, urllib.error, base64, re

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# (post_id, html_widget_id, NEW subtitle text)
TARGETS = [
    (5029, 'b82358c',
     'Industrial IoT &amp; system integration &mdash; Modbus RTU/TCP to MQTT gateways, edge computing, AWS IoT Core &amp; SURGE cloud dashboards for manufacturing, oil &amp; gas, shipyard, water utilities &amp; renewable energy across Indonesia.'),
    (5037, '6546043',
     'AI &amp; industrial data analytics &mdash; predictive maintenance, OEE, energy optimisation, KPI dashboards &amp; computer vision QC for manufacturing, oil &amp; gas, mining, water utilities &amp; logistics across Indonesia.'),
    (5033, '7bf887c',
     'Digital transformation consulting &mdash; Industry 4.0 roadmap, OT/IT convergence, IIoT readiness audit, SCADA modernisation &amp; cloud migration strategy for Indonesian manufacturers, energy &amp; maritime operators.'),
    (5039, '5996e42',
     'SURGE SaaS platform &mdash; multi-tenant industrial IoT monitoring for energy (kWh, power factor), water (KLHK SPARING, pH/COD/TSS/NH3) &amp; vessel tracking. 70% cheaper than ThingsBoard, made in Indonesia.'),
]

# sx-hero-sub paragraph regex — captures content between class tag and closing </p>
SUB_RE = re.compile(r'(<p class="sx-hero-sub">)([^<]*(?:<[^/p][^>]*>[^<]*)*?)(</p>)')

for post_id, eid, new_sub in TARGETS:
    print(f'\n=== {post_id} ({eid}) ===')
    # 1) Fetch current settings via element settings endpoint isn't available for raw write — use post REST
    r = urllib.request.Request(
        f'https://suriota.com/wp-json/wp/v2/pages/{post_id}?context=edit&_fields=id,meta',
        headers=HDRS
    )
    try:
        data = json.loads(urllib.request.urlopen(r, timeout=30).read())
    except urllib.error.HTTPError as e:
        print(f'fetch fail: {e.code} {e.read().decode()[:200]}')
        continue

    meta = data.get('meta', {})
    elementor = meta.get('_elementor_data')
    if not elementor:
        print('no _elementor_data')
        continue

    # _elementor_data may be string or already-parsed list
    if isinstance(elementor, str):
        try:
            tree = json.loads(elementor)
        except Exception as e:
            print(f'json parse fail: {e}')
            continue
    else:
        tree = elementor

    # Recursively find widget by id and patch the html setting
    def patch(node):
        if isinstance(node, list):
            return any(patch(n) for n in node)
        if not isinstance(node, dict):
            return False
        if node.get('id') == eid and node.get('widgetType') == 'html':
            html = node.get('settings', {}).get('html', '')
            m = SUB_RE.search(html)
            if m:
                new_html = html[:m.start()] + '<p class="sx-hero-sub">' + new_sub + '</p>' + html[m.end():]
                node['settings']['html'] = new_html
                print(f'  patched, len {len(html)} -> {len(new_html)}')
                return True
            else:
                print('  sx-hero-sub regex did not match!')
                return False
        # recurse
        elements = node.get('elements')
        if elements:
            return any(patch(c) for c in elements)
        return False

    if not patch(tree):
        print('  no patch applied')
        continue

    # Push back
    payload = json.dumps({'meta': {'_elementor_data': json.dumps(tree, separators=(',', ':'))}}).encode()
    req = urllib.request.Request(
        f'https://suriota.com/wp-json/wp/v2/pages/{post_id}',
        data=payload, method='POST', headers=HDRS
    )
    try:
        resp = urllib.request.urlopen(req, timeout=60).read().decode()
        print('  pushed OK')
    except urllib.error.HTTPError as e:
        print(f'  push fail: {e.code} {e.read().decode()[:300]}')

print('\nDone.')
