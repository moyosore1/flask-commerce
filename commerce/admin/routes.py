from flask import Blueprint, jsonify, request

from cloudinary.uploader import upload


from commerce import db
from commerce.errors import bad_request

from commerce.store.models import Product, Category

admin = Blueprint('admin', __name__)


@admin.route('/admin/product/create', methods=['POST'])
def api_create_product():
    if request.method == "POST":
        data = request.get_json() or request.form

        fields = ['name', 'price', 'description', 'category_id']
        for field in fields:
            if field not in data:
                print(f'Ran check for {field}')
                message = f'{field} is required'
                return bad_request(message)

        name = data.get('name', '')
        price = data.get('price', '')
        description = data.get('description', '')
        image = data.get('image', None)
        print(image)
        category_id = data.get('category_id', '')
        return add_product(name, description, price, category_id, image)


@admin.route('/admin/category/create', methods=['POST'])
def api_create_category():
    if request.method == "POST":
        data = request.get_json() or request.form

        category = Category.query.filter_by(
            slug=data.get('slug', '')).first()

        if 'name' not in data:
            return bad_request('name is required')

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
