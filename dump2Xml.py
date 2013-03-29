#! /usr/bin/python
import cgi,sys
import dbutils
#import cgitb; cgitb.enable()
"""
Dump to xml
using mysqldump in a subprocess as implemented in utils
"""


form=cgi.FieldStorage()
"""
 Need connect. | separated string
 Sequence is important:
 user|password|host|database|table
"""
try:
    # always connect
    connect=form['connect'].value
    # set up parameters
    p=dbutils.prepareDumpParameters(connect)
    if len(p) >0:
        res=dbutils.doProcess(p,'data/dump.xml')
        if res.startswith('ok'):
            # return the produced file
            print "Location: data/dump.xml\n"
        else:   
            print 'Content-type: text/plain; charset=utf-8 \n'
            print res
    else:
        print 'Content-type: text/plain; charset=utf-8 \n'
        print 'error bad parameter list in connect'
except:
        print 'Content-type: text/plain; charset=utf-8 \n'
        res=sys.exc_info()
        print 'error '+str(res[1])
