from flask import Blueprint, jsonify, request

from cloudinary.uploader import upload


from commerce import db

from .models import Category, Product

store = Blueprint('store', __name__)


@store.route('/admin/product/create', methods=['POST'])
def api_create_product():
    if request.method == "POST":
        data = request.get_json() or request.form
        product = Product.query.filter_by(
            slug=data.get('slug', '')).first()

        if not product:
            name = data.get('name', '')
            price = data.get('price', '')
            description = data.get('description', '')
            image = data.get('image', None)
            print(image)
            category_id = data.get('category_id', '')
            return add_product(name, description, price, category_id, image)


@store.route('/admin/category/create', methods=['POST'])
def api_create_category():
    if request.method == "POST":
        data = request.get_json() or request.form

        category = Category.query.filter_by(
            slug=data.get('slug', '')).first()

        if not category:
            print(data.get('name', ''))
            return add_category(category_name=data.get('name', ''))


@store.route('/store/categories')
def all_categories():
    return get_categories()


@store.route('/store/products')
def all_products():
    return get_products()


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


def get_categories():
    categories = db.session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


def get_products():
    products = db.session.query(Product).all()
    return jsonify(products=[product.serialize for product in products])
