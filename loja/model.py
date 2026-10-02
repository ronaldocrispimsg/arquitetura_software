from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from loja.ext.database import db, SerializerMixin, mapped_column, Mapped


class Product(db.Model, SerializerMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(unique=True)
    price: Mapped[float]


class User(db.Model, UserMixin):
    """Usuário com acesso à interface administrativa.

    A senha é armazenada de forma segura, gravando apenas o hash criptográfico
    gerado com salt individual (scrypt), nunca em texto puro.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]

    def set_password(self, password: str) -> None:
        """Gera o hash da senha usando werkzeug.security (scrypt por padrão)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Compara a senha informada com o hash armazenado."""
        return check_password_hash(self.password_hash, password)


def populate_db():
    # Verifica se a tabela já possui produtos antes de popular
    if db.session.execute(db.select(Product).limit(1)).first():
        return

    products = [
        Product(id=1, description="Resistor 470 ohms", price=0.05),
        Product(id=2, description="Arduino Nano R3", price=50.00),
        Product(id=3, description="Raspberry PI 3", price=200.00),
    ]

    db.session.add_all(products)
    db.session.commit()
