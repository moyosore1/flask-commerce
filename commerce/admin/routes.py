from flask import Blueprint, jsonify, request
from cloudinary.uploader import upload
from commerce.admin.controllers.category import api_category, api_create_category, api_delete_category, api_edit_category
from commerce.admin.controllers.product import api_create_product, api_delete_product, api_product, api_edit_product
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


@admin.route('/admin/category/edit/<int:id>', methods=['PUT'])
def category_edit(id):
    return api_edit_category(id)


@admin.route('/admin/category/delete/<int:id>', methods=['DELETE'])
def category_delete(id):
    return api_delete_category(id)

@admin.route('/admin/product/edit/<int:id>', methods=['PUT'])
def product_edit(id):
    return api_edit_product(id)

@admin.route('/admin/product/delete/<int:id>', methods=['DELETE'])
def product_delete(id):
    return api_delete_product(id)