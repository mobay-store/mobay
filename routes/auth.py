from flask import Blueprint, render_template, request, redirect, session, flash
from services.user_services import register_user, check_user, check_auth
import

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_number():
    if request.method == "POST":

        if session.get("logged"):
            return redirect("/")
            
        telefone = request.form["telefone"]
        

        telefone = telefone.strip()

        # Apenas números e entre 9 e 12 dígitos
        if not telefone.isdigit():
            flash("O telefone deve conter apenas números.")
            return redirect("/login")
    
        if len(telefone) < 9 or len(telefone) > 12:
            flash("O telefone deve ter entre 9 e 12 dígitos.")
            return redirect("/login")

        session["temp"] = telefone
        if check_user(telefone):
            
            return render_template("pass_form.html", hello="Já tens conta 🥹", telefone=telefone)

        return render_template("name_form.html", telefone=telefone)

    return render_template("number_form.html")


@auth_bp.route("/login/name", methods=["GET", "POST"])
def login_name():
    if request.method == "POST":
        try:
            nome = request.form["nome"].strip()
        
            # Mínimo 5 caracteres
            if len(nome) < 5:
                flash("Nome muito curto.")
                return redirect("/login/name")
        
            # Apenas letras e espaços
            if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome):
                flash("O nome deve conter apenas letras.")
                return redirect("/login/name")
            
            user = register_user(
                nome=nome,
                telefone=session.get("temp"),
                pin=request.form["pin"]
            )

            session["user_id"] = user.id
            session["logged"] = session.get("temp")
            session["temp"] = ""

        
        except Exception as e:
            flash(str(e))
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
