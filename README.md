### Workload API
---

#### Local instance

To access workload API locally, clone this repo and run `pip install -r requirements.txt` once in the directory and either:  
    1. export FLASK_APP and run with `flask run` and go to localhost:5000  
    2. run with `python backend.py` (python must be version 3) and go to localhost:5000  
    3. run with `gunicorn wsgi` and go to localhost:8000  

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

To view total costs and total casual hours, append `/costing`.

To edit staff, append `staff/{staff_id}` and post the json in the format:  
```
{"fraction":<some float max 1>,  
	"supervision":<some float>,  
	 "research":<some float>,  
	 "service":<some float>,  
	 "extra":<some float>,  
	 "service_description":<some text max 128 char>,  
	 "comments":<some text max 128 char>   
}
```

To edit offering, append `offering/{offering_id}` and post the json in the format:  
```
{"confirm":<some boolean>,  
	"enrolment":<some integer>,  
	"tutorial_to_staff":<some integer>,  
	"tutorial_to_casual":<some integer>,  
	"staff_id":<some integer>
}
```


To add new offering, append `/new/offering` and post the json in the format:  
```  
//mandatory fields  
{"unit_id":<some int>,  
	"pattern_id":<some int>,  
	"period_id":<some int>   
//optional fields (these fields have either have default values or nullable)  
	"confirm":<some boolean default false>,  
	"enrolment":<some int default 0>,  
	"tutorial_to_staff":<some int default 0>,  
	"tutorial_to_casual":<some int default 0>  
}  
```

To add new pattern, append `/new/pattern` and post the json in the format:  
```  
//mandatory fields  
{"code":<some unique string max 8 char>,  
	"location_id":<some int>,  
	"mode":<some char 'D' or 'X'>,  
	"activities: [{  
		"activity_id":<some int>  
	}. {  
		"activity_id":<some int>  
	}]  
//optional fields (close the json before this comment if the fields below are not needed)  
	"description": <some string max 64 char no default>,  
	"long_description": <some string max 256 char no default>,  
	"student_per_group": <some int default 0>,  
	"hour_per_tutorial": <some int default 0>  
}
```

The last four methods do not allow bulk inserts.

