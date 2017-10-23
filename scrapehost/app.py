from flask import Flask
from scrapehost.utils import is_loggedin
from scrapehost.views.api import bp as api_bp
from scrapehost.views.index import bp as index_bp
from scrapehost.views.register import bp as register_bp
from scrapehost.views.login import bp as login_bp 
from scrapehost.views.admin import bp as admin_bp 
from scrapehost.views.siteposts import bp as siteposts_bp 


app = Flask(__name__)

app.config.update(
    SECRET_KEY='abc123',
    TEMPLATES_AUTO_RELOAD=True
)

app.register_blueprint(api_bp)
app.register_blueprint(index_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(siteposts_bp)

app.jinja_env.globals.update(is_loggedin=is_loggedin)
