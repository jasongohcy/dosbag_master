from flask_assets import Bundle

bundles = {

    'home_js': Bundle(
        'js/vendor/jquery-3.3.1.js',
        'js/vendor/popper.js',
        'js/vendor/bootstrap-4.1.3.js',
        'js/custom.js',
        filters='jsmin',
        output='gen/home.%(version)s.js'),

    'home_css': Bundle(
        'css/vendor/bootstrap-4.1.3.css',
        'css/custom.css',
        filters='cssmin',
        output='gen/home.%(version)s.css'),

    'homepage_js': Bundle(
        'assets/web/assets/jquery/jquery.min.js',
        'assets/popper/popper.min.js',
        'assets/tether/tether.min.js',
        'assets/smoothscroll/smooth-scroll.js',
        'assets/dropdown/js/script.min.js',
        'assets/touchswipe/jquery.touch-swipe.min.js',
        'assets/viewportchecker/jquery.viewportchecker.js',
        'assets/parallax/jarallax.min.js',
        'assets/formoid/formoid.min.js',
        'assets/theme/js/script.js',
        'assets/bootstrap/js/bootstrap.min.js',
        filters='jsmin',
        output='gen/home_page.%(version)s.js'),


    'homepage_css': Bundle(
        'assets/bootstrap/css/bootstrap.min.css',
        'assets/bootstrap/css/bootstrap-grid.min.css',
        'assets/bootstrap/css/bootstrap-reboot.min.css',
        'assets/animatecss/animate.min.css',
        'assets/web/assets/mobirise-icons/mobirise-icons.css',
        'assets/tether/tether.min.css',
        'assets/dropdown/css/style.css',
        'assets/socicon/css/styles.css',
        'assets/theme/css/style.css',
        'assets/mobirise/css/mbr-additional.css',
        filters='cssmin',
        output='gen/home_page.%(version)s.css')
        
    # 'admin_js': Bundle(
    #     'js/lib/jquery-1.10.2.js',
    #     'js/lib/Chart.js',
    #     'js/admin.js',
    #     output='gen/admin.js'),

    # 'admin_css': Bundle(
    #     'css/lib/reset.css',
    #     'css/common.css',
    #     'css/admin.css',
    #     output='gen/admin.css')
}
