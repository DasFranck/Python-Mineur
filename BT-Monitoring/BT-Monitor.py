#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

import getBTmessages
import write_summary_to_server
from plotify import Plotify

LOG_PATH = "chat_logs/BreakTime-discussion.log"


def main():
    parser = argparse.ArgumentParser(description="BT-Monitor Script")
    parser.add_argument("token")
    parser.add_argument("--no-getlog", action='store_true', default=False)
    parser.add_argument("--no-plotify", action='store_true', default=False)
    parser.add_argument("--silent", action='store_true', default=False)
    args = parser.parse_args()

    if not args.no_getlog:
        getBTmessages.client.run(args.token)

    if not args.no_plotify:
        plotify = Plotify(LOG_PATH)
        plotify.plotify()
        plotify.write_standing_history_html()
        plotify.write_all_plots_html()
        plotify.write_main_html()

    if not args.silent:
        text = "DiscoLog Monitoring has been updated.\n\nStandings of yesterday:\n```\n"
        text += plotify.top10yesterday
        text += "```\n\nMore stats and graphs here : https://dasfranck.fr/DiscoLog/Monitoring/BT/"
        write_summary_to_server.set_message(text)
        write_summary_to_server.client.run(args.token)


if __name__ == '__main__':
    main()
