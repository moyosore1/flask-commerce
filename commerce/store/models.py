import uuid
from datetime import datetime

from slugify import slugify

from commerce import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    products = db.relationship('Product', backref='category', lazy=True)

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }


# db.event.listen(Category.name, 'set', Category.slugify, retval=False)
# # @db.event.listen(Category.name, "after_insert")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(5, 2))
    description = db.Column(db.Text)
    image = db.Column(db.String(200), nullable=True)
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
