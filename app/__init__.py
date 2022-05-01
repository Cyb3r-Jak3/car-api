"""Main App"""
import os
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from .models import db, RangeModel, ChargingModel, TripModel

app = Flask(__name__)

TEST_DB = "postgresql://ffzhzfvhpgqvrk:ebb7da41dc00e411bfa74c4e7e19f382e0a47a369718e64d9735e1a777b5b4d0@ec2-34-197-84-74.compute-1.amazonaws.com:5432/d6h0tfe7i6l7e"
db_uri = os.getenv("DATABASE_URL", TEST_DB)
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    """
    Render Index Page
    :return:
    """
    return render_template("index.jinja")


@app.route("/api/submit", methods=["POST"])
def action_endpoint():
    """
    Endpoint that handles form submission
    :return:
    """
    form = request.form
    # Handle battery + range fields
    if any([form["BatteryPercentage"] or form["BatteryRange"]]):
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

    # Handle post trip info
    if any([form["miles"], form["kwh"], form["time"], form["destination"]]):
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
    if any([form["ChargeTime"] or form["ChargeAmount"]]):
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

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run()
