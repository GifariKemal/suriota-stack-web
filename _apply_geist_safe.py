"""Apply Geist - SAFE version using wp_enqueue_style + wp_add_inline_style only."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Pure PHP, no inline HTML toggle, no top-level eager calls
SNIPPET = r"""
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style(
        'sx-geist',
        'https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap',
        array(),
        '1.0'
    );
    $css = "
    :root { --sx-font-sans: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif; --sx-font-mono: 'Geist Mono', ui-monospace, monospace; }
    html, body, p, span, a, li, td, th, label, input, textarea, select, button, h1, h2, h3, h4, h5, h6,
    .elementor-widget-text-editor, .elementor-widget-heading, .elementor-widget-button, .elementor-button,
    .elementor *:not(i):not(svg):not([class*='fa-']):not([class*='icon-']):not([class*='eicon-']) {
        font-family: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif !important;
    }
    code, pre, kbd, samp, tt, var, .sx-mono, [class*='mono'],
    .elementor-widget-code, .elementor-widget-html code {
        font-family: 'Geist Mono', ui-monospace, monospace !important;
    }
    body { letter-spacing: -0.005em; font-feature-settings: 'ss01','cv11'; }
    h1, h2, h3, h4, h5, h6 { letter-spacing: -0.02em; font-feature-settings: 'ss01','cv11'; }
    .fa, .fab, .fas, .far, .fal, .fad { font-family: 'Font Awesome 6 Free','Font Awesome 6 Brands' !important; }
    [class*='eicon-'] { font-family: 'eicons' !important; }
    ";
    wp_add_inline_style('sx-geist', $css);
}, 999);
"""

# First: deactivate any broken Geist snippet from previous attempt
r = urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets?per_page=100', headers=HDRS)
d = json.loads(urllib.request.urlopen(r, timeout=60).read())
geist_ids = []
purge_ids = []
for s in d:
    nm = s['name'].lower()
    if 'eist' in nm:
        geist_ids.append(s['id'])
    if 'purge after geist' in nm or 'sx: purge' in nm:
        purge_ids.append(s['id'])

print(f'Found geist snippet IDs: {geist_ids}')
print(f'Found purge snippet IDs: {purge_ids}')

# Deactivate purge auto-runs (these run top-level, risky)
for pid in purge_ids:
    try:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/code-snippets/v1/snippets/{pid}', data=json.dumps({'active':False}).encode(), method='POST', headers=HDRS), timeout=30).read()
        print(f'  Deactivated purge ID:{pid}')
    except Exception as e:
        print(f'  purge {pid} err: {e}')

# Update Geist snippet with safe code
target_id = geist_ids[0] if geist_ids else None
if target_id:
    try:
        data = json.dumps({'code': SNIPPET, 'active': True, 'name': 'SX: Font Geist v2 (safe)'}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/code-snippets/v1/snippets/{target_id}', data=data, method='POST', headers=HDRS), timeout=30).read()
        print(f'  Updated Geist ID:{target_id} -> safe version')
    except Exception as e:
        print(f'  update err: {e}')
else:
    # Create new
    try:
        data = json.dumps({'code': SNIPPET, 'active': True, 'name': 'SX: Font Geist v2 (safe)'}).encode()
        resp = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets', data=data, method='POST', headers=HDRS), timeout=30).read()
        res = json.loads(resp)
        print(f'  Created Geist ID:{res.get("id")}')
    except Exception as e:
        print(f'  create err: {e}')

print('Done')
