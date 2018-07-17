from backend import app, db, q
from flask import jsonify, Response, request, abort
import pandas as pd, json
from backend.models import Pattern, Unit, Staff, Location, Offering, Activity, Period
from backend.triggers import Trigger

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World! Visit github.com/funkybase/workload-management-system for instructions to use API"

#READS
@app.route('/api/stafftotals', methods=['GET']) #GET
def stafftotals(): #5 second read time, try to automap sqlalchemy
    df = pd.read_sql('staff_totals', db.engine)
    #change this to return a response object 
    resp = Response(df.to_json(orient='records'), mimetype='application/json')
    return resp 

@app.route('/api/offering', methods=['GET']) #GET
def offerings(): #5 second read time, try to automap sqlalchemy
    df = pd.read_sql('offering_full', db.engine) 
    #change this to return a response object 
    resp = Response(df.to_json(orient='records'), mimetype='application/json')
    return resp

@app.route('/api/pattern', methods=['GET']) #GET
def patterns(): #5 second read time, try to automap sqlalchemy
    df = pd.read_sql('pattern_full', db.engine)
    #change this to return a response object 
    resp = Response(df.to_json(orient='records'), mimetype='application/json')
    return resp

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

@app.route('/api/period', methods=['GET'])
def periods():
    periods = Period.query.all()
    periodArr = []
    for period in periods:
        periodArr.append(period.toDict())
    return jsonify(periodArr)

@app.route('/api/periodoptions/<int:location_id>', methods=['GET']) #GET
def period_options(location_id):
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

@app.route('/api/activity', methods=['GET'])
def activities():
    activities = Activity.query.all()
    activityArr = []
    for activity in activities:
        activityArr.append(activity.toDict())
    return jsonify(activityArr)

@app.route('/api/offeringlookup/<int:staff_id>', methods=['GET'])
def offering_lookup(staff_id):
    staff = Staff.query.get(staff_id)
    offerings = staff.offerings
    offeringArr = []
    for offering in offerings:
        offeringArr.append(offering.toDict())
    return jsonify(offeringArr)

@app.route('/api/costing', methods=['GET'])
def costing():
    resp = Response(Trigger.costing(), mimetype='application/json')
    return resp

@app.route('/api/unitlookup/<int:unit_id>', methods=['GET'])
def unit_lookup(unit_id):
    unit = Unit.query.get(unit_id)
    return jsonify(unit.toDict())

@app.route('/api/periodlookup/<int:period_id>', methods=['GET'])
def period_lookup(period_id):
    period = Period.query.get(period_id)
    return jsonify(period.toDict())

@app.route('/api/locationlookup/<int:location_id>', methods=['GET'])
def location_lookup(location_id):
    location = Location.query.get(location_id)
    return jsonify(location.toDict())

#WRITES
@app.route('/api/staff/<int:staff_id>', methods=['POST']) #POST
def edit_staff(staff_id):
    #update cache (redis) and then make a task queue to update postgres
    if request.data and bool(request.json):
        content = request.json
        #replace with function single_update_staff
        job = q.enqueue.call(
                func=single_update_staff, args=(content, staff_id), result_ttl=5000
        )
        return job.get_id(), 200
    return abort(404)

@app.route('/api/offering/<int:offering_id>', methods=['POST']) #POST
def edit_offering(offering_id):
    #update cache (redis) and then make a task queue to update postgres
    print("successfully reached checkpoint 1")
    print(bool(request.json) == True)
    if request.data and bool(request.json):
        content = request.json
        # offering = Offering.query.get(offering_id)
        # if "confirm" in content:
            # offering.confirm = content["confirm"]
        # if "enrolment" in content:
            # offering.enrolment = content["enrolment"]
        # if "tutorial_to_staff" in content:
            # offering.tutorial_to_staff = content["content_to_staff"]
        # if "tutorial_to_casual" in content:
            # offering.tutorial_to_casual = content["tutorial_to_casual"]
        # if "staff_id" in content:
            # offering.UC = Staff.query.get(content["staff_id"])
        # db.session.commit()
        # Trigger.offering()
        # Trigger.totals()
        print('successfully reached here checkpoint 2')
        job = q.enqueue.call(
                func=single_update_offering, args=(content, offering_id), result_ttl=5000
        )
        return job.get_id(), 200
    return abort(404)

@app.route('/api/new/offering', methods=['POST']) #POST
def new_offering():
    #update cache (redis) and then make a task queue to update postgres
    if request.data and bool(request.json):
        content = request.json
        if ("unit_id" and "period_id" and "pattern_id") in content:
            # offering = Offering()
            # with db.session.no_autoflush:
                # offering.unit = Unit.query.get(content["unit_id"])
                # pattern = Pattern.query.get(content["pattern_id"])
                # period = Period.query.get(content["period_id"])
                # offering.period = period
                # offering.pattern = pattern
            # if "confirm" in content:
                # offering.confirm = content["confirm"]
            # if "enrolment" in content:
                # offering.enrolment = content["enrolment"]
            # if "tutorial_to_staff" in content:
                # offering.tutorial_to_staff = content["tutorial_to_staff"]
            # if "tutorial_to_casual" in content:
                # offering.tutorial_to_casual = content["tutorial_to_casual"]
            # db.session.commit()
            # Trigger.offering()
            # Trigger.totals()
            job = q.enqueue.call(
                    func=single_insert_offering, args=(content), result_ttl=5000
            )
            return job.get_id(), 200
    return abort(404)

            
@app.route('/api/new/pattern', methods=['POST']) #POST
def new_pattern():
    #update cache (redis) and then make a task queue to update postgres
    if request.data and bool(request.json):
        content = request.json
        if ("code" and "location_id" and "activities" and "mode") in content:
            # location = Location.query.get(content["location_id"])
            # pattern = Pattern(code=content["code"], mode=content["mode"])
            # pattern.location = location
            # activities = content["activities"]
            # for activity in activities:
                # act = Activity.query.get(activity["activity_id"])
                # pattern.pattern_activity.append(act)
            # if "description" in content:
                # pattern.description = content["description"]
            # if "long_description" in content:
                # pattern.long_description = content["long_description"]
            # if "student_per_group" in content:
                # pattern.student_per_group = content["student_per_group"]
            # if "hour_per_tutorial" in content:
                # pattern.hour_per_tutorial = content["hour_per_tutorial"]
            # db.session.commit()
            # Trigger.pattern()
            job = q.enqueue.call(
                    func=single_insert_pattern, args=(content), result_ttl=5000
            )
            return job.get_id(), 200
    return abort(404)

@app.route('/api/update/offering', methods=['POST'])
def update_offering():
    if request.data and bool(request.json):
        content = request.json
        # for key in content:
            # offering = Offering.query.get(key)
            # if "confirm" in key:
                # offering.confirm = key["confirm"]
            # if "enrolment" in key:
                # offering.enrolment = key["enrolment"]
            # if "tutorial_to_staff" in key:
                # offering.tutorial_to_staff = key["content_to_staff"]
            # if "tutorial_to_casual" in key:
                # offering.tutorial_to_casual = key["tutorial_to_casual"]
            # if "staff_id" in key:
                # offering.UC = Staff.query.get(key["staff_id"])
        # db.session.commit()
        # Trigger.offering()
        # Trigger.totals()
        job = q.enqueue.call(
                func=bulk_update_offering, args=(content), result_ttl=5000
        )
        return job.get_id(), 200
    return abort(404)

@app.route('/api/update/staff', methods=['POST'])
def update_staff():
    if request.data and bool(request.json):
        content = request.json
        # for key in content:
            # staff = Staff.query.get(key)
            # if "fraction" in key:
                # staff.fraction = key["fraction"]
            # if "supervision" in key:
                # staff.supervision = key["supervision"]
            # if "research" in key:
                # staff.research = key["research"]
            # if "service" in key:
                # staff.service = key["service"]
            # if "extra" in key:
                # staff.extra = key["extra"]
            # if "service_description" in key:
                # staff.service_description = key["service_description"]
            # if "comments" in key:
                # staff.comments = key["comments"]
        # db.session.commit()
        # Trigger.totals()
        job = q.enqueue.call(
                func=bulk_update_staff, args=(content), result_ttl=5000
        )
        return job.get_id(), 200
    return abort(404)

@app.route("/results/<job_key>", methods=['GET'])
def get_result(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202

def single_update_staff(content, id):
    staff = Staff.query.get(id)
    try:
        if "fraction" in content:
            staff.fraction = content["fraction"]
        if "supervision" in content:
            staff.supervision = content["supervision"]
        if "research" in content:
            staff.research = content["research"]
        if "service" in content:
            staff.service = content["service"]
        if "extra" in content:
            staff.extra = content["extra"]
        if "service_description" in content:
            staff.service_description = content["service_description"]
        if "comments" in content:
            staff.comments = content["comments"]
        db.session.commit()
        Trigger.totals()
        return {"status": "Saved"}
    except:
        errors.append("Unable to edit item to database.")
        return {"error": errors}

def single_update_offering(content, id):
    offering = Offering.query.get(id)
    try:
        if "confirm" in content:
            offering.confirm = content["confirm"]
        if "enrolment" in content:
            offering.enrolment = content["enrolment"]
        if "tutorial_to_staff" in content:
            offering.tutorial_to_staff = content["tutorial_to_staff"]
        if "tutorial_to_casual" in content:
            offering.tutorial_to_casual = content["tutorial_to_casual"]
        if "staff_id" in content:
            offering.UC = Staff.query.get(content["staff_id"])
        db.session.commit()
        Trigger.offering()
        Trigger.totals()
        return {"status": "Saved"}
    except:
        errors.append("Unable to edit item to database.")
        return {"error": errors}

def single_insert_offering(content):
    try:
        offering = Offering()
        with db.session.no_autoflush:
            offering.unit = Unit.query.get(content["unit_id"])
            pattern = Pattern.query.get(content["pattern_id"])
            period = Period.query.get(content["period_id"])
            offering.period = period
            offering.pattern = pattern
        if "confirm" in content:
            offering.confirm = content["confirm"]
        if "enrolment" in content:
            offering.enrolment = content["enrolment"]
        if "tutorial_to_staff" in content:
            offering.tutorial_to_staff = content["tutorial_to_staff"]
        if "tutorial_to_casual" in content:
            offering.tutorial_to_casual = content["tutorial_to_casual"]
        db.session.commit()
        Trigger.offering()
        Trigger.totals()
        return {"status": "Saved"}
    except:
        errors.append("Unable to insert new item to database.")
        return {"error": errors}

def single_insert_pattern(content):
    try:
        location = Location.query.get(content["location_id"])
        pattern = Pattern(code=content["code"], mode=content["mode"])
        pattern.location = location
        activities = content["activities"]
        for activity in activities:
            act = Activity.query.get(activity["activity_id"])
            pattern.pattern_activity.append(act)
        if "description" in content:
            pattern.description = content["description"]
        if "long_description" in content:
            pattern.long_description = content["long_description"]
        if "student_per_group" in content:
            pattern.student_per_group = content["student_per_group"]
        if "hour_per_tutorial" in content:
            pattern.hour_per_tutorial = content["hour_per_tutorial"]
        db.session.commit()
        Trigger.pattern()
        return {"status": "Saved"}
    except:
        errors.append("Unable to insert new item to database.")
        return {"error": errors}

def bulk_update_offering(content):
    try:
        for key in content:
            offering = Offering.query.get(key)
            if "confirm" in key:
                offering.confirm = key["confirm"]
            if "enrolment" in key:
                offering.enrolment = key["enrolment"]
            if "tutorial_to_staff" in key:
                offering.tutorial_to_staff = key["content_to_staff"]
            if "tutorial_to_casual" in key:
                offering.tutorial_to_casual = key["tutorial_to_casual"]
            if "staff_id" in key:
                offering.UC = Staff.query.get(key["staff_id"])
        db.session.commit()
        Trigger.offering()
        Trigger.totals()
        return {"status": "Saved"}
    except:
        errors.append("Unable to update new items to database.")
        return {"error": errors}

def bulk_update_staff(content):
    try:
        for key in content:
            staff = Staff.query.get(key)
            if "fraction" in key:
                staff.fraction = key["fraction"]
            if "supervision" in key:
                staff.supervision = key["supervision"]
            if "research" in key:
                staff.research = key["research"]
            if "service" in key:
                staff.service = key["service"]
            if "extra" in key:
                staff.extra = key["extra"]
            if "service_description" in key:
                staff.service_description = key["service_description"]
            if "comments" in key:
                staff.comments = key["comments"]
        db.session.commit()
        Trigger.totals()
        return {"status": "Saved"}
    except:
        errors.append("Unable to update new items to database.")
        return {"error": errors}
