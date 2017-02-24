'''
Created on Feb 21, 2016

@author: azaringh
'''

'''
Retrieve topology of the network
'''

import requests
requests.packages.urllib3.disable_warnings()
import json
import sys

def gettopology():
	url = "https://10.10.2.29:8443/oauth2/token"

	payload = {'grant_type': 'password', 'username': 'group8', 'password': 'Group8'}
	response = requests.post (url, data=payload, auth=('group8','Group8'), verify=False)
	json_data = json.loads(response.text)
	authHeader= {"Authorization":"{token_type} {access_token}".format(**json_data)}

	r = requests.get('https://10.10.2.29:8443/NorthStar/API/v1/tenant/1/topology/1', headers=authHeader, verify=False)
	jsonob = r.json()
	jsonstr = json.dumps(jsonob, indent=4, separators=(',', ':'))
	dictob = json.loads(jsonstr)
	topolist = dictob['nodes']
	#nodes_cnt = len(topolist)
	#for i in range(nodes_cnt):
	#	print topolist[i]
	return topolist

		

if __name__ == "__main__":
	if (sys.argv[1] == "pri"):
		gettopology()
	if (sys.argv[1] == "aziz"):
		gettopology()
	if (sys.argv[1] == "veda"):
		gettopology()
