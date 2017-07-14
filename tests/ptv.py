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

route_id = 7 #for Glen Waverley line
stop_id = 1137 #For mount waverly
route_type = 0 #ID for trains
direction_id = 1 #for heading to city

#stop_id = 1071 #Flinders
#stop_id = 1120 #Melbourne Central
#direction_id = 7#Heading towards Glen Waverley



#request = '/v3/disruptions'
#request = '/v3/departures/route_type/0/stop/1137?direction_id=1'
#request = '/v3/route_types'
#request = '/v3/routes?route_types=0'
#request = '/v3/stops/route/7/route_type/0'
#request = '/v3/directions/route/7'



# print getUrl(request)
# r = requests.get(getUrl(request))
# r = json.loads(r.content)
# print(r)

from dateutil import parser, tz
#Converts UTC time to AEST
def melbourneTime(isostr):
  d = parser.parse(isostr)
  d.replace(tzinfo=tz.gettz('UTC')) # Not sure if needed
  return d.astimezone(tz.gettz('Australia/Melbourne'))

#Returns timetable of trains departing from the specified stop id
def getDepartures(stop_id):
    from datetime import datetime
    #Convert current time to utc iso 1806 for comparing with api timetable
    now = datetime.now().utcnow().isoformat()
    print now

    departs=[]

    #If stop is at mount waverley, set direction to towards Flinders
    if(stop_id==1137):
        dir_id = 1
    #Otherwise set direction to towards Mount Waverley
    else:
        dir_id = 7

    request = '/v3/departures/route_type/0/stop/%d?direction_id=%d' % (stop_id,dir_id)

    r = requests.get(getUrl(request))
    r = json.loads(r.content)

    for d in r["departures"]:
        departTime = d["scheduled_departure_utc"]
        if(now<parser.parse(departTime).isoformat()):
            departs.append(melbourneTime(departTime))
    return departs



departs = getDepartures(1120)
for d in departs:
    print str(d)[0:16]
print departs
