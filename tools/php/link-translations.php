<?php
/**
 * SURIOTA Translation Linker - Temporary Helper
 * 
 * INSTRUCTIONS:
 * 1. Upload this file to: /wp-content/plugins/suriota-link-translations.php
 * 2. Go to WordPress Admin > Plugins > Installed Plugins
 * 3. Activate "SURIOTA Translation Linker"
 * 4. The plugin will auto-run and link all translations
 * 5. Deactivate and delete the plugin after use
 * 
 * This links the 5 new pillar pages (EN/ID/ZH) as Polylang translations.
 */

if (!defined('ABSPATH')) exit;

function suriota_link_all_translations() {
    if (!function_exists('pll_save_post_translations') || !function_exists('pll_set_post_language')) {
        error_log('SURIOTA Translation Linker: Polylang functions not available');
        return;
    }
    
    $groups = array(
        // Pillar 1: Industrial IoT & System Integration
        array('en' => 5554, 'id' => 5566, 'zh' => 5571),
        // Pillar 2: AI & Industrial Analytics
        array('en' => 5555, 'id' => 5567, 'zh' => 5572),
        // Pillar 3: Digital Transformation Consulting
        array('en' => 5556, 'id' => 5568, 'zh' => 5573),
        // Pillar 4: Industrial Engineering & Automation
        array('en' => 5557, 'id' => 5569, 'zh' => 5574),
        // Pillar 5: SURGE SaaS Platform
        array('en' => 5558, 'id' => 5570, 'zh' => 5575),
    );
    
    $linked = 0;
    foreach ($groups as $group) {
        // Verify all posts exist
        $valid = true;
        foreach ($group as $lang => $post_id) {
            if (!get_post($post_id)) {
                error_log("SURIOTA Translation Linker: Post ID {$post_id} not found");
                $valid = false;
                break;
            }
            pll_set_post_language($post_id, $lang);
        }
        if ($valid) {
            pll_save_post_translations($group);
            $linked++;
            error_log('SURIOTA Translation Linker: Linked group ' . json_encode($group));
        }
    }
    
    error_log("SURIOTA Translation Linker: Completed. Linked {$linked}/5 groups.");
}

// Run on activation
register_activation_hook(__FILE__, 'suriota_link_all_translations');

// Also add admin notice
add_action('admin_notices', function() {
    $screen = get_current_screen();
    if ($screen && $screen->id === 'plugins') {
        echo '<div class="notice notice-success"><p><strong>SURIOTA Translation Linker:</strong> ';
        echo 'If you just activated this plugin, check the error log for linking results. ';
        echo 'You can now deactivate and delete this plugin.</p></div>';
    }
});
