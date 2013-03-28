#! /usr/bin/python
import cgi,sys
import subprocess
import dbutils
#import cgitb; cgitb.enable()
"""
Select to XML
using mysql in a subprocess as implemented in utils
"""

form=cgi.FieldStorage()
"""
 Need connect. | separated string
 Sequence is important
 user|password|host|database

 and sql
"""
try:
    # always connect
    connect=form['connect'].value
    sql=form['sql'].value
    # set up parameters
    p=dbutils.prepareSelectParameters(connect,sql)
    if len(p) > 0:                           
        res=dbutils.doProcess(p,'data/sqlselect.xml')
        if res.startswith('ok'):
            # return the produced file
            print "Location: data/sqlselect.xml\n"
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
