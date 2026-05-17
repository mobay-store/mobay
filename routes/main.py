from flask import Blueprint, render_template, session
from models import Product, db, Transaction
import requests as rq

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def homepage():

    products = Product.query.filter_by(status="ativo").all()
    rq.get("https://api.callmebot.com/facebook/send.php?apikey=vKkkSqQtWSvxeMPv&text=Ola+aqui+fala+mobay")

    return render_template(
        "homepage.html",
        logged=session.get("logged"),
        products=products
    )






@main_bp.route("/produtos", methods=["GET"])
def listar_produtos():

    from flask import request, jsonify

    # -------------------------
    # PARÂMETROS
    # -------------------------
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 4))

    q = request.args.get("q", "").strip()
    category = request.args.get("category")
    sort = request.args.get("sort")

    # -------------------------
    # QUERY BASE
    # -------------------------
    query = Product.query

    # 🔍 SEARCH (título + descrição)
    if q:
        query = query.filter(
            db.or_(
                Product.titulo.ilike(f"%{q}%"),
                Product.descricao.ilike(f"%{q}%")
            )
        )

    # 📦 CATEGORIA
    if category:
        query = query.filter(Product.categoria == category)

    # 🚫 EXCLUIR VENDIDOS
    query = query.filter(Product.status == "ativo")

    # 📅 / 💰 ORDENAÇÃO
    if sort == "price_asc":
        query = query.order_by(Product.preco.asc())

    elif sort == "price_desc":
        query = query.order_by(Product.preco.desc())

    elif sort == "new":
        query = query.order_by(Product.criado_em.desc())

    else:
        query = query.order_by(Product.criado_em.desc())

    # -------------------------
    # PAGINAÇÃO
    # -------------------------
    total_items = query.count()

    produtos = query.offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    base_url = request.host_url.rstrip("/")

    # -------------------------
    # SERIALIZAÇÃO
    # -------------------------
    lista_produtos = [
        {
            "id": p.id,
            "titulo": p.titulo,
            "preco": p.preco,
            "descricao": p.descricao,
            "categoria": p.categoria,
            "provincia": p.provincia,
            "imagem": f"{p.images[0].url}" if p.images else None,
            "vendedor": p.owner.nome if p.owner else None,
            "data_criacao": p.criado_em.strftime("%d/%m/%Y") if p.criado_em else None,
        }
        for p in produtos
    ]

    return jsonify({
        "produtos": lista_produtos,
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "query": q,
        "category": category,
        "sort": sort
    })





"""
@main_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    from sqlalchemy import func
    from flask import request, jsonify

    # Paginação
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 4))

    # Query base (todos produtos)
    query = Product.query

    # 🔥 Filtrar produtos disponíveis (sem venda confirmada)
    query = query.filter(
        ~Product.transactions.any(
            Transaction.status.ilike("confirmado")
        )
    )

    # Totais globais
    total_produtos = query.count()

    total_vendidos = db.session.query(func.count(Product.id))\
        .filter(
            Product.transactions.any(
                Transaction.status.ilike("confirmado")
            )
        ).scalar() or 0

    # Paginação
    produtos = query.offset((page - 1) * per_page).limit(per_page).all()

    base_url = request.host_url.rstrip("/")

    # Serialização
    lista_produtos = [
        {
            "id": p.id,
            "titulo": p.titulo,
            "preco": p.preco,
            "descricao": p.descricao,
            "imagem": f"{base_url}/{p.images[0].url}" if p.images else None,
            "vendedor": p.owner.nome if p.owner else None,
            "data_criacao": p.criado_em.strftime("%d/%m/%Y") if p.criado_em else None,
            "disponivel": not any(
                (t.status or "").lower() == "confirmada"
                for t in p.transactions
            )
        }
        for p in produtos
    ]

    return jsonify({
        "totais": {
            "produtos_disponiveis": total_produtos,
            "produtos_vendidos": total_vendidos
        },
        "produtos": lista_produtos,
        "page": page,
        "per_page": per_page,
        "total_items": total_produtos
    })







@main_bp.route("/produtos/pesquisa", methods=["GET"])
def pesquisar_produtos():
    from sqlalchemy import func
    from flask import request, jsonify

    # parâmetros
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 4))
    q = request.args.get("q", "").strip()

    # query base
    query = Product.query

    # 🔎 filtro de pesquisa (título e descrição)
    if q:
        query = query.filter(
            db.or_(
                Product.titulo.ilike(f"%{q}%"),
                Product.descricao.ilike(f"%{q}%")
            )
        )

    # 🚫 excluir vendidos
    query = query.filter(
        ~Product.transactions.any(
            Transaction.status.ilike("confirmado")
        )
    )

    # totais
    total_items = query.count()

    total_vendidos = db.session.query(func.count(Product.id))\
        .filter(
            Product.transactions.any(
                Transaction.status.ilike("confirmado")
            )
        ).scalar() or 0

    # paginação
    produtos = query.offset((page - 1) * per_page).limit(per_page).all()

    base_url = request.host_url.rstrip("/")

    lista_produtos = [
        {
            "id": p.id,
            "titulo": p.titulo,
            "preco": p.preco,
            "descricao": p.descricao,
            "imagem": f"{p.images[0].url}" if p.images else None,
            "vendedor": p.owner.nome if p.owner else None,
            "data_criacao": p.criado_em.strftime("%d/%m/%Y") if p.criado_em else None,
            "disponivel": True
        }
        for p in produtos
    ]

    return jsonify({
        "totais": {
            "produtos_disponiveis": total_items,
            "produtos_vendidos": total_vendidos
        },
        "produtos": lista_produtos,
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "query": q
    })

"""
