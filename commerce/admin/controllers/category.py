import os

from unicodedata import category
from flask import Blueprint, jsonify, request
from werkzeug.http import HTTP_STATUS_CODES

from commerce import db
from commerce.errors import bad_request
from commerce.store.models import  Category


def api_category():
    category = Category.query.all()
    return jsonify([*map(category_serializer, category)])

def api_create_category():
    if request.method == "POST":
        data = request.get_json() or request.form

        category = Category.query.filter_by(
            name=data['name']).first()

        if 'name' not in data:
            return bad_request('name is required')

        if category:
            return "Category already exists"
        else:
            print(data['name'])
            result = add_category(data['name'])
            return result, HTTP_STATUS_CODES.get(201)

def api_edit_category(id):
    if request.method == "PUT":
        category = Category.query.get_or_404(id)
        data = request.json() or request.form
        if 'name' in data:
            category.name = data.get("name")
            db.session.commit()
            return jsonify(category_serializer(category)), HTTP_STATUS_CODES.get(200)

def api_delete_category(id):
    if request.method == "DELETE":
        category = Category.query.get_or_404(id) 
        name = category.name   
        db.session.delete(category)
        db.session.commit()
        return jsonify({"Success": f'Successfully deleted product {name}'}), HTTP_STATUS_CODES.get(204)

def category_serializer(category):
    return{
        "id": category.id,
        "name": category.name,
        "slug": category.slug
    }


def add_category(category_name):
    category = Category(name=category_name)
    pick = jsonify({
        'name': category.name,
        'slug': category.slug
    })
    db.session.add(category)
    db.session.commit()
    return pick