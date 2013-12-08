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
    recordlist = []
    for name in archive.namelist():
        print "Processing file: " + name
        f = archive.open(name, 'rU')
        tmpstr = f.readline()
        while tmpstr:
            if tmpstr[0] != '#':
                entry = tmpstr[:-1].split('|')
                if len(entry) != 9:
                    print entry
                recordlist.append(tuple(entry))
            tmpstr = f.readline()
        f.close()
    archive.close()
    data.close()
    print "Extracted to record list: " + str(len(recordlist)) + " entries."
    return recordlist

def dump(recordlist):
    f = open('record.csv','w')
    for entry in recordlist:
        tmpstr = ''
        for item in entry:
            tmpstr += item + '|'
        f.write(tmpstr[:-1]+'\n')
    f.close()
    print "Record object dumped."

def analyseMainCategory(recordlist):
    print "Analysing MainCategory-Frequency.."
    catedict = {}
    for entry in recordlist:
        if len(entry) != 9:
            print entry
            continue
        cate = entry[5]
        if catedict.has_key(cate):
            catedict[cate] = catedict[cate] + 1
        else:
            catedict[cate] = 1
    return catedict

def analyseLocation(recordlist):
    print "Analysing Location-Frequency.."
    locdict = {}
    for entry in recordlist:
        if len(entry) != 9:
            print entry
            continue
        loc = entry[7]+entry[8]
        if locdict.has_key(loc):
            locdict[loc] = locdict[loc] + 1
        else:
            locdict[loc] = 1
    return locdict

def output(resdict, path):
    f = open(path, 'w')
    for key in resdict.keys():
        entry = key+' '+str(resdict[key])+'\n'
        print entry
        f.write(entry)
    f.close()

if __name__ == "__main__":
    remotePath = "http://pilvilinna.cert.fi/opendata/autoreporter/csv.zip"
    data = retrieve(remotePath)
    recordlist = extract(data)
    dump(recordlist)
    catedict = analyseMainCategory(recordlist)
    locdict = analyseLocation(recordlist)
    output(catedict, 'category-frequency.csv')
    output(locdict, 'location-frequency.csv')
