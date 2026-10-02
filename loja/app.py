from flask import Flask, redirect, url_for
from loja.ext import database, admin, appearance, configuration, auth, commands
from loja.blueprints import webui, restapi, auth as auth_bp

def create_app(**config): 

    app = Flask(__name__, template_folder='templates')
    configuration.init_app(app, **config)
    database.init_app(app)
    appearance.init_app(app)
    auth.init_app(app)
    admin.init_app(app)
    commands.init_app(app)
    webui.init_app(app)
    restapi.init_app(app)
    auth_bp.init_app(app)

    @app.route("/")
    def index():
        return redirect(url_for("webui.index"))

    return app
