#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Name:    awsum.py
Desc:    Automatic Website Status and Uptime Monitoring

Author:  "Das" Franck Hochstaetter
Version: v0.X (XX/XX/201X)

Dependencies :  - hjson
    A configuration file format for humans.
    Relaxed syntax, fewer mistakes, more comments.
                - aiohttp
    Http client/server for asyncio.
                - pandas
'''

import asyncio                              # Coroutine/Asynchronous routine
import aiohttp                              # asyncio's http client
import hjson                                # Config File
import pandas as pd
import signal
import sys
import time
from argparse import ArgumentParser         # ArgumentParser


DESCRIPTION = "Automatic Website Status and Uptime Monitoring"


# The main class (one by website)
class awsum():
    # Init the awsum class with the config file (as a string), the argument namepace
    #   and the index of his website in the target/timespan array
    def __init__(self, config, i, df):
        try:
            self.target = config["targets"][i]
            self.timespan = config["timespans"][i]
            self.references = config["references"]
            self.df = df
            self.index = i
        except KeyError as missing_key:
            raise self.InvalidConfigFile("Incorrect hjson config file, %s is missing." % missing_key)
        if len(config["targets"]) != len(config["timespans"]):
            raise self.InvalidConfigFile("The array of target and the array of timespan must have the same length.")
        print("%s added." % self.target)

    # Launch the monitoring
    async def start(self, loop):
        line = [""] * len(self.df.columns)
        line[0] = str(int(time.time()))

        # Check if the website is up, if not check the network.
        if await self.check_website_status() is False:
            if await self.check_network_status() is False:
                print("Network is down.")
                line[self.index + 1] = "NETWORK_DOWN"
            else:
                print("%s is down." % self.target)
                line[self.index + 1] = "WEBSITE_DOWN"
        else:
            print("%s is up." % self.target)
            line[self.index + 1] = "WEBSITE_UP"
        self.df.loc[len(self.df.index)] = line
        # print(self.df)
        loop.call_later(self.timespan, asyncio.ensure_future, self.start(loop))

    # Check if the website is up or down (True for Up, False for Down)
    async def check_website_status(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.target) as response:
                    return (True if response.status == 200 else False)
            except aiohttp.errors.ClientOSError:
                return (False)

    # Check if the network by checking references websites is up or down (True for Up, False for Down)
    async def check_network_status(self):
        for ref in self.references:
            async with aiohttp.ClientSession() as session:
                try:
                    await session.get(ref)
                    return (True)
                except aiohttp.errors.ClientOSError:
                    pass
        return (False)

    # My own exception for an invalid Config File
    class InvalidConfigFile(Exception):
        def __init__(self, *args, **kwargs):
            Exception.__init__(self, *args, **kwargs)


# Signal handler
def exit_sigcatch(signame, loop):
    print("%s catched, exiting..." % signame)
    loop.stop()


def main():
    # Argument parsing
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-c", "--configfile", help="path to the config file", default="config.hjson")
    args = parser.parse_args()

    # Configuration parsing
    config = hjson.load(open(args.configfile))

    # Create the asyncio loop
    loop = asyncio.get_event_loop()

    try:
        df = pd.DataFrame(columns=["timestamp"] + config["targets"])
        for i in range(len(config["targets"])):
            asyncio.async(awsum(config, i, df).start(loop))
    # Except if a value was missing in the config file
    except awsum.InvalidConfigFile as err_msg:
        print("Error: IncorrectConfigFile: %s" % err_msg)

    # Adding signal handlers
    loop.add_signal_handler(getattr(signal, "SIGINT"), exit_sigcatch, "SIGINT", loop)
    loop.add_signal_handler(getattr(signal, "SIGTERM"), exit_sigcatch, "SIGTERM", loop)
    loop.run_forever()
    df = df.groupby(by="timestamp").sum()
    print(df)
    sys.exit(0)


if __name__ == "__main__":
    main()
