from flask import Blueprint
from flask import render_template
from flask import request

from flask_login import login_required

from app.models.bus import Bus

user = Blueprint("user", __name__)


@user.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")


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