import click
from loja.ext.database import db
from loja.model import User

MIN_PASSWORD_LENGTH = 8


def init_app(app):
    @app.cli.command("create-user")
    @click.argument("username")
    @click.password_option(confirmation_prompt=True, help="Senha do usuário.")
    def create_user(username, password):
        """Cria um usuário com acesso à interface administrativa.

        A senha é informada de forma oculta no terminal (não exposta no histórico
        nem no código) e armazenada de forma segura com hash criptográfico (scrypt).
        """
        if len(password) < MIN_PASSWORD_LENGTH:
            raise click.ClickException(
                f"A senha deve ter ao menos {MIN_PASSWORD_LENGTH} caracteres."
            )
        if db.session.execute(db.select(User).filter_by(username=username)).scalar():
            raise click.ClickException(f"O usuário '{username}' já existe.")

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Usuário '{username}' criado com sucesso.")
