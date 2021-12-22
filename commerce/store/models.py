from slugify import slugify

from commerce import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(255))
    products = db.relationship('Product', backref='category', lazy=True)

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    # db.event.listen(Category.name, 'set', Category.slugify, retval=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(5, 2))
    description = db.Column(db.Text)
    image = db.Column(db.String(200), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)

    def __repr__(self) -> str:
        return '<Product %r>' % self.name
