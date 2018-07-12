from app import db
import pandas as pd

df1 = pd.read_sql('offering_full', db.engine)

df1 = df1[['hours_to_casual', 'casual_hours_billable']]

df1 = df1.assign(total_cost = df1.casual_hours_billable * 123.59)

df1 = df1.rename(columns={'hours_to_casual': 'total_casual_load', 'casual_hours_billable': 'total_billable_hours'}).sum()

df1.to_json()

