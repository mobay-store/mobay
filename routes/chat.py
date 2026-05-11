from flask import Blueprint, render_template, session, redirect, request
from models import Product, Chat, Message, db
from services.chat_service import get_chats_with_products
chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat/<int:product_id>")
def open_chat(product_id):
    if not session.get("logged"):
        return redirect("/login")


    product = Product.query.get(product_id)

    chat = Chat.query.filter_by(product_id=product.id, buyer_id=session.get("user_id")).first()
    print(chat, session.get("user_id"))


    if chat:
        messages = get_chats_with_products(session.get("user_id"))
        return render_template("chat.html",  messages=messages, product=product)

    return render_template("chat.html", product=product)



from sqlalchemy.exc import IntegrityError

@chat_bp.route("/send-message", methods=["POST"])
def send_msg():
    data = request.get_json()

    user_id = session.get("logged")
    product_id = data.get("product_id")
    content = data.get("conteudo")

    if not user_id:
        return {"error": "not authenticated"}, 401

    if not product_id or not content:
        return {"error": "missing data"}, 400

    product = Product.query.get_or_404(product_id)

    # impedir enviar mensagem para si mesmo
    if product.user_id == user_id:
        return {"error": "cannot message yourself"}, 403

    # tentar encontrar chat existente
    chat = Chat.query.filter_by(
        product_id=product_id,
        buyer_id=user_id,
        seller_id=product.user_id
    ).first()

    # criar chat se não existir
    if not chat:
        chat = Chat(
            product_id=product_id,
            buyer_id=user_id,
            seller_id=product.user_id
        )

        try:
            db.session.add(chat)
            db.session.flush()  # pega ID sem commit
        except IntegrityError:
            db.session.rollback()
            chat = Chat.query.filter_by(
                product_id=product_id,
                buyer_id=user_id,
                seller_id=product.user_id
            ).first()

    # criar mensagem
    message = Message(
        chat_id=chat.id,
        sender_id=user_id,
        receiver_id=product.user_id,
        conteudo=content
    )

    db.session.add(message)
    db.session.commit()

    return {
        "success": True,
        "chat_id": chat.id
    }



@chat_bp.route("/chat/send", methods=["POST"])
def send_message():
    data = request.get_json()

    product_id = data["product_id"]
    content = data["conteudo"]
    chat_id = data["chat_id"]


    sender_id = session["user_id"]

    product = Product.query.filter_by(id=product_id).first()

    seller_id = product.user_id

    chat = Chat.query.filter_by(product_id=product.id, buyer_id=session.get("user_id")).first()
    if chat:
        old_chat = chat
    else:

        old_chat = Chat.query.filter_by(id=int(chat_id)).first()

    if not old_chat:
        print("I'm in")
        chat = Chat(
            product_id=product_id,
            buyer_id=sender_id,
            seller_id=seller_id
        )
        db.session.add(chat)
        db.session.commit()
    else:
        chat = old_chat

    print(chat)
    message = Message(
        chat_id=chat.id,
        sender_id=sender_id,
        receiver_id = seller_id if sender_id != seller_id else chat.buyer_id,
        conteudo=content
    )

    db.session.add(message)
    db.session.commit()

    return {"status": "ok"}

@chat_bp.route("/mensagens")
def mensagens():
    data = get_chats_with_products(session.get("user_id"))

    result = []
    user_id = session.get("user_id")

    for chat, product, buyer, seller, last_date in data:

        if buyer.id == user_id:
            other = seller
        else:
            other = buyer

        # pega a última mensagem do chat
        last_message = Message.query\
            .filter_by(chat_id=chat.id)\
            .order_by(Message.criado_em.desc())\
            .first()

        result.append({
            "chat_id": chat.id,
            "product_id": product.id,
            "product": product.titulo,
            "other_name": other.nome,
            "message": last_message.conteudo if last_message else "",
            "last_date": last_message.criado_em.strftime("%H:%M - %d/%m/%Y") if last_message else None
        })

    return render_template("messages.html", messages=result)








@chat_bp.route("/chat/res/<string:parameters>")
def chat_res(parameters):
    if not session.get("user_id"):
        return redirect("/login")
    print(parameters)
    data=parameters.split("+")
    product_id = data[1]
    buyer_id = data[2]
    chat_id = data[0]


    if chat_id != "None":
        print(f"Erro: {chat_id}")
        chat = Chat.query.filter_by(id=int(chat_id)).first()
        messages = Message.query.filter_by(chat_id=chat.id)
        product = Product.query.filter_by(id=int(product_id)).first()

        return render_template("chat.html", messages=messages, product=
        product, chat_id=chat.id)




    chat = Chat.query.filter_by(product_id=int(product_id), buyer_id=int(buyer_id)).first()

    if chat:
        product = Product.query.filter_by(id=int(product_id)).first()
        messages = Message.query.filter_by(chat_id=chat.id)

        return render_template("chat.html", messages=messages, product=
        product)

    product = Product.query.filter_by(id=int(product_id)).first()
    return render_template("chat.html", product=product)



