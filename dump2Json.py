#! /usr/bin/python
import cgi,sys
#import subprocess
from lxml import etree
import dbutils
#import cgitb; cgitb.enable()
"""
Dump to json
Server script producing json
Using lxml from: http://lxml.de/
and 
dbutils.py as in this repository
"""

XSLT_FILE='tojson.xsl'       

form=cgi.FieldStorage()
"""
 Need connect. | separated string
 Sequence is important:
 user|password|host|database|table
"""
print 'Content-type: text/plain; charset=utf-8 \n'

try:
    # always connect
    connect=form['connect'].value
    # set up parameters
    p=utils.prepareDumpParameters(connect)
    parts=connect.split('|')
    if len(p) > 0:                           
        print utils.makeJson(p,'data/dump.xml',XSLT_FILE)
    else:
        print 'error bad parameter list in connect'
except:
        res=sys.exc_info()
        print 'error '+str(res[1])
