'''
Created on Feb 21, 2016

@author: azaringh
'''
import requests
requests.packages.urllib3.disable_warnings()
import json

def getlsprest():
    url = "https://10.10.2.29:8443/oauth2/token"

    payload = {'grant_type': 'password', 'username': 'group8', 'password': 'Group8'}
    response = requests.post (url, data=payload, auth=('group8','Group8'), verify=False)
    json_data = json.loads(response.text)
    authHeader= {"Authorization":"{token_type} {access_token}".format(**json_data)}

    r = requests.get('https://10.10.2.29:8443/NorthStar/API/v1/tenant/1/topology/1/te-lsps/', headers=authHeader, verify=False)

    p = json.dumps(r.json())
    lsp_list = json.loads(p)
    return lsp_list, authHeader

SF_CH = "10.210.16.2"
CH_SF = "10.210.16.1"

NY_CH = "10.210.17.2"
CH_NY = "10.210.17.1"

def modifylsprest(lsp_list, ero, name):
    # Find target LSP to use lspIndex
    for lsp in lsp_list:
        if lsp['name'] == name:
            break

    # Fill only the required fields
    '''
    ero= [
                    { 'topoObjectType': 'ipv4', 'address': '10.210.15.2'},
                    { 'topoObjectType': 'ipv4', 'address': '10.210.13.2'},
                    { 'topoObjectType': 'ipv4', 'address': '10.210.17.1'}
                   ]
    '''

    new_lsp = {}
    for key in ('from', 'to', 'name', 'lspIndex', 'pathType'):
        new_lsp[key] = lsp[key]

    new_lsp['plannedProperties'] = {
        'ero': ero
    }
    return new_lsp;

def setlsprest(new_lsp, authHeader):
    response = requests.put('https://10.10.2.29:8443/NorthStar/API/v1/tenant/1/topology/1/te-lsps/' + str(new_lsp['lspIndex']),
                            json = new_lsp, headers=authHeader, verify=False)
    #print response.text
    return response.text

if __name__ == "__main__":
    ero = [
            {u'topoObjectType': u'ipv4', u'address': SF_CH},
            {u'topoObjectType': u'ipv4', u'address': CH_NY},
    ]

    lsp_list , authHeader = getlsprest();
    lsp = modifylsprest(lsp_list, ero, 'GROUP_TEN_SF_NY_LSP3')
    setlsprest(lsp, authHeader);
