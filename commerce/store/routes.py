from flask import Blueprint, jsonify, request

from cloudinary.uploader import upload


from commerce import db

from .models import Category, Product

store = Blueprint('store', __name__)

ROWS_PER_PAGE = 7


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


# using the slug of the category, get products in said category
def get_products_in_category(slug):
    page = request.args.get('page', 1, type=int)

    # gets the category_id of the catego
    category_id = Category.query.filter_by(slug=slug).first_or_404(
        description=f'There is no category with slug {slug}').id
    products = Product.query.filter_by(category_id=category_id).paginate(
        page=page, per_page=ROWS_PER_PAGE)
    paginated_products = (products.items)
    results = [product.serialize() for product in paginated_products]

    return jsonify({'results': results, 'count': len(paginated_products)})


def get_products():
    products = db.session.query(Product).all()
    return jsonify(products=[product.serialize for product in products])
