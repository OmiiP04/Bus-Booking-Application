from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user

from app.extensions import db
from app.models.bus import Bus
from app.models.booking import Booking

from datetime import datetime

user = Blueprint("user", __name__)


# ---------------- Dashboard ---------------- #

@user.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# ---------------- Search Bus ---------------- #

@user.route("/search", methods=["GET", "POST"])
@login_required
def search_bus():

    if request.method == "POST":

        source = request.form["source"]
        destination = request.form["destination"]

        buses = Bus.query.filter_by(
            source=source,
            destination=destination
        ).all()

        return render_template(
            "search_result.html",
            buses=buses
        )

    return render_template("search_bus.html")


# ---------------- Passenger Details ---------------- #

@user.route("/passenger/<int:bus_id>", methods=["GET", "POST"])
@login_required
def passenger(bus_id):

    bus = Bus.query.get_or_404(bus_id)

    if request.method == "POST":

        session["booking"] = {
            "passenger_name": request.form["passenger_name"],
            "passenger_age": request.form["passenger_age"],
            "passenger_gender": request.form["passenger_gender"],
            "phone": request.form["phone"],
            "travel_date": request.form["travel_date"]
        }

        return redirect(url_for("user.select_seat", id=bus.id))

    return render_template(
        "passenger_details.html",
        bus=bus
    )


# ---------------- Select Seat ---------------- #

@user.route("/book/<int:id>")
@login_required
def select_seat(id):

    bus = Bus.query.get_or_404(id)

    booked = Booking.query.filter_by(
        bus_id=id,
        status="Booked"
    ).all()

    booked_seats = [b.seat_number for b in booked]

    return render_template(
        "select_seat.html",
        bus=bus,
        booked_seats=booked_seats
    )


# ---------------- Confirm Booking ---------------- #

@user.route("/confirm-booking/<int:bus_id>/<int:seat>")
@login_required
def confirm_booking(bus_id, seat):

    bus = Bus.query.get_or_404(bus_id)

    existing = Booking.query.filter_by(
        bus_id=bus_id,
        seat_number=seat,
        status="Booked"
    ).first()

    if existing:
        flash("Seat already booked!", "danger")
        return redirect(url_for("user.select_seat", id=bus_id))

    booking_data = session.get("booking")

    if not booking_data:
        flash("Please enter passenger details first.", "warning")
        return redirect(url_for("user.passenger", bus_id=bus_id))

    booking = Booking(
        user_id=current_user.id,
        bus_id=bus.id,
        passenger_name=booking_data["passenger_name"],
        passenger_age=int(booking_data["passenger_age"]),
        passenger_gender=booking_data["passenger_gender"],
        phone=booking_data["phone"],
        travel_date=datetime.strptime(
            booking_data["travel_date"],
            "%Y-%m-%d"
        ).date(),
        seat_number=seat,
        status="Booked"
    )

    db.session.add(booking)

    bus.available_seats -= 1

    db.session.commit()

    session.pop("booking", None)

    flash("Ticket Booked Successfully!", "success")

    return redirect(url_for("user.my_bookings"))


# ---------------- My Bookings ---------------- #

@user.route("/my-bookings")
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )


# ---------------- Cancel Booking ---------------- #

@user.route("/cancel-booking/<int:id>")
@login_required
def cancel_booking(id):

    booking = Booking.query.get_or_404(id)

    if booking.user_id != current_user.id:
        flash("Unauthorized!", "danger")
        return redirect(url_for("user.my_bookings"))

    booking.status = "Cancelled"

    bus = Bus.query.get(booking.bus_id)

    if bus:
        bus.available_seats += 1

    db.session.commit()

    flash("Booking Cancelled Successfully!", "success")

    return redirect(url_for("user.my_bookings"))