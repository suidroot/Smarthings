#!/usr/bin/env python
# coding=utf-8

""" Smarthings database querier

by Ben Mason

"""

import MySQLdb as mdb
import sys
import cgi


DEBUG = True

if DEBUG:
    import cgitb
    cgitb.enable()

# Gather CGI fields
CGIDATA = cgi.FieldStorage()

SCRIPTNAME = "smartthings-showevents.py"
DEFAULTQTY = 50

# Database information
DATABASEHOST = "mysql.spacecatcastle.the-collective.net"
DBDATABASE = "spacecatcastle"
DBUSERNAME = "locutusthecollec"
DBPASSWORD = "tZ?yrBde"
EVENTTABLE = "smartthingsevents"
ACTIONTABLE = "actions"
DEVICETABLE = "devices"

from smartthingscommon import listofdevices
from smartthingscommon import listofactions
from smartthingscommon import printhtmlheader
from smartthingscommon import printhtmlfooter

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
    print "</select></td>"

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

    print '''</select></td>
<td><input type="text" size="3" name="returnlimit" value="{0}">\
</td><td><input type="submit" value="Submit"><a href={1}>Reset</a></td></tr>
</table></form></p>'''.format(RETURNQTY, SCRIPTNAME)

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
        devicequery = devicequery + ' AND {1}.id = \
        {0}'.format(DEVICELIMIT, DEVICETABLE)

    actionquery = 'INNER JOIN {1} ON {0}.name = \
    {1}.id'.format(EVENTTABLE, ACTIONTABLE)
    if ACTIONLIMIT:
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


if __name__ == '__main__':

    printhtmlheader("SmartThings Events")

    # Clean up argument input, remove all white space and invalid characters.
    if CGIDATA.has_key('nextevents'):
        try:
            printevents(start=int(CGIDATA['nextevents'].value))
        except ValueError:
            print "<p>invalid start, not number</p>"
    else:
        printevents()

    printhtmlfooter()
