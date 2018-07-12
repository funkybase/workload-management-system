### Workload API
---

#### Local instance

To access workload API locally, clone this repo and either:  
    1. export FLASK_APP and run with `flask run`  
    2. run with `python backend.py` (python must be version 3)  
    3. run with `gunicorn wsgi`  

---

#### API calls

Once application is running, access the application via a browser and append the `/api` extension then continue below.

To view staff totals, append `/stafftotals`.

To view offerings, append `/offering`.

To view patterns, append `/pattern`.

To view activities, append `/activity`.

To view units, append `/unit`.

To view staffs, append `/staff`.

To view locations, append `/location`.

To view activities of a certain pattern, append `/activitylookup/{pattern_id}`. (pattern_id is a unique key integer)

To view periods of a certain location, append `/periodlookup/{location_id}`. (location_id is a unique key integer)

To view offerings of a certain staff, append `/offeringlookup/{staff_id}`. (staff_id is a unique key integer)

To view total costs and total casual hours, append `/casual`.

To edit staff, append `staff/{staff_id}` and post the json in the format:  
`{xxx}`

To edit offering, append `offering/{offering_id}` and post the json in the format:  
`{xxx}`

To add new offering, append `/new/offering` and post the json in the format:  
`{xxx}`

To add new pattern, append `/new/pattern` and post the json in the format:  
`{xxx}`

The last two methods do not allow bulk inserts.

