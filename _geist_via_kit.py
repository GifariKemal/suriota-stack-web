"""Deploy Geist via Elementor Kit Custom CSS — no Code Snippets dependency."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

GEIST_CSS = """/* SX: Geist Font System - Industrial Editorial */
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap');

:root {
    --sx-font-sans: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif;
    --sx-font-mono: 'Geist Mono', ui-monospace, monospace;
}

/* Apply Geist to all text elements */
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

/* Geist Mono for code/technical */
code, pre, kbd, samp, tt, var,
.sx-mono, [class*='mono'], .sx-code,
.elementor-widget-code, .elementor-widget-html code {
    font-family: 'Geist Mono', ui-monospace, 'JetBrains Mono', monospace !important;
}

/* Typography refinements */
body {
    letter-spacing: -0.005em;
    font-feature-settings: 'ss01', 'cv11';
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
h1, h2, h3, h4, h5, h6,
.elementor-heading-title {
    letter-spacing: -0.02em;
    font-feature-settings: 'ss01', 'cv11';
    font-weight: 600;
}
h1, .elementor-heading-title.elementor-size-xxl { letter-spacing: -0.03em; font-weight: 700; }

/* Preserve icon fonts */
.fa, .fab, .fas, .far, .fal, .fad,
i.fa, i.fab, i.fas, i.far, i.fal, i.fad {
    font-family: 'Font Awesome 6 Free', 'Font Awesome 6 Brands' !important;
}
[class*='eicon-'], [class^='eicon-'] { font-family: 'eicons' !important; }
[class*='dashicons'] { font-family: 'dashicons' !important; }
.material-icons, [class*='material-icon'] { font-family: 'Material Icons' !important; }
"""

# Fetch current Kit page_settings
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_library/5?context=edit', headers=HDRS)
d = json.loads(urllib.request.urlopen(r, timeout=30).read())
meta = d.get('meta', {})
ps = meta.get('_elementor_page_settings', {})
if isinstance(ps, str):
    ps = json.loads(ps) if ps else {}

old_css = ps.get('custom_css', '') if isinstance(ps, dict) else ''
print(f'Old custom_css: {len(old_css)} chars')

# Append our Geist CSS (don't replace, to avoid losing existing styles)
if 'SX: Geist Font System' not in old_css:
    new_css = old_css + '\n\n' + GEIST_CSS if old_css else GEIST_CSS
else:
    # Replace existing Geist block
    start = old_css.find('/* SX: Geist Font System')
    end_marker = '/* End SX: Geist */'
    end = old_css.find(end_marker, start)
    if end < 0:
        # No end marker, replace from start to end of file
        new_css = old_css[:start] + GEIST_CSS
    else:
        new_css = old_css[:start] + GEIST_CSS + old_css[end+len(end_marker):]

print(f'New custom_css: {len(new_css)} chars')

ps['custom_css'] = new_css

# Push update
payload = json.dumps({'meta': {'_elementor_page_settings': ps}}).encode()
try:
    resp = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_library/5', data=payload, method='POST', headers=HDRS), timeout=30).read()
    print('Kit updated')
except Exception as e:
    print(f'update fail: {e}')

# Verify
time.sleep(2)
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_library/5?context=edit', headers=HDRS)
d = json.loads(urllib.request.urlopen(r, timeout=30).read())
ps2 = d.get('meta', {}).get('_elementor_page_settings', {})
if isinstance(ps2, str): ps2 = json.loads(ps2) if ps2 else {}
print(f'Verified: custom_css now {len(ps2.get("custom_css",""))} chars')
print(f'Contains Geist: {"Geist" in ps2.get("custom_css","")}')

# Trigger frontend refresh
time.sleep(2)
try:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    print('Frontend refreshed')
except Exception as e:
    print(f'refresh err: {e}')
