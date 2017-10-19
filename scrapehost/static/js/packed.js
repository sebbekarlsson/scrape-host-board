document.addEventListener('DOMContentLoaded',function(e){var navbar=document.getElementById('navbar');if(navbar!=null){if(navbar.className.indexOf('navbar-contrast')<=0){setInterval(function(){var y=(window.pageYOffset||document.scrollTop)-(document.clientTop||0);if(y==null||isNaN(y))
y=0;var opacity=Math.min(0.5,y*0.002);var rgba='rgba(0, 0, 0, '+opacity+')';navbar.style.backgroundColor=rgba;},0);}}});document.addEventListener('DOMContentLoaded',function(e){var admin_menu_btn=document.getElementById('admin-mobile-menu-btn');if(admin_menu_btn==null)
return;var admin_menu=document.getElementById('admin-mobile-menu');if(admin_menu==null)
return;admin_menu_btn.addEventListener('click',function(e){if(admin_menu.getAttribute('data-active')=='0')
admin_menu.setAttribute('data-active',1);else
admin_menu.setAttribute('data-active',0);});});