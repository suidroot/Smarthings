#!/usr/bin/env python

MAINTITLE = "SpaceCat Castle"

def listofdevices():
    """ Gather List of devices """

    # Connect to Database
    try:
        dbconn = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = dbconn.cursor()
    except mdb.Error, errorcode:
        print "Error %d: %s" % (errorcode.args[0], errorcode.args[1])
        sys.exit(1)

    sql = "SELECT id, display_name FROM {0} ORDER BY id".format(DEVICETABLE)

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

    sql = "SELECT id, action FROM {0} ORDER BY id".format(ACTIONTABLE)

    cursor.execute(sql)
    actions = cursor.fetchall()

    if dbconn:
        dbconn.close()

    return actions


def printhtmlheader(title):
    """ Print Standard HTML Header """

    print '''Content-Type: text/html

<html>
<head>
<TITLE>{0}: {1}</TITLE>
</head>
<body>
<H1>{0}</H1>'''.format(MAINTITLE, title)

def printhtmlfooter():
    """ Print Started HTML Footer """
    print "</body></html>"


