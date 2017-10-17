from flask import Blueprint, render_template 


bp = Blueprint(__name__, __name__, template_folder='templates')

@bp.route('/login')
def show():
    return render_template('login.html')
