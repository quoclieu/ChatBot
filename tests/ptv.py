from hashlib import sha1
import hmac
import binascii

import requests
import json

def getUrl(request):
    devId = 3000315
    key = '7e46d5b8-15f1-4314-a123-7f3ff852425a'
    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(devId)
    hashed = hmac.new(key, raw, sha1)
    signature = hashed.hexdigest()
    return 'http://timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature)

route_id = 7 #for Glen Waverly line
stop_id = 1137 #For mount waverly
route_type = 0 #ID for trains
direction_id = 1#for heading to city
#request = '/v3/disruptions'
request = '/v3/departures/route_type/0/stop/1137?direction_id=1'#?date_utc=2017-07-09T20:59:00Z'
#request = '/v3/route_types'
#request = '/v3/routes?route_types=2'
#request = '/v3/stops/route/7/route_type/0'
#request = '/v3/directions/route/7'
print getUrl(request)

r = requests.get(getUrl(request))
r = json.loads(r.content)
for i in range(0,30,1):
    print(r["departures"][i]["scheduled_departure_utc"])
