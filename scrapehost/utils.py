from functools import wraps
from flask import session, redirect
from scrapehost.mongo import db
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
import glob
import os
import json


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

def agreement_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        redir = False
        
        if 'accepted_agreement' not in user:
            redir = True
        else:
            if not user['accepted_agreement']:
                redir = True

        if redir:
            return redirect('/admin/agreement')
        
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
    with open('pricing.json') as pricingfile:
        pricing_obj = json.loads(pricingfile.read())
    pricingfile.close()

    return pricing_obj['scraper_plans']

def get_user_agreement():
    content = ''

    with open('user-agreement.txt') as agreementfile:
        content = agreementfile.read()
    agreementfile.close()

    return content
