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

    def offering():
        df1 = pd.read_sql('offering', db.engine)
        df2 = pd.read_sql('unit', db.engine)
        df3 = pd.read_sql('pattern_full', db.engine)
        df1 = pd.merge(df1, df2, left_on='unit_id', right_on='id').drop(columns=['id_y', 'unit_id']).rename(index=str, columns={'id_x': 'id'})
        df1 = pd.merge(df1, df3, left_on='pattern_id', right_on='id').drop(columns=['id_y', 'hours_per_tutorial', 'description', 'long_description', 'pattern_id']).rename(index=str, columns={'id_x': 'id', 'code_x': 'unit_code', 'code_y': 'pattern_code'}).sort_values('id')
        df1 = df1.assign(group_required = np.ceil(df1.enrolment / df1.student_per_group))
        df1['group_required'] = df1.group_required.astype(int)
        df1 = df1.assign(total_workload = df1.base + df1.tutorial * df1.group_required + df1.student * df1.enrolment)
        df1 = df1.assign(coordination = df1.base + df1.student * df1.enrolment)
        df1 = df1.assign(hours_to_staff = df1.coordination + df1.tutorial_to_staff * df1.tutorial)
        df1 = df1.assign(hours_to_casual = df1.tutorial_to_casual * df1.tutorial)
        df1 = df1.assign(tally = (df1.group_required - df1.tutorial_to_staff - df1.tutorial_to_casual) == 0)
        df1 = df1.assign(casual_hours_billable = df1.tutorial_to_casual * df1.hours_per_period)
        df1 = df1.reset_index(drop=True)
        df1.to_sql('offering_full', db.engine, if_exists='replace')

    def pattern():
        df1 = pd.read_sql('pattern', db.engine)
        df2 = pd.read_sql('activity', db.engine)
        df3 = pd.read_sql('pattern_activity', db.engine)
        df4 = pd.merge(df3, df2, left_on='activity_id', right_on='id').drop(columns=['name', 'activity_id', 'id'])
        df5 = df4[df4.type == 'fr']
        df6 = df4[df4.type == 'pt']
        df7 = df4[df4.type == 'ps']
        df5 = df5.groupby(['pattern_id']).sum()
        df6 = df6.groupby(['pattern_id']).sum()
        df7 = df7.groupby(['pattern_id']).sum()
        df1 = pd.merge(df1, df5, left_on='id', right_on='pattern_id', how='left')
        df1 = pd.merge(df1, df6, left_on='id', right_on='pattern_id', how='left')
        df1 = pd.merge(df1, df7, left_on='id', right_on='pattern_id', how='left')
        df1 = df1.rename(index=str, columns={'hour_x': 'base', 'hour_y': 'tutorial', 'hour': 'student'})
        df1 = df1.fillna(0)
        df1 = df1.assign(hour_per_period = df1.hour_per_tutorial * 12)
        df1.to_sql('pattern_full', db.engine, if_exists='replace')

    def totals():
        df1 = pd.read_sql('staff', db.engine)
        df2 = pd.read_sql('offering_full', db.engine)
        df3 = df2[['staff_id', 'hours_to_staff']].groupby('staff_id').sum().rename(columns={'hours_to_staff': 'teaching_hours'})
        df2 = df2[['staff_id', 'hours_to_staff']].groupby('staff_id').count().rename(columns={'hours_to_staff': 'offerings_taken'})
        df2 = pd.merge(df2, df3, on='staff_id')
        df1 = pd.merge(df1, df2, left_on='id', right_on='staff_id', how='left')
        df1 = df1.assign(target = df1.fraction * 1725)
        df1 = df1.assign(baseline_research = df1.target * 0.2)
        df1 = df1.assign(baseline_service = df1.target * 0.1)
        df1 = df1.assign(total_load = df1.supervision + df1.research + df1.service + df1.extra + df1.teaching_hours + df1.baseline_research + df1.baseline_service)
        df1.to_sql('staff_totals', db.engine, if_exists='replace')

#def addPattern():
    #generate new pattern_full

#def addEditOffering():
    #generate new offering_full and staff_totals

#def editStaff()
    #generate new staff_totals
