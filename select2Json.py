#! /usr/bin/python
import cgi,sys
from lxml import etree
import dbutils
#import cgitb; cgitb.enable()
"""
select from database to json
using mysql in a subprocess as implemented in utils
"""


# transform xml -> json
XSLT_FILE='tojson.xsl'       

form=cgi.FieldStorage()
"""
 Need connect. | separated string
 Sequence is important:
 user|password|host|database|table

 sql
"""
print 'Content-type: text/plain; charset=utf-8 \n'

try:
    # always connect
    connect=form['connect'].value
    sql=form['sql'].value
    # set up parameters
    p=dbutils.prepareSelectParameters(connect,sql)
    if len(p) > 0:                           
        print dbutils.makeJson(p,'data/select.xml',XSLT_FILE)

    else:
        print 'error bad parameter list in connect'
except:
        res=sys.exc_info()
        print 'error '+str(res[1])
