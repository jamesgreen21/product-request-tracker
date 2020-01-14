from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extensions import db
from datetime import datetime

class User(UserMixin, db.Model):
    """
    The User model contains username and password along with the user type.
    The User Type field: 1=Admin,1=Health&Safety, 2=Quality, 3=Cagefill, 4=Restaurant.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    user_type = db.Column(db.Integer)
    admin = db.Column(db.Boolean, default=False)

    requests_created = db.relationship('Posts',
                               foreign_keys='Posts.user_id',
                               backref='published_by',
                               lazy=True)

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password!')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)


class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(80), nullable=False)


class ProductType(db.Model):
    """
    Create a model for the Product Type table (tracker_post: one-to-many)
    """
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String(50), nullable=False)
    chamber = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)


class Posts(db.Model):
    """
    The Post model is the master list of all Product Requests. The Action
    fields (healthandsafety, quality, cagefill, restaurantimpact) are
    denoted by: 0=No Actions, 1=Fail, 2=In-progress, 3=Pass. 
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'),
        nullable=False)
    contact_name = db.Column(db.String(50), unique=True)
    new_product = db.Column(db.Boolean, default=False)
    product_number = db.Column(db.Integer)
    product_name = db.Column(db.String(80), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'),
        nullable=False)
    product_length = db.Column(db.Integer)
    product_width = db.Column(db.Integer)
    product_height =db.Column(db.Integer)
    product_weight = db.Column(db.Float)
    case_orientation = db.Column(db.Boolean, default=False)
    units_per_case = db.Column(db.Float)
    healthandsafety = db.Column(db.Integer, default=0)
    quality = db.Column(db.Integer, default=0)
    cagefill = db.Column(db.Integer, default=0)
    restaurantimpact = db.Column(db.Integer, default=0)
    complete = db.Column(db.Boolean, default=False)


class Actions(db.Model):
    """
    The Action model is used for creating and answering actions for each
    Product Request. The Approval field is: 1=Fail, 2=In-progress, 3=Pass.
    The Stage field is: 1=Health&Safety, 2=Quality, 3=Cagefill, 4=Restaurant.
    This has a many-to-one relationship with the Posts model
    """
    id = db.Column(db.Integer, primary_key=True)
    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'),
        nullable=False)
    stage = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=True)
    approval = db.Column(db.Integer, default=2)
    image = db.Column(db.String(80), nullable=True)
    layer_type = db.Column(db.String(50), nullable=True)
    case_per_layer = db.Column(db.Integer, default=0)
    total_layers = db.Column(db.Integer, default=0)
