from models import Chat,db, User, Product, Message
from sqlalchemy import or_

def get_chat(user_id, product_id):

    try:
        product = Product.query.filter_by(user_id=user_id).first()

        chat = Chat.query.filter(
            or_(

                Chat.buyer_id == user_id,
                Chat.seller_id == user_id
            )
        ).order_by(Chat.criado_em.desc()).all()
    except Exception as e:
        chat = None
        print(f"Erro: {e}")



    return chat


def get_conv():
    pass





def get_chats_with_products(user_id):
    from sqlalchemy.orm import aliased
    from sqlalchemy import or_, func

    UserBuyer = aliased(User)
    UserSeller = aliased(User)

    # subquery para pegar a data da última mensagem
    last_message_subquery = db.session.query(
        Message.chat_id,
        func.max(Message.criado_em).label("last_message_date")
    ).group_by(Message.chat_id).subquery()

    data = db.session.query(
        Chat,
        Product,
        UserBuyer,
        UserSeller,
        last_message_subquery.c.last_message_date
    )\
    .join(Product, Chat.product_id == Product.id)\
    .join(UserBuyer, Chat.buyer_id == UserBuyer.id)\
    .join(UserSeller, Chat.seller_id == UserSeller.id)\
    .outerjoin(
        last_message_subquery,
        Chat.id == last_message_subquery.c.chat_id
    )\
    .filter(
        or_(
            Chat.buyer_id == user_id,
            Chat.seller_id == user_id
        )
    )\
    .order_by(
        last_message_subquery.c.last_message_date.desc()
    )\
    .all()

    return data