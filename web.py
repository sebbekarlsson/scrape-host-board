import os
from scrapehost.app import app
import flask_assets
from flask_assets import Environment, Bundle
import subprocess


STATIC_DIR = 'scrapehost/static'

def run():
    try:
        subprocess.Popen(
            'sass --watch {STATIC_DIR}/css/style.scss:{STATIC_DIR}/css/style.css'.format(
                STATIC_DIR=STATIC_DIR
            ),
            shell=True
        )
        
        env = flask_assets.Environment(app)

        # Tell flask-assets where to look for our coffeescript and sass files.
        env.load_path = [
            os.path.join(os.path.dirname(__file__), '{STATIC_DIR}/js'.format(
                STATIC_DIR=STATIC_DIR
            ))
        ]

        env.register(
            'js_all',
            flask_assets.Bundle(
                'utils.js',
                'navbar.js',
                'admin-mobile-menu.js',
                'scraper-editor.js',
                'app.js',
                filters=['jsmin'],
                output='js/packed.js'
            )
        )

        app.run(debug=True, threaded=True)

    except KeyboardInterrupt:
        subprocess.Popen(
            'pkill -f sass',
            shell=True
        )

run()
