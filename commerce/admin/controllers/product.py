from flask import Blueprint, jsonify, request
from cloudinary.uploader import upload
from werkzeug.http import HTTP_STATUS_CODES

from math import prod
from unicodedata import category

from commerce import db
from commerce.errors import bad_request
from commerce.store.models import Product


# -------------------------------Controllers
def api_product():
    product = Product.query.order_by(Product.id).all()
    return jsonify([*map(product_serializer, product)])


def api_create_product():
    if request.method == "POST":
        data = request.get_json() or request.form

        name = data['name']
        price = data['price']
        description = data['description']
        image = request.files['image'] or None
        category_id = data['category_id']
        return add_product(name, description, price, category_id, image)


def api_edit_product(id):
    if request.method == "PUT":
        product = Product.query.get_or_404(id)
        data = request.get_json() or request.form
        product.from_dict(data)
        db.session.commit()
        return jsonify(product.serialize)


def api_delete_product(id):
    if request.method == "DELETE":
        product = Product.query.get_or_404(id)
        name = product.name
        db.session.delete(product)
        db.session.commit()
        return jsonify({"Success": f'Successfully deleted product {name}'}), HTTP_STATUS_CODES.get(204)
# -----------------------------------Controllers


#  ---------------------------- Helper Functions
def product_serializer(product):
    return{
        "id": product.id,
        "name": product.name,
        "description": product.slug,
        "image": product.image,
        "category": product.category_id
    }


def add_product(name, description, price, category_id, image=None):
    if image:
        cloud_image = upload(image)
        image_url = cloud_image.get('secure_url')
    product = Product(name=name, description=description,
                      price=price, category_id=category_id, image=image_url)
    db.session.add(product)
    db.session.commit()
    return jsonify({
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image': product.image,
        ' category': product.category_id
    })


# ----------------------------------Helper Functions
