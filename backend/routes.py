from backend import app, triggers, db
from flask import jsonify
import pandas as pd, json
from backend.models import Pattern, Unit, Staff, Location, Offering, Activity, Period

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

#READS
@app.route('/api/stafftotals', methods=['GET']) #GET
def stafftotals(): #5 second read time, try to automap sqlalchemy
    df = pd.read_sql('staff_totals', db.engine)
    return df.to_json(orient='records')

@app.route('/api/offering', methods=['GET']) #GET
def offerings(): #5 second read time, try to automap sqlalchemy
    df = pd.read_sql('offering_full', db.engine) 
    return df.to_json(orient='records')

@app.route('/api/pattern', methods=['GET']) #GET
def patterns(): #5 second read time, try to automap sqlalchemy
    df = pd.read_sql('pattern_full', db.engine)
    return df.to_json(orient='records')

@app.route('/api/activitylookup/<int:pattern_id>', methods=['GET']) #GET
def pattern_lookup(pattern_id):
    pattern = Pattern.query.get(pattern_id)
    activities = pattern.pattern_activity
    activityArr = []
    for activity in activities:
        activityArr.append(activity.toDict())
    return jsonify(activityArr)


@app.route('/api/unit', methods=['GET']) #GET
def units():
    units = Unit.query.all()
    unitArr = []
    for unit in units:
        unitArr.append(unit.toDict())
    return jsonify(unitArr)

@app.route('/api/periodlookup/<int:location_id>', methods=['GET']) #GET
def period_lookup(location_id):
    location = Location.query.get(location_id)
    periods = location.period
    periodArr = []
    for period in periods:
        periodArr.append(period.toDict())
    return jsonify(periodArr)

@app.route('/api/staff', methods=['GET']) #GET
def staffs():
    staffs = Staff.query.all()
    staffArr=[]
    for staff in staffs:
        staffArr.append(staff.toDict())
    return jsonify(staffArr)

@app.route('/api/location', methods=['GET']) #GET
def locations():
    locations = Location.query.all()
    locationArr=[]
    for location in locations:
        locationArr.append(location.toDict())
    return jsonify(locationArr)

#WRITES
@app.route('/api/staff/<int:staff_id>', methods=['POST']) #POST
def edit_staff(staff_id):
    return 0

@app.route('/api/offering/<int:offering_id>', methods=['POST']) #POST
def edit_offering(offering_id):
    return 0

@app.route('/api/new/offering', methods=['POST']) #POST
def new_offering():
    return 0

@app.route('/api/new/pattern', methods=['POST']) #POST
def new_pattern():
    return 0;