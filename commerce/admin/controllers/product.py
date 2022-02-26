from math import prod
from unicodedata import category
from flask import Blueprint, jsonify, request
from cloudinary.uploader import upload
from commerce import db
from commerce.errors import bad_request
from commerce.store.models import Product

# -------------------------------Controllers
def api_product():
    product = Product.query.all()
    return jsonify([*map(product_serializer, product)])

def api_create_product():
    if request.method == "POST":
        data = request.get_json() or request.form

        name = data['name']
        price = data['price']
        description = data['description']
        image = request.files['image']
        category_id = data['category_id']
        return add_product(name, description, price, category_id, image)


def api_edit_product(id):
    if request.method == "PUT":
        product = Product.query.get_or_404(id)
        data = request.get_json() or request.form
        product.from_dict(data)
        db.session.commit()
        print(product.to_dict())
        return jsonify(product.to_dict())
#-----------------------------------Controllers


#  ---------------------------- Helper Functions
def product_serializer(product):
    return{
        "id": product.id,
        "name": product.name,
        "description": product.slug,
        "image": product.image,
        "category": product.category_id
    }

def add_product(name, description, price, category_id, image):
    cloud_image = upload(image)
    image_url = cloud_image.get('secure_url')
    print(image_url)
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


#----------------------------------Helper Functions
