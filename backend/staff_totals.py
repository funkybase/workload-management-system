from app import db
from app.models import Pattern, Activity, Location, Period, Unit, Staff, Offering
import pandas as pd
#import datetime


df1 = pd.read_sql('staff', db.engine)

df2 = pd.read_sql('offering_full', db.engine)

# get year
#now = datetime.datetime.now()
# filter df2 by this year
#df2 = df2.loc[df2['year'] == now.year]

df3 = df2[['staff_id', 'hours_to_staff']].groupby('staff_id').sum().rename(columns={'hours_to_staff': 'teaching_hours'})

df2 = df2[['staff_id', 'hours_to_staff']].groupby('staff_id').count().rename(columns={'hours_to_staff': 'offerings_taken'})

df2 = pd.merge(df2, df3, on='staff_id')

df1 = pd.merge(df1, df2, left_on='id', right_on='staff_id', how='left')

df1 = df1.assign(target = df1.fraction * 1725)

df1 = df1.assign(baseline_research = df1.target * 0.2)

df1 = df1.assign(baseline_service = df1.target * 0.1)

df1 = df1.assign(total_load = df1.supervision + df1.research + df1.service + df1.extra + df1.teaching_hours + df1.baseline_research + df1.baseline_service)

df1.to_sql('staff_totals', db.engine, if_exists='replace')

