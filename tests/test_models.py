from app.models import ChargingModel, TripModel, RangeModel


def test_charge_model():
    record = ChargingModel(charge_time="0:30", charge_amount=7.8)
    assert record.charge_time == "0:30"
    assert record.charge_amount == 7.8
    assert repr(record) == "Charge Time: 0:30 Charge Amount: 7.8 kWh"


def test_trip_model():
    record = TripModel(miles=1.2, kwh=2.3, trip_time="0:45", destination="Test")
    assert record.miles == 1.2
    assert record.kwh == 2.3
    assert record.trip_time == "0:45"
    assert record.destination == "Test"
    assert repr(record) == "Trip Test was 1.2 miles, took 0:45, average kWh 2.3"


def test_range_model():
    record = RangeModel(battery_range=200, percentage=60)
    assert record.battery_range == 200
    assert record.percentage == 60
    assert repr(record) == "Battery Percentage: 60% Battery Range: 200 miles"
