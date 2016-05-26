#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    awesum.py
## Desc:    Automatic Website Status and Uptime Monitoring
##
## Author:  "Das" Franck Hochstaetter
## Version: v0.X (XX/XX/201X)
##
## Dependencies : - json (pip install hjson)
##    A configuration file format for humans.
##    Relaxed syntax, fewer mistakes, more comments.

import hjson                                # Config File
import socket                               # Except socket.error
from http.client import HTTPConnection      # HTTPConnection
from urllib.parse import urlparse           # URLParser
from argparse import ArgumentParser         # ArgumentParser

DESCRIPTION = "Automatic Website Status and Uptime Monitoring"


# The main class (one by website)
class awsum():
    target = ""
    reference = []
    timespan = 0

    # Init the awsum class with the config file (as a string), the argument namepace
    #   and the index of his website in the target/timespan array
    def __init__(self, config, args, i):
        # To be modified with args
        self.target = config["target"][i]
        self.timespan = config["timespan"][i]
        self.reference = config["reference"]

        #if target.length != timespan.length:
        #    except

    def check_network_status(self):
        url = urlparse(website)
        status = HTTPConnection(url[1])
        try:
            status.request("HEAD", url[2])
            return (status.getresponse().status)
        except socket.error:
            return (self.check_network_status())



def main():
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-c", "--configfile", help="path to the config file", default="config.hjson")
    args = parser.parse_args()
    config = hjson.load(open(args.configfile))

    awsum_array = []
    try:
        for i in range(len(config["target"])):
            awsum_array.append(awsum(config, args, i))
            print(awsum_array[i].target)
    #If a value was missing in the config file
    except KeyError as missing_key:
        print("Incorrect hjson config file, %s is missing." % missing_key)

if __name__ == "__main__":
    main()
