# -*-Mode:python-*-

import os
import tempfile
import sys
import subprocess
import webbrowser
import urllib
import threading
import logging
from StringIO import StringIO

class ThreadedFunc(threading.Thread):
    def __init__(self, target):
        self.__target = target
        threading.Thread.__init__(self)
        self.__success = False
        self.__retval = None
        self.start()

    def run(self):
        self.__retval = self.__target()
        self.__success = True

    def wasSuccessful(self):
        if self.isAlive():
            raise Exception( "Thread not finished" )
        return self.__success

    def getRetval(self):
        if self.isAlive():
            raise Exception( "Thread not finished" )
        return self.__retval

def _get_filelike_timestamp():
    import time

    return time.strftime("%Y%m%d%H%M%S")

def cmd_character_count(ensoapi):
    text = ensoapi.get_selection().get("text", "").strip()
    if not text:
        ensoapi.display_message( "No selection." )
    ensoapi.display_message( "%d characters." % len(text) )

def cmd_date(ensoapi):
    import time

    ensoapi.display_message( "%s" % time.asctime() )

def cmd_insert_date(ensoapi):
    import time

    ensoapi.set_selection( time.asctime() )
    
def cmd_count_lines(ensoapi):
    seldict = ensoapi.get_selection()
    ensoapi.display_message( "Selection is %s lines." % 
                             len(seldict.get("text","").splitlines()) )