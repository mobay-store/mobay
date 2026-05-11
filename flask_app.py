from flask import Flask
from models import db
from routes import register_blueprints   # 👈 novo

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'dev-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 👇 aqui muda tudo
    register_blueprints(app)

    return app


app = create_app()


with app.app_context():
    db.create_all()
