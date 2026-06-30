from app.extensions import db
from datetime import datetime


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    bus_id = db.Column(db.Integer, db.ForeignKey("buses.id"))

    seat_number = db.Column(db.String(10))

    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(20), default="Booked")