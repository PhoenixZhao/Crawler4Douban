#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A script to import JSON data to Mysql record of Douban Movie items
'''

import json
import MySQLdb as mdb
import sys

# Test MySQLdb module
print "Test mysql..."
try:
    con = mdb.connect('localhost', 'lihang', 'lilihang', 'test_json_to_mysql')
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
    data = cur.fetchone()
    print "Database version: %s" % data
except mdb.Error, e:
    print "Error: %d %s" % (e.args[0], e.args[1])
    sys.exit(1)
finally:
    if con:
        con.close()

# Create Database and Tables
create_movie_items_table = "CREATE TABLE IF NOT EXISTS \
        movie_items(id INT PRIMARY KEY AUTO_INCREMENT, \
                    rating_max INT, \
                    rating_average FLOAT, \
                    rating_stars VARCHAR(20), \
                    rating_min INT, \
                    reviews_count INT, \
                    wish_count INT, \
                    douban_site VARCHAR(50), \
                    year VARCHAR(10), \
                    image_small VARCHAR(50), \
                    image_large VARCHAR(50), \
                    image_medium VARCHAR(50), \
                    subject_url VARCHAR(50), \
                    subject_id INT, \
                    mobile_url VARCHAR(50), \
                    title VARCHAR(50), \
                    do_count INT, \
                    seasons_count INT, \
                    schedule_url VARCHAR(50), \
                    episodes_count INT, \
                    genres VARCHAR(50), \
                    current_season INT, \
                    collect_count INT, \
                    casts VARCHAR(300), \
                    countries VARCHAR(20), \
                    original_title VARCHAR(20), \
                    summary TEXT, \
                    summary_segmentation TEXT, \
                    subtype VARCHAR(10), \
                    directors VARCHAR(100), \
                    comments_count INT, \
                    ratings_count INT, \
                    aka VARCHAR(50) \
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf-8 COLLATE utf8_unicode_ci; \
                    "

#print create_movie_items_table

'''
# Simple Load
jsonFile = file("test.json")
jsonString = json.load(jsonFile)
print "Contents by json.load method:"
print jsonString
jsonFile.close()
'''

# Using JSONDecoder
jsonFile = file("test.json")
jsonSource = jsonFile.read()
#print "Contents by pure File.read method:"
#print jsonSource

jsonTarget = json.JSONDecoder().decode(jsonSource)
#print "Contents after using JSONDecoder method:"
#print jsonTarget

jsonKeys = jsonTarget.keys()

print "JSON keys:"
#print jsonTarget.keys()

for jsonKey in jsonKeys:
    #print jsonKey
    fieldValue = jsonTarget[jsonKey]
    if hasattr(fieldValue, 'keys'):
        subKeys = fieldValue.keys()
        for subKey in subKeys:
            print subKey
    else:
        print jsonKey
    '''
    if jsonKey == "genres":
        print fieldValue[0] + fieldValue[1] + fieldValue[2]
    elif jsonKey == "do_count":
        print fieldValue
    elif jsonKey == "rating":
        print "rating: " + str(fieldValue["max"]) + " " + str(fieldValue["average"]) + " " + str(fieldValue["stars"]) + " " + str(fieldValue["min"])
        subKeys = fieldValue.keys()
        for subKey in subKeys:
            print subKey
            print fieldValue[subKey]
    elif jsonKey == "images":
        subKeys = fieldValue.keys()
        for subKey in subKeys:
            print subKey
            print fieldValue[subKey]
    else:
        print fieldValue
    '''
jsonFile.close()

def insertMysqlRecordFromJson(jsonFileName):
    pass

def getSeperateFieldFromJson(jsonString):
    pass

def getJsonStringFromJsonFile(jsonFileName):
    try:
        jsonFile = file(jsonFileName)
        jsonString = json.load(jsonFile)
        jsonFile.close()
        return jsonString
    except IOError:
        print "IOError occured!"
