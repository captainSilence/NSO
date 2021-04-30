# This module will add new device to the Cisco NSO using restconf
# Version: 1.0
# Author: Bizhou Duan
# Copyright 2021, Sparklight ®. All rights reserved
import requests
from requests.auth import HTTPBasicAuth
from xml.dom import minidom

# Open the xml config file
with open('device.xml', 'r') as f:
    result = f.read()

# Get the hostname from the xml file
myxml = minidom.parse('device.xml')
name = myxml.getElementsByTagName('name')
hostname = name[0].firstChild.data


def main():
    base_uri = "http://10.140.63.11:8080/restconf/data/tailf-ncs:devices"
    auth = HTTPBasicAuth('autoeng', 'AHrz3ANhfLESs44')
    headers = {'Accept': 'application/yang-data+json',
               'Content-Type': 'application/yang-data+xml'}

    # Create a Device in the CDB
    response = requests.post(base_uri, auth=auth, headers=headers, data=result, verify=False)
    print(response)
    # SSH Fetch-Host-Keys Device
    response = requests.post(base_uri + "/device=" + hostname + "/ssh/fetch-host-keys",
                             auth=auth, headers=headers, verify=False)
    print(response)
    # Sync-from Device
    response = requests.post(base_uri + "/device=" + hostname + "/sync-from",
                             auth=auth, headers=headers, verify=False)
    print(response)


if __name__ == "__main__":
    main()
