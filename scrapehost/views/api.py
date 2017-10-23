from flask import Blueprint, render_template, jsonify, request
from scrapehost.mongo import db
from bson.objectid import ObjectId


bp = Blueprint(__name__, __name__, template_folder='templates', url_prefix='/api')

@bp.route('/scraper/<scraper_id>/data')
def show_scraper_data(scraper_id):
    offset = 0
    limit = 100

    if request.args.get('o'):
        args_o = request.args.get('o')

        offset = int(args_o) if args_o.isdigit() else offset

    if request.args.get('l'):
        args_l = request.args.get('l')

        limit = min(int(args_l) if args_l.isdigit() else limit, 100)
    
    try:
        scraper_id = ObjectId(scraper_id)
    except:
        return jsonify({'error': 'invalid id'})

    scraper = db.collections.find_one({
        'structure': '#Scraper',
        '_id': scraper_id
    })

    if not scraper:
        return jsonify({'error': 'Nu such scraper'})

    data = list(scraper['data'])

    data = data[offset:(limit + offset)]

    return jsonify(data)
