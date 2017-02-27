# all the imports
import os
import sys
import sqlite3
#import getlinkinfo
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from links_rest import *
from topology_rest import *
from link_event_rest import *
from lsp_rest import *
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sdnapp
import ast

cwd = "/home/group-eight/sdn/sdnapp"

routers = [
           { 'name': 'chicago', 'router_id': '10.210.10.124', 'interfaces': [
                                                                            { 'name': 'ge-1/0/1', 'address': '10.210.16.2' },
                                                                            { 'name': 'ge-1/0/2', 'address': '10.210.13.2' },
                                                                            { 'name': 'ge-1/0/3', 'address': '10.210.14.2' },
                                                                            { 'name': 'ge-1/0/4', 'address': '10.210.17.2' }
                                                                            ]
            },
           { 'name': 'san francisco', 'router_id': '10.210.10.100', 'interfaces': [
                                                                            { 'name': 'ge-1/0/0', 'address': '10.210.18.1' },
                                                                            { 'name': 'ge-1/0/1', 'address': '10.210.15.1' },
                                                                            { 'name': 'ge-1/0/3', 'address': '10.210.16.1' }
                                                                            ]
            },
           { 'name': 'dallas', 'router_id': '10.210.10.106', 'interfaces': [
                                                                             { 'name': 'ge-1/0/0', 'address': '10.210.15.2' },
                                                                             { 'name': 'ge-1/0/1', 'address': '10.210.19.1' },
                                                                             { 'name': 'ge-1/0/2', 'address': '10.210.21.1' },
                                                                             { 'name': 'ge-1/0/3', 'address': '10.210.11.1' },
                                                                             { 'name': 'ge-1/0/4', 'address': '10.210.13.1' }
                                                                             ]
            },
           { 'name': 'miami', 'router_id': '10.210.10.112', 'interfaces': [
                                                                            { 'name': 'ge-1/0/0', 'address': '10.210.22.1' },
                                                                            { 'name': 'ge-1/0/1', 'address': '10.210.24.1' },
                                                                            { 'name': 'ge-1/0/2', 'address': '10.210.12.1' },
                                                                            { 'name': 'ge-1/0/3', 'address': '10.210.11.2' },
                                                                            { 'name': 'ge-1/0/4', 'address': '10.210.14.1' }
                                                                            ]
            },
           { 'name': 'new york', 'router_id': '10.210.10.118', 'interfaces': [
                                                                               { 'name': 'ge-1/0/3', 'address': '10.210.12.2' },
                                                                               { 'name': 'ge-1/0/5', 'address': '10.210.17.1' },
                                                                               { 'name': 'ge-1/0/7', 'address': '10.210.26.1' }
                                                                               ]
            },
           { 'name': 'los angeles', 'router_id': '10.210.10.113', 'interfaces': [
                                                                                  { 'name': 'ge-1/0/0', 'address': '10.210.18.2' },
                                                                                  { 'name': 'ge-1/0/1', 'address': '10.210.19.2' },
                                                                                  { 'name': 'ge-1/0/2', 'address': '10.210.20.1' }
                                                                                  ]
            },
           { 'name': 'houston', 'router_id': '10.210.10.114', 'interfaces': [
                                                                              { 'name': 'ge-1/0/0', 'address': '10.210.20.2' },
                                                                              { 'name': 'ge-1/0/1', 'address': '10.210.21.2' },
                                                                              { 'name': 'ge-1/0/2', 'address': '10.210.22.2' },
                                                                              { 'name': 'ge-1/0/3', 'address': '10.210.25.1' }
                                                                              ]
            },
           { 'name': 'tampa', 'router_id': '10.210.10.115', 'interfaces': [
                                                                            { 'name': 'ge-1/0/0', 'address': '10.210.25.2' },
                                                                            { 'name': 'ge-1/0/1', 'address': '10.210.24.2' },
                                                                            { 'name': 'ge-1/0/2', 'address': '10.210.26.2' }
                                                                            ]
            }
           ]


def printdict(dictobj):
    for key in dictobj:
        print "\n\t" + key +" = " + dictobj[key],

    print ""

def removekeys(topolist, requiredkeys):
    total_nodes = len(topolist)
    to_be_deleted = []

    for key in topolist[0]:
        #print key, topolist[0][key]
        if key not in requiredkeys:
            to_be_deleted.append(key)

    #print "delete" , to_be_deleted
    #print "add" , requiredkeys

    #delete non required keys
    for i in range(total_nodes):
        for key in to_be_deleted:
            del topolist[i][key]
    return topolist

def getnodes():
    nodes = gettopoinfo();
    total_nodes = len(nodes)
    """
    for node in nodes:
        for key in node:
            print key + " = " + str(node[key])
    """
    requiredkeys = ["name", "hostName","AutonomousSystem","topology"]
    removekeys(nodes, requiredkeys)
    for node in nodes:
        if  node['hostName'] == "SF":
            node['Type'] = 'PE'
        elif  node['hostName'] == "NY":
            node['Type'] = 'PE'
        else:
            node['Type'] = 'Core'
        #print node
        node["AS"]=str(node["AutonomousSystem"]["asNumber"])
        node["coordinate"]=str(node["topology"]["coordinates"]["coordinates"])

    for node in nodes:
        del node["AutonomousSystem"]
        del node["topology"]
        #printdict(node)
    return nodes

def getlinks():
    links = getlinkinfo();
    total_links = len(links)
    """
    for link in links:
        for key in link:
            print key + " = " + str(link[key])
    """
    requiredkeys = ["name", "operationalStatus", "endA", "endZ"]
    removekeys(links, requiredkeys)
    #print links
    for link in links:
            link["IP_A"] = link["endA"]["ipv4Address"]["address"]
            link["IP_Z"] = link["endZ"]["ipv4Address"]["address"]
            #print link
            #print link["endA"]["TEmetric"]
            #link["AZ_metric"] = str(link["endA"]["TEmetric"])
            #link["ZA_metric"] = str(link["endA"]["TEmetric"])
            #link["AZ_BW"] = str(link["endA"]["bandwidth"])
            #link["ZA_BW"] = str(link["endZ"]["bandwidth"])


    for link in links:
        del link["endA"]
        del link["endZ"]
        #printdict(link)

    return links;

def getlinkfromaddress(address, links):

    for link in links:
        if link['IP_A'] == address or link['IP_Z'] == address:
            return link;




def getlspforset():
    LSPs, authHeader = getlsprest()
    total_lsp = len(LSPs)
    requiredkeys = ["from", "to", "name", "lspIndex", "pathType", "plannedProperties"]

    removekeys(LSPs, requiredkeys)

    return LSPs, authHeader

def recentevents():
    events=[]
    tot_events=10
    filetoread = cwd + "/logs_test"
    for line in reversed(open(filetoread, "r").readlines()):
        tot_events = tot_events - 1
        if(tot_events == 0):
            break
        data = ast.literal_eval(json.loads(line))
        events.append(data)
    #for event in events:
        #printdict(event)
    return(events)

def getlinkfromevent(event, links):
    if (event["status"] == "failed" or event["status"] == "healed"):
            for link in links:
                if link["IP_A"] == event["interface_address"]:
                    break
    return link

def getrouterfromaddress(address):
    got = 0
    for router in routers:
        if router['router_id'] == address:
            return router
        for key in router['interfaces']:
            if key['address'] == address:
                got = 1
                break
        if (got == 1):
            break
    return router

SF_CH = "10.210.16.2"
CH_SF = "10.210.16.1"

NY_CH = "10.210.17.2"
CH_NY = "10.210.17.1"

SF_DA = "10.210.15.2"
DA_SF = "10.210.15.1"

DA_MI = "10.210.11.2"
MI_DA = "10.210.11.1"

MI_NY = "10.210.12.2"
NY_MI = "10.210.12.1"

available_erosSFNY = [
    {"SF_CH_NY" :   [{u'topoObjectType': u'ipv4', u'address': SF_CH},
                    {u'topoObjectType': u'ipv4', u'address': CH_NY},
                    ]
    },
    {"SF_DA_MI_NY" :    [{u'topoObjectType': u'ipv4', u'address': SF_DA},
                        {u'topoObjectType': u'ipv4', u'address': DA_MI},
                        {u'topoObjectType': u'ipv4', u'address': MI_NY},
                        ]
    }
]

available_erosNYSF = [
    {"NY_CH_SF" :   [{u'topoObjectType': u'ipv4', u'address': NY_CH},
                    {u'topoObjectType': u'ipv4', u'address': CH_SF},
                    ]
    },
    {"NY_MI_DA_SF" :    [{u'topoObjectType': u'ipv4', u'address': NY_MI},
                        {u'topoObjectType': u'ipv4', u'address': MI_DA},
                        {u'topoObjectType': u'ipv4', u'address': DA_SF},
                        ]
    },
]


def computeero(lsp, link):
    available_eros = []
    if lsp['name'].find('NY_SF') != -1:
        available_eros = available_erosNYSF

    if lsp['name'].find('SF_NY') != -1:
        available_eros = available_erosSFNY

    linkA = link['IP_A']
    linkB = link['IP_Z']
    print linkA
    print linkB

    #print "-----------"
    #print available_eros
    #print "-----------"

    #prune failed links
    for ero in available_eros:
        for key in ero:
            for path in ero[key]:
                for key in path:
                    if key == "address":
                        if  path[key] == linkA or path[key] == linkB:
                            available_eros.remove(ero)
    print "+---------+"
    for key in available_eros[0]:
        print available_eros[0][key]
        ero = available_eros[0][key]

    print "+---------+"

    return ero

grouplspname = "GROUP_TEN_SF_NY_LSP3"

def tunnelchange(test):
    print "got event changing tunnel"
    LSPs, authHeader = getlsp()
    #nodes = getnodes();
    links = getlinks();
    #events = recentevents();

    if (test == 0):
            link = getlinkfromevent(recentevent, links)

            routerA = getrouterfromaddress(link['IP_A'])
            routerZ = getrouterfromaddress(link['IP_Z'])
            print "link from " + routerA['name']  + " to ",
            print routerZ['name'] + " failed "

    if (test == 1):
        print "++++++++++++"
        recentevent = {'status': 'healed', 'router_id': '10.210.10.113',
            'timestamp': 'Sun:05:43:46', 'interface_address': '10.210.16.1',
            'interface_name': 'ge-1/0/0', 'router_name': 'los angeles'}
        for failedlink in links:
            if failedlink['name'] == 'L10.210.16.1_10.210.16.2':
                break
            failedlink['operationalStatus'] = 'Down'

    if (test == 2):
        recentevent = {'status': 'healed', 'router_id': '10.210.10.113',
            'timestamp': 'Sun:05:43:46', 'interface_address': '10.210.15.1',
            'interface_name': 'ge-1/0/0', 'router_name': 'los angeles'}
        for failedlink in links:
            if failedlink['name'] == 'L10.210.15.1_10.210.15.2':
                break
            failedlink['operationalStatus'] = 'Down'


    failedlsps = getfailedlsps(LSPs, failedlink, test);
    for failedlsp in failedlsps:
        if failedlsp['name'] == "GROUP_TEN_SF_NY_LSP3":
            break

    ero = computeero(failedlsp, failedlink)
    lsp_list , authHeader = getlsprest();
    lsp = modifylsprest(lsp_list, ero, 'GROUP_TEN_SF_NY_LSP3')

    setlsprest(lsp, authHeader);

def checklinksstatus(linkname, test):
    links = getlinks();
    if (test == 1):
        for link in links:
            if link['name'] == 'L10.210.16.1_10.210.16.2':
                link['operationalStatus'] = 'Down'
                break
    if (test == 2):
        for link in links:
            if link['name'] == 'L10.210.15.1_10.210.15.2':
                link['operationalStatus'] = 'Down'
                break

    for link in links:
        #print link['name'], link['operationalStatus']
        if link['operationalStatus'] == 'Up':
            continue
        elif link['name'] == linkname:
            return False
    return True

def getfailedlsps(LSPs, failedlink, test):
    failedlsps = []
    for lsp in LSPs:
        for key in lsp:
            if key.find("link") != -1:
                if checklinksstatus(lsp[key], test) == False:
                    failedlsps.append(lsp);
    #print failedlsps
    return failedlsps

def getlsp():
    LSPs, authHeader = getlsprest()
    total_lsp = len(LSPs)
    links = getlinks()

    #filter out our lsps
    LSPs = [lsp for lsp in LSPs if lsp['name'].find("TEN") != -1]
    '''
    for lsp in LSPs:
        for key in lsp:
            print key + " = " + str(lsp[key])
        break
    '''

    requiredkeys = ["from", "to", "name", "pathType","lspIndex","tunnelId","operationalStatus","liveProperties"]
    removekeys(LSPs, requiredkeys)
    for lsp in LSPs:
            lsp["From"] = lsp["from"]["address"]
            lsp["To"] = lsp["to"]["address"]
            lsp["tunnelId"] = str(lsp["tunnelId"])
            lsp["routehops"] = str(len(lsp["liveProperties"]["ero"]))
            i = 0;
            testlinks = [];
            lsp["route0"] = lsp["from"]["address"]
            router = getrouterfromaddress(lsp["route0"])
            lsp["router0"] = router['name']
            for ero in lsp["liveProperties"]["ero"]:
                i = i + 1;
                for key in ero:
                    if key == "address":
                        newkey = "route" + str(i)
                        lsp[newkey] = ero[key]
                        #testlinks.append(getlinkfromaddress(lsp[newkey]));

                        router = getrouterfromaddress(lsp[newkey])
                        newkey = "router" + str(i)
                        lsp[newkey] = router['name']

                        link = getlinkfromaddress(ero[key], links)
                        newkey = "link" + str(i)
                        lsp[newkey] = link['name']


            destkey = "route" + str(len(lsp["liveProperties"]["ero"]) + 1)
            lsp[destkey] = lsp["to"]["address"]
            #print lsp['name']
            #for link in testlinks:
                #print "\t" + link['name']
            #lsp["computestatus"] = str(checklinksstatus(testlinks))
            #router = getrouterfromaddress(lsp[destkey])
            #destkey = "router" + str(len(lsp["liveProperties"]["ero"]) + 1)
            #lsp[destkey] = router['name']
    for lsp in LSPs:
        del lsp["from"]
        del lsp["to"]
        del lsp["liveProperties"]
        #printdict(lsp)
    return LSPs, authHeader

if __name__ == "__main__":
    print len(sys.argv)
    if (len(sys.argv) == 3):
        test = int(sys.argv[2])
        tunnelchange(test)
    else:
        globals()[sys.argv[1]]()
