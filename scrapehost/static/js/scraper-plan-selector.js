document.addEventListener('DOMContentLoaded', function(e) {
    var scraper_plan_selector = document.getElementById('scraper-plan-selector');

    if (scraper_plan_selector == null)
        return;

    var plan_selector_input = scraper_plan_selector.querySelector('input');
    var cards = scraper_plan_selector.querySelectorAll('.card');

    for (var i = 0; i < cards.length; i++) {
        cards[i].addEventListener('click', function(e) {
            for (var i = 0; i < cards.length; i++) {
                cards[i].setAttribute('data-selected', 0);
            }
            
            this.setAttribute('data-selected', 1);
            plan_selector_input.value = this.getAttribute('data-id');
        });
    }
});
