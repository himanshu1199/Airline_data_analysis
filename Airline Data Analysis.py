#!/usr/bin/env python
# coding: utf-8

# ### Import Required Libraries 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns


# ### Load Dataset

# In[2]:


airlinedata=pd.read_csv('Population.csv')
airlinedata


# ### Explore Dataset

# In[3]:


airlinedata.info()


# In[4]:


## Check for wrong or unrealistic entry

for i in airlinedata.iloc[:,2:].columns:
    print(airlinedata[i].value_counts())
    print('='*25)


# In[5]:


airlinedata.isnull().sum()


# In[6]:


airlinedata.shape


# In[7]:


airlinedata['id'].value_counts().sum() 

## value counts or unique counts of 'id' column is same as number of records, it means there is no duplicate 'id'. 


# #### All the data types are correctly allocated except 'Arrival Delay in Minutes' Col. which is in float64, 310 Null Values in 'Arrival Delay in minutes' column, No duplicate in 'id' column, and No mismatch values in dataset. 

# ### Data Cleaning and Modifications 

# In[8]:


airlinedata.drop('Unnamed: 0', axis=1, inplace=True)


# In[9]:


airlinedata.dropna(inplace=True)


# In[10]:


airlinedata.isnull().sum()


# In[11]:


airlinedata['Arrival Delay in Minutes']=airlinedata['Arrival Delay in Minutes'].astype('int64')
airlinedata.info()


# ### Removing Outliers

# In[12]:


airlinedata.describe()


# #### 1. Here in 'Age' Column min. age is 7, Which is too small to give a authentic Rating about the airline. So, Make minimun age which should be consider for eligibility to rate the airline is 16.
# #### 2. In columns 'Departure Delay in Minutes' and 'Arrival Delay in Minutes' Outliers are present. Remove by Using IQR Method.

# In[13]:


## Select Passengers of age equal to 16 or more than 16. 

airlinedata=airlinedata[airlinedata['Age']>=16]


# In[14]:


## IQR Method to remove outliers of Departure delay and Arrival delay (Because data is skewedly distributed)

## Lower and Upper fence range of Departure delay
q1_of_departure=np.percentile(airlinedata['Departure Delay in Minutes'],25)
q3_of_departure=np.percentile(airlinedata['Departure Delay in Minutes'],75)
iqr_of_departure=q3_of_departure-q1_of_departure
lower_fence_of_departure_delay=q1_of_departure-(1.5*iqr_of_departure)
upper_fence_of_departure_delay=q3_of_departure+(1.5*iqr_of_departure)

## Lower and Upper fence range of Arrival delay
q1_of_arrival=np.percentile(airlinedata['Arrival Delay in Minutes'],25)
q3_of_arrival=np.percentile(airlinedata['Arrival Delay in Minutes'],75)
iqr_of_arrival=q3_of_arrival-q1_of_arrival
lower_fence_of_arrival_delay=q1_of_arrival-(1.5*iqr_of_arrival)
upper_fence_of_arrival_delay=q3_of_arrival+(1.5*iqr_of_arrival)

## Remove Outliers (Outside the Lower and Upper fence range)
airlinedata=airlinedata[airlinedata['Departure Delay in Minutes']>lower_fence_of_departure_delay]
airlinedata=airlinedata[airlinedata['Departure Delay in Minutes']<upper_fence_of_departure_delay]
airlinedata=airlinedata[airlinedata['Arrival Delay in Minutes']>lower_fence_of_arrival_delay]
airlinedata=airlinedata[airlinedata['Arrival Delay in Minutes']<upper_fence_of_arrival_delay]


# In[15]:


airlinedata.describe()


# In[16]:


airlinedata.head(5)


# #### Now the data is good to go.

# ### Data Analysis and Findings 

# In[17]:


airlinedata.columns


# In[18]:


satisfaction=round(airlinedata['satisfaction'].value_counts(normalize=True)*100,2)
print('Satisfaction or Dissatisfaction among the passengers',satisfaction)


# #### Here, around 53% Passenegers are neutral or dissatisfied

# In[19]:


## Departure delay impact on satisfaction of the passengers 

plt.figure(figsize=(12,6))
sns.countplot(data=airlinedata[airlinedata['Departure Delay in Minutes']>0], x='Departure Delay in Minutes', hue='satisfaction')
plt.title('Departure delay impact on satisfaction')
plt.show()


# In[20]:


## Arrival delay time impact on satisfaction of the passengers

plt.figure(figsize=(12,6))
sns.countplot(data=airlinedata[airlinedata['Arrival Delay in Minutes']>0], x='Arrival Delay in Minutes', hue='satisfaction')
plt.title('Arrival delay impact on satisfaction')
plt.show()


# #### Here, we clearly see that impact of departure delay is not much, but impact of arrival delay specially after delay of more than 5 minutes are really concerning. 

# In[21]:


## Arrival delay impact on type of travllers 

plt.figure(figsize=(6,4))
sns.countplot(data=airlinedata[airlinedata['Arrival Delay in Minutes']>5], x='Type of Travel', hue='satisfaction')
plt.title('Arrival delayed more than 5 minutes impact on type of travllers')
plt.show()


# #### Here in this graph more than 90% of personal travllers are dissatisfied by the delay in arrival time, although business travellers are in around 50-50 ratio of satisfaction.

# In[22]:


## Impact of arrival delay on loyal and disloyal Business travellers satisfaction.

plt.figure(figsize=(6,4))
sns.countplot(data=airlinedata[(airlinedata['Arrival Delay in Minutes']>5) & (airlinedata['Type of Travel']=='Business travel')], x='Customer Type', hue='satisfaction')
plt.title('Impact of arrival delay on loyal and disloyal business travellers satisfaction')
plt.show()


# #### In this graph around 75% of disloyal business travellers are dissatisfied by the delay in arrival, although moslty loyal business travellers are satisfied after the delay in arrival but loyal those who are dissatisfied are more than disloyal those who are dissatisfied in terms of numbers. 

# ### Finding 1:
# ### By the above data analysis we find that, delay in departure have not much impact on satisfaction of the passengers, but passengers who face delay in arrival are moslty dissatisfied Specially after 5 minutes of delay. 
# ### It look like delay in arrival definitely impact on the satisfaction of the travellers, rest other factors will be consider. 
# 

# In[23]:


## Amenities with 0 rating means no service provided 

## Inflight wifi service not available ( 0 rating means no wifi service )

no_wifi=airlinedata[airlinedata['Inflight wifi service']==0]

## Online booking service not available ( 0 rating means no Online booking service )

no_online_booking=airlinedata[airlinedata['Ease of Online booking']==0]

## Online boarding service not available ( 0 rating means no Online boarding service )

no_online_boarding=airlinedata[airlinedata['Online boarding']==0]


# In[24]:


## Inflight wifi service not available by class

print('Passengers report NO wifi')
print('Total','     ',no_wifi.count()['Inflight wifi service'])
print('-'*25)
print('Ratio of Class passengers who report no wifi')
print(round(no_wifi['Class'].value_counts()/airlinedata['Class'].value_counts()*100,2) )
print('-'*25)
plt.figure(figsize=(4,4))
plt.pie(x=no_wifi['Class'].value_counts()/airlinedata['Class'].value_counts(), labels=['Business','Eco','Eco Plus'], autopct='%1.2f%%')
plt.title('Share of ratio of class passengers who report no wifi')
plt.show()


# #### Business class with highest share of ratio of passengers who report no wifi out of total passengers.

# In[25]:


### Pivot table of those preferred Class who report no Inflight wifi service

pt_no_wifi=airlinedata[airlinedata['Inflight wifi service']==0].pivot_table(values='Inflight wifi service', index='satisfaction', columns='Class', aggfunc='count')
pt_no_wifi=round(pt_no_wifi/airlinedata[airlinedata['Inflight wifi service']==0]['Inflight wifi service'].count()*100,2)

## Heat map of pt_no_wifi

plt.figure(figsize=(6,4))
sns.heatmap(data=pt_no_wifi, annot=True, linewidths=5, cmap='crest')
plt.title('% of satisfaction of preferred class who reported no Inflight wifi service')
plt.show()


# #### Here, whether the passengers are from business or eco or eco plus class, there satisfaction may not effected by the inflight wifi service unavailablity.

# In[26]:


## Online booking service not available by type of travellers

print('Passengers report NO Online booking service')
print('Total','     ',no_online_booking.count()['Ease of Online booking'])
print('-'*25)
print('Ratio of Type of travellers who report No Online booking')
print(round(no_online_booking['Type of Travel'].value_counts()/airlinedata['Type of Travel'].value_counts()*100,2))
print('-'*25)
plt.figure(figsize=(4,4))
plt.pie(x=no_online_booking['Type of Travel'].value_counts()/airlinedata['Type of Travel'].value_counts(), labels=['Business travel','Personal Travel'], autopct='%1.2f%%')
plt.title('Share of ratio of Type of travellers who report No Online booking')
plt.show()


# #### Personal travellers have highest share of ratio of passengers out of total passengers who report No online booking

# In[27]:


### Pivot table of those Travellers who report no online booking service

pt_no_online_booking=airlinedata[airlinedata['Ease of Online booking']==0].pivot_table(values='Ease of Online booking', index='satisfaction', columns='Type of Travel', aggfunc='count')
pt_no_online_booking=round(pt_no_online_booking/airlinedata[airlinedata['Ease of Online booking']==0]['Ease of Online booking'].count()*100,2)

## Heat map of pt_no_online_booking

plt.figure(figsize=(6,4))
sns.heatmap(data=pt_no_online_booking, annot=True, linewidths=5, cmap='crest')
plt.title('% of satisfaction of travellers who reported no Online booking service')
plt.show()


# #### In case of Business travellers most of them are look satisfied, it may because business travellers booked thier tickets by the contact of agents, hence they do not face any difficulty whether Online booking service is available or not. But In case of Personal travellers scenario is different, here most of them report dissatisfaction, It may have a chance that no online booking service impact on there satisfaction rating.
# 

# In[28]:


## Online boarding service not available by type of travellers

print('Passengers report NO Online boarding service')
print('Total','     ',no_online_boarding.count()['Online boarding'])
print('-'*25)
print('Ratio Type of travellers who report No Online boarding')
print(round(no_online_boarding['Type of Travel'].value_counts()/airlinedata['Type of Travel'].value_counts()*100,2))
print('-'*25)
plt.figure(figsize=(4,4))
plt.pie(x=no_online_boarding['Type of Travel'].value_counts()/airlinedata['Type of Travel'].value_counts(), labels=['Business travel','Personal Travel'], autopct='%1.2f%%')
plt.title('Share of ratio Type of travellers who report No Online boarding')
plt.show()


# #### Personal travellers have highest share of ratio of passengers who report No online boarding out of total passengers.

# In[29]:


### Pivot table of those Travellers who report no online boarding service

pt_no_online_boarding=airlinedata[airlinedata['Online boarding']==0].pivot_table(values='Online boarding', index='satisfaction', columns='Type of Travel', aggfunc='count')
pt_no_online_boarding=round(pt_no_online_boarding/airlinedata[airlinedata['Online boarding']==0]['Online boarding'].count()*100,2)

## Heat map of pt_no_online_booking

plt.figure(figsize=(6,4))
sns.heatmap(data=pt_no_online_boarding, annot=True, linewidths=5, cmap='crest')
plt.title('% of satisfaction of travellers who reported no Online boarding service')
plt.show()


# ####  Unavailablity  of online boarding service may effect the satisfaction of personal travellers, but for business travellers it look like they do not have much issue whether the online boarding service available or not. 

# ### Finding 2: 
# ### By the above analysis, Mostly Business class passengers reported no Inflight wifi service, but it may not impact on thier satisfaction decision, similar case in other preferred class.
# ### In other unavailable services like online booking and online boarding, it look like Personal travellers hold the high chance to get dissatisfied but unavailablity of these serivces. 

# In[30]:


## Airline Amenities with mode (Most Frequent) of rating equal to 3 or less than 3 ( General )

for i in airlinedata.iloc[:,7:21]:
    if airlinedata[i].mode()[0]<=3:
        print(i,'Most frequent Rating: ',airlinedata[i].mode()[0])
        print('-'*25)


# In[31]:


airlinedata[['Inflight wifi service', 'Ease of Online booking', 'Gate location']].describe()


# #### Here, Inflight wifi service and Ease of Online booking have mode of rating is 2 and 3 respectively with high standard deviation compare to Gate location with respectively low standard deviation which means rating of gate location is sort of similar with less dispersion between the rating points.
# #### And also gate location is one of those things which regulated by the airport authorities, airlines can not do much about that. 
# #### Taking Inflight wifi service and Ease of online booking for further study 
# #### Note:- '0' rating in Inflight wifi and Online booking is consider as service not provided.

# In[32]:


## Count plot of Inflight wifi rating 

plt.figure(figsize=(6,4))
sns.countplot(data= airlinedata[airlinedata['Inflight wifi service']!=0], x='Inflight wifi service', palette='rocket' )
plt.title('Count plot of inflight wifi service')
plt.show()


# #### For Inflight wifi service most of the passengers rate below 4.

# In[33]:


## Which Class give what rating to in flight wifi service 

plt.figure(figsize=(8,4))
sns.countplot(data=airlinedata[airlinedata['Inflight wifi service']!=0], hue='Inflight wifi service', x='Class', palette='rocket')
plt.title('Preferred Class rating distribution of Inflight wifi service')
plt.show()


# #### Here, This plot show that Whether it is business class or eco or eco plus mostly of the passengers give 2 and 3 rating, which is not a good rating.

# In[34]:


## Count plot of Ease of Online booking rating 

plt.figure(figsize=(6,4))
sns.countplot(data= airlinedata[airlinedata['Ease of Online booking']!=0], x='Ease of Online booking', palette='rocket')
plt.title('Count plot of Ease of Online booking')
plt.show()


# #### Similar as Inflight wifi service rating, Ease of online booking have low rating score, mostly below 4.

# In[35]:


## Which Class give what rating to in flight wifi service 

plt.figure(figsize=(8,5))
sns.countplot(data=airlinedata[airlinedata['Ease of Online booking']!=0], hue='Ease of Online booking', x='Type of Travel', palette='rocket')
plt.title('Type of travellers rating distribution of Ease of online booking')
plt.show()


# #### In this plot, Although Business travellers mostly rate 2 and 3 but also there are sort of similar count of business travellers who rate 4, but in case of personal travellers mostly rate 2 and 3 followed by 1 rating which means there is definitely personal travellers face some issue with online booking.  

# ### Finding 3 
# ### Inflight wifi service is really concerning because all of the preferred class report low rating of 2-3 which is not consider as good rating, also there are many passengers who report no wifi as well in above data analysis, which means at many place wifi service is not available yet and if wifi service is present it is not working well.
# ### And for online booking it look like business travellers are sort of neutral but personal travellers give low rating of 2 and 3, it may because  many business travellers book thier ticket through agencies and personal travellers mostly book by them self.

# In[36]:


## Mean rating of particular amenity is small then 3 by Class and type of travellers 

print('Mean of Ratings of amenities by class and type of travellers ( any mean of rating smaller than 3)')
print('')
for i in airlinedata.iloc[:,7:21]:
    pt=airlinedata[airlinedata[i]!=0].pivot_table(values=i, index='Class', columns='Type of Travel', aggfunc='mean', margins=True, margins_name='Total')
    if i == 'Gate location':
        continue
    if np.any(pt.values<3):    
        print(i)
        print('-'*25)
        print(pt)
        print('='*25)


# #### After take a view on the above output, there are some amenities to address like : Inlfight wifi service which we already analyse, similarly we analysed online booking and other looks ok but Online boarding for personal travellers seems to be concerning.
# #### In online boarding personal travellers average rating was low.

# In[37]:


##Travellers rating distribution on Online boarding

plt.figure(figsize=(8,4))
sns.countplot(data=airlinedata[airlinedata['Online boarding']!=0], hue='Online boarding',x='Type of Travel', palette='rocket')
plt.title('Type of Travellers rating distribution on Online boarding')
plt.show()


# #### Here, Business travellers give good rating to online boarding, on the other hand personal travellers give moslty 3 followed by 2 and 4, which is consider as neutral rating. 

# ### Finding 4 
# ### Here, it look like business travellers are sort of positive with online boarding, but personal travellers report sort of neutral rating of 3 followed by 2 and 4. which is consider as ok ok condition of online bording. In above analysis there are also some passengers who report no online boarding which show impact specially on personal travellers. It means first at many place there are no online boarding service, and if it is there then it may not work satisfactory. 

# ## Conclusion
# ## At the last of this data analysis we found that there are 4 kind of issue with the airline. Delay in arrival, Inflight wifi service, Ease of online booking, Online boarding service
# ## If we consider other factors constant, delay in arrival have definitely impact on satisfaction of the passengers specially when the delay is more than 5 minutes and those passengers who travel for personal reasons are mostly dissatisfied, So if flights will have more delays in arrival this will definitely become one of the reason of dissatisfaction among the passengers.
# ## Now come to the other issues like Inflight wifi, Online booking and Online boarding. Some of the passengers report unavailability of these service and if these service were there then they are not working well, in case of wifi most of passengers gave rating of below 3 which is really concerning, similar case with online booking, many of the passengers reported No online booking, mostly personal travellers were there it may because many business travellers prefer to book there tickets through agencies, but personal travellers really do it with Website or other portals, and if the online booking service was there then it would not working well, thats why moslty personal travellers give low rating to online booking service. But in Online boarding, ratings were sort of neutral but average rating of personal travellers was lower side, but at some place passengers reported No online boarding service, mostly personal travellers reported this and these are some issues which could be the reason of dissatisfaction among the passengers. 
