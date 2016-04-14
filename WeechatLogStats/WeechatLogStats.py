#!/usr/bin/env python

import argparse
import rrdtool
from datetime import datetime
from os.path import basename

class WLS:
    def __init__(self, args):
        self.now = datetime.now()

        # Time of the first and last message on the logs
        self.start_time = 0
        self.end_time = 0

        # Get channel and network names from filename
        network = basename(args.file).split('.')[1]
        channel = basename(args.file).split('.')[2]

        # Init Stats
        self.stats = {}
        self.nick_stats = {}
        self.emotes_stats = {}
        self.domains_stats = {}
        self.words_stats = {}

        fd_log = open(args.file, "w")
        content = fd_log.read()

def main():
    parser = argparse.ArgumentParser(description="Nothing til now")
    parser.add_argument("file", help="Path to the log file", type=str)
    args = parser.parse_args()

    wls = WLS(args)
    return (0)

if __name__ == "__main__":
    main()
