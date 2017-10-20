from flask import Blueprint, render_template
from jinja2.exceptions import TemplateNotFound


bp = Blueprint(__name__, __name__, template_folder='templates', url_prefix='/site-posts')

@bp.route('/<post_name>')
def show(post_name):
    template_filename = 'site-posts/{}.html'.format(post_name)

    try:
        return render_template(template_filename)
    except TemplateNotFound:
        return render_template('404.html'), 404
