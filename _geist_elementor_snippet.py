"""Deploy Geist via Elementor Custom Code (elementor_snippet) — bypasses WPO Minify cache."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Geist HTML+CSS payload (injected directly to wp_head)
GEIST_CODE = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap">
<style id="sx-geist-fonts">
:root {
    --sx-font-sans: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif;
    --sx-font-mono: 'Geist Mono', ui-monospace, monospace;
}
html, body,
p, span, a, li, td, th, label, input, textarea, select, button, blockquote, q, cite,
h1, h2, h3, h4, h5, h6,
.elementor-widget-text-editor, .elementor-widget-heading,
.elementor-widget-button, .elementor-button,
.elementor-widget-icon-box, .elementor-widget-icon-list,
.elementor-widget-image-box, .elementor-widget-testimonial,
.elementor-widget-tabs, .elementor-widget-accordion,
.elementor-widget-toggle, .elementor-widget-counter,
.elementor-widget-call-to-action, .elementor-widget-price-table,
.elementor-widget-flip-box, .elementor-widget-blockquote,
.elementor-widget-divider, .elementor-widget-progress,
.elementor-widget-table-of-contents,
.elementor-widget-nav-menu, .elementor-nav-menu,
.elementor-post__title, .elementor-post__excerpt,
.elementor-post__read-more, .elementor-post__meta,
.sx-stat-num, .sx-stat-label, .sx-card-title, .sx-card-body,
.sx-eyebrow, .sx-hero-title, .sx-hero-subtitle, .sx-meta-row,
.sx-callout, .sx-trust-card, .sx-service-card,
.elementor *:not(i):not(svg):not([class*='fa-']):not([class*='icon-']):not([class*='eicon-']):not([class*='dashicons']) {
    font-family: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif !important;
}
code, pre, kbd, samp, tt, var,
.sx-mono, [class*='mono'], .sx-code,
.elementor-widget-code, .elementor-widget-html code {
    font-family: 'Geist Mono', ui-monospace, 'JetBrains Mono', monospace !important;
}
body { letter-spacing: -0.005em; font-feature-settings: 'ss01','cv11'; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
h1, h2, h3, h4, h5, h6, .elementor-heading-title { letter-spacing: -0.02em; font-feature-settings: 'ss01','cv11'; font-weight: 600; }
h1, .elementor-heading-title.elementor-size-xxl { letter-spacing: -0.03em; font-weight: 700; }
.fa, .fab, .fas, .far, .fal, .fad, i.fa, i.fab, i.fas, i.far, i.fal, i.fad { font-family: 'Font Awesome 6 Free','Font Awesome 6 Brands' !important; }
[class*='eicon-'], [class^='eicon-'] { font-family: 'eicons' !important; }
[class*='dashicons'] { font-family: 'dashicons' !important; }
.material-icons, [class*='material-icon'] { font-family: 'Material Icons' !important; }
</style>"""

# Create new elementor_snippet
payload = {
    'title': 'SX / Geist Font System Sitewide',
    'status': 'publish',
    'meta': {
        '_elementor_location': 'elementor_head',
        '_elementor_priority': 1,
        '_elementor_code': GEIST_CODE
    }
}
try:
    resp = urllib.request.urlopen(urllib.request.Request(
        'https://suriota.com/wp-json/wp/v2/elementor_snippet',
        data=json.dumps(payload).encode(),
        method='POST',
        headers=HDRS
    ), timeout=30).read()
    res = json.loads(resp)
    sid = res.get('id')
    print(f'Created elementor_snippet ID:{sid}')
    print(f'  status: {res.get("status")}')
    print(f'  link: {res.get("link")}')
except Exception as e:
    print(f'create err: {e}')
    sys.exit(1)

# Clean up Kit's custom_css (remove Geist block since elementor_snippet handles it now)
print('\nCleaning Kit custom_css...')
try:
    r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_library/5?context=edit', headers=HDRS)
    d = json.loads(urllib.request.urlopen(r, timeout=30).read())
    ps = d.get('meta', {}).get('_elementor_page_settings', {})
    if isinstance(ps, str): ps = json.loads(ps) if ps else {}
    css = ps.get('custom_css', '')
    start = css.find('/* SX: Geist Font System')
    if start >= 0:
        # Strip Geist block from Kit
        ps['custom_css'] = css[:start].rstrip()
        payload2 = json.dumps({'meta': {'_elementor_page_settings': ps}}).encode()
        urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_library/5', data=payload2, method='POST', headers=HDRS), timeout=30).read()
        print('  Kit cleaned (Geist removed from Kit, now only via elementor_snippet)')
    else:
        print('  no Geist in Kit')
except Exception as e:
    print(f'  err: {e}')

# Clear Elementor cache
print('\nClearing Elementor cache...')
try:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
    print('  Elementor cache cleared')
except Exception as e:
    print(f'  err: {e}')

# Trigger frontend refresh + verify
time.sleep(3)
print('\nVerifying...')
import urllib.parse
for i in range(3):
    try:
        r = urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/?nc={int(time.time())}{i}', headers={'User-Agent':'Mozilla/5.0','Cache-Control':'no-cache'}), timeout=30)
        body = r.read().decode('utf-8', errors='replace')
        geist_count = body.count('Geist')
        print(f'  attempt {i+1}: code={r.status}, Geist count={geist_count}')
        if geist_count > 0:
            print(f'  ✓ Geist deployed successfully')
            break
    except Exception as e:
        print(f'  err: {e}')
    time.sleep(3)
