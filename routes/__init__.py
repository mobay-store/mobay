from .auth import auth_bp
from .product import product_bp
from .user import user_bp
from .main import main_bp
from .chat import chat_bp
from .transaction import transaction_bp
from .confirm import confirm_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(confirm_bp)