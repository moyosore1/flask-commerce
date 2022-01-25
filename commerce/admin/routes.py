from flask import Blueprint, jsonify, request
from cloudinary.uploader import upload
from commerce.admin.controllers.category import api_category, api_create_category
from commerce.admin.controllers.product import api_create_product, api_product
from .auth import token_auth



admin = Blueprint('admin', __name__)


@admin.route('/admin/product', methods=['GET'])
# @token_auth.login_required
def product_load():
    data = api_product()
    return data

@admin.route('/admin/category', methods=['GET'])
# @token_auth.login_required
def category_load():
    data = api_category()
    return data


@admin.route('/admin/product/create', methods=['POST'])
# @token_auth.login_required
def product_create():
    data = api_create_product()
    return data
    


@admin.route('/admin/category/create', methods=['POST'])
# @token_auth.login_required
def category_create():
    data = api_create_category()
    return data



