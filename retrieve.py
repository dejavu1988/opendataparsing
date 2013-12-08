#!/usr/bin/env python

import urllib2
import threading
import shutil
import os
import zipfile
import sys

def clear(localPath, localDir):
    zipExists = os.path.exists(localPath)
    dirExists = os.path.exists(localDir)
    if zipExists:
        os.remove(localPath)
        print "zip removed"
    if dirExists:
        shutil.rmtree(localDir)
        print "dir removed"

def retrieve(remotePath):
    try:
        remotedata = urllib2.urlopen(remotePath)
        print "Loading..."
    except IOError:
        print("Network down.")
        sys.exit() 
    
    output = os.tmpfile() 
    output.write(remotedata.read())
    #output.close()
    print "Zip Downloaded."
    return output

def extract(data):
    archive = zipfile.ZipFile(data) 
    if archive.testzip() != None:
        print "Invalid zipfile"
        sys.exit() 
    record = []
    for name in archive.namelist():
        f = archive.open(name, 'rU')
        tmpstr = f.readline()
        while tmpstr:
            if tmpstr[0] != '#':
                entry = tmpstr[:-1].split('|')
                record.append(entry)
            tmpstr = f.readline()
    print "Extracted to record list."
    return record


if __name__ == "__main__":
    remotePath = "http://pilvilinna.cert.fi/opendata/autoreporter/csv.zip"
    #localPath = "csv.zip"
    #localDir = "csv"
    #clear(localPath, localDir)
    data = retrieve(remotePath)
    record = extract(data)
    print len(record)
