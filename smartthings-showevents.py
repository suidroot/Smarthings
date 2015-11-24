#!/usr/bin/env python
# coding=utf-8

""" Smarthings database querier

by Ben Mason

"""

import MySQLdb as mdb
import sys
import cgi
from time import strftime

# Gather CGI fields
CGIDATA = cgi.FieldStorage()

if CGIDATA.has_key('debug'):
    DEBUG = True
else:
    DEBUG = False

if DEBUG:
    import cgitb
    cgitb.enable()

SCRIPTNAME = "smartthings-showevents.py"
MAINTITLE = "SpaceCat Castle"
DATABASEHOST = "mysql.spacecatcastle.the-collective.net"
HEADERLINKS = '<a href="https://graph.api.smartthings.com/api/smartapps/installations/9a6a1a42-b55f-4b90-83a8-71a2c51cdfd7/ui?access_token=2fee3501-c6fc-41dd-b224-4d795f309e2f">ActiON4</a> | <a href="http://spacecatcastle.the-collective.net/graphs.html">Graphs</a>'
DEFAULTQTY = 50

# Database information
DBDATABASE = "spacecatcastle"
DBUSERNAME = "locutusthecollec"
DBPASSWORD = "tZ?yrBde"
EVENTTABLE = "smartthingsevents"
ACTIONTABLE = "actions"
DEVICETABLE = "devices"

if CGIDATA.has_key('returnlimit'):
    try:
        RETURNQTY = int(CGIDATA['returnlimit'].value)
    except ValueError:
        print "<p>invalid start, not number</p>"
        RETURNQTY = DEFAULTQTY
else:
    RETURNQTY = DEFAULTQTY

if CGIDATA.has_key('action'):
    try:
        ACTIONLIMIT = int(CGIDATA['action'].value)
    except ValueError:
        print "<p>invalid action limit</p>"
else:
    ACTIONLIMIT = False

if CGIDATA.has_key('device'):
    try:
        DEVICELIMIT = int(CGIDATA['device'].value)
    except ValueError:
        print "<p>invalid device limit</p>"
else:
    DEVICELIMIT = False

if CGIDATA.has_key('device-invert'):
    DEVICEINVERT = True
else:
    DEVICEINVERT = False

if CGIDATA.has_key('action-invert'):
    ACTIONINVERT = True
else:
    ACTIONINVERT = False

def listofdevices():
    """ Gather List of devices """

    # Connect to Database
    try:
        dbconn = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = dbconn.cursor()
    except mdb.Error, errorcode:
        print "Error %d: %s" % (errorcode.args[0], errorcode.args[1])
        sys.exit(1)

    sql = "SELECT id, display_name FROM {0} ORDER BY display_name".format(DEVICETABLE)

    cursor.execute(sql)
    devices = cursor.fetchall()

    if dbconn:
        dbconn.close()

    return devices

def listofactions():
    """ Gather list of Actions """

    # Connect to Database
    try:
        dbconn = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = dbconn.cursor()
    except mdb.Error, errorcode:
        print "Error %d: %s" % (errorcode.args[0], errorcode.args[1])
        sys.exit(1)

    sql = "SELECT id, action FROM {0} ORDER BY action".format(ACTIONTABLE)

    cursor.execute(sql)
    actions = cursor.fetchall()

    if dbconn:
        dbconn.close()

    return actions

def printevents(start=0, returnlimit=RETURNQTY):
    """ Query and Print List of messages """
    url = ""

    ##### Start search header  ########
    print '''<form action="{0}" method="get">
<table><tr><td>Filter on Device</td><td>Filter on Action</td><td>Qty</td><td>\
</td></tr>
<tr><td><select name="device">
'''.format(SCRIPTNAME)

    # Device Filter List
    devices = listofdevices()
    if DEVICELIMIT:
        print '<option value=""></option>'
    else:
        print '<option value="" selected></option>'

    for devid, display_name in devices:
        if DEVICELIMIT == devid:
            print '<option value="{0}" selected>{1}</option>'.format(devid, \
                display_name)
            url = url + "device={0};".format(DEVICELIMIT)
        else:
            print '<option value="{0}">{1}</option>'.format(devid, display_name)
    # Device Invert filter
    if DEVICEINVERT:
        checked = 'checked="yes"'
        url = url + "device-invert=True;"
    else:
        checked =  ''

    print '</select><input type="checkbox" name="device-invert" value="True" {0} /></td>'.format(checked)

    # Action List
    actions = listofactions()
    print '<td><select name="action">'
    if ACTIONLIMIT:
        print '<option value=""></option>'
    else:
        print '<option value="" selected></option>'
    for devid, action_name in actions:
        if ACTIONLIMIT == devid:
            print '<option value="{0}" selected>{1}</option>'.format(devid, \
                action_name)
            url = url + "action={0};".format(ACTIONLIMIT)
        else:
            print '<option value="{0}">{1}</option>'.format(devid, action_name)

    # Action Invert filter
    if ACTIONINVERT:
        checked = 'checked="yes"'
        url = url + "action-invert=True;"
    else:
        checked =  ''

    print '''</select><input type="checkbox" name="action-invert" value="True" {2}></td>
<td><input type="text" size="3" name="returnlimit" value="{0}">\
</td><td><input type="submit" value="Submit"><a href={1}>Reset</a> | \
<a href={1}?report="">Report</a> | <a href={1}?laststatus="">Last Status</a></td></tr>
</table></form></p>'''.format(RETURNQTY, SCRIPTNAME, checked)

    ##### Title Row #####

    print '''<table border="1">
<tr><td><b>Description</b></td><td><b>Device Name</b></td>\
<td><b>Created</b></td><td><b>Action</b></td></tr>'''

    # Connect to Database
    try:
        dbconn = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = dbconn.cursor()
    except mdb.Error, errorcode:
        print "Error %d: %s" % (errorcode.args[0], errorcode.args[1])
        sys.exit(1)

    ### Assemble Querty string
    devicequery = 'INNER JOIN {1} ON {0}.display_name = \
    {1}.id'.format(EVENTTABLE, DEVICETABLE)
    if DEVICELIMIT:
        if DEVICEINVERT == True:
            devicequery = devicequery + ' AND {1}.id != \
            {0}'.format(DEVICELIMIT, DEVICETABLE)
        else:
            devicequery = devicequery + ' AND {1}.id = \
            {0}'.format(DEVICELIMIT, DEVICETABLE)

    actionquery = 'INNER JOIN {1} ON {0}.name = \
    {1}.id'.format(EVENTTABLE, ACTIONTABLE)
    if ACTIONLIMIT:
        if ACTIONINVERT == True:
            actionquery = actionquery + ' AND {1}.id != \
            {0}'.format(ACTIONLIMIT, ACTIONTABLE)
        else:
            actionquery = actionquery + ' AND {1}.id = \
            {0}'.format(ACTIONLIMIT, ACTIONTABLE)

    sql = """SELECT {0}.description, {2}.display_name, {0}.created, {1}.action
    FROM {0}
    {3}
    {4}
    ORDER BY {0}.id DESC
    LIMIT {5} , {6}""".format(EVENTTABLE, ACTIONTABLE, DEVICETABLE, \
        devicequery, actionquery, start, returnlimit)

    if DEBUG:
        print "<pre>{0}</pre>".format(sql)

    # run sql query
    cursor.execute(sql)
    results = cursor.fetchall()

    for line in results:
        print "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>\
        </tr>".format(line[0], line[1], line[2], line[3])
    print "</table>"

    url = url + "returnlimit={0};".format(returnlimit)

    if int(start) == 0:
        print '<p><a href=?{2}nextevents={0}>show next {1} events</a>\
        </p>'.format(start+returnlimit+1, returnlimit, url)
    else:
        print '<p><a href=?{3}nextevents={0}>show previous {2} events</a> | \
        <a href=?{3}nextevents={1}>show next {2} events</a>\
        </p>'.format(start-returnlimit-1, start+returnlimit+1, returnlimit, url)

    if dbconn:
        dbconn.close()

def laststatus():
    devices = listofdevices()

    try:
        dbconn = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = dbconn.cursor()
    except mdb.Error, errorcode:
        print "Error %d: %s" % (errorcode.args[0], errorcode.args[1])
        sys.exit(1)

    # print '<table><tr><td>'
    # print '<h3>Count by Device</h3></td><td><h3>Count by Action</h3></td></tr>'
    # print '<tr><td valign="top">'
    # count by device
    print '''<table border="1">'''
    print '<tr><td><b>Device Name</b></td><td><b>Last Status</b></td><td><b>Date</b></td></tr>'

    for devid, name in devices:

        sql = "SELECT description, created FROM {0} WHERE display_name = {1} \
        ORDER BY id DESC LIMIT 1".format(EVENTTABLE, devid)

        cursor.execute(sql)
        results = cursor.fetchall()
        try:
            print '<tr><td>' + name + '</td><td>' + str(results[0][0]) + '</td><td>' + str(results[0][1]) + '</td></tr>\n'
        except IndexError:
            print '<tr><td>' + name + '</td><td>None</td><td>None</td></tr>\n'

    print "</table>"

    # if dbconn:
    #     dbconn.close()    
    # print "</td></tr></table>"

    print '<a href={0}>Return to Search</a>'.format(SCRIPTNAME)

    if dbconn:
        dbconn.close()    

def report():

    # sql = "SELECT COUNT(id) from {0} WHERE id = {1}".format()

    devices = listofdevices()

    try:
        dbconn = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = dbconn.cursor()
    except mdb.Error, errorcode:
        print "Error %d: %s" % (errorcode.args[0], errorcode.args[1])
        sys.exit(1)

    print '<table><tr><td><h3>Count by Device</h3></td><td><h3>Count by Action</h3></td></tr>'
    print '<tr><td valign="top">'
    # count by device
    print '''<table border="1">'''
    print '<tr><td><b>Device Name</b></td><td><b>Count</b></td></tr>'

    for devid, name in devices:

        sql = "SELECT COUNT(id) from {0} WHERE display_name = {1}".format(EVENTTABLE, devid)

        cursor.execute(sql)
        results = cursor.fetchall()
        print '<tr><td>' + name + '</td><td>' + str(int(results[0][0])) + '</td></tr>'

    print "</table>"

    if dbconn:
        dbconn.close()

    # count by action
    actions = listofactions()

    try:
        dbconn = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = dbconn.cursor()
    except mdb.Error, errorcode:
        print "Error %d: %s" % (errorcode.args[0], errorcode.args[1])
        sys.exit(1)

    print '</td><td valign="top">'
    print '''<table border="1">'''
    print '<tr><td><b>Action</b></td><td><b>Count</b></td></tr>'

    for actionid, name in actions:

        sql = "SELECT COUNT(id) from {0} WHERE name = {1}".format(EVENTTABLE, actionid)

        cursor.execute(sql)
        results = cursor.fetchall()
        print '<tr><td>' + name + '</td><td>' + str(int(results[0][0])) + '</td></tr>'

    print "</table>"
    print "</td></tr></table>"

    print '<a href={0}>Return to Search</a>'.format(SCRIPTNAME)

    if dbconn:
        dbconn.close()

def printhtmlheader(title):
    """ Print Standard HTML Header """


    now = strftime("%c")

    print '''Content-Type: text/html

<html>
<head>
<TITLE>{0}: {1}</TITLE>
</head>
<body>
<H1>{0}</H1>
<p>{3}</p>
<p>Current time {2}</p>'''.format(MAINTITLE, title, now, HEADERLINKS)

def printhtmlfooter():
    """ Print Started HTML Footer """
    print "</body></html>"


if __name__ == '__main__':

    printhtmlheader("SmartThings Events")

    # Clean up argument input, remove all white space and invalid characters.
    if CGIDATA.has_key('nextevents'):
        try:
            printevents(start=int(CGIDATA['nextevents'].value))
        except ValueError:
            print "<p>invalid start, not number</p>"
    elif CGIDATA.has_key('report'):
        report()
    elif CGIDATA.has_key('laststatus'):
        laststatus()
    else:
        printevents()

    printhtmlfooter()
