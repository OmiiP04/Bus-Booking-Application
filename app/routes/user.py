from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user

from app.extensions import db
from app.models.bus import Bus
from app.models.booking import Booking

from datetime import datetime

user = Blueprint("user", __name__)


@user.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@user.route("/search", methods=["GET", "POST"])
@login_required
def search_bus():

    if request.method == "POST":

        buses = Bus.query.filter_by(
            source=request.form["source"],
            destination=request.form["destination"]
        ).all()

        return render_template(
            "search_result.html",
            buses=buses
        )

    return render_template("search_bus.html")


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

        return redirect(
            url_for(
                "user.select_seat",
                id=bus.id
            )
        )

    return render_template(
        "passenger_details.html",
        bus=bus
    )


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