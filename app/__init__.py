"""Main App"""
import os
from datetime import datetime
import json

import pandas
from flask import Flask, render_template, request, jsonify

import plotly.express as px
import plotly.graph_objects as go
import plotly
from flask_migrate import Migrate
from .auth import auth_needed
from .models import db, RangeModel, ChargingModel, TripModel


def create_app():
    """
    Returns a Flask App with settings
    :return:
    """
    created = Flask(__name__)
    created.secret_key = os.getenv("FLASK_SECRET_KEY", "INSECURE-KEY")
    created.config["BASIC_AUTH_USERNAME"] = os.getenv("BASIC_AUTH_USER")
    created.config["BASIC_AUTH_PASSWORD"] = os.getenv("BASIC_AUTH_PASS")

    db_uri = os.environ["DATABASE_URL"]
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)

    created.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    created.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(created)
    Migrate(created, db)
    return created


app = create_app()


@app.route("/")
@auth_needed
def index():
    """
    Render Index Page
    :return:
    """
    return render_template("index.jinja")


@app.route("/api/submit", methods=["POST"])
@auth_needed
def action_endpoint():
    """
    Endpoint that handles form submission
    :return:
    """
    date = datetime.utcnow()
    form = request.form
    # Handle battery + range fields
    if any([form.get("BatteryPercentage") or form.get("BatteryRange")]):
        battery_percentage = form["BatteryPercentage"]
        battery_range = form["BatteryRange"]
        if all([battery_percentage, battery_range]):
            new_record = RangeModel(
                battery_range=battery_range,
                percentage=battery_percentage,
                submit_time=date,
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
    if any(
        [form.get("miles"), form.get("kwh"), form.get("time"), form.get("destination")]
    ):
        miles = form["miles"]
        kwh = form["kwh"]
        trip_time = form["time"]
        destination = form["destination"]
        if all([miles, kwh, trip_time]):
            new_record = TripModel(
                miles=miles,
                kwh=kwh,
                trip_time=trip_time,
                destination=destination,
                submit_time=date,
            )
            db.session.add(new_record)
            db.session.commit()
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Need all miles, kwh, and time filled out",
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
                charge_time=charge_time,
                charge_amount=charge_amount,
                submit_time=date,
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
@auth_needed
def range_graph():
    """
    Endpoint to show a graph of battery percentage vs battery range
    """
    fig = px.scatter(
        data_frame=pandas.read_sql_query(
            db.select([RangeModel.battery_range, RangeModel.percentage]), con=db.engine
        ),
        x="battery_range",
        y="percentage",
        trendline="ols",
        title="Range vs Battery Percentage",
        labels={"x": "Estimate Range", "y": "Battery Range"},
    )

    fig.update_layout(
        xaxis_title="Estimated Miles",
        yaxis_title="Battery Percentage",
    )
    return render_template(
        "plotly.jinja",
        title="Range Graph",
        graphs=[json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)],
    )


@app.route("/trips")
@auth_needed
def trip_graph():
    """
    Endpoint to show a table of trips
    """
    trip_data: list[TripModel] = TripModel.query.all()
    fig = go.Figure(
        data=go.Table(
            header=dict(
                values=[
                    "Miles",
                    "Average kWh",
                    "Trip Time",
                    "Destination",
                    "Battery Range",
                ]
            ),
            cells=dict(
                values=[
                    [trip.miles for trip in trip_data],
                    [trip.kwh for trip in trip_data],
                    [str(trip.trip_time) for trip in trip_data],
                    [trip.destination for trip in trip_data],
                    [trip.battery_range for trip in trip_data],
                ]
            ),
        )
    )
    return render_template(
        "plotly.jinja",
        title="Trip Graph",
        graphs=[json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)],
    )


if __name__ == "__main__":  # pragma: nocover
    app.run()
