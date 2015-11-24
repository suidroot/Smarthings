#!/usr/bin/env python
#
# This script is based on the Alfred script to send switch commands 
# to SmartThings
# currently required the files requred
# endpoints.txt, token.txt and devices.txt frorm Alfred plugin
# does not (yet) support login to ST and download device list.
#

import argparse
import string
import urllib2
import json
from settings import PROTOCOL, HOSTNAME
from http_server import stop


def initargs():
    """ initialize variables with command-line arguments """
    parser = argparse.ArgumentParser(description='input -f [file]')

    parser.add_argument('-l', '--list', \
        help='List end Points', \
        action='store_true')
    parser.add_argument('-r', '--refresh', \
        help='Refresh list of end Points', \
        action='store_true')
    parser.add_argument('-d', '--device', \
        help='Device Name', \
        default="")
    parser.add_argument('-c', '--command', \
        help='Command to run (on or off)', \
        default="")

    arg = parser.parse_args()

    return arg

def execute_command(query=""):
    ''' Send command to ST server '''

    args = string.split(query, ".")
    url = args[0]
    command = args[1]

    url = "{protocol}://{hostname}{url}".format(protocol=PROTOCOL, hostname=HOSTNAME, url=url)
    
    requestBody = '{"command":"' + "{command}".format(command=command) + '"}'
    request = urllib2.Request(url, data=requestBody)

    tokenFile = open("token.txt")
    token = tokenFile.read()
    tokenFile.close()
    request.add_header('Authorization', "Bearer %s" % token)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    opener.open(request)

    return "Turned " + command

def device_collector():
    ''' Load list of devices from local files '''

    print "List of devices"
    print "---------------"

    with open("endpoints.txt", 'r') as fh:
        try:
            deviceFile = open("devices.txt")
            for deviceDataString in deviceFile.readlines():
                deviceData = string.split(deviceDataString, ":")
                # deviceEndpoint = deviceData[0].strip()
                deviceLabel = deviceData[1].strip()
    
                print deviceLabel
            
            deviceFile.close()
        except IOError:
            print "Uh oh"
    
    return  

def geturl(device=""):
    ''' 
    Get URL from local device file 
    Returns URL

    '''

    with open("endpoints.txt", 'r') as fh:

        try:
            deviceFile = open("devices.txt")
            for deviceDataString in deviceFile.readlines():
                deviceData = string.split(deviceDataString, ":")
                deviceEndpoint = deviceData[0].strip()
                deviceLabel = deviceData[1].strip()


                if deviceLabel == device:
                    break
                    deviceFile.close()
            
            deviceFile.close()
        except IOError:
            print "Uh oh"

    return deviceEndpoint

def refresh_devices():
    # stop()

    tokenFile = open("token.txt")
    token = tokenFile.read()
    tokenFile.close()
    
    devicesFile = open("devices.txt", "w")

    with open("endpoints.txt", 'r') as fh:
        for endpoint in fh.readlines():
            if endpoint.__len__() > 1:
                ### collect devices for each endpoint
                
                for deviceType in ("switches", "locks"):
                    endpoint = endpoint.strip()
                    url = "{protocol}://{hostname}{endpoint}/{deviceType}".format(protocol=PROTOCOL, hostname=HOSTNAME, endpoint=endpoint, deviceType=deviceType)

                    req = urllib2.Request(url)
                    req.add_header('Authorization', "Bearer %s" % token)
                    response = urllib2.urlopen(req)
                    the_page = response.read()
                    jsonData = json.loads(the_page)
                    
                    for device in jsonData:
                        deviceKey = "{endpoint}/{deviceType}/{deviceId}".format(endpoint=endpoint, deviceType=deviceType, deviceId=device['id'])                        
                        deviceValue = device['name'] if len(device['label']) == 0 else device['label']
                        deviceCache = "{key}:{value}\n".format(key=deviceKey, value=deviceValue)
                        devicesFile.write(deviceCache)
                        
    devicesFile.close()
    
    return "Your SmartThings device cache has been updated"

#######

arg = initargs()

if arg.list:
    device_collector()
elif arg.refresh:
    print refresh_devices()
elif arg.device:
    url = geturl(arg.device) 
    print(execute_command(url+"."+arg.command))