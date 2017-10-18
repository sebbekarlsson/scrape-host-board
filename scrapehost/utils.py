from functools import wraps
from flask import session, redirect
from scrapehost.mongo import db
from bson.objectid import ObjectId


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
