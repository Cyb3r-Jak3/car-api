"""Database models"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import types

db = SQLAlchemy()


class RangeModel(db.Model):  # pylint: disable=too-few-public-methods
    """
    DB Model that represents range table
    """

    __tablename__ = "range_table"

    id = db.Column(types.Integer, primary_key=True)

    battery_range = db.Column(types.Integer)
    percentage = db.Column(types.Integer)

    def __init__(self, battery_range, percentage):
        self.battery_range = battery_range
        self.percentage = percentage

    def __repr__(self):
        return f"Battery Percentage: {self.percentage}% Battery Range: {self.battery_range} miles"


class ChargingModel(db.Model):  # pylint: disable=too-few-public-methods
    """
    DB Model that represents a charge
    """

    __tablename__ = "charging_table"

    id = db.Column(types.Integer, primary_key=True)
    charge_time = db.Column(types.Interval)
    charge_amount = db.Column(types.Float)

    def __init__(self, charge_time, charge_amount):
        self.charge_time = charge_time
        self.charge_amount = charge_amount

    def __repr__(self):
        return (
            f"Charge Time: {self.charge_time} Charge Amount: {self.charge_amount} kWh"
        )


class TripModel(db.Model):  # pylint: disable=too-few-public-methods
    """
    DB Model that represents a trip
    """

    __tablename__ = "trip_table"

    id = db.Column(types.Integer, primary_key=True)
    miles = db.Column(types.Float)
    kwh = db.Column(types.Float)
    trip_time = db.Column(types.Interval)
    destination = db.Column(types.Text)

    def __init__(self, miles, kwh, trip_time, destination):
        self.miles = miles
        self.kwh = kwh
        self.trip_time = trip_time
        self.destination = destination

    def __repr__(self):
        return (
            f"Trip {self.destination} was {self.miles} miles, "
            f"took {self.trip_time}, average kWh {self.kwh}"
        )
