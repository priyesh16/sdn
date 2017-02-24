'''
Created on Feb 20, 2016

@author: azaringh
'''

import redis
import json
import pprint

def getevents():
    r = redis.StrictRedis(host='10.10.4.252', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe('link_event')

    for item in pubsub.listen():
        print item['channel'], ":", item['data']
        if isinstance(item['data'], basestring):
            print item['data']
            d = json.loads(item['data'])
            pprint.pprint(d, width=1)

if __name__ == "__main__":
    getevents();
