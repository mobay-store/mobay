from models import Product, db, Transaction, User

from flask import Blueprint, render_template, session, redirect, request, flash
from services.notify import notify

confirm_bp = Blueprint("confirm", __name__)

@confirm_bp.route("/confirm/<int:product_id>")
def confirm(product_id):

    
    product = Product.query.filter_by(id=product_id).first()




    return render_template("confirm.html", product=product)

@confirm_bp.route("/confirm/submit", methods=["POST", "GET"])
def confirm_submit():

    
    if not session.get("logged"):
        return redirect("/login")    
    
    if request.method == "POST":

        destino = request.form.get("destino")

        pin = request.form.get("pin")
        destino = request.form.get("destino")


        product_id = int(request.form.get("product_id"))

        product = Product.query.filter_by(id=product_id).first()

        buyer_id = session.get("user_id")

        user = User.query.get_or_404(buyer_id)

        if pin != user.pin:
            flash("PIN incorreto")
            return redirect(f"/confirm/{product_id}")

        if product.user_id == buyer_id:
            return "Erro fatal"

        seller_id = product.user_id


        transaction = Transaction.query.filter_by(product_id=product_id, buyer_id
        =buyer_id).first()

        if transaction:
            flash("Transacao ja existente")
            return redirect("/transactions")




        transaction = Transaction(
            product_id = product_id,
            buyer_id = buyer_id,
            seller_id = seller_id,
            destino = destino,
        )

        db.session.add(transaction)
        db.session.commit()
        #notify(f"Acao: Confirmacao de compra\n\nUsuario: {user.nome}\nTelefone: {user.telefone}\nProduto: {product.titulo}\nPreco: {product.preco}")
    return redirect("/transactions")




@confirm_bp.route("/confirm/recebido", methods=["POST", "GET"])
def confirm_recepcao():

    
    if not session.get("logged"):
        return redirect("/login")    
    
    if request.method == "POST":

        user = User.query.get_or_404(session.get("user_id"))
        pin = request.form.get("pin")
        product_id = int(request.form.get("product_id"))
        if pin != user.pin:
            flash("PIN Incorreto")
            return redirect("/transactions")
        
        product = Product.query.filter_by(id=product_id).first()
        transaction = Transaction.query.filter_by(product_id=product_id).first()

        if transaction.status == "confirmada":
            return "Confirmada"
        product.status = "inativo"
        transaction.status = "confirmada"


        db.session.commit()
        
        return redirect("/transactions")

    flash("Erro desconhecido")
    return redirect("/transactions")
        
