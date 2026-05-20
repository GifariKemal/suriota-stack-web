"""Refactor language switcher: remove floating pill, add navbar dropdown EN/ID/CN."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# 1) Disable old floating switcher snippet
print('1) Disabling old floating switcher snippet via PHP...')
disable_php = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/disable-old-switcher.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
global $wpdb;
$snippets_table = $wpdb->prefix . 'snippets';
$names = ['SX: Polylang Language Switcher Server', 'SX: Polylang Language Switcher v1'];
foreach ($names as $name) {
    $found = $wpdb->get_row($wpdb->prepare("SELECT id FROM $snippets_table WHERE name=%s", $name));
    if ($found) {
        $wpdb->update($snippets_table, ['active' => 0, 'modified' => current_time('mysql')], ['id' => $found->id]);
    }
}
file_put_contents($log, 'done @ ' . date('c'));
if (function_exists('code_snippets')) { code_snippets()->deactivate(5); }
'''
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':disable_php, 'active':True, 'name':'SX: disable old switcher'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(2)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
time.sleep(3)
print('Old switchers disabled')

# 2) Modify header snippet 5153 to add language dropdown in navbar
print('\n2) Inserting language dropdown into header snippet 5153...')
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5153?context=edit&_fields=meta', headers=HDRS)
d = json.loads(urllib.request.urlopen(r).read())
code = d['meta']['_elementor_code']

# Check if already inserted
if 'sx-hf-v5-lang' in code:
    print('Already has lang dropdown — replacing')
    # Remove old inserted block
    import re
    code = re.sub(r"'<div class=\"sx-hf-v5-dropdown sx-hf-v5-lang\">.*?'</div>' \+\s*\n\s*", '', code, flags=re.DOTALL)

# Build the language dropdown HTML — JS-string-concatenated style matching existing pattern
# Two variants needed:
# - When on EN: button shows EN, dropdown shows ID + CN(soon)
# - When on ID: button shows ID, dropdown shows EN + CN(soon)
# Use JS-detected isID and dynamic links

lang_dropdown = """          '<div class="sx-hf-v5-dropdown sx-hf-v5-lang">' +
            '<button class="sx-hf-v5-dropbtn" aria-haspopup="true" aria-expanded="false"><span class="sx-lang-flag">' + (isID?'ID':'EN') + '</span> <span class="sx-hf-v5-caret">&#9662;</span></button>' +
            '<div class="sx-hf-v5-dropcontent sx-hf-v5-lang-content">' +
              (isID? '<a href="' + enUrl + '" hreflang="en"><span class="sx-lang-flag-mini">EN</span> English</a>' : '<a href="' + idUrl + '" hreflang="id"><span class="sx-lang-flag-mini">ID</span> Bahasa Indonesia</a>') +
              '<span class="sx-lang-disabled" aria-disabled="true"><span class="sx-lang-flag-mini">CN</span> 中文 <em class="sx-lang-soon">Coming Soon</em></span>' +
            '</div>' +
          '</div>' +
"""

# Insert before '</nav>'
nav_close_idx = code.find("'</nav>'")
if nav_close_idx == -1:
    print('ERROR: </nav> not found')
else:
    code = code[:nav_close_idx] + lang_dropdown + code[nav_close_idx:]
    print(f'Lang dropdown inserted at {nav_close_idx}')

# Add JS to detect current language + populate dynamic URLs
# Find injectHeader function start
inject_idx = code.find('function injectHeader()')
if inject_idx > -1:
    # Find the line before header.innerHTML
    # Insert variable definitions
    open_brace = code.find('{', inject_idx)
    insert_point = open_brace + 1
    lang_detect_js = '''
    var isID = location.pathname.indexOf('/id/') === 0;
    var enUrl = (document.querySelector('link[rel="alternate"][hreflang="en"]') || {}).href || base + '/';
    var idUrl = (document.querySelector('link[rel="alternate"][hreflang="id"]') || {}).href || base + '/id/';
'''
    if 'var isID = location.pathname' not in code:
        code = code[:insert_point] + lang_detect_js + code[insert_point:]
        print('Lang detection JS injected')

# Add CSS for language dropdown - find existing <style> end
style_end = code.find('</style>')
if style_end > -1:
    lang_css = '''
/* === Language Switcher in Navbar === */
header.sx-hf-v5 .sx-hf-v5-lang .sx-hf-v5-dropbtn {
  font-family: 'IBM Plex Mono', ui-monospace, monospace !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em;
  padding: 6px 12px !important;
  margin-left: 8px;
  border: 1px solid rgba(255,255,255,0.18) !important;
  border-radius: 6px !important;
  background: rgba(255,255,255,0.06) !important;
  min-height: 34px;
}
header.sx-hf-v5 .sx-hf-v5-lang .sx-hf-v5-dropbtn:hover {
  background: rgba(245,158,11,0.18) !important;
  border-color: rgba(245,158,11,0.6) !important;
}
header.sx-hf-v5 .sx-hf-v5-lang .sx-lang-flag {
  font-weight: 700;
  letter-spacing: 0.08em;
}
header.sx-hf-v5 .sx-hf-v5-lang-content {
  min-width: 200px;
  right: 0;
  left: auto;
}
header.sx-hf-v5 .sx-hf-v5-lang-content a,
header.sx-hf-v5 .sx-hf-v5-lang-content .sx-lang-disabled {
  display: flex !important;
  align-items: center;
  gap: 10px;
  padding: 12px 18px !important;
  white-space: nowrap;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
}
header.sx-hf-v5 .sx-hf-v5-lang-content .sx-lang-flag-mini {
  display: inline-block;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 3px 7px;
  background: rgba(245,158,11,0.16);
  color: #FBBF24;
  border-radius: 3px;
  min-width: 28px;
  text-align: center;
}
header.sx-hf-v5 .sx-hf-v5-lang-content .sx-lang-disabled {
  color: rgba(255,255,255,0.4) !important;
  cursor: not-allowed;
  background: transparent !important;
}
header.sx-hf-v5 .sx-hf-v5-lang-content .sx-lang-disabled .sx-lang-flag-mini {
  background: rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.45);
}
header.sx-hf-v5 .sx-hf-v5-lang-content .sx-lang-soon {
  margin-left: auto;
  font-style: normal;
  font-size: 10px;
  font-family: 'IBM Plex Mono', monospace;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #F59E0B;
  background: rgba(245,158,11,0.12);
  padding: 2px 8px;
  border-radius: 3px;
}
/* Mobile - language dropdown sits below other menu items */
@media (max-width:768px) {
  header.sx-hf-v5 .sx-hf-v5-lang .sx-hf-v5-dropbtn {
    margin-left: 0 !important;
    width: 100% !important;
    text-align: left;
    justify-content: space-between;
  }
  header.sx-hf-v5 .sx-hf-v5-lang-content { min-width: auto; right: auto; left: auto; }
}
'''
    if '=== Language Switcher in Navbar' not in code:
        code = code[:style_end] + lang_css + code[style_end:]
        print('Lang switcher CSS injected')

# Push updated snippet
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5153', data=json.dumps({'meta':{'_elementor_code':code}}).encode(), method='POST', headers=HDRS), timeout=60).read()
print(f'Snippet 5153 updated, new size: {len(code)}')

# Purge
print('\n3) Purging cache...')
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-lang-navbar.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
file_put_contents($log, 'done');
if (function_exists('code_snippets')) { code_snippets()->deactivate(5); }
'''
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: purge lang navbar'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
