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
formatted_hourly = hourly_text.replace('"',"").replace(",","").split("number")#cant split by '{' or '}' because of nested braces

#[0] is intro data/metadata stuff. [1] starts at current day/current hour script was ran and goes to [156?] for future hours/days
#print(formatted_hourly[1])

hourly = formatted_hourly[1].split()
print(hourly)




########################## should probably append the values to the lists below as to have all of the values in one list to reference in Access database/Tableau #################
number = hourly[1]
precipitation_chance = hourly[7]
relative_humidity = hourly[14]


def find_words_between_strings(hourly):
    found_words = []
    start_index = -1
    global end_index
    end_index = -1
    global final_words

    for i in range(len(hourly)):
        if hourly[i] == "shortForecast:":
            start_index = i + 1
        elif hourly[i] == "startTime:":
            end_index = i
            break
        elif start_index != -1 and end_index == -1:
            found_words.append(hourly[i])
    final_words = " ".join(found_words)


find_words_between_strings(hourly)
print("Number: " + number + "\n" + "Chance of Precipitation: " + precipitation_chance + "%" + "\n" + "Relative Humidity: " + relative_humidity + "\n" + "Short Forecast: " + final_words)

print(end_index) ####### Can use end_index variable to position the remainder of the array placements since short forecast can be different word legths #############
print(hourly[end_index + 1])#this will be the start date (will need to be formatted)

#start_time = hourly[]