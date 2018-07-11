
# coding: utf-8

# In[1]:


from app import db
from app.models import Pattern, Activity, Location, Period, Unit, Staff, Offering
import pandas as pd


# In[28]:


import numpy as np


# In[93]:


df1 = pd.read_sql('offering', db.engine)


# In[56]:


df2 = pd.read_sql('unit', db.engine)


# In[57]:


df3 = pd.read_sql('pattern_full', db.engine)


# In[94]:


df1 = pd.merge(df1, df2, left_on='unit_id', right_on='id').drop(columns=['id_y', 'unit_id']).rename(index=str, columns={'id_x': 'id'})


# In[95]:


df1 = pd.merge(df1, df3, left_on='pattern_id', right_on='id').drop(columns=['id_y', 'hour_per_tutorial', 'description', 'long_description','pattern_id']).rename(index=str, columns={'id_x': 'id', 'code_x': 'unit_code', 'code_y': 'pattern_code'}).sort_values('id')


# In[96]:


df1 = df1.assign(group_required = np.ceil(df1.enrolment / df1.student_per_group))


# In[97]:


df1['group_required'] = df1.group_required.astype(int)


# In[98]:


df1 = df1.assign(total_workload = df1.base + df1.tutorial * df1.group_required + df1.student * df1.enrolment)


# In[99]:


df1 = df1.assign(coordination = df1.base + df1.student * df1.enrolment)


# In[100]:


df1 = df1.assign(hours_to_staff = df1.coordination + df1.tutorial_to_staff * df1.tutorial)


# In[101]:


df1 = df1.assign(hours_to_casual = df1.tutorial_to_casual * df1.tutorial)


# In[102]:


df1 = df1.assign(tally = (df1.group_required - df1.tutorial_to_staff - df1.tutorial_to_casual) == 0)


# In[103]:


df1 = df1.assign(casual_hours_billable = df1.tutorial_to_casual * df1.hour_per_period)


# In[109]:


df1 = df1.reset_index(drop=True)


# In[110]:


df1.to_sql('offering_full', db.engine, if_exists='replace')


# In[111]:


pd.read_sql('offering_full', db.engine)

