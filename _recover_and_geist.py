"""Recovery: deactivate broken snippets + deploy safe Geist."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Step 1: Probe until REST is reachable
print('Waiting for REST...')
for i in range(120):
    try:
        r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?per_page=1', headers=HDRS), timeout=10)
        if r.status < 500:
            print(f'  ready (code={r.status})')
            break
    except urllib.error.HTTPError as e:
        if e.code < 500:
            print(f'  ready (code={e.code})')
            break
        print(f'  attempt {i}: {e.code}', end='\r')
    except Exception as e:
        print(f'  attempt {i}: err {str(e)[:30]}', end='\r')
    time.sleep(15)
else:
    print('REST never recovered, abort')
    sys.exit(1)

# Step 2: List snippets, deactivate any Geist + purge ones
print('\nDeactivating bad snippets...')
r = urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets?per_page=100', headers=HDRS)
d = json.loads(urllib.request.urlopen(r, timeout=30).read())
for s in d:
    nm = s['name'].lower()
    if ('eist' in nm or 'purge after geist' in nm) and s['active']:
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/code-snippets/v1/snippets/{s["id"]}', data=json.dumps({'active':False}).encode(), method='POST', headers=HDRS), timeout=30).read()
            print(f'  Deactivated ID:{s["id"]} {s["name"]}')
        except Exception as e:
            print(f'  ERR {s["id"]}: {e}')

# Step 3: Deploy safe Geist snippet
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

print('\nDeploying safe Geist v2...')
try:
    data = json.dumps({'code': SNIPPET, 'active': True, 'name': 'SX: Font Geist v2 (safe)', 'scope':'global'}).encode()
    resp = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets', data=data, method='POST', headers=HDRS), timeout=30).read()
    res = json.loads(resp)
    print(f'  Created ID:{res.get("id")} active:{res.get("active")}')
except Exception as e:
    print(f'  ERR: {e}')

# Step 4: Verify site loads
print('\nVerify site...')
time.sleep(3)
try:
    r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30)
    print(f'  Homepage code={r.status}')
    body = r.read().decode('utf-8', errors='replace')
    if 'Geist' in body:
        print('  ✓ Geist found in HTML')
    else:
        print('  ✗ Geist not in HTML (may need cache flush)')
except Exception as e:
    print(f'  ERR: {e}')
