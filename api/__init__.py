import os
from flask import Flask,send_from_directory
from api.configs.config import config_by_name

def create_app():
    app = Flask(__name__,static_url_path='')
    app.config.from_object(config_by_name[os.environ.get("FLASK_ENV", "development")])
    return app