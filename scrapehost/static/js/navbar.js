document.addEventListener('DOMContentLoaded', function(e) {
    var navbar = document.getElementById('navbar');

    if (navbar != null) {
        setInterval(function(){
            var y = (window.pageYOffset || document.scrollTop)  - (document.clientTop || 0);
            if (y == null || isNaN(y))
                y = 0;

            var opacity = Math.min(0.5, y * 0.002);
            var rgba = 'rgba(0, 0, 0, '+ opacity +')';

            navbar.querySelector('.site-content').style.backgroundColor = rgba;
        }, 0);
    }
});
