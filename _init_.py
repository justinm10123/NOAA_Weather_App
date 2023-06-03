import requests
import geocoder as geo
import json

geo_location = geo.ip('me') #only provides somewhat of an accurace GPS coordinate, may want to try and use something else
coordinates_list = str(geo_location.latlng)
coordinates = coordinates_list.replace("[","").replace("]","").replace(" ","")


MASTER_URL = "https://api.weather.gov/points/"
NOAA_URL = MASTER_URL + coordinates

#user coordinates (Lat: xx.xxx,Lon: xx.xxx)
#print(NOAA_URL)


response = requests.get(NOAA_URL)
NOAA_points = response.json()

json_text = json.dumps(NOAA_points, sort_keys = True, indent = 1)
formatted_text = json_text.split()

for x in formatted_text:
    if "/hourly" in x:
        global hourly_forecast
        hourly_forecast = x

hourly_search_url = hourly_forecast.replace('"',"")
hourly_search_url = hourly_search_url[:-1]

hourly_response = requests.get(hourly_search_url)
NOAA_hourly = hourly_response.json()

hourly_text = json.dumps(NOAA_hourly, sort_keys = True, indent = 1)
formatted_hourly = hourly_text.replace('"',"").replace(",","").split()#cant split by '{' or '}' because of nested braces


hour_segments = []

for z in formatted_hourly:
    print(z)




