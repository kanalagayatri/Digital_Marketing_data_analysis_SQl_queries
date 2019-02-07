# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 11:11:08 2018

@author: Gayatri
"""

import pandas as pd
from geopy.geocoders import Nominatim

data1= pd.read_csv("place.csv") #File that contains the name of places and count of times it occured
data1.head(5)
data2=pd.read_csv("lat_long.csv") #File that contains placename and the lat and long of that place
data2.head(5)

final_data = pd.merge(data1,
                 data2[['placename', 'latitude', 'longitude']],
                 on='placename') #Merging only those placenames which are there in both csvs


median=final_data['count'].median()
cond=final_data['count'] >=median
data=final_data[cond].sort_values('placename').groupby('placename').first() #Since lat and long cant be perfect, a single place might have multiple lat and long with 
#little variation, so here I am taking only the 1st lat and long record of each placename 

loc_add = []
loc_country =[] 
loc_neighbour=[] 
loc_postcode=[]
loc_suburb=[]
loc_road=[]
loc_state=[]
lat=[]
lon=[]
placename=[]
count=[]

geolocator = Nominatim(user_agent="xyz")
for index, row in data.iterrows():
    print index
    latitude = row["latitude"]
    longitude = row["longitude"]
    loc=latitude,longitude
    placename.append(index)
    count.append(row["count"])
    try:
        location = geolocator.reverse(loc)
    except:
         location = "N/A"
    lat.append(latitude)
    lon.append(longitude)
    try:
        loc_add.append(location.address)
    except:
        loc_add ="N/A"
    try:
    		loc_country.append(location.raw["address"]["country"])
    except:
		loc_country.append("N/A")
    try:
        loc_neighbour.append(location.raw["address"]["neighbourhood"])
    except:
        loc_neighbour.append("N/A")
    try:
    		loc_postcode.append(location.raw["address"]["postcode"])
    except:
		loc_postcode.append("N/A")
    try:
        loc_suburb.append(location.raw["address"]["suburb"])
    except:
        loc_suburb.append("N/A")
    try:
        loc_road.append(location.raw["address"]["road"])
    except:
        loc_road.append("N/A")
    try:
    		loc_state.append(location.raw["address"]["state"])
    except:
		loc_state.append("N/A")
   

data_op = pd.DataFrame({
        'A_placename':placename,
        'B_lat':lat,
        'C_lon':lon,
        'D_loc_add':loc_add,
        'E_loc_country':loc_country,
        'J_loc_neighbour':loc_neighbour,
        'H_loc_postcode':loc_postcode,
        'G_loc_suburb':loc_suburb,
        'I_loc_road':loc_road,
        'F_loc_state':loc_state,
        'K_count':count})

final_op = pd.DataFrame({'place_name':loc_suburb,
                         'visit_count':count}) #Assigning place_name column to suburb

final_op_grp=final_op.groupby('place_name')["visit_count"].sum().reset_index(name='visitor_count') #Grouping by place_name and taking the sum of count 


final_op_grp=final_op_grp.sort_values(by="visitor_count",ascending=False)

final_op_grp.to_csv("lat_long_places_area.csv", index=False,
                columns=["place_name","visitor_count"]) #Only the suburb data with count

data_op.to_csv("full_data.csv") #Full data including placename, country, postcode, state, road, neighbourhood etc.
