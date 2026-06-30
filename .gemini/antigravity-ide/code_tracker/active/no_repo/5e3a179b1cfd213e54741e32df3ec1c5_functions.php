à<?php

function wpdevs_load_scripts() {
    wp_enqueue_style('wpdevs-style', get_stylesheet_uri(), array(), filemtime(
        get_template_directory() . '/style.css'), 'all');

    wp_enqueue_script('google-fonts', 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap', array(), null);
    wp_enqueue_script('dropdown', get_template_directory_uri() . '/js/dropdown.js', array(), '1.0', true);
}

add_action('wp_enqueue_scripts', 'wpdevs_load_scripts');

register_nav_menus(
    array(
        'wp_devs_main_menu' => 'Main Menu',
        'wp_devs_footer_menu' => 'Footer Menu'
    )
);l lš
š› ›¡
¡¢ ¢Õ
ÕÙ Ùí
íî îÿ
ÿ€ €›
›œ œ£
£¤ ¤³
³¶ 
¶¾ 
¾Í ÍÕ
Õü üƒ
ƒŠ 
Š¡ 
¡Ü 
Üü 
ü… 
… ¦
¦± ±×
×Ü 
Üà 2bfile:///Users/Jeff/Local%20Sites/humweb/wp-devs/app/public/wp-content/themes/wp-devs/functions.php