from urllib.parse import urlsplit
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from loja.ext.database import db
from loja.model import User
from .forms import LoginForm

# Hash gerado uma única vez na inicialização para consumir tempo de CPU comparável
# quando o usuário não existe, mitigando ataques de enumeração por medição de tempo (timing attacks).
_DUMMY_HASH = generate_password_hash("senha_descartavel_para_timing_defense")


def _safe_next(target):
    """Valida se o redirecionamento é interno para evitar vulnerabilidade de Open Redirect."""
    if not target:
        return None
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or not target.startswith("/") or target.startswith("//"):
        return None
    return target


def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(
            db.select(User).filter_by(username=form.username.data.strip())
        ).scalar()

        if user:
            password_ok = user.check_password(form.password.data)
        else:
            check_password_hash(_DUMMY_HASH, form.password.data)
            password_ok = False

        if password_ok:
            login_user(user)
            flash("Autenticação realizada com sucesso.", "success")
            next_url = _safe_next(request.args.get("next"))
            return redirect(next_url or url_for("admin.index"))

        flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html", form=form)


def logout():
    logout_user()
    flash("Você saiu da área administrativa.", "info")
    return redirect(url_for("webui.index"))
