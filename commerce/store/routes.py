from flask import Blueprint, jsonify, request

from cloudinary.uploader import upload


from commerce import db

from .models import Category, Product


ROWS_PER_PAGE = 7

store = Blueprint('store', __name__)


@store.route('/api/<string:slug>/products')
def api_category_products(slug):
    return get_products_in_category(slug)


@store.route('/api/store/categories')
def api_all_categories():
    return get_categories()


@store.route('/api/store/products')
def api_all_products():
    return get_products()


def get_categories():
    categories = db.session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


# using the slug of the category, get products in said category
def get_products_in_category(slug):
    page = request.args.get('page', 1, type=int)

    # gets the category_id of the category
    category_id = Category.query.filter_by(slug=slug).first_or_404(
        description=f'There is no category with slug {slug}').id
    products = Product.query.filter_by(category_id=category_id).paginate(
        page=page, per_page=ROWS_PER_PAGE)
    paginated_products = (products.items)
    results = [product.serialize() for product in paginated_products]

    return jsonify({'results': results, 'count': len(paginated_products)})


def get_products():
    page = request.args.get('page', 1, type=int)
    data = Product.to_collection_dict(Product.query, page, ROWS_PER_PAGE,
                                      'store.api_all_products')
    return jsonify(data)


def get_product(slug):
    product = Product.query.filter_by(slug=slug).first_or_404(
        description=f'There is no product with slug {slug}')
    return jsonify(product.serialize)
