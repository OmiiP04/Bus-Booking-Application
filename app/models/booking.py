from datetime import datetime
from app.extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    bus_id = db.Column(
        db.Integer,
        db.ForeignKey("buses.id"),
        nullable=False
    )

    passenger_name = db.Column(
        db.String(100),
        nullable=False
    )

    passenger_age = db.Column(
        db.Integer,
        nullable=False
    )

    passenger_gender = db.Column(
        db.String(10),
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    travel_date = db.Column(
        db.Date,
        nullable=False
    )

    seat_number = db.Column(
        db.Integer,
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        default="Booked"
    )