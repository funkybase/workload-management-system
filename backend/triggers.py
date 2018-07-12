from backend import db
from backend.models import Pattern, Activity, Location, Period, Unit, Staff, Offering
import pandas as pd
import numpy as np

class Trigger:
    def costing():
        df1 = pd.read_sql('offering_full', db.engine)
        df1 = df1[['hours_to_casual', 'casual_hours_billable']]
        df1 = df1.assign(total_cost = df1.casual_hours_billable * 123.56)
        df1 = df1.rename(columns={'hours_to_casual': 'total_casual_load', 'casual_hours_billable': 'total_billable_hours'}).sum()
        return df1.to_json()

#def addPattern():
    #generate new pattern_full

#def addEditOffering():
    #generate new offering_full and staff_totals

#def editStaff()
    #generate new staff_totals
