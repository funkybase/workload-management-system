
# coding: utf-8

# In[1]:


from app import db
from app.models import Pattern, Activity, Location, Period, Unit, Staff, Offering
import pandas as pd


# In[2]:


df1 = pd.read_sql('staff', db.engine)


# In[16]:


df2 = pd.read_sql('offering_full', db.engine)


# In[28]:


df3 = df2[['staff_id', 'hours_to_staff']].groupby('staff_id').sum().rename(columns={'hours_to_staff': 'teaching_hours'})


# In[29]:


df2 = df2[['staff_id', 'hours_to_staff']].groupby('staff_id').count().rename(columns={'hours_to_staff': 'offerings_taken'})


# In[32]:


df2 = pd.merge(df2, df3, on='staff_id')


# In[34]:


df1 = pd.merge(df1, df2, left_on='id', right_on='staff_id', how='left')


# In[36]:


df1 = df1.assign(target = df1.fraction * 1725)


# In[38]:


df1 = df1.assign(baseline_research = df1.target * 0.2)


# In[40]:


df1 = df1.assign(baseline_service = df1.target * 0.1)


# In[43]:


df1 = df1.assign(total_load = df1.supervision + df1.research + df1.service + df1.extra + df1.teaching_hours + df1.baseline_research + df1.baseline_service)


# In[44]:


df1.to_sql('staff_totals', db.engine, if_exists='replace')

