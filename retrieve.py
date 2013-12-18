#!/usr/bin/env python
"""
    Explicitly retrieve csv.zip from url, merge and analyse category & location - frequency.
    by Xiang Gao (https://github.com/dejavu1988/opendataparsing)
    
    To execute in shell:
    ./retrieve.py

    There will be verbose info of processing, and results output separately to
    'category-frequency.csv' and 'location-frequency.csv'
"""

import urllib2
import shutil
import os
import zipfile
import sys

def clear(localPath, localDir):
    """ Clearing local cache if exists
        @param localPath: path of cached csv.zip
        @param localDir: path of cached directory
    """
    zipExists = os.path.exists(localPath)
    dirExists = os.path.exists(localDir)
    if zipExists:   # incase zip file exists
        os.remove(localPath)
        print "zip removed"
    if dirExists:   # in case directory exists
        shutil.rmtree(localDir)
        print "dir removed"

def retrieve(remotePath):
    """ Retrieving zip file from remote url using urllib2 library
        @param remotePath: url
        @return output: zip (temporary) file object
    """
    try:
        remotedata = urllib2.urlopen(remotePath)    # get zip from url
        print "Loading..."
    except IOError:
        print("Network down.")
        sys.exit() 
    
    output = os.tmpfile() # create tmp file for zip
    output.write(remotedata.read())
    print "Zip Downloaded."
    return output

def extract(data):
    """ Extracting csv files and merging into one data structure (a list of tuples)
        @param data: file reference of zip (tmp)
        @return recordlist: data structure (a list of tuples) to store merged records, with each entry as a tuple
    """
    archive = zipfile.ZipFile(data) # ZipFile object
    if archive.testzip() != None:   # test zip validity
        print "Invalid zipfile"
        sys.exit() 
    recordlist = []
    for name in archive.namelist(): # get list of csvs in archive
        print "Processing file: " + name
        f = archive.open(name, 'r')
        linelist = f.readlines()    # for each csv, get lines
        for tmpstr in linelist:
            if tmpstr[0] != '#':    # in case of valid entry
                entry = tmpstr[:-1].split('|')
                recordlist.append(tuple(entry)) # store tuple of entry into data structure
        f.close()
    archive.close()
    data.close()    # on close of tmp file reference, tmp file be automatically cleared
    print "Extracted to record list: " + str(len(recordlist)) + " entries."
    return recordlist

def dump(recordlist):
    """ Dumping data structure to file for debugging
        @param recordlist: data structure (a list of tuples) to store merged records
    """
    with open('record.csv','w') as f:
        for entry in recordlist:
            tmpstr = ''
            for item in entry:
                tmpstr += item + '|'
            f.write(tmpstr[:-1]+'\n')

    print "Record object dumped."

def analyseMainCategory(recordlist):
    """ Traverse data structure to accumulate MainCategory-Frequency
        @param recordlist: data structure (a list of tuples) to store merged records
        @return catedict: dictionary(map) of MainCategory-Frequency
    """
    print "Analysing MainCategory-Frequency.."
    catedict = {}
    for entry in recordlist:
        cate = entry[5]
        if catedict.has_key(cate):  # in case accumulated dict has record: increase frequency by 1
            catedict[cate] = catedict[cate] + 1
        else:   # otherwise (not yet accumulated): assignment 1to new member in dict
            catedict[cate] = 1
    print "Done."
    return catedict

def analyseLocation(recordlist):
    """ Traverse data structure to accumulate Location-Frequency
        @param recordlist: data structure (a list of tuples) to store merged records
        @return locdict: dictionary(map) of Location-Frequency
    """
    print "Analysing Location-Frequency.."
    locdict = {}
    for entry in recordlist:
        loc = entry[7]+entry[8]
        if locdict.has_key(loc):    # in case accumulated dict has record: increase frequency by 1
            locdict[loc] = locdict[loc] + 1
        else:   # otherwise (not yet accumulated): assignment 1to new member in dict
            locdict[loc] = 1
    print "Done."
    return locdict

def output(resdict, path):
    """ Outputing result data structure (dictionary) to formatted representation (<key><space><frequency>'\n')
        @param resdict: result data structure (dictionary)
        @param path: path of output csv file
    """
    with open(path, 'w') as f:
        for key in resdict.keys():
            entry = key+' '+str(resdict[key])+'\n'
            f.write(entry)

def main():
    """ Main function to execute
    """
    remotePath = "http://pilvilinna.cert.fi/opendata/autoreporter/csv.zip"  # url of csv.zip
    data = retrieve(remotePath)
    recordlist = extract(data)
    #dump(recordlist)
    catedict = analyseMainCategory(recordlist)
    locdict = analyseLocation(recordlist)
    output(catedict, 'category-frequency.csv')
    output(locdict, 'location-frequency.csv')


if __name__ == "__main__":
    main()
