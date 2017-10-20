document.addEventListener('DOMContentLoaded', function(e) {
    var scraper_editor = document.getElementById('scraper-editor');

    if (scraper_editor == null)
        return;

    var scraper_preset_select = document.getElementById('scraper-query-preset');
    var scraper_query_textarea = document.getElementById('scraper-query');

    if (scraper_preset_select != null && scraper_query_textarea != null) {
        scraper_preset_select.addEventListener('change', function(e) {
            scraper_query_textarea.innerHTML = this.options[this.selectedIndex].getAttribute('data-code');
        });
    }
});
