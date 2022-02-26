import uuid
from datetime import datetime

from flask import url_for


from slugify import slugify

from commerce import db


class PaginatedAPIMixin(object):

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # paginate(page=None, per_page=None, error_out=True, max_per_page=None) ¶
        resources = query.paginate(page, per_page, False)

        data = {

            'items': [item.serialize for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }

        return data


class Category(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    products = db.relationship('Product', backref='category', lazy=True)

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    # @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }


# db.event.listen(Category.name, 'set', Category.slugify, retval=False)
# # @db.event.listen(Category.name, "after_insert")


class Product(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric())
    description = db.Column(db.Text)
    image = db.Column(db.String(400), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    product_items = db.relationship(
        'OrderItem', backref='product_item', lazy=True)

    def __repr__(self) -> str:
        return f'Product {self.name}'

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'price': self.price,
            'description': self.description,
            'image': self.image,
            'category_id': self.category_id,

        }
    
    # converts Python representation to a model
    def from_dict(self, data):
        # loop through fields that can be set by user 
        # checks if a value was provided by user and sets it
        for field in ['name', 'description', 'category_id', 'price', 'image']:
            if field in data:
                setattr(self, field, data[field])
         


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_ordered = db.Column(db.DateTime, nullable=False)
    order_items = db.relationship('OrderItem', backref='order_item', lazy=True)

    def __init__(self, *args, **kwargs):
        self.date_ordered = datetime.now()


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    order = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        self.date_added = datetime.now()
