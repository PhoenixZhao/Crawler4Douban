#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding:utf-8

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

import MySQLdb as mdb

from sqlConstants import *

#what need to do 
#step 1. change config below
#step 2. make right connection to the sql
#step 3. choose right table
#step 4. select the field of the table you need to index or store


#------step 1------
#---start config---

#the dir to store the index file
INDEX_DIR = "/home/rio/workspace/lucene_index"
#the field name you want to index
FIELD = 'summary'

#---end config---



class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexMySql(object):
    """Usage: python IndexFiles.py"""

    def __init__(self, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexTable(writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexTable(self, writer):

        #connection 
        con = None

        #define the index of all the fields
        #---------step 2----------
        con = mdb.connect('localhost','nger','nger','moviedata')

        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        with con:
            cur = con.cursor()

            # Careful with codecs
            con.set_character_set('utf8')

            cur = con.cursor()
            # Aagin the codecs
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            
            #------step 3------
            cur.execute("SELECT * FROM movie_items")

            numrows = int(cur.rowcount)
            print 'numrows:',numrows
            for i in range(numrows):
                row = cur.fetchone()

                #------step 4------
                summary = row[SUMMARY]  
                subject_id = row[SUBJECT_ID]


                #print 'id'+subject_id
                #print 'summary'+summary+'end'

                doc = Document()
                doc.add(Field("subject_id", subject_id, t1))
                #doc.add(Field("path", root, t1))
                if len(summary) > 0:
                    print subject_id +'--->'+':\n    '+ 'summary'
                    try:
                        summary_unicoded = unicode(summary, 'utf-8') #test the encoding 
                    except Exception,e:
                        print "Decode Failed: ", e
                    doc.add(Field('summary', summary, t2))
                else:
                    print "warning:\n" + subject_id +'---> No content!'
                writer.addDocument(doc)



if __name__ == '__main__':
    if len(sys.argv) !=1:
        print IndexMySql.__doc__
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    #try:
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    IndexMySql(os.path.join(base_dir, INDEX_DIR), StandardAnalyzer(Version.LUCENE_CURRENT))
    end = datetime.now()
    print end - start
    #except Exception, e:
    #    print "Failed: ", e
    #    raise e
