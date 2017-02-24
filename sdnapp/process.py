# all the imports
import os
import sys
import sqlite3
#import getlinkinfo
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from getlinkinfo import getlinkobject
from topology import gettopology

def removekeys(topolist, requiredkeys):
    total_routers = len(topolist)
    to_be_deleted = []

    for key in topolist[0]:
        print key
        if key not in requiredkeys:
            to_be_deleted.append(key)

    #print "delete" , to_be_deleted
    #print "add" , requiredkeys

    #delete non required keys
    for i in range(total_routers):
        for key in to_be_deleted:
            del topolist[i][key]

    return topolist

def processtopo():
    topology = gettopology();
    linkinfo = getlinkobject()
    requiredkeys = ["name"]
    removekeys(topology, requiredkeys)
    requiredkeys = ["name"]
    removekeys(linkinfo, requiredkeys)
    for item in topology:
        print item
    print "==================================="
    for item in linkinfo:
        print item


    print links[0]

if __name__ == "__main__":
    if (sys.argv[1] == "pri"):
        processtopo();
    if (sys.argv[1] == "aziz"):
        processtopo();
    if (sys.argv[1] == "veda"):
        processtopo();
