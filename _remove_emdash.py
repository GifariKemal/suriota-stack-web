"""Remove em dash (—) globally — pages, AIOSEO meta, snippets."""
import sys, io, json, urllib.request, base64, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Replacement strategy (order matters — longest first)
REPS = [
    (' \u2014 ', ' - '),         # em dash with surrounding spaces → hyphen with spaces
    ('\u2014', '-'),              # bare em dash → hyphen
    (' &mdash; ', ' - '),         # HTML entity with spaces
    ('&mdash;', '-'),             # HTML entity bare
    (' \\u2014 ', ' - '),         # JSON-escaped form
    ('\\u2014', '-'),             # JSON-escaped bare
]

def replace_text(s):
    if not isinstance(s, str): return s, 0
    count = 0
    for o, n in REPS:
        if o in s:
            count += s.count(o)
            s = s.replace(o, n)
    return s, count


# ===== All page IDs =====
EN_PAGES = [12, 29, 839, 1127, 945, 5039, 5260, 37, 35, 39, 5029, 5037, 5033, 934, 1542, 1546, 1547, 1740, 1741, 1742, 1765, 929]
ID_PAGES = [5273, 5274, 5275, 5276, 5277, 5278, 5279, 5281, 5282, 5283, 5284, 5285, 5286, 5287, 5288, 5289, 5290, 5291, 5292, 5293, 5294, 5295]
ALL_PAGES = EN_PAGES + ID_PAGES

print(f'Processing {len(ALL_PAGES)} pages...')

total_replacements = 0
pages_changed = 0
for pid in ALL_PAGES:
    try:
        r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=id,content,meta', headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    except Exception as e:
        print(f'  {pid}: fetch fail {e}')
        continue

    changes = 0
    payload_meta = {}

    # 1) Content (raw HTML)
    content_raw = d.get('content', {}).get('raw', '')
    new_content, c1 = replace_text(content_raw)
    payload_content = None
    if c1 > 0:
        payload_content = new_content
        changes += c1

    # 2) _elementor_data (raw JSON string with embedded text)
    ed = d.get('meta', {}).get('_elementor_data', '')
    if not isinstance(ed, str): ed = json.dumps(ed)
    new_ed, c2 = replace_text(ed)
    if c2 > 0:
        payload_meta['_elementor_data'] = new_ed
        changes += c2

    if changes > 0:
        payload = {}
        if payload_content is not None: payload['content'] = payload_content
        if payload_meta: payload['meta'] = payload_meta
        try:
            urllib.request.urlopen(urllib.request.Request(
                f'https://suriota.com/wp-json/wp/v2/pages/{pid}',
                data=json.dumps(payload).encode(), method='POST', headers=HDRS
            ), timeout=60).read()
            print(f'  page {pid}: {changes} em-dashes replaced')
            total_replacements += changes
            pages_changed += 1
        except Exception as e:
            print(f'  page {pid}: push fail {e}')

print(f'\nPages: {pages_changed}/{len(ALL_PAGES)} updated, {total_replacements} total replacements')


# ===== Update AIOSEO meta via PHP =====
print('\nUpdating AIOSEO meta...')
aioseo_php = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/emdash-aioseo.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
global $wpdb;
$table = $wpdb->prefix . 'aioseo_posts';
$rows = $wpdb->get_results("SELECT post_id, title, description FROM $table WHERE title LIKE '%\xe2\x80\x94%' OR description LIKE '%\xe2\x80\x94%'");
$updated = 0;
foreach ($rows as $r) {
    $new_t = str_replace([' \xe2\x80\x94 ', '\xe2\x80\x94'], [' - ', '-'], $r->title);
    $new_d = str_replace([' \xe2\x80\x94 ', '\xe2\x80\x94'], [' - ', '-'], $r->description);
    if ($new_t !== $r->title || $new_d !== $r->description) {
        $wpdb->update($table, ['title' => $new_t, 'description' => $new_d, 'updated' => current_time('mysql')], ['post_id' => $r->post_id]);
        $updated++;
    }
}
file_put_contents($log, "AIOSEO updated: $updated rows @ " . date('c'));

// Clear caches
if (function_exists('aioseo')) {
    $a = aioseo();
    if (isset($a->core->cache) && method_exists($a->core->cache, 'clear')) $a->core->cache->clear();
}
if (class_exists('\\\\Elementor\\\\Plugin')) {
    foreach ([12,29,839,1127,945,5039,5260,37,35,39,5029,5037,5033,934,1542,1546,1547,1740,1741,1742,1765,929,5273,5274,5275,5276,5277,5278,5279,5281,5282,5283,5284,5285,5286,5287,5288,5289,5290,5291,5292,5293,5294,5295] as $pid) {
        $f = \\Elementor\\Core\\Files\\CSS\\Post::create($pid);
        if ($f) { $f->delete(); $f->update(); }
    }
    \\Elementor\\Plugin::instance()->files_manager->clear_cache();
}
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
if (function_exists('code_snippets')) { code_snippets()->deactivate(5); }
'''
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':aioseo_php, 'active':True, 'name':'SX: emdash AIOSEO'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(2)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('AIOSEO meta cleaned + cache purged')


# ===== Update Elementor snippets =====
print('\nUpdating Elementor snippets (custom content)...')
# Get list of all snippets
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet?per_page=50&_fields=id,title&status=publish', headers=HDRS)
snips = json.loads(urllib.request.urlopen(r).read())
snip_changes = 0
for s in snips:
    sid = s['id']
    try:
        rs = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/elementor_snippet/{sid}?context=edit&_fields=id,meta', headers=HDRS)
        sd = json.loads(urllib.request.urlopen(rs, timeout=30).read())
        code = sd.get('meta', {}).get('_elementor_code', '')
        if not code: continue
        new_code, count = replace_text(code)
        if count > 0:
            payload = json.dumps({'meta': {'_elementor_code': new_code}}).encode()
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/elementor_snippet/{sid}', data=payload, method='POST', headers=HDRS), timeout=60).read()
            print(f'  snippet {sid} ({s["title"]["rendered"][:40]}): {count} em-dashes replaced')
            snip_changes += count
    except Exception as e:
        pass
print(f'\nSnippets: {snip_changes} replacements')

# Final purge
purge2 = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/emdash-final.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
file_put_contents($log, 'done @ ' . date('c'));
if (function_exists('code_snippets')) { code_snippets()->deactivate(5); }
'''
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge2, 'active':True, 'name':'SX: final purge emdash'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('\nFinal cache purge done')
