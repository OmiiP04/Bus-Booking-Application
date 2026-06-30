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