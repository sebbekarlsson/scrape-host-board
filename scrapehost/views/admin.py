from flask import Blueprint, render_template, redirect, request
from scrapehost.utils import login_required, get_current_user
from scrapehost.mongo import db
from scrapehost.models import Scraper
from bson.objectid import ObjectId


bp = Blueprint(__name__, __name__, template_folder='templates', url_prefix='/admin')

@bp.route('/')
@login_required
def show():
    return redirect('/admin/scrapers')

@bp.route('/scrapers')
@login_required
def show_scrapers():
    current_user = get_current_user()

    scrapers = list(db.collections.find({
        'structure': '#Scraper',
        'user_id': current_user['_id']
    }))

    return render_template('admin/scrapers.html', scrapers=scrapers)

@bp.route('/scrapers/edit/<scraper_id>', methods=['POST', 'GET'])
@bp.route('/scrapers/edit', methods=['POST', 'GET'], defaults={'scraper_id': None})
@login_required
def show_scrapers_edit(scraper_id):
    current_user = get_current_user()
    scraper = None

    if request.method == 'POST':
        if request.form.get('save'):
            name = request.form.get('scraper-name')
            location = request.form.get('scraper-location')

            if not scraper_id:
                scraper = Scraper(
                    name=name,
                    location=location,
                    user_id=current_user['_id']
                )

                res = db.collections.insert_one(scraper.export())
                scraper_id = str(res.inserted_id)
            else:
                db.collections.update_one({
                    '_id': ObjectId(scraper_id)
                },
                {
                    '$set': {
                        'name': name,
                        'location': location
                    }
                }
                )

    if scraper_id:
        scraper = db.collections.find_one({
            'structure': '#Scraper',
            '_id': ObjectId(scraper_id)
        })

    return render_template('admin/scraper_editor.html', scraper=scraper)

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
