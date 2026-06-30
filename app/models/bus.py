from app.extensions import db


class Bus(db.Model):
    __tablename__ = "buses"

    id = db.Column(db.Integer, primary_key=True)

    bus_name = db.Column(db.String(100), nullable=False)

    bus_number = db.Column(db.String(20), unique=True, nullable=False)

    source = db.Column(db.String(100), nullable=False)

    destination = db.Column(db.String(100), nullable=False)

    departure_time = db.Column(db.String(50))

    arrival_time = db.Column(db.String(50))

    total_seats = db.Column(db.Integer)

    available_seats = db.Column(db.Integer)

    price = db.Column(db.Float)

    bookings = db.relationship("Booking", backref="bus", lazy=True)