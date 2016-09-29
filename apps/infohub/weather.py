from .models import InfoSource, Audit
from ..login_reg.models import User
import time
import urllib2
import json
import time

def getWeather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    country_code = "us" #default to US
    api_key = "163bd75ee602dde7c9a370f073b57f04"
    # city_id = "5809844" #this is for Seattle

    url = base_url + city + "," + country_code + "^mode=JSON&appid=" + api_key

    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    content = json.load(resp)

    weather = []
    #details to add to weather array to return to index/views
    weather.append(content["name"])
    weather.append(content["weather"][0]["main"])
    weather.append(content["weather"][0]["description"])
    weather.append(round((content["main"]["temp"]) * 9/5 - 459.67, 2)) #API returns Kelvins, converting to F, round using 'round()' function
    weather.append(content["main"]["humidity"])
    weather.append(content["coord"]["lat"])
    weather.append(content["coord"]["lon"])
    return weather
