from flask import Blueprint, render_template, jsonify
from scrapehost.mongo import db
from bson.objectid import ObjectId


bp = Blueprint(__name__, __name__, template_folder='templates', url_prefix='/api')

@bp.route('/scraper/data/<scraper_id>')
def show_scraper_data(scraper_id):
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

    return jsonify(scraper['data'])
