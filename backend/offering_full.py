from app import db
from app.models import Pattern, Activity, Location, Period, Unit, Staff, Offering
import pandas as pd
import numpy as np

df1 = pd.read_sql('offering', db.engine)

df2 = pd.read_sql('unit', db.engine)

df3 = pd.read_sql('pattern_full', db.engine)

df1 = pd.merge(df1, df2, left_on='unit_id', right_on='id').drop(columns=['id_y', 'unit_id']).rename(index=str, columns={'id_x': 'id'})

df1 = pd.merge(df1, df3, left_on='pattern_id', right_on='id').drop(columns=['id_y', 'hour_per_tutorial', 'description', 'long_description','pattern_id']).rename(index=str, columns={'id_x': 'id', 'code_x': 'unit_code', 'code_y': 'pattern_code'}).sort_values('id')

df1 = df1.assign(group_required = np.ceil(df1.enrolment / df1.student_per_group))

df1['group_required'] = df1.group_required.astype(int)

df1 = df1.assign(total_workload = df1.base + df1.tutorial * df1.group_required + df1.student * df1.enrolment)

df1 = df1.assign(coordination = df1.base + df1.student * df1.enrolment)

df1 = df1.assign(hours_to_staff = df1.coordination + df1.tutorial_to_staff * df1.tutorial)

df1 = df1.assign(hours_to_casual = df1.tutorial_to_casual * df1.tutorial)

df1 = df1.assign(tally = (df1.group_required - df1.tutorial_to_staff - df1.tutorial_to_casual) == 0)

df1 = df1.assign(casual_hours_billable = df1.tutorial_to_casual * df1.hour_per_period)

df1 = df1.reset_index(drop=True)

df1.to_sql('offering_full', db.engine, if_exists='replace')
