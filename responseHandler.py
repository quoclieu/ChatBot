import datetime ,requests, json

def process_response(message):
    message = message.lower()
    greetings = ['hey','hello','hi','hallo']
    if(message in grettings):
        response = summary()
    else:
        #default message
        response = 'Hi there! Please send a greeting for a quick summary'
    return response

#Prints a summary of date, PTV, Weather and news
def summary():
    today = datetime.datetime.now()

    newsapi_key = 'e13df0c66f70462abf1dff41505a880f'
    weatherapi_key = '3f014abc78d36de57476f92891bb6360'

    weather = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Melbourne,au&units=metric&appid="+weatherapi_key)
    weather = json.loads(weather.content)
    w_max = weather["main"]["temp_max"]
    w_min = weather["main"]["temp_min"]
    w_curr = weather["main"]["temp"]
    w_desc = weather["weather"][0]["description"]

    news = requests.get("https://newsapi.org/v1/articles?source=techcrunch&apiKey="+newsapi_key)
    news = json.loads(news.content)


    summary = "Summary for today:"+today.strftime("%a %d %b")
summary = '''
Weather
Temperature: %d (%s) Max: %d Min: %d

''' % (w_curr,w_desc,w_max,w_min)


    return summary
