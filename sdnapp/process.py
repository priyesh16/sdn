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
    requiredkeys = ["name", "hostName"]
    removekeys(nodes, requiredkeys)
    for node in nodes:
        if  node['hostName'] == "SF":
            node['Type'] = 'PE'
        elif  node['hostName'] == "NY":
            node['Type'] = 'PE'
        else:
            node['Type'] = 'Core'
        #printdict(node)
    return nodes

def getlinks():
    links = getlinkinfo();
    total_links = len(links)
    requiredkeys = ["name", "operationalStatus", "endA", "endZ"]
    removekeys(links, requiredkeys)
    #print links
    for link in links:
            link["endA_address"] = link["endA"]["ipv4Address"]["address"]
            link["endZ_address"] = link["endZ"]["ipv4Address"]["address"]

    '''
    for link in links:
        del link["endA"]
        del link["endZ"]
        printdict(link)
    '''
    return links;

def getevents():
    links = getlinkinfo();
    total_links = len(links)
    requiredkeys = ["name", "operationalStatus", "endA", "endZ"]
    removekeys(links, requiredkeys)
    #print links
    for link in links:
            link["endA_address"] = link["endA"]["ipv4Address"]["address"]
            link["endZ_address"] = link["endZ"]["ipv4Address"]["address"]

    '''
    for link in links:
        del link["endA"]
        del link["endZ"]
        printdict(link)
    '''
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
    '''
    # Fill only the required fields

    #print links
    for link in links:
            link["endA_address"] = link["endA"]["ipv4Address"]["address"]
            link["endZ_address"] = link["endZ"]["ipv4Address"]["address"]
    '''
    return lsp;

def processtopo():
    topology = gettopology();
    linkinfo = getlinkobject()
    requiredkeys = ["name", "hostname","endA", "endZ"]
    print "==================================="

    removekeys(topology, requiredkeys)
    print "==================================="

    requiredkeys = ["name", "hostname"]
    #removekeys(linkinfo, requiredkeys)
    for item in topology:
        print item, topology
    print "==================================="
    #for item in linkinfo:
        #print item


    #print links[0]

if __name__ == "__main__":
    if (sys.argv[1] == "pri"):
        lsp , authHeader = getlsp();
        setlsp(lsp, authHeader, 'GROUP_FIVE_SF_NY_LSP3');

        setlsp();
    if (sys.argv[1] == "aziz"):
        processtopo();
    if (sys.argv[1] == "veda"):
        processtopo();
