from flask import Blueprint, render_template, request, redirect, session, flash
from services.user_services import register_user, check_user, check_auth

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_number():
    if request.method == "POST":

        if session.get("logged"):
            return redirect("/")
        telefone = request.form["telefone"]
        session["temp"] = telefone

        if check_user(telefone):
            return render_template("pass_form.html", hello="Já tens conta 🥹", telefone=telefone)

        return render_template("name_form.html", telefone=telefone)

    return render_template("number_form.html")


@auth_bp.route("/login/name", methods=["GET", "POST"])
def login_name():
    if request.method == "POST":
        try:
            user = register_user(
                nome=request.form["nome"],
                telefone=session.get("logged"),
                pin=request.form["pin"]
            )

            session["user_id"] = user.id
            session["logged"] = telefone
        except Exception as e:
            flash(e)
            return redirect("/login/name")

        return redirect(session.get("current", "/"))

    return render_template("name_form.html")


@auth_bp.route("/pass", methods=["GET", "POST"])
def login_pass():
    if request.method == "POST":
        auth = check_auth(session.get("temp"), request.form["pin"])
        if auth:

            session["user_id"] = auth.id
            session["logged"] = auth.telefone
            session["temp"] = ""
            session["workwith"] = ""
            return redirect(session.get("current", "/"))
        else:
            flash("PIN incorrecto")
            return redirect("/pass")



    return render_template("pass_form.html")


@auth_bp.route("/sair")
def sair():
    session.clear()
    return redirect("/")
