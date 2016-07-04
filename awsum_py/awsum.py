#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    awsum.py
## Desc:    Automatic Website Status and Uptime Monitoring
##
## Author:  "Das" Franck Hochstaetter
## Version: v0.X (XX/XX/201X)
##
## Dependencies : - hjson
##    A configuration file format for humans.
##    Relaxed syntax, fewer mistakes, more comments.
##                - aiohttp
##    Http client/server for asyncio.

## TODO : Find a better way to end the Futures/Tasks

import asyncio                              # Coroutine/Asynchronous routine
import aiohttp                              # asyncio's http client
import hjson                                # Config File
import signal
import sys
import warnings
from argparse import ArgumentParser         # ArgumentParser
from concurrent.futures import CancelledError

DESCRIPTION = "Automatic Website Status and Uptime Monitoring"


# The main class (one by website)
class awsum():

    # Init the awsum class with the config file (as a string), the argument namepace
    #   and the index of his website in the target/timespan array
    def __init__(self, config, i):
        try:
            self.target = config["targets"][i]
            self.timespan = config["timespans"][i]
            self.references = config["references"]
        except KeyError as missing_key:
            raise self.InvalidConfigFile("Incorrect hjson config file, %s is missing." % missing_key)

        if len(config["targets"]) != len(config["timespans"]):
            raise self.InvalidConfigFile("The array of target and the array of timespan must have the same length.")
        print("%s added." % self.target)

    # Launch the monitoring
    async def start(self):
        #I should find something less ugly but hey, if it doesn't wreck the CPU that should be fine.
        while True:
            #Check if the website is up, if not check the network.
            if (await self.check_website_status() == False):
                if (await self.check_network_status() == False):
                    print("Network is down.")
                    ## Add Network_Down
                else:
                    print("%s is down." % self.target)
                    ## Add Website_Down
            else:
                print("%s is up." % self.target)
                ## Add Website_Up
            await asyncio.sleep(self.timespan)

    # Check if the website is up or down (True for Up, False for Down)
    async def check_website_status(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.target) as response:
                    if response.status == 200:
                        return (True)
                    else:
                        return (False)
            except aiohttp.errors.ClientOSError:
                return (False)

    # Check if the network by checking references websites is up or down (True for Up, False for Down)
    async def check_network_status(self):
        for ref in self.references:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(ref) as response:
                        return (True)
                except aiohttp.errors.ClientOSError:
                    pass;
        return (False)


    # My own exception for an invalid Config File
    class InvalidConfigFile(Exception):
        def __init__(self, *args, **kwargs):
            Exception.__init__(self, *args, **kwargs)

#Signal handler
async def exit_sigint(signame, loop):
    print("%s catched, exiting..." % signame)
    for task in asyncio.Task.all_tasks():
        task.cancel()

def main():
    #Argument parsing
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-c", "--configfile", help="path to the config file", default="config.hjson")
    args = parser.parse_args()

    #Condifguration parsing
    config = hjson.load(open(args.configfile))

    awsum_array = []
    try:
        for i in range(len(config["targets"])):
            awsum_array.append(asyncio.ensure_future(awsum(config, i).start()))
    #Except if a value was missing in the config file
    except awsum.InvalidConfigFile as err_msg:
        print("Error: IncorrectConfigFile: %s" % err_msg)

    #Create the asyncio loop
    loop = asyncio.get_event_loop()
    #Adding signal handlers
    loop.add_signal_handler(getattr(signal, "SIGINT"), asyncio.ensure_future, exit_sigint("SIGINT", loop))
    loop.add_signal_handler(getattr(signal, "SIGTERM"), asyncio.ensure_future, exit_sigint("SIGTERM", loop))
    try:
        while True:
            result = loop.run_until_complete(asyncio.gather(*awsum_array))

    # I don't care about those "errors" - TO BE FIXED
    except CancelledError:
        pass
#        logging.info('CancelledError')
    loop.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
