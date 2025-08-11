#!/usr/bin/env python
# coding: utf-8

# <h1 style="color:green;">Electric Vehicle Population Analysis</h1>

# In[1]:


import pandas as pd
from sqlalchemy import create_engine


# In[2]:


engine = create_engine("mysql+pymysql://mysql_username:mysql_password@localhost/electric_vehicle_population_analysis")

query = "SELECT * FROM EV_Cleaned"
df = pd.read_sql(query, con=engine)


# <b style="color:purple;">Just replace your MySQL Username and Password here. Also, don't forget the Database that you want to Load.</b>😁

# In[3]:


df.columns


# In[4]:


df.head()


# In[5]:


df.shape


# <h3 style="color:green;">Quick Data Inspection</h3>

# <b style="color:purple;">Datatypes, and Non-Null Values</b>

# In[6]:


df.info()


# <b style="color:purple;">Missing/Blank Values</b>

# In[7]:


df.isnull().sum()


# <b style="color:purple;">Just to ignore Warnings!</b>

# In[8]:


import warnings
warnings.filterwarnings("ignore")


# In[9]:


df['postal_code'].fillna('Unknown', inplace=True)
df['census_tract'].fillna(-1, inplace=True)
df['legislative_district'].fillna(-1, inplace=True)


# In[10]:


df[['postal_code', 'census_tract', 'legislative_district']].isnull().sum()


# <b style="color:purple;">Unique values</b>

# In[11]:


df.nunique()


# <b style="color:purple;">Summary Statistics for Numeric Columns</b>

# In[12]:


df.describe().round(2)


# <h2><a href="http://localhost:8888/view/All%20Data%20Analytics%20Projects%20right%20here/EV_EDA_Report.html" style="color:green;">Electric Vehicle Population Analysis</a></h2>

# <b style="color:purple;">Checking Duplicates</b>

# In[13]:


df.duplicated().sum()


# In[14]:


df[df.duplicated()].head()


# <b style="color:purple;">Checking Uniqueness Across Key Columns</b>

# In[15]:


df.duplicated(subset=[
    'model_year', 'make', 'model', 'ev_type',
    'electric_range', 'cafv_eligibility', 'county', 'city'
]).sum()


# <b style="color:blue;">We originally had:</b>
# - <p style="color:purple;">
#     <b style="color:green; 
#               background-color:yellow;">97,690 total</b> rows.</p>
# - <p style="color:purple;">
#     <b style="color:green; 
#               background-color:yellow;">73,714</b> are basically clones of other EVs</p>
# 
# 
# <p style="color:purple;">The dataset is heavily bloated with identical 
#     <b style="color:green; 
#               background-color:yellow;">Vehicle Profile</b> records. Possibly from government registration dumps or bulk dealer entries.</p>

# In[16]:


df_full = df.copy() # Full dataset with actual volumes
df_full.shape


# <b style="color:red;">Which Approach is better?</b> 
# - <b style="color:purple;">Option 1: 
#     <b style="color:green; 
#               background-color:yellow;">df.drop_duplicates()</b> (Full Row Deduplication)</b> 
# - <b style="color:purple;">Option 2: 
#     <b style="color:green; 
#               background-color:yellow;">drop_duplicates(subset=[...key columns...])</b></b>
# 
# <b style="color:blue;">Let's do both:</b>

# In[17]:


# Version 1: Full data with only exact duplicates removed
df_deduped = df.drop_duplicates()

# Version 2: Highly unique EV configs only
df_unique_profiles = df.drop_duplicates(subset=[
    'model_year', 'make', 'model', 'ev_type',
    'electric_range', 'cafv_eligibility', 'county', 'city'
])


# <b style="color:blue;">We'll use:</b>
# 
# - <b style="color:purple;"> 
#     <b style="color:green; 
#               background-color:yellow;">df_deduped</b> for insights, trends, volume-based visuals.</b>
# - <b style="color:purple;"> 
#     <b style="color:green; 
#               background-color:yellow;">df_unique_profiles</b> for patterns, relationships, distributions.</b>

# In[18]:


df_deduped.shape


# In[19]:


df_unique_profiles.shape


# <h2 style="color:green;">Exploratory Data Analysis (<span style="background-color:yellow;">EDA</span>)</h2>

# In[20]:


from matplotlib import pyplot as plt
import seaborn as sns


# <h3 style="color:green;">Total EV Count by Model Year</h3>

# <b style="color:purple;">Grouping Total EVs by Model Year</b>

# In[21]:


ev_count_by_year = df_deduped.groupby('model_year').size().reset_index(
    name='ev_count').sort_values(by='ev_count', ascending=False)

ev_count_by_year


# In[22]:


plt.figure(figsize = (12, 6))
sns.barplot(data = ev_count_by_year, x = "model_year", y = "ev_count", palette = "crest")
plt.title("Total EV Count by Model Year", fontsize = 16)
plt.xlabel("Model Year", fontsize = 12)
plt.ylabel("Number of EVs", fontsize = 12)
plt.show()


# <b style="color:blue;">
#     <b style="color:green; 
#               background-color:yellow;">2020</b> recorded the 
#     <b style="color:green; 
#               background-color:yellow;">highest number of EVs</b>, marking a significant spike in adoption, possibly due to better model availability and incentives.
# Earlier years like 
#     <b style="color:green; 
#               background-color:yellow;">2018</b> and 
#     <b style="color:green; 
#               background-color:yellow;">2019</b> also saw notable growth, while years before 
#     <b style="color:white; 
#               background-color:red;">2010</b> had minimal presence, showing how recent the EV boom truly is.</b>

# <h3 style="color:green;">Average Electric Range by Model Year</h3>

# <b style="color:purple;">Grouping Average Electric Range by Model Year</b>

# In[23]:


avg_range_by_year = df_deduped.groupby("model_year", 
                                       as_index=False)["electric_range"].mean().round(2).sort_values(
    by='electric_range', ascending=False)
avg_range_by_year


# In[24]:


plt.figure(figsize = (12, 6))
sns.lineplot(data = avg_range_by_year, x = "model_year", y = "electric_range", 
             marker = "o", ms = 10, color = "g")
plt.title("Average Electric Range by Model Year", fontsize = 16)
plt.xlabel("Model Year", fontsize = 12)
plt.ylabel("Average Range (Miles)", fontsize = 12)
plt.show()


# <b style="color:blue;">Electric range steadily increased from 
#     <b style="color:green; 
#               background-color:yellow;">2000</b> to 
#     <b style="color:green; 
#               background-color:yellow;">2010</b>, but saw a 
#     <b style="color:white; 
#               background-color:red;">drop afterward</b>—possibly due to PHEVs entering the scene. After 
#     <b style="color:green; 
#               background-color:yellow;">2015</b>, range improved again, peaking around 
#     <b style="color:green; 
#               background-color:yellow;">2020</b>. However, the 
#     <b style="color:white; 
#               background-color:red;">years following 2020 show a noticeable dip</b>, hinting at either newer low-range models or incomplete data for future EVs.</b>

# <h3 style="color:green;">Distribution of EV Types (<span style="color:green; background-color:yellow;">BEV</span> vs 
#     <span style="color:green; background-color:yellow;">PHEV</span>)</h3>

# In[25]:


ev_type_counts = df_deduped["ev_type"].value_counts().reset_index()
ev_type_counts


# In[26]:


plt.figure(figsize = (8, 5))
sns.barplot(data = ev_type_counts, x = "ev_type", y = "count", palette = ["g", "y"])
plt.title("Distribution of Electric Vehicle Types", fontsize = 16)
plt.xlabel("EV Type", fontsize = 12)
plt.ylabel("Number of Vehicles", fontsize = 12)
plt.show()


# <b style="color:blue;">Surprisingly, 
#     <b style="color:green; 
#               background-color:yellow;">PHEVs outnumber BEVs</b> in this dataset, highlighting a strong preference for hybrids—possibly due to affordability or range concerns. This also explains some of the dips in average electric range we saw earlier.</b>

# <h3 style="color:green;">Top 10 EV Makes</h3>

# In[27]:


top_makes = df_deduped["make"].value_counts().nlargest(10).reset_index()
top_makes


# In[28]:


plt.figure(figsize = (10, 6))
sns.barplot(data = top_makes, x = "count", y = "make", palette = "Greens_r")
plt.title("Top 10 EV Makes", fontsize = 16)
plt.xlabel("Number of Vehicles", fontsize = 12)
plt.ylabel("Make", fontsize = 12)
plt.show()


# <b style="color:blue;">
#     <b style="color:green; 
#               background-color:yellow;">Tesla dominates the EV market</b> by a wide margin, nearly 
#     <b style="color:green; 
#               background-color:yellow;">doubling the count of its closest competitors</b>. Chevrolet, Toyota, and Nissan follow behind, showing how Tesla's all-electric strategy has paid off in market adoption.</b>

# <h3 style="color:green;">Top 10 EV Models</h3>

# In[29]:


top_models = df_deduped["model"].value_counts().nlargest(10).reset_index()
top_models


# In[30]:


plt.figure(figsize = (10, 6))
sns.barplot(data = top_models, x = "count", y = "model", palette = "cubehelix")
plt.title("Top 10 EV Models", fontsize = 16)
plt.xlabel("Number of Vehicles", fontsize = 12)
plt.ylabel("Model", fontsize = 12)
plt.show()


# <b style="color:blue;">
#     <b style="color:green; 
#               background-color:yellow;">Nissan’s LEAF takes the lead</b> as the most popular EV model, ahead of even 
#     <b style="color:green; 
#               background-color:yellow;">Tesla’s Model 3 and S</b>. The top 10 list reflects a mix of BEVs and PHEVs, showing that affordability and accessibility drive model-level adoption more than brand alone.</b>

# <h3 style="color:green;">Top 10 Counties by EV count</h3>

# In[31]:


top_counties = df_deduped["county"].value_counts().nlargest(10).reset_index()
top_counties


# In[32]:


plt.figure(figsize = (12, 6))
sns.barplot(data = top_counties, x = "count", y = "county", palette = "gist_earth")
plt.title("Top 10 Counties by EV Count", fontsize = 16)
plt.xlabel("Number of EVs", fontsize = 12)
plt.ylabel("County", fontsize = 12)
plt.show()


# <b style="color:blue;"> 
#     <b style="color:green; 
#               background-color:yellow;">King County dominates EV registrations</b> in Washington, with nearly 
#     <b style="color:green; 
#               background-color:yellow;">30,000 vehicles</b>—more than triple the next-highest county. This underscores the strong influence of urban centers on electric vehicle adoption.</b>

# <h3 style="color:green;">Sub_Topic</h3>

# In[33]:


avg_range_by_type = df_deduped.groupby("ev_type")["electric_range"].mean().round(2).reset_index()
avg_range_by_type


# In[34]:


plt.figure(figsize = (8, 5))
sns.barplot(data = avg_range_by_type, x = "ev_type", y = "electric_range", palette = ["g", "y"])
plt.title("Average Electric Range by EV Type", fontsize = 16)
plt.xlabel("EV Type", fontsize = 12)
plt.ylabel("Average Electric Range (miles)", fontsize = 12)
plt.show()


# <b style="color:blue;">BEVs offer a significantly higher average electric range (~
#     <b style="color:green; 
#               background-color:yellow;">194 miles</b>) compared to PHEVs (~
#     <b style="color:white; 
#               background-color:red;">31 miles</b>), making them more suitable for long-distance driving and showing a clear technological edge in battery capacity.</b>

# <h3 style="color:green;">EV Count by CAFV Eligibility</h3>

# In[35]:


cafv_count = df_deduped["cafv_eligibility"].value_counts().reset_index()
cafv_count


# In[36]:


plt.figure(figsize = (10, 5))
sns.barplot(data = cafv_count, x = "cafv_eligibility", y = "count", palette = ["g", "y"])
plt.title("EV Count by CAFV Eligibility", fontsize = 16)
plt.xlabel("Number of Vehicles", fontsize = 12)
plt.ylabel("CAFV Eligibility", fontsize = 12)
plt.show()


# <b style="color:blue;">Over 
#     <b style="color:green; 
#               background-color:yellow;">51,000 EVs qualify for CAFV incentives</b>, highlighting a strong alignment with Washington’s clean transportation goals.
# However, nearly 
#     <b style="color:white; 
#               background-color:red;">19,000 vehicles remain ineligible</b> due to limited battery range, mostly likely PHEVs.</b>

# <h3 style="color:green;">Top 10 Electric Utilities by EV Count</h3>

# In[37]:


top_utilities = df_deduped["electric_utility"].value_counts().nlargest(10).reset_index()
top_utilities


# In[38]:


plt.figure(figsize = (12, 6))
sns.barplot(data = top_utilities, x = "count", y = "electric_utility", palette = "Blues_r")
plt.title("Top 10 Electric Utilities by EV Count", fontsize = 16)
plt.xlabel("Number of EVs", fontsize = 12)
plt.ylabel("Electric Utility", fontsize = 12)
plt.show()


# <b style="color:blue;">
#     <b style="color:green; 
#               background-color:yellow;">Puget Sound Energy Inc dominates</b> the EV charging landscape, appearing in over 
#     <b style="color:green; 
#               background-color:yellow;">30K vehicle records</b>, either alone or jointly with other local utilities — highlighting its key role in supporting Washington’s EV infrastructure.</b>

# <h2 style="color:green;">Feature Engineering</h2>

# <h3 style="color:green;">Extracting Latitude & Longitude from Vehicle Location</h3>

# In[39]:


df_deduped["coords"] = df_deduped["vehicle_location"].str.replace("POINT (", "").str.replace(")", "")
df_deduped["coords"]


# In[40]:


df_deduped[["longitude", "latitude"]] = df_deduped["coords"].str.split(" ", expand=True)
df_deduped[["longitude", "latitude"]]


# In[41]:


import numpy as np


# <b style="color:purple;">Replace Blank Strings with NaN</b>

# In[42]:


df_deduped["longitude"] = df_deduped["longitude"].replace("", np.nan)
df_deduped["latitude"] = df_deduped["latitude"].replace("", np.nan)


# In[43]:


df_deduped["longitude"] = df_deduped["longitude"].astype(float)
df_deduped["latitude"] = df_deduped["latitude"].astype(float)


# In[44]:


df_deduped[["longitude", "latitude"]].isnull().sum()


# <b style="color:purple;">Imputing Missing Lat/Lon with Dummy Coordinates</b>

# In[45]:


df_deduped["longitude"].fillna(0.0, inplace=True)
df_deduped["latitude"].fillna(0.0, inplace=True)


# In[46]:


df_deduped[["longitude", "latitude"]].isnull().sum()


# <b style="color:blue;">To preserve dataset consistency across all visuals, 
#     <b style="color:green; background-color:yellow;">missing latitude and longitude values (6 rows) were imputed with 0.0 instead of dropping them</b> — ensuring no rows were removed post-analysis.</b>

# <b style="color:purple;">Flagging them for Future Filtering if needed (Optional)</b>

# In[47]:


df_deduped["coords_imputed"] = (df_deduped["latitude"] == 0.0) & (df_deduped["longitude"] == 0.0)
df_deduped["coords_imputed"].sum()


# <h3 style="color:green;">EV Distribution Across Locations (<span style="color:green; 
#     background-color:yellow;">Latitude</span> vs 
#     <span style="color:green; background-color:yellow;">Longitude</span>)</h3>

# In[48]:


plt.figure(figsize = (10, 6))
sns.scatterplot(
    data = df_deduped,
    x = "longitude",
    y = "latitude",
    hue = "ev_type",
    palette = "prism",
    s = 20
)

plt.title("EV Geographic Distribution by Vehicle Type", fontsize=16)
plt.xlabel("Longitude", fontsize=12)
plt.ylabel("Latitude", fontsize=12)
plt.legend(title = "EV Type", loc = "upper right")
plt.grid(True, linestyle = ":", linewidth = 0.5)
plt.show()


# <b style="color:blue;">This scatter plot displays the geographic spread of electric vehicles by type. Most vehicles are concentrated in a dense band between latitudes 30–50 and longitudes -130 to -100, highlighting activity primarily across the U.S. West Coast (likely Washington state). However, a few outliers with invalid coordinates (like 0 or 145) appear due to missing/imputed data, which are visually distant from the main cluster. BEVs and PHEVs are both represented across the region, but PHEVs slightly dominate in the spread.</b>

# <b style="color:purple;">Remove placeholder coords from plot</b>

# In[49]:


df_valid_coords = df_deduped[(df_deduped["latitude"] != 0.0) & (df_deduped["longitude"] != 0.0)]

plt.figure(figsize = (10, 6))
sns.scatterplot(
    data = df_valid_coords,
    x = "longitude",
    y = "latitude",
    hue = "ev_type",
    palette = "prism",
    s = 20
)

plt.title("EV Geographic Distribution by Vehicle Type", fontsize=16)
plt.xlabel("Longitude", fontsize=12)
plt.ylabel("Latitude", fontsize=12)
plt.legend(title = "EV Type", loc = "upper right")
plt.grid(True, linestyle = ":", linewidth = 0.5)
plt.show()


# <b style="color:blue;">Most electric vehicles are clustered in the Western United States, with a high concentration between 30°–50° latitude and -130° to -100° longitude. Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) are evenly spread across the region, with a few imputed or invalid outliers. This shows a dense EV presence in states like Washington and Oregon.</b>

# <h3 style="color:green;">Creating a Power BI Specific DataFrame</h3>

# In[50]:


PowerBI_df = df_deduped[[
    "model_year",
    "make",
    "model",
    "ev_type",
    "electric_range",
    "county",
    "latitude",
    "longitude"
]].copy()

PowerBI_df


# <b style="color:purple;">Shortening EV Type</b>

# In[51]:


PowerBI_df["ev_type"] = df_deduped["ev_type"].replace({
    "Battery Electric Vehicle (BEV)": "BEV",
    "Plug-in Hybrid Electric Vehicle (PHEV)": "PHEV"
})

PowerBI_df["ev_type"].value_counts().reset_index()


# <b style="color:purple;">Shortening CAFV Eligibility</b>

# In[52]:


PowerBI_df["cafv_status"] = df_deduped["cafv_eligibility"].replace({
    "Clean Alternative Fuel Vehicle Eligible": "Eligible",
    "Not eligible due to low battery range": "Not Eligible"
})

PowerBI_df["cafv_status"].value_counts().reset_index()


# <b style="color:purple;">Saving Back to MySQL</b>

# In[53]:


PowerBI_df.to_sql("EV_PowerBI", con=engine, if_exists="replace", index=False)


# --------------------
# --------------------
