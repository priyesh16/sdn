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
from process import *

class EventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print event.src_path
        if event.src_path != "./logs":
            return;
        target = open("./testfile", "a+")
        target.write("this is it \n")
        tunnelchange()


def handleevents():
    print "running handler"
    print "asdfa"
    target = open("./testfile", "a+")
    target.write("this is it \n")
    target.close();
    print "started from"

    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    handleevents()
