#! /usr/bin/python
import cgi,sys
import subprocess
from lxml import etree


"""
Run a subprocess, used to perform:
extract from database with mysqldump   or    mysql
return ok or error....
"""
def doProcess(params,targetfile):
    try:
        f=open(targetfile,'wb')
        p=subprocess.check_call(params,stdout=f,stderr=f,shell=False)
        f.flush()
        f.close()
        if p==0:            
            return 'ok'
        else:
            return 'error in subprocess: '+str(p)
    except:
        res=sys.exc_info()
        return 'error '+ str(res[1])

 
"""
 extract from database and
 make an xslt transform to legal JSON
 return the JSON string or error....
"""
def makeJson(params,xmlfile,xslfile):
    res=doProcess(params,xmlfile)
    if res.startswith('error'):
        return res
    try:
        tree=etree.parse(xmlfile)
        xsltree=etree.parse(xslfile)
        transform=etree.XSLT(xsltree)    
        resulttree=transform(tree)
        return str(resulttree)
    except:
        res=sys.exc_info()
        return 'error '+ str(res[1])
 
"""
 extract from database,
 make an xslt transform to legal JSON
 and save the string as a compact Javascript string variable
  var obj='....'
"""
def saveJSVariable(params,xslfile,targetfile):
    S=makeJson(params,"data/tmp",xslfile)
    if S.startswith('error'):
        S='{"message":"S"}'
    else:
        S=S.replace('\r','').replace('\n','')
    T="var obj='"+S+"'"
    res=storeTextFile(targetfile,T)
    return res[0]
 
"""
 Set up parameters for a use of mysqldump
 user|password|host|database|table
"""
def prepareDumpParameters(connect):
    p=[]
    parts=connect.split('|')
    if len(parts) == 5:                           
        p.append('mysqldump')
        p.append('--xml')
        p.append('--lock-tables=false')#when limited user rights        
        p.append('--user='+parts[0])
        p.append('--password='+parts[1])
        p.append('--default-character-set=utf8')
        p.append('--host='+parts[2])
        p.append(parts[3]) #database
        p.append(parts[4]) #table
    return p

"""
 Set up parameters for a use of mysql
 user|password|host|database
"""
def prepareSelectParameters(connect,sql):
    p=[]
    parts=connect.split('|')
    if len(parts) == 4:                           
        p.append('mysql')
        p.append('-X')
        p.append('--execute='+sql)
        p.append('--user='+parts[0])
        p.append('--password='+parts[1])
        p.append('--default-character-set=utf8')
        p.append('--host='+parts[2])
        p.append(parts[3]) #database
    return p
 

"""
Read / write text files
"""
def getTextFile(filename):
    try:
        file=open(filename,'r')
        res=file.read()
        file.close()
        return ('ok',res)
    except:
        res=sys.exc_info()
        return('error',res[1])
    
    
def storeTextFile(filename,txt):
    try:
        file=open(filename,'w')
        file.write(txt)
        file.close()
        return('ok','')
    except:
        res=sys.exc_info()
        return('error',res[1])
