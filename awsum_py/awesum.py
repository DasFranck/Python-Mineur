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


def check_status(website):
    url = urlparse(website)
    status = HTTPConnection(url[1])
    try:
        status.request("HEAD", url[2])
        return (status.getresponse().status)
    except socket.error:
        return (-1)


def main():
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-c", "--configfile", help="path to the config file", default="config.hjson")
    args = parser.parse_args()
    config_file = hjson.load(open(args.configfile))
    print(check_status(config_file["target"][0]))


if __name__ == "__main__":
    main()
