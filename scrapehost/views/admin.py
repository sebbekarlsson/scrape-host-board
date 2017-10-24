from flask import Blueprint, render_template, redirect, request, Response
from scrapehost.utils import login_required, get_current_user, get_scraper_query_presets, get_scraper_plans
from scrapehost.mongo import db
from scrapehost.models import Scraper, Order
from bson.objectid import ObjectId
import json


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
    errors = []
    current_user = get_current_user()
    plans = get_scraper_plans()
    scraper = None

    if request.method == 'POST':
        if request.form.get('delete-data'):
            if scraper_id:
                db.collections.update_one({
                    'structure': '#Scraper',
                    '_id': ObjectId(scraper_id)
                },
                {
                    '$set': {
                        'data': [],
                        'found_urls': [],
                        'url_index': 0
                    }
                }
                )

        if request.form.get('delete'):
            if scraper_id:
                db.collections.remove({
                    'structure': '#Scraper',
                    '_id': ObjectId(scraper_id)
                })

                return redirect('/admin/scrapers')

        if request.form.get('save'):
            name = request.form.get('scraper-name')
            location = request.form.get('scraper-location')
            query = request.form.get('scraper-query')
            plan = request.form.get('scraper-plan')
            status = 0
            domain_restrict = False

            if 'http' not in location:
                errors.append('Location needs to be a valid http/https Address')
            
            if request.form.get('scraper-status'):
                status = 1

            if request.form.get('scraper-domain_restrict'):
                domain_restrict = True

            if len(errors) == 0:
                if not scraper_id:
                    scraper = Scraper(
                        name=name,
                        location=location,
                        user_id=current_user['_id'],
                        status=status,
                        domain_restrict=domain_restrict,
                        query=query,
                        plan=int(plan)
                    )

                    order = Order(
                        object=scraper.export(),
                        user_id=current_user['_id'],
                        price=str(plans[int(plan)]['price']),
                        done=False,
                    )

                    res = db.collections.insert_one(order.export())
                    order_id = str(res.inserted_id)

                    return redirect('/order?order_id={}'.format(order_id))
                    
                else:
                    db.collections.update_one({
                        '_id': ObjectId(scraper_id)
                    },
                    {
                        '$set': {
                            'name': name,
                            'location': location,
                            'status': status,
                            'domain_restrict': domain_restrict,
                            'query': query,
                            'plan': int(plan)
                        }
                    }
                    )

    if scraper_id:
        scraper = db.collections.find_one({
            'structure': '#Scraper',
            '_id': ObjectId(scraper_id)
        })

    
    presets = get_scraper_query_presets()

    return render_template('admin/scraper_editor.html', scraper=scraper, presets=presets, plans=plans, errors=errors)

@bp.route('/scrapers/download/<scraper_id>', methods=['POST', 'get'])
def show_download_scraper_data(scraper_id):
    if scraper_id:
        
        scraper = db.collections.find_one({
            'structure': '#Scraper',
            '_id': ObjectId(scraper_id)
        })

        return Response(json.dumps(scraper['data']),
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename=data.json'})

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
