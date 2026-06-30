from flask import Blueprint
from flask import render_template

from flask_login import login_required

user = Blueprint("user", __name__)


@user.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")