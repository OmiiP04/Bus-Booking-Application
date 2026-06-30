from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db
from app.models.bus import Bus
from app.models.booking import Booking

user = Blueprint("user", __name__)


# -------------------------
# Dashboard
# -------------------------
@user.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# -------------------------
# Search Bus
# -------------------------
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


# -------------------------
# Select Seat
# -------------------------
@user.route("/book/<int:id>")
@login_required
def select_seat(id):

    bus = Bus.query.get_or_404(id)

    bookings = Booking.query.filter_by(
        bus_id=id
    ).all()

    booked_seats = [booking.seat_number for booking in bookings]

    return render_template(
        "select_seat.html",
        bus=bus,
        booked_seats=booked_seats
    )


# -------------------------
# Confirm Booking
# -------------------------
@user.route("/confirm-booking/<int:bus_id>/<int:seat>")
@login_required
def confirm_booking(bus_id, seat):

    bus = Bus.query.get_or_404(bus_id)

    # Prevent double booking
    existing = Booking.query.filter_by(
        bus_id=bus_id,
        seat_number=seat,
        status="Booked"
    ).first()

    if existing:
        flash("Seat already booked.", "danger")
        return redirect(url_for("user.select_seat", id=bus_id))

    if bus.available_seats <= 0:
        flash("No seats available.", "danger")
        return redirect(url_for("user.search_bus"))

    booking = Booking(
        user_id=current_user.id,
        bus_id=bus.id,
        seat_number=seat
    )

    db.session.add(booking)

    bus.available_seats -= 1

    db.session.commit()

    flash("Ticket booked successfully!", "success")

    return redirect(url_for("user.my_bookings"))


# -------------------------
# My Bookings
# -------------------------
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