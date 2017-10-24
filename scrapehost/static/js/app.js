document.addEventListener('DOMContentLoaded', function(e) {
    var save_buttons = document.querySelectorAll('input[name="save"]');


    for (var i = 0; i < save_buttons.length; i++) {
        save_buttons[i].addEventListener('click', function(e) {
            window.loading_screen = window.pleaseWait({
                logo: "",
                backgroundColor: '#6CCAA3',
                loadingHtml: '<div class="spinner"><div class="dot1"></div><div class="dot2"></div></div>' 
            });
        });
    }
});
