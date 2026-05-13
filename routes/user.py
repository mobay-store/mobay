from flask import Blueprint, render_template, session, redirect, request, flash
from services.user_services import get_user
from models import db, Carteira, User

user_bp = Blueprint("user", __name__)

@user_bp.route("/profile")
def profile():
    session["current"] = "/profile"

    if session.get("logged"):
        user = get_user(session["user_id"])
        return render_template("profile.html", user=user)

    return redirect("/login")


@user_bp.route("/seller")
def seller():
    return render_template("seller_profile.html")

@user_bp.route("/payments")
def payments():

    user_id = session.get("user_id")
    if not session.get("logged"):
        return redirect("/login")
    carteira = Carteira.query.filter_by(user_id=user_id).first()
    return render_template("payments.html", carteira=carteira)



@user_bp.route("/remover-pay")
def rem_pay():

    user_id = session.get("user_id")
    if not session.get("logged"):
        return redirect("/login")

    carteira = Carteira.query.filter_by(user_id=user_id).first()

    db.session.delete(carteira)
    db.session.commit()
    return redirect("/payments")


@user_bp.route("/add-pay", methods=["POST", "GET"])
def add_pay():

    erro = ""
    user_id = session.get("user_id")
    if not session.get("logged"):
        return redirect("/login")
    
    if request.method == "POST":
        operadora = request.form.get("operadora")
        telefone = request.form.get("telefone")
        pin = request.form.get("pin")

        carteira = Carteira.query.filter_by(user_id=user_id).first()
        user = User.query.filter_by(id=user_id).first()

        if pin == user.pin:
            
            carteira = Carteira(user_id=user_id,operadora=operadora, telefone=telefone)
            db.session.add(carteira)
            db.session.commit()
            return redirect("/payments")
        else:
            flash("PIN incorreto", "erro")
            return redirect("/add-pay")




    return render_template("add-pay.html", erro = erro)
