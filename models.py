from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# =====================
# USER
# =====================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False, index=True)
    foto = db.Column(db.String(255))
    pin = db.Column(db.String(128), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship(
        "Product",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy=True
    )

# =====================
# PRODUCT
# =====================
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), default="geral", index=True)
    provincia = db.Column(db.String(50), nullable=False)

    status = db.Column(db.String(20), default="ativo")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # relações
    owner = db.relationship("User", back_populates="products")

    images = db.relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy=True
    )

    transactions = db.relationship(
        "Transaction",
        back_populates="product",
        cascade="all, delete-orphan"
    )

# =====================
# PRODUCT IMAGE
# =====================
class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    url = db.Column(db.String(255), nullable=False)

    product = db.relationship("Product", back_populates="images")

# =====================
# CHAT
# =====================
class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        lazy=True
    )

    __table_args__ = (
        db.UniqueConstraint("product_id", "buyer_id", "seller_id"),
    )

# =====================
# MESSAGE
# =====================
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    conteudo = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), default="texto")

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    chat = db.relationship("Chat", back_populates="messages")

# =====================
# TRANSACTION
# =====================
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    destino = db.Column(db.String(50), nullable=False)

    status = db.Column(db.String(20), default="pendente")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # RELAÇÃO CORRIGIDA (sem conflito)
    product = db.relationship("Product", back_populates="transactions")

# =====================
# REVIEW
# =====================
class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    rating = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("rating >= 1 AND rating <= 5"),
    )

# =====================
# REPORT
# =====================
class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)

    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    motivo = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

# =====================
# CARTEIRA
# =====================
class Carteira(db.Model):
    __tablename__ = "carteiras"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    operadora = db.Column(db.String(10), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)