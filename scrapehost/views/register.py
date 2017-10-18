from flask import Blueprint, render_template, request, redirect
from scrapehost.mongo import db
from scrapehost.models import User


bp = Blueprint(__name__, __name__, template_folder='templates')

@bp.route('/register', methods=['POST', 'GET'])
def show():
    password_len = 8
    errors = []

    if request.method == 'POST':
        if request.form.get('register'):
            email = request.form.get('user-email')
            password = request.form.get('user-password')
            password_confirm = request.form.get('user-password-confirm')

            if '@' not in email:
                errors.append('Invalid email')

            if len(password) < password_len:
                errors.append('Password needs to be at least {} characters.'.\
                        format(password_len))

            if password != password_confirm:
                errors.append('Passwords does not match')

            existing = db.collections.find_one({
                'structure': '#User',
                'email': email
            })

            if existing:
                errors.append('User with email already exists')

            if len(errors) == 0:
                user = User(
                    email=email,
                    password=password
                )

                res = db.collections.insert_one(user.export())

                if res.inserted_id:
                    return redirect('/login?user_id={}'.format(res.inserted_id))

    return render_template('register.html', errors=errors)
