from flask import redirect, url_for, request
from flask_babel import Babel
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_admin.menu import MenuLink
from flask_login import current_user

from loja.ext.database import db
from loja.model import Product


class AuthMixin:
    """Exige usuário autenticado para visualização e operações no admin."""

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Redireciona para o login repassando a URL de destino desejada
        return redirect(url_for("auth.login", next=request.full_path.rstrip("?")))


class SecureAdminIndexView(AuthMixin, AdminIndexView):
    pass


class SecureModelView(AuthMixin, ModelView):
    form_base_class = SecureForm  # Ativa proteção CSRF nos formulários do admin


def init_app(app):
    babel = Babel(app)
    admin = Admin(app, index_view=SecureAdminIndexView())
    admin.add_view(SecureModelView(Product, db.session))
    admin.add_link(MenuLink(name="Ver Loja", url="/"))
    admin.add_link(MenuLink(name="Sair", endpoint="auth.logout"))
