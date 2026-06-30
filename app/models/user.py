from app.extensions import db
from flask_login import UserMixin
from flask import flash
from flask import redirect
from flask import url_for

from flask_login import current_user



from app.models.booking import Booking

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    bookings = db.relationship("Booking", backref="user", lazy=True)