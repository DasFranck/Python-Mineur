#!/usr/bin/env python3

import argparse
import re
import rrdtool
from datetime import datetime
from os.path import basename

class WLS:
    # WLS Constructor
    def __init__(self, args):
        self.now = datetime.now()

        # Time of the first and last message on the logs
        self.start_time = 0
        self.end_time = 0

        # Get channel and network names from filename
        network = basename(args.file).split('.')[1]
        channel = basename(args.file).split('.')[2]

        # Init Stats
        self.stats          = {}
        self.nick_stats     = {}
        self.emotes_stats   = {}
        self.domains_stats  = {}
        self.words_stats    = {}

        # Init Values
        self.lines = 0;

        # Open log file
        try :
            self.fd_log = open(args.file, "r")
        except OSError as err:
            print("OSError: {0}".format(err))


    def parse(self):
        line_re = re.compile("(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})\t[@+&~!%]?([^\t]+)\t(.+)")
        for line in self.fd_log:
            res = line_re.match(line)
            if (res is not None):
                res = res.groups()
                self.lines += 1;

                # Init local values
                year        = res[0]
                month       = res[1]
                day         = res[2]
                hour        = res[3]
                minute      = res[4]
                second      = res[5]
                nick        = res[6]
                msg         = res[7]
                msg_array   = msg.split()
                is_action   = nick == ' *'
                nick        = text_arr[0] if is_action else nick

                print (year, month, day)
                print (hour, minute, second)
                print (nick)
                print (msg)
                print (msg_array)
                print ()



def main():
    parser = argparse.ArgumentParser(description="Nothing til now")
    parser.add_argument("file", help="Path to the log file", type=str)
    args = parser.parse_args()

    wls = WLS(args)
    wls.parse()
    return (0)

if __name__ == "__main__":
    main()
