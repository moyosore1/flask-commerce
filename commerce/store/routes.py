from flask import Blueprint, jsonify, request

from cloudinary.uploader import upload


from commerce import db

from .models import Category, Product

store = Blueprint('store', __name__)


@store.route('/store/product/create', methods=['POST'])
def api_create_product():
    if request.method == "POST":
        # data = request.get_json()
        product = Product.query.filter_by(
            slug=request.args.get('slug', '')).first()

        if not product:
            name = request.args.get('name', '')
            price = request.args.get('price', '')
            description = request.args.get('description', '')
            image = request.files.get('image', None)
            category_id = request.args.get('category_id', '')
            return add_product(name, description, price, category_id, image)

    else:
        return jsonify({"error": "The request payload is not in JSON format"})


@store.route('/admin/category/create', methods=['POST'])
def api_create_category():
    if request.method == "POST":
        data = request.get_json() or request.form

        category = Category.query.filter_by(
            slug=data.get('slug', '')).first()

        if not category:
            print(data.get('name', ''))
            return add_category(category_name=data.get('name', ''))


def add_product(name, description, price, category_id, image=None):
    image_url = 'sth'
    if image is not None:
        cloud_image = upload(image)
        image_url = cloud_image.get('url')

    product = Product(name=name, description=description,
                      price=price, category_id=category_id, image=image_url)
    db.session.add(product)
    db.session.commit()
    return jsonify(Product=product.serialize)


def add_category(category_name):
    category = Category(name=category_name)
    db.session.add(category)
    db.session.commit()
    return jsonify(Category=category.serialize)
