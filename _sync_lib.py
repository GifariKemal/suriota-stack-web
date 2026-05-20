"""Robust translation pipeline — walks Elementor JSON tree, applies translations to widget settings."""
import json, urllib.request, urllib.error, base64, sys, io, time

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Settings keys that contain translatable text
TRANSLATABLE_KEYS = ['title', 'editor', 'text', 'html', 'button_text', 'sub_heading', 'subtitle',
                     'caption', 'placeholder', 'label', 'description', 'content', 'message',
                     'field_label', 'before_text', 'after_text', 'header_text', 'item_description',
                     'tab_title', 'tab_content']


def fetch_page(post_id):
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{post_id}?context=edit&_fields=meta,template', headers=HDRS)
    return json.loads(urllib.request.urlopen(r, timeout=60).read())


def push_page(post_id, elementor_data, page_settings=None):
    payload_meta = {'_elementor_data': elementor_data if isinstance(elementor_data, str) else json.dumps(elementor_data),
                    '_elementor_edit_mode': 'builder',
                    '_elementor_template_type': 'wp-page'}
    if page_settings:
        payload_meta['_elementor_page_settings'] = page_settings
    payload = json.dumps({'meta': payload_meta}).encode()
    req = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{post_id}', data=payload, method='POST', headers=HDRS)
    return urllib.request.urlopen(req, timeout=60).read()


def apply_translations_to_tree(node, trans_dict, stats):
    """Walk Elementor JSON tree, apply translations to widget settings."""
    if isinstance(node, list):
        for n in node:
            apply_translations_to_tree(n, trans_dict, stats)
        return
    if not isinstance(node, dict):
        return

    if node.get('widgetType'):
        settings = node.get('settings', {})
        for key in TRANSLATABLE_KEYS:
            if key in settings and isinstance(settings[key], str):
                original = settings[key]
                new = original
                for en, id_text in trans_dict.items():
                    if en in new:
                        new = new.replace(en, id_text)
                        stats['replacements'] += 1
                if new != original:
                    settings[key] = new
                    stats['widgets_changed'].add(node.get('id', ''))

    for child in node.get('elements', []) or []:
        apply_translations_to_tree(child, trans_dict, stats)


def purge_page_cache(page_id):
    purge = f'''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-sync-{page_id}.txt";
if (file_exists($log)) {{ if (function_exists('code_snippets')) {{ code_snippets()->deactivate(5); }} return; }}
if (class_exists('\\\\Elementor\\\\Plugin')) {{
    $f = \\Elementor\\Core\\Files\\CSS\\Post::create({page_id});
    if ($f) {{ $f->delete(); $f->update(); }}
    \\Elementor\\Plugin::instance()->files_manager->clear_cache();
}}
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
file_put_contents($log, 'done');
if (function_exists('code_snippets')) {{ code_snippets()->deactivate(5); }}
'''
    data = json.dumps({'code': purge, 'active': True, 'name': f'SX: purge {page_id}'}).encode()
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=data, method='POST', headers=HDRS), timeout=60).read()
    time.sleep(2)


def sync_page(en_id, id_id, trans_dict, page_label='', trigger_url=None):
    """Full sync: fetch EN, translate, push to ID, purge cache."""
    print(f'\n=== Sync EN {en_id} → ID {id_id} [{page_label}] ===')
    en = fetch_page(en_id)
    ed = en['meta']['_elementor_data']
    if not isinstance(ed, str):
        ed = json.dumps(ed)
    page_settings = en['meta'].get('_elementor_page_settings', {})

    try:
        tree = json.loads(ed)
    except Exception as e:
        print(f'  parse fail: {e}')
        return False

    stats = {'replacements': 0, 'widgets_changed': set()}
    apply_translations_to_tree(tree, trans_dict, stats)

    new_ed = json.dumps(tree, separators=(',', ':'))
    print(f'  EN size: {len(ed)} → ID size: {len(new_ed)}')
    print(f'  Replacements applied: {stats["replacements"]}')
    print(f'  Widgets changed: {len(stats["widgets_changed"])}')

    push_page(id_id, new_ed, page_settings)
    print(f'  Pushed to ID page {id_id}')

    purge_page_cache(id_id)
    if trigger_url:
        try:
            urllib.request.urlopen(urllib.request.Request(trigger_url + '?cb=' + str(int(time.time())), headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read()
            print(f'  Triggered {trigger_url}')
        except: pass
    return True
