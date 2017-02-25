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
    requiredkeys = ["name", "hostName","AutonomousSystem","topology"]
    removekeys(nodes, requiredkeys)
    for node in nodes:
        if  node['hostName'] == "SF":
            node['Type'] = 'PE'
        elif  node['hostName'] == "NY":
            node['Type'] = 'PE'
        else:
            node['Type'] = 'Core'

        node["AS"]=str(node["AutonomousSystem"]["asNumber"])
        node["coordinate"]=str(node["topology"]["coordinates"]["coordinates"])

    for node in nodes:
        del node["AutonomousSystem"]
        del node["topology"]
        printdict(node)
    return node



def getlinks():
    links = getlinkinfo();
    total_links = len(links)
    requiredkeys = ["name", "operationalStatus", "endA", "endZ"]
    removekeys(links, requiredkeys)
    #print links
    for link in links:
            link["endA_address"] = link["endA"]["ipv4Address"]["address"]
            link["endZ_address"] = link["endZ"]["ipv4Address"]["address"]
            link["endZ_metric"] = str(link["endZ"]["TEmetric"])


    for link in links:
        del link["endA"]
        del link["endZ"]
        printdict(link)

    return links;

def getlsp():
    LSPs, authHeader = getlsprest()
    total_lsp = len(LSPs)
    requiredkeys = ["from", "to", "name", "lspIndex", "pathType", "plannedProperties"]

    removekeys(LSPs, requiredkeys)
    return LSPs, authHeader

def setlsp(LSPs, authHeader, lspname):
    for lsp in LSPs:
        if lsp['name'] == lspname:
            break

    print lsp

    ero= [{ 'topoObjectType': 'ipv4', 'address': '10.210.15.2'},
          { 'topoObjectType': 'ipv4', 'address': '10.210.13.2'},
          { 'topoObjectType': 'ipv4', 'address': '10.210.17.1'}
         ]
    lsp['plannedProperties'] = {
        'ero': ero
    }

    response = setlsprest(lsp, authHeader)
    print "----"
    print response
    return lsp;

def recentevents():
    lst=[]
    k=0
    filetoread = cwd + "/logs_test"
    for line in reversed(open(filetoread, "r").readlines()):
        k=k+1
        if(k==10):
            break
        data = ast.literal_eval(json.loads(line))
        lst.append(data)
    return(lst)

def getevents():
    event = {}
    return event;

def tunnelchange():
    print "got event changing tunnel"
    nodes = getnodes();
    links = getlinks();
    events = getevents();



if __name__ == "__main__":
    if (sys.argv[1] == "pri"):
        lsp , authHeader = getlsp();
        setlsp(lsp, authHeader, 'GROUP_FIVE_SF_NY_LSP3');
        setlsp();
    if (sys.argv[1] == "aziz"):
        getnodes();
    if (sys.argv[1] == "veda"):
        processtopo();event_handler = MyHandler()
