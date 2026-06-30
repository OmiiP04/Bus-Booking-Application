from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from app.models.bus import Bus
from app.extensions import db
from app.models.bus import Bus

admin = Blueprint("admin", __name__)


@admin.route("/admin")
def dashboard():

    return render_template("admin_dashboard.html")


@admin.route("/admin/add-bus", methods=["GET", "POST"])
def add_bus():

    if request.method == "POST":

        bus = Bus(

            bus_name=request.form["bus_name"],

            bus_number=request.form["bus_number"],

            source=request.form["source"],

            destination=request.form["destination"],

            departure_time=request.form["departure_time"],

            arrival_time=request.form["arrival_time"],

            total_seats=int(request.form["total_seats"]),

            available_seats=int(request.form["total_seats"]),

            price=float(request.form["price"])

        )

        db.session.add(bus)

        db.session.commit()

        flash("Bus Added Successfully!", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template("add_bus.html")

@admin.route("/admin/buses")
def manage_buses():

    buses = Bus.query.all()

    return render_template(
        "manage_buses.html",
        buses=buses
    )


@admin.route("/admin/delete-bus/<int:id>")
def delete_bus(id):

    bus = Bus.query.get_or_404(id)

    db.session.delete(bus)

    db.session.commit()

    flash("Bus Deleted Successfully!", "success")

    return redirect(url_for("admin.manage_buses"))