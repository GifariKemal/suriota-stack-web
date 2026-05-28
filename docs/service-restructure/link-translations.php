<?php
/**
 * SURIOTA Polylang Translation Linker
 * 
 * Upload ke: /wp-content/plugins/suriota-link-translations.php
 * Jalankan via browser: https://suriota.com/wp-content/plugins/suriota-link-translations.php?run=1&token=secure123
 * 
 * ATAU gunakan WP-CLI:
 * wp eval-file /path/to/wp-content/plugins/suriota-link-translations.php
 */

if (!defined('ABSPATH')) {
    require_once dirname(__FILE__) . '/../../../wp-load.php';
}

// Simple token check for browser access
if (php_sapi_name() !== 'cli' && (!isset($_GET['token']) || $_GET['token'] !== 'secure123')) {
    wp_die('Access denied. Add ?token=secure123 to run.');
}

if (!function_exists('pll_set_post_language') || !function_exists('pll_save_post_translations')) {
    wp_die('Polylang plugin is not active.');
}

$translations = [
    'p1' => ['en' => 5554, 'id' => 5566, 'zh' => 5571],
    'p2' => ['en' => 5555, 'id' => 5567, 'zh' => 5572],
    'p3' => ['en' => 5556, 'id' => 5568, 'zh' => 5573],
    'p4' => ['en' => 5557, 'id' => 5569, 'zh' => 5574],
    'p5' => ['en' => 5558, 'id' => 5570, 'zh' => 5575],
];

$results = [];
foreach ($translations as $group => $langs) {
    foreach ($langs as $lang => $post_id) {
        $post = get_post($post_id);
        if (!$post) {
            $results[] = "❌ Post $post_id not found";
            continue;
        }
        pll_set_post_language($post_id, $lang);
        $results[] = "✅ Set post $post_id ({$post->post_title}) to language: $lang";
    }
    pll_save_post_translations($langs);
    $results[] = "🔗 Linked translation group $group: " . json_encode($langs);
}

// Output
if (php_sapi_name() === 'cli') {
    echo implode("\n", $results) . "\n";
} else {
    header('Content-Type: text/plain; charset=utf-8');
    echo "=== SURIOTA Polylang Translation Linker ===\n\n";
    echo implode("\n", $results) . "\n";
    echo "\n=== DONE ===\n";
    echo "You can now delete this file from /wp-content/plugins/\n";
}
