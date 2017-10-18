from flask import Blueprint, render_template, redirect
from scrapehost.utils import login_required


bp = Blueprint(__name__, __name__, template_folder='templates', url_prefix='/admin')

@bp.route('/')
@login_required
def show():
    return redirect('/admin/scrapers')

@bp.route('/scrapers')
@login_required
def show_scrapers():
    return render_template('admin/scrapers.html')

@bp.route('/scrapers/edit/<scraper_id>', methods=['POST', 'GET'])
@bp.route('/scrapers/edit', methods=['POST', 'GET'], defaults={'scraper_id': None})
@login_required
def show_scrapers_edit(scraper_id):
    return render_template('admin/scraper_editor.html')

@bp.route('/messages')
@login_required
def show_messages():
    return render_template('admin/messages.html')

@bp.route('/api')
@login_required
def show_api():
    return render_template('admin/api.html')

@bp.route('/settings')
@login_required
def show_settings():
    return render_template('admin/settings.html')
