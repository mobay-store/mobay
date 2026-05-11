# services/auth_service.py
from werkzeug.security import generate_password_hash
from models import User, db


def check_user(telefone):
    user_exists = User.query.filter_by(telefone=telefone).first()
    if user_exists:
        return 1
    else:
        return 0


def check_auth(telefone, pin):
    user_exists = User.query.filter_by(telefone=telefone).first()
    if not user_exists:
        return 0
    if telefone == user_exists.telefone and user_exists.pin == pin:
        return user_exists
     
     
def get_user(telefone):
    user_exists = User.query.filter_by(telefone=telefone).first()
    if not user_exists:
        return 0
    else:
        return user_exists        


def register_user(nome, telefone, pin):
    # verifica duplicado
    user_exists = User.query.filter_by(telefone=telefone).first()
    if user_exists:
        raise ValueError("Telefone já cadastrado!")



    # cria usuário
    user = User(
        nome=nome,
        telefone=telefone,
        pin=pin
    )

    db.session.add(user)
    db.session.commit()

    return user