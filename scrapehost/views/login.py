from flask import Blueprint, render_template, request, session, redirect
from scrapehost.mongo import db
from scrapehost.password import check_password


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
