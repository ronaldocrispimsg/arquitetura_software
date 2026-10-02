from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Formulário de login com proteção CSRF integrada."""
    username = StringField("Usuário", validators=[DataRequired(message="Informe o usuário.")])
    password = PasswordField("Senha", validators=[DataRequired(message="Informe a senha.")])
