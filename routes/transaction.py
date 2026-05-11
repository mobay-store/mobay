from flask import Blueprint, render_template, session, redirect
from models import Transaction, Product, db
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


@transaction_bp.route("/confirm_receipt/<int:id>")
def confirm_receipt(id):

    if not session.get("logged"):
        return redirect("/login")
    
    transaction = Transaction.query.filter_by(id=int(id)).first()
    transaction.status = "confirmada"
    db.session.commit()

    return redirect("/transactions")