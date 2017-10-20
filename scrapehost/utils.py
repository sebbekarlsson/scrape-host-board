from functools import wraps
from flask import session, redirect
from scrapehost.mongo import db
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
import glob
import os


def is_loggedin():
    if not 'user_id' in session:
        return False

    return session['user_id'] is not None

def get_current_user():
    if not is_loggedin():
        return None

    return db.collections.find_one({
        'structure': '#User',
        '_id': ObjectId(session['user_id'])
    })

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def get_scraper_query_presets():
    presets = []
    presets_files = glob.glob('scrapehost/scraping/presets/*.py')

    for preset in presets_files:
        with open(preset) as pfile:
            presets.append({'name': os.path.basename(preset), 'code': pfile.read()})
        pfile.close()

    return presets

def get_scraper_plans():
    return [
        {
            "name": "basic",
            "price": 40,
            "data_slots": 1200,
            "code_lines": 25
        },
        {
            "name": "standard",
            "price": 50,
            "data_slots": 10000,
            "code_lines": 100
        },
        {
            "name": "Professional",
            "price": 90,
            "data_slots": 100000,
            "code_lines": 1000
        }
    ]
