from models import Product
from PIL import Image
import os

from sqlalchemy.orm import joinedload

def get_product(slug):
    product = Product.query.options(
        joinedload(Product.owner),
        joinedload(Product.images)
    ).filter_by(id=int(slug)).first()
    print(product.owner.nome)
    return product



