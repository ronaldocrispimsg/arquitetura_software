from flask_login import LoginManager
from loja.ext.database import db

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from loja.model import User
    return db.session.get(User, int(user_id))


def init_app(app):
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar a área administrativa."
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"
    login_manager.init_app(app)
