from flask import Blueprint, render_template, request, redirect, session, flash
from services.product_service import get_product
from models import Product, ProductImage, db, User
import os, uuid
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader



from PIL import Image
import io

cloudinary.config(
    cloud_name="di5xpqgcx",
    api_key="243372635448879",
    api_secret="zdabFGmgS3xQ7GQK055XDs2-vXg"
)



def upload_image(file):

    print("Aquiiiiiiiiiiiiiiiiii")
    filename = secure_filename(file.filename)

    img = Image.open(file)

    # converte para RGB
    if img.mode != "RGB":
        img = img.convert("RGB")

    img.thumbnail((800, 800))

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=70)
    buffer.seek(0)

    result = cloudinary.uploader.upload(
        buffer,
        public_id=filename.rsplit(".", 1)[0],
        folder="products"
    )

    print("De novooooooooooooooooooooo", result)

    return result["secure_url"]


product_bp = Blueprint("product", __name__)

UPLOAD_FOLDER = "static/uploads"

@product_bp.route("/p/<slug>")
def product_page(slug):
    data = get_product(slug)
    buyer_id = session.get("user_id")
    return render_template("product.html", product=data, buyer_id=buyer_id, criado_em = data.criado_em.strftime("%d %b %Y"))


@product_bp.route("/vender", methods=["GET", "POST"])
def add_product():
    from models import User

    if not session.get("logged"):
        return redirect("/login")

    if request.method == "POST":
        files = request.files.getlist("images")
        valid_files = [f for f in files if f and f.filename != ""]

        if not valid_files:
            return "Adiciona pelo menos uma imagem"

        user = User.query.filter_by(telefone=session["logged"]).first()
        if not user:
            return redirect("/login")

        try:
            preco = float(request.form["preco"])
        except:
            return "Preço inválido"

        product = Product(
            user_id=user.id,
            titulo=request.form["titulo"],
            preco=preco,
            descricao=request.form.get("descricao"),
            categoria=request.form.get("categoria"),
            provincia = request.form.get("provincia"),
        )

        db.session.add(product)
        db.session.flush()  # evita commit precoce

        for file in valid_files[:3]:
            try:
                image_url = upload_image(file)
                

                db.session.add(ProductImage(
                    product_id=product.id,
                    url=image_url
                ))

            except Exception as e:
                return f"Erro na imagem:, {e}"
                

        db.session.commit()

        return redirect(f"/p/{product.id}")

    return render_template("add_product.html")



@product_bp.route("/stock")
def stock():


    if not session.get("logged"):
        return redirect("/login")    
    products = Product.query.filter_by(user_id=session.get("user_id"), status="ativo").all()
    return render_template("stock.html", products=products)


@product_bp.route("/loja/<user_id>")
def loja(user_id):

    products = Product.query.filter_by(user_id=user_id, status="ativo").all()
    user = User.query.get_or_404(user_id)
    owner = user.nome
    return render_template("my_store.html", products=products, owner=owner)


@product_bp.route("/del-prod", methods=["POST", "GET"])
def del_prod():
    user_id = session.get("user_id")
    product_id = request.form.get("product_id")
    pin = request.form.get("pin")


    if not user_id:
        return redirect("/login")
    product = Product.query.get_or_404(product_id)

    if user_id != product.user_id:
        return "Bitch"


    user = User.query.get_or_404(user_id)

    if user.pin != pin:
        flash("PIN incorrecto", "error")
        return redirect("/stock")
    # 1. apagar arquivos físicos primeiro
    for img in product.images:
        if img.url and os.path.exists(img.url):
            try:
                os.remove(img.url)
            except Exception as e:
                print("Erro ao apagar imagem:", e)

    # 2. depois apagar do banco
    db.session.delete(product)
    db.session.commit()

    return redirect("/stock")
