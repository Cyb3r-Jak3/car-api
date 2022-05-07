"""Main App"""
import os
import json

from flask import Flask, render_template, request, jsonify
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
import plotly.express as px
import plotly

from .models import db, RangeModel, ChargingModel, TripModel

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.getenv("BASIC_AUTH_USER")
app.config['BASIC_AUTH_PASSWORD'] = os.getenv("BASIC_AUTH_PASS")

db_uri = os.environ["DATABASE_URL"]
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)


@app.route("/")
@basic_auth.required
def index():
    """
    Render Index Page
    :return:
    """
    return render_template("index.jinja")


@app.route("/api/submit", methods=["POST"])
@basic_auth.required
def action_endpoint():
    """
    Endpoint that handles form submission
    :return:
    """
    form = request.form
    # Handle battery + range fields
    if any([form.get("BatteryPercentage") or form.get("BatteryRange")]):
        battery_percentage = form["BatteryPercentage"]
        battery_range = form["BatteryRange"]
        if all([battery_percentage, battery_range]):
            new_record = RangeModel(
                battery_range=battery_range, percentage=battery_percentage
            )
            db.session.add(new_record)
            db.session.commit()
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Need both battery percentage and battery range",
                    }
                ),
                400,
            )

    # Handle trip info
    if any([form.get("miles"), form.get("kwh"), form.get("time"), form.get("destination")]):
        miles = form["miles"]
        kwh = form["kwh"]
        trip_time = form["time"]
        destination = form["destination"]
        if all([miles, kwh, trip_time, destination]):
            new_record = TripModel(
                miles=miles, kwh=kwh, trip_time=trip_time, destination=destination
            )
            db.session.add(new_record)
            db.session.commit()
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Need all miles, kwh, destination and time filled out",
                    }
                ),
                400,
            )

    # Handle charging submission
    if any([form.get("ChargeTime") or form.get("ChargeAmount")]):
        charge_time = form["ChargeTime"]
        charge_amount = form["ChargeAmount"]
        if all([charge_amount, charge_time]):
            new_record = ChargingModel(
                charge_time=charge_time, charge_amount=charge_amount
            )
            db.session.add(new_record)
            db.session.commit()
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Need both ChargeTime and ChargeAmount filled out",
                    }
                ),
                400,
            )

    return jsonify({"success": True}), 200


@app.route("/range")
@basic_auth.required
def charge_graph():
    query = RangeModel.query.all()
    fig = px.scatter(x=[point.percentage for point in query], y=[point.battery_range for point in query], trendline="ols", title="Range vs Battery Percentage")
    return render_template('plotly.jinja', title="Range Graph", graphJSON=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))


if __name__ == "__main__":
    app.run()
