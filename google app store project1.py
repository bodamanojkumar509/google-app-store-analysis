#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import plotly
plotly.offline.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import seaborn as sns
sns.set_style("darkgrid")
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt


# In[4]:


apps_with_duplicates = pd.read_csv('C:/Users/KADAVATH LATHA/Downloads/googleplaystoredata.csv')


# In[5]:


apps = apps_with_duplicates.drop_duplicates()


# In[6]:


print('Total number of apps: ', len(apps['App']))


# In[7]:


print(apps.info())


# In[8]:


delete_char= ['+',',','$']


# In[9]:


cols_to_clean = ['Installs','Price']


# In[10]:


# Loop over columns for each row
for col in cols_to_clean:
    # Replace each character with an empty string
    for char in delete_char:
        apps[col] = apps[col].astype(str).str.replace(char,'')
    # Convert col to numeric
    apps[col] = pd.to_numeric(apps[col]) 
#See if the results improved; check the dtype() of each column
print(apps.info())


# In[11]:


cats = len(apps['Category'].unique())
print('Number of categories: ', cats)


# In[12]:


num_apps_in_category = apps['Category'].value_counts().sort_values(ascending = False)


# In[13]:


data = [go.Bar(
        x = num_apps_in_category.index, 
        y = num_apps_in_category.values, 
)]


# In[14]:


#Plot the data
plotly.offline.iplot(data)


# In[15]:


# Mean app rating
avg_rating = apps['Rating'].mean()
print('Average app rating is ', avg_rating)


# In[16]:


# Data list of the rating; plotted graph is a histogram
data = [go.Histogram(
        x = apps['Rating']
)]


# In[17]:


# Add a vertical line indicating the mean value.
layout = {'shapes': [{
              'type' :'line',
              'x0': avg_rating,
              'y0': 0,
              'x1': avg_rating,
              'y1': 1000,
              'line': { 'dash': 'dashdot'}
          }]
          }


# In[18]:


plotly.offline.iplot({'data': data, 'layout': layout})


# In[19]:


# Filter out rows with no value for Rating/Size
apps_with_size_rating= apps[(~apps['Rating'].isnull()) & (~apps['Size'].isnull())]


# In[20]:


# Subset categories where there are more than 250 apps
large_cats = apps_with_size_rating.groupby(apps_with_size_rating['Category']).filter(lambda x: len(x) >= 250).reset_index()


# In[21]:


# Plot size vs. rating
plt1 = sns.jointplot(x = large_cats['Size'], y = large_cats['Rating'], kind = 'hex')


# In[22]:


# Subset apps with 'paid' type
paid_apps = apps_with_size_rating[apps_with_size_rating['Type'] == 'Paid']


# In[23]:


# Plot price vs. rating
plt2 = sns.jointplot(x = paid_apps['Price'], y = paid_apps['Rating'])


# In[24]:


# define the size of the type and the size of the plot
fig, ax = plt.subplots()
fig.set_size_inches(15, 8)


# In[25]:


# Select app categories
popular_app_cats = apps[apps.Category.isin(['TOOLS', 'BUSINESS', 'FINANCE',
                                            'MEDICAL', 'GAME', 'PHOTOGRAPHY',
                                            'LIFESTYLE','FAMILY'])]


# In[28]:


# Apps with prices larger than $200
apps_200 = popular_app_cats[['Category', 'Price', 'App']][popular_app_cats['Price'] > 200]
apps_200


# In[29]:


fig, ax = plt.subplots()
fig.set_size_inches(15, 8)


# In[30]:


# Apps with prices less than $100
apps_100 =  popular_app_cats[popular_app_cats['Price'] < 100]


# In[31]:


#Paid apps installs distribution
box0 = go.Box(
    y=apps[apps['Type'] == 'Paid']['Installs'],
    name = 'Paid'
)


# In[32]:


#Free apps installs distribution
box1 = go.Box(
    y=apps[apps['Type'] == 'Free']['Installs'],
    name = 'Free'
)
layout = go.Layout(
    title = "Free versus Paid Installs",
    yaxis = dict(
        type = 'log',
        autorange = True
    )
)


# In[33]:


# Add box 0 and box 1 for plotting
data = [box0,box1]
plotly.offline.iplot({'data': data, 'layout': layout})


# In[41]:


reviews= pd.read_excel("C:/Users/KADAVATH LATHA/Downloads/googleplaystore_user_reviews.csv.xlsx")


# In[42]:


# Metge dataframes
merged = pd.merge(apps, reviews, on = 'App', how = "inner")


# In[43]:


# Drop NA values from Sentiment and Translated_Review columns
merged = merged.dropna(subset=['Sentiment', 'Translated_Review'])


# In[44]:


sns.set_style('ticks')
fig, ax = plt.subplots()
fig.set_size_inches(11, 8)


# In[45]:


# User review sentiment polarity for paid vs. free apps
ax = sns.boxplot(x = 'Type', y = 'Sentiment_Polarity', data = merged)
ax.set_title('Sentiment Polarity Distribution')


# In[ ]:




