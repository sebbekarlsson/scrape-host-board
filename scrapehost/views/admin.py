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
