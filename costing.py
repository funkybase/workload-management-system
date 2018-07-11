
# coding: utf-8

# In[1]:


from app import db
import pandas as pd


# In[21]:


df1 = pd.read_sql('offering_full', db.engine)


# In[22]:


df1 = df1[['hours_to_casual', 'casual_hours_billable']]


# In[24]:


df1 = df1.assign(total_cost = df1.casual_hours_billable * 123.59)


# In[28]:


df1 = df1.rename(columns={'hours_to_casual': 'total_casual_load', 'casual_hours_billable': 'total_billable_hours'}).sum()


# In[29]:


df1.to_json()

