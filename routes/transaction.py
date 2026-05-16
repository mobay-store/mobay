from flask import Blueprint, render_template, session, redirect, flash, request
from models import Transaction, Product, db, User
from sqlalchemy import or_

transaction_bp = Blueprint("transaction", __name__)

@transaction_bp.route("/transactions")
def transactions():
    session["current"] = "/transactions"

    if not session.get("logged"):
        return redirect("/login")
        
    user_id = session.get("user_id")

    transactions = Transaction.query.filter(or_(Transaction.buyer_id == user_id,Transaction.seller_id == user_id)).all()
    

    return render_template("transactions.html", transactions = transactions)


@transaction_bp.route("/confirm_receipt", methods=["POST", "GET"])
def confirm_receipt():

    if not session.get("logged"):
        return redirect("/login")

    product_id = request.form.get("product_id")

    transaction_id = request.form.get("transaction_id")

    pin = request.form.get("pin")

    user = User.query.get_or_404(session.get("user_id"))

    if user.pin != pin:

        flash("PIN incorrecto")

        return redirect("/transactions")

    transaction = Transaction.query.filter_by(
        id=int(transaction_id)
    ).first()

    product = Product.query.filter_by(
        id=int(product_id)
    ).first()

    transaction.status = "confirmada"

    product.status = "inactivo"

    db.session.commit()

    # -------------------------
    # EMAIL
    # -------------------------

    current_app.send_email(

        "Pagamento confirmado",

        f"""
Pagamento confirmado.

Transaction ID:
{transaction.id}

Produto:
{product.title}

Produto ID:
{product.id}

Status:
{transaction.status}
"""
    )

    return redirect("/transactions")
