# -*- coding: utf-8 -*-
import datetime ,requests, json

def process_response(message):
    message = message.lower()
    response = {}

    greetings = ['hey','hello','hi','hallo']
    if(message in greetings):
        response = summary()
    elif(message == "tech news"):
        response = getNews("techNews")
    else:
        #default message
        response = {'error':'Hi there! Please send a greeting for a quick summary'}

    return response

def getWeather():
    weatherapi_key = '3f014abc78d36de57476f92891bb6360'
    weather = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=3151,au&units=metric&appid="+weatherapi_key)
    weather = json.loads(weather.content)
    return weather


def getNews(source):
    newsapi_key = 'e13df0c66f70462abf1dff41505a880f'
    news = requests.get("https://newsapi.org/v1/articles?source="+source+"&apiKey="+newsapi_key)
    news = json.loads(news.content)
    return news["articles"]

#
# from hashlib import sha1
# import hmac
# import binascii
#
# def getUrl(request):
#     devId = 3000315
#     key = '7e46d5b8-15f1-4314-a123-7f3ff852425a'
#     request = request + ('&' if ('?' in request) else '?')
#     raw = request+'devid={0}'.format(devId)
#     hashed = hmac.new(key, raw, sha1)
#     signature = hashed.hexdigest()
#     return 'http://timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature)
#
# def getTrains():
#     return 1



#Returns a dictionary with a summary of date, PTV, Weather and news
def summary():
    summary = {}

    #Date
    today = datetime.datetime.now()
    summary["date"]="Summary for today: "+today.strftime("%a %d %b")


    #Summary for weather
    weather = getWeather()

    w_max = weather["main"]["temp_max"]
    w_min = weather["main"]["temp_min"]
    w_curr = weather["main"]["temp"]
    w_desc = weather["weather"][0]["description"]
    summary["weather"]='''
Weather
Temperature: %d (%s)
Max: %d
Min: %d
''' % (w_curr,w_desc,w_max,w_min)


    #Summary for news
    tech_news = getNews("techcrunch")
    abc_news = getNews("abc-news-au")

    summary["news"]=''
    for article in abc_news:
        summary["news"] += article["url"] +'\n'


    #Upcoming trains


    return summary

# print(process_response("hi"))
# response=process_response("hi")
# for key in response:
#     if(len(response[key])>640):
#         print("Error: Msg was too long")
#         continue
#     print response[key]
