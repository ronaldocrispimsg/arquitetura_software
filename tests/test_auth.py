import os
import tempfile
import pytest
from loja.app import create_app
from loja.ext.database import db
from loja.model import User, Product


@pytest.fixture
def app():
    temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_db_path = temp_db.name
    temp_db.close()

    app = create_app(
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{temp_db_path}",
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test-secret-key",
    )
    with app.app_context():
        db.create_all()
        user = db.session.execute(db.select(User).filter_by(username="admin")).scalar()
        if not user:
            user = User(username="admin")
            user.set_password("SenhaForte123@")
            db.session.add(user)
            db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

    if os.path.exists(temp_db_path):
        try:
            os.remove(temp_db_path)
        except OSError:
            pass


@pytest.fixture
def client(app):
    return app.test_client()


def test_public_routes(client):
    # Loja e API continuam públicas
    res_loja = client.get("/main/v1/")
    assert res_loja.status_code == 200

    res_api = client.get("/api/v1/product/")
    assert res_api.status_code == 200


def test_admin_requires_authentication(client):
    # Acesso a /admin/ sem estar logado redireciona para login
    res = client.get("/admin/", follow_redirects=False)
    assert res.status_code == 302
    assert "/login" in res.headers["Location"]


def test_login_invalid_credentials(client):
    res = client.post(
        "/login",
        data={"username": "admin", "password": "senha_errada"},
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert "Usuário ou senha inválidos" in res.get_data(as_text=True)


def test_login_success_and_admin_access(client):
    res = client.post(
        "/login?next=/admin/",
        data={"username": "admin", "password": "SenhaForte123@"},
        follow_redirects=True,
    )
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "Produtos" in html or "Início" in html or "Sair" in html

    # Acessa admin autenticado
    res_admin = client.get("/admin/")
    assert res_admin.status_code == 200


def test_logout(client):
    # Efetua login
    client.post(
        "/login",
        data={"username": "admin", "password": "SenhaForte123@"},
        follow_redirects=True,
    )
    # Efetua logout
    res_logout = client.get("/logout", follow_redirects=True)
    assert res_logout.status_code == 200
    assert "Você saiu da área administrativa" in res_logout.get_data(as_text=True)

    # Verifica que o admin voltou a ficar bloqueado
    res_admin = client.get("/admin/", follow_redirects=False)
    assert res_admin.status_code == 302
    assert "/login" in res_admin.headers["Location"]
