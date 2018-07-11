
# coding: utf-8

# In[98]:


from app import db
from app.models import Pattern, Activity, Location, Period, Unit, Staff, Offering
import pandas as pd


# In[99]:


df1 = pd.read_sql('pattern', db.engine)


# In[100]:


df2 = pd.read_sql('activity', db.engine)


# In[101]:


df3 = pd.read_sql_table('pattern_activity', db.engine)


# In[102]:


df4 = pd.merge(df3, df2, left_on='activity_id', right_on='id').drop(columns=['name', 'activity_id','id'])
#df4 = df4.drop(columns='name')
df5 = df4[df4.type == 'fr']
df6 = df4[df4.type == 'pt']
df7 = df4[df4.type == 'ps']
#group by 'pattern_id' sum of hours


# In[103]:


df5 = df5.groupby(['pattern_id']).sum()
df6 = df6.groupby(['pattern_id']).sum()
df7 = df7.groupby(['pattern_id']).sum()


# In[104]:


df1 = pd.merge(df1, df5, left_on='id', right_on='pattern_id', how='left')
#df1 = pd.merge(df1, df6, left_on='id', right_on='pattern_id', how='left')

df1


# In[105]:


df1 = pd.merge(df1, df6, left_on='id', right_on='pattern_id', how='left')
df1


# In[106]:


df1 = pd.merge(df1, df7, left_on='id', right_on='pattern_id', how='left')
df1


# In[107]:


df1 = df1.rename(index=str, columns={'hour_x': 'base', 'hour_y': 'tutorial', 'hour': 'student'})


# In[108]:


df1 = df1.fillna(0)


# In[112]:


df1 = df1.assign(hour_per_period = df1.hour_per_tutorial * 12)
#have not run


# In[113]:


df1.to_sql('pattern_full', db.engine, if_exists='replace')


# In[119]:


sample = pd.read_sql_table('pattern_full', db.engine)
sample


# In[123]:


sample.to_json(orient='records')
