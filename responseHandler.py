# -*- coding: utf-8 -*-
import datetime ,requests, json
from collections import OrderedDict
import random

#Reads the message and returns a list containing the appropriate response
def process_response(message):
    message = message.lower()
    response = []

    greetings = ['hey','hello','hi','hallo']

    response = random.choice([['Haha!'],['Nice!'],["I don't understand!"]])
    if(message in greetings):
        response = summary()
    elif(len(message)>2):
        if(message in "tech news"):
            response = newsURLs(getNews("techcrunch"))
        elif(message in "abc news"):
            response = newsURLs(getNews("abc-news-au"))
        elif(message in "weather"):
            response = weatherTodayStr(getWeather())
        # elif(message in "forecast"):
        #     response = weatherTodayStr(getWeather())
        elif("trains" in message):
            route_id = 7 #for Glen Waverley line
            direction_id = 7#Heading towards Glen Waverley
            num_departs = 5 #number of departure times
            if("more" in message):
                num_departs = 20
            if("mc" in message):
                stop_id = 1120 #Melbourne Central
                station = "Melbourne Central"
            elif("flinder" in message):
                stop_id = 1071 #Flinders
                station = "Flinders"

            else:
                stop_id = 1137 #For mount waverley
                direction_id = 1#for heading to city
                station = "Mount Waverley"
            response = getDepartures(stop_id,direction_id,num_departs)
            response.insert(0,"Glen Waverley Line. Departing: %s" % station)
    return response

def getWeather():
    weatherapi_key = '3f014abc78d36de57476f92891bb6360'
    weather = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=3151,au&units=metric&appid="+weatherapi_key)
    weather = json.loads(weather.content)
    return weather

#Returns string of the weather for today
def weatherTodayStr(weather):

    w_max = weather["main"]["temp_max"]
    w_min = weather["main"]["temp_min"]
    w_curr = weather["main"]["temp"]
    w_desc = weather["weather"][0]["description"]
    weather = ('''
Weather
Temperature: %d (%s)
Max: %d
Min: %d
''' % (w_curr,w_desc,w_max,w_min))
    return weather

def getNews(source):
    newsapi_key = 'e13df0c66f70462abf1dff41505a880f'
    news = requests.get("https://newsapi.org/v1/articles?source="
    +source+"&apiKey="+newsapi_key)
    news = json.loads(news.content)
    return news

#Returns a list of all URLs from a news source dctionary of articles
def newsURLs(news):
    news = news["articles"]
    urls = []
    for article in news:
        urls.append(article["url"])
    return urls


## PTV
from hashlib import sha1
import hmac
import binascii

def getUrl(request):
    devId = 3000315
    key = '7e46d5b8-15f1-4314-a123-7f3ff852425a'
    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(devId)
    hashed = hmac.new(key, raw, sha1)
    signature = hashed.hexdigest()
    return 'http://timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature)


from dateutil import parser, tz
#Converts UTC time to AEST
def melbourneTime(isostr):
  d = parser.parse(isostr)
  d.replace(tzinfo=tz.gettz('UTC')) # Not sure if needed
  return d.astimezone(tz.gettz('Australia/Melbourne'))

 #Returns timetable of trains departing from the specified stop id
def getDepartures(stop_id, dir_id,num_departs):
    from datetime import datetime
    #Convert current time to utc iso 1806 for comparing with api timetable
    now = datetime.now().utcnow().isoformat()

    departs=[]

    request = '/v3/departures/route_type/0/stop/%d?direction_id=%d' % (stop_id,dir_id)

    r = requests.get(getUrl(request))
    r = json.loads(r.content)
    i = 0
    for d in r["departures"]:
        departTime = d["scheduled_departure_utc"]
        if(now<parser.parse(departTime).isoformat()):
            departs.append(str(melbourneTime(departTime))[0:16])
            if(i>num_departs):
                break
            i+=1
    return departs



#Returns a dictionary with a summary of date, PTV, Weather and news
def summary():
    summary = []

    #Date
    today = datetime.datetime.now()
    summary.append("Summary for today: "+today.strftime("%a %d %b"))


    #Summary for weather
    weather = getWeather()
    summary.append(weatherTodayStr(weather))

    #Summary for news
    abc_news = getNews("abc-news-au")["articles"]
    summary.append([])
    i = 0
    for article in abc_news:
        summary[2].append(article["url"])
        i+=1
        #Limit to 4 urls for the summary
        if(i>3):
            summary[2].append('There are '+str(len(abc_news)-i)+' other'
            ' articles. Let me know if you want to read the others!')
            break


    #Upcoming trains


    return summary
# response=process_response("trains")
# print(response)
#
# response=process_response("hi")
# for msg in response:
#     if(len(msg)>640):
#         print("Msg too long")
#         continue
#     #Checks if this section of the list is holding a list of urls
#     if(isinstance(msg,list)):
#         for url in msg:
#             print url
#         continue
#     print(msg)
