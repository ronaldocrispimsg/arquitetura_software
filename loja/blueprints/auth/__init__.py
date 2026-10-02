from flask import Blueprint
from .views import login, logout

bp = Blueprint("auth", __name__, template_folder="templates")

bp.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
bp.add_url_rule("/logout", view_func=logout, methods=["GET"])


def init_app(app):
    app.register_blueprint(bp)
