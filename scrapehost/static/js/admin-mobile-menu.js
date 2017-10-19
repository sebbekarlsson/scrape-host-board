document.addEventListener('DOMContentLoaded', function(e) {
    var admin_menu_btn = document.getElementById('admin-mobile-menu-btn');

    if (admin_menu_btn == null)
        return;

    var admin_menu = document.getElementById('admin-mobile-menu');

    if (admin_menu == null)
        return;

    admin_menu_btn.addEventListener('click', function(e) {
        if (admin_menu.getAttribute('data-active') == '0')
            admin_menu.setAttribute('data-active', 1);
        else
            admin_menu.setAttribute('data-active', 0);
    });
});
