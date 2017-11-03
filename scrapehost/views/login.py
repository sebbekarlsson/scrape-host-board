from flask import Blueprint, render_template, request, session, redirect
from scrapehost.mongo import db
from scrapehost.password import check_password, get_hashed_password
from scrapehost.utils import get_random_token 


bp = Blueprint(__name__, __name__, template_folder='templates')

@bp.route('/login', methods=['POST', 'GET'])
def show():
    errors = []

    if request.method == 'POST':
        if request.form.get('login'):
            email = request.form.get('user-email')
            password = request.form.get('user-password')

            existing = db.collections.find_one({
                'structure': '#User',
                'email': email
            })

            if not existing:
                errors.append('No user with that email')
            
            if len(errors) == 0:
                if check_password(existing['password'], password):
                    session['user_id'] = str(existing['_id'])

                    return redirect('/admin/scrapers')
                else:
                    errors.append('Wrong password')

    return render_template('login.html', errors=errors)

@bp.route('/logout', methods=['POST', 'GET'])
def show_logout():
    session['user_id'] = None
    del session['user_id']

    return redirect('/')

@bp.route('/forgot-password', methods=['POST', 'GET'])
def show_forgot_password():
    msg = None

    if request.method == 'POST':
        if request.form.get('forgot'):
            email = request.form.get('user-email')
            forgot_password_token = get_random_token()
            
            db.collections.update_one({
                'structure': '#User',
                'email': email
            },
            {
                '$set': {
                    'forgot_password_token': forgot_password_token    
                }
            }
            )

            msg = 'We have sent you an email'

    return render_template('forgot_password.html', msg=msg)

@bp.route('/reset-password/<forgot_password_token>', methods=['POST', 'GET'])
def show_reset_password(forgot_password_token):
    errors = []
    msg = None

    existing_user = db.collections.find_one({
        'structure': '#User',
        'forgot_password_token': forgot_password_token
    })

    if not existing_user:
        return 'Access Denied'

    if request.method == 'POST':
        if request.form.get('reset'):
            new_password = request.form.get('user-password')

            db.collections.update_one({
                'structure': '#User',
                '_id': existing_user['_id']
            },
            {
                '$set': {
                    'password': get_hashed_password(new_password),
                    'forgot_password_token': None
                }
            })

            msg = 'Password has been changed'

    return render_template('reset_password.html', msg=msg)
