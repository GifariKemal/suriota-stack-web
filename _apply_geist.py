"""Apply Geist + Geist Mono sitewide via code snippet."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Snippet: load Geist + override Plus Jakarta Sans / IBM Plex Mono globally
SNIPPET = r"""
// SX: Font Swap - Geist + Geist Mono (replace Plus Jakarta + IBM Plex Mono)
add_action('wp_head', function() {
    ?>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap">
    <style id="sx-geist-override">
    /* Geist sitewide override - replaces Plus Jakarta Sans + IBM Plex Mono */
    :root {
        --sx-font-sans: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif;
        --sx-font-mono: 'Geist Mono', ui-monospace, 'JetBrains Mono', monospace;
    }
    html, body,
    p, span, a, li, td, th, label, input, textarea, select, button,
    h1, h2, h3, h4, h5, h6,
    .elementor-widget-text-editor, .elementor-widget-heading,
    .elementor-widget-button, .elementor-button,
    .elementor *:not(i):not(svg):not([class*="fa-"]):not([class*="icon-"]):not([class*="eicon-"]) {
        font-family: 'Geist', system-ui, -apple-system, 'Segoe UI', sans-serif !important;
    }
    code, pre, kbd, samp, tt, var,
    .sx-mono, [class*="mono"],
    .elementor-widget-code, .elementor-widget-html code {
        font-family: 'Geist Mono', ui-monospace, monospace !important;
    }
    /* Slightly tune for comfort - Geist reads best with these tweaks */
    body { font-feature-settings: 'ss01', 'cv11'; letter-spacing: -0.005em; }
    h1, h2, h3, h4, h5, h6 { letter-spacing: -0.02em; font-feature-settings: 'ss01', 'cv11'; }
    /* Preserve icon fonts */
    .fa, .fab, .fas, .far, .fal, .fad,
    [class*="eicon-"], [class*="elementor-icon"] i,
    .material-icons, [class^="icon-"] {
        font-family: inherit !important;
    }
    .fa, .fab, .fas, .far, .fal, .fad { font-family: "Font Awesome 6 Free", "Font Awesome 6 Brands" !important; }
    [class*="eicon-"] { font-family: 'eicons' !important; }
    </style>
    <?php
}, 999);

// Dequeue old Plus Jakarta + IBM Plex Mono enqueues (if any handle matches)
add_action('wp_enqueue_scripts', function() {
    foreach (['plus-jakarta-sans', 'ibm-plex-mono', 'google-fonts-plus-jakarta', 'sx-fonts'] as $h) {
        wp_dequeue_style($h);
        wp_deregister_style($h);
    }
}, 100);
"""

# POST new snippet
data = json.dumps({
    'name': 'SX: Font Geist v1',
    'code': SNIPPET,
    'active': True,
    'scope': 'global',
    'priority': 10,
    'description': 'Sitewide font swap: Geist + Geist Mono replaces Plus Jakarta Sans + IBM Plex Mono'
}).encode()

# Check if slot 5 already used; create new snippet
r = urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets', data=data, method='POST', headers=HDRS)
try:
    resp = urllib.request.urlopen(r, timeout=60).read()
    res = json.loads(resp)
    print(f'Created snippet ID:{res.get("id")} active:{res.get("active")}')
except Exception as e:
    print(f'create fail: {e}')
    # Try slot 14 if slot 5 conflict
    r = urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/14', data=data, method='POST', headers=HDRS)
    try:
        resp = urllib.request.urlopen(r, timeout=60).read()
        res = json.loads(resp)
        print(f'Updated snippet ID:14')
    except Exception as e2:
        print(f'fallback fail: {e2}')

# Purge caches
time.sleep(2)
purge = """
if (class_exists('\\\\Elementor\\\\Plugin')) {
    \\Elementor\\Plugin::instance()->files_manager->clear_cache();
}
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
"""
purge_data = json.dumps({'code': purge, 'active': True, 'name': 'SX: purge after geist'}).encode()
try:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets', data=purge_data, method='POST', headers=HDRS), timeout=60).read()
    print('Purge snippet created')
except Exception as e:
    print(f'purge create fail: {e}')

time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Site refreshed')
