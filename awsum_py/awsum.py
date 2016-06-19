#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    awsum.py
## Desc:    Automatic Website Status and Uptime Monitoring
##
## Author:  "Das" Franck Hochstaetter
## Version: v0.X (XX/XX/201X)
##
## Dependencies : - json (pip install hjson)
##    A configuration file format for humans.
##    Relaxed syntax, fewer mistakes, more comments.

import asyncio                              # Coroutine/Asynchronous routine
import aiohttp
import hjson                                # Config File
import socket                               # Except socket.error
from http.client import HTTPConnection      # HTTPConnection
from urllib.parse import urlparse           # URLParser
from argparse import ArgumentParser         # ArgumentParser

DESCRIPTION = "Automatic Website Status and Uptime Monitoring"


# The main class (one by website)
class awsum():

    # Init the awsum class with the config file (as a string), the argument namepace
    #   and the index of his website in the target/timespan array
    def __init__(self, config, i):
        try:
            self.target = config["target"][i]
            self.timespan = config["timespan"][i]
            self.reference = config["reference"]
        except KeyError as missing_key:
            raise self.InvalidConfigFile("Incorrect hjson config file, %s is missing." % missing_key)

        if len(config["target"]) != len(config["timespan"]):
            raise self.InvalidConfigFile("The array of target and the array of timespan must have the same length.")

    # Launch the monitoring
    async def start(self):
        #I should find something less ugly
        while True:
            #Check if the website is up, if not check the network.
            if (await check_website_status() == False):
                if (await check_network_status() == False):
                    print("Network is down.")
                    ## Add Network_Down
                else:
                    print("Website is up.")
                    ## Add Website_Up
            else:
                print("Website is down.")
                ## Add Website_Down
            await asyncio.sleep(self.timespan)           ##Check this one day

    # Check if the network is up or down (True for Up, False for Down)
    async def check_network_status(self):
        url = urlparse(self.website)
        status = HTTPConnection(url[1])
        try:
            status.request("HEAD", url[2])
            return (1)
        except socket.error:
            return (0)


    # My own exception for an invalid Config File
    class InvalidConfigFile(Exception):
        def __init__(self, *args, **kwargs):
            Exception.__init__(self, *args, **kwargs)



def main():
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-c", "--configfile", help="path to the config file", default="config.hjson")
    args = parser.parse_args()
    config = hjson.load(open(args.configfile))

    awsum_array = []
    try:
        for i in range(len(config["target"])):
            awsum_array.append(awsum(config, i))
            print(awsum_array[i].target)
    #If a value was missing in the config file
    except awsum.InvalidConfigFile as err_msg:
        print("Error: IncorrectConfigFile: %s" % err_msg)

if __name__ == "__main__":
    main()
