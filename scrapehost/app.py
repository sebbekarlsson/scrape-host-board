from flask import Flask
from scrapehost.views.index import bp as index_bp
from scrapehost.views.register import bp as register_bp
from scrapehost.views.login import bp as login_bp 


app = Flask(__name__)

app.config.update(
    SECRET_KEY='abc123',
    TEMPLATES_AUTO_RELOAD=True
)

app.register_blueprint(index_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
