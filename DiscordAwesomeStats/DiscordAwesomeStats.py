#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import yaml

import get_server_messages
import write_summary_to_server
from plotify import Plotify


def main():
    parser = argparse.ArgumentParser(description="BT-Monitor Script")
    parser.add_argument("config_file", default="./config.yaml")
    parser.add_argument("--no-getlog", action='store_true', default=False)
    parser.add_argument("--no-plotify", action='store_true', default=False)
    parser.add_argument("--silent", action='store_true', default=False)
    args = parser.parse_args()

    with open(args.config_file, 'r') as file:
        config = yaml.load(file)

    if "servers" not in config:
        return (1)

    if not os.path.isdir("chat_logs/"):
        os.mkdir("chat_logs")

    if not args.no_getlog:
        with open("chat_logs/summary.txt", 'w') as summary_file:
            summary = []
            get_server_messages.set_config(config["servers"], summary)
            get_server_messages.client.run(config["token"])
            json.dump(summary, summary_file, indent=4)
    else:
        get_server_messages.client.close()

    if not args.no_plotify:
        with open("chat_logs/summary.txt", 'r') as summary_file:
            summary_json = json.load(summary_file)
            for channel in summary_json:
                print("Doing plots for %s #%s" % (channel["Server name"], channel["Channel name"]))
                plotify = Plotify(config["outputdir"], channel)
                plotify.plotify()
                plotify.write_standing_history_html()
                plotify.write_all_plots_html()
                plotify.write_main_html()

    # if not (args.silent or not ("silent" in server and server["silent"])):
    #     text = "DiscoLog Monitoring has been updated.\n\nStandings of yesterday:\n```\n"
    #     text += plotify.top10yesterday
    #     text += "```\n\nMore stats and graphs here : https://dasfranck.fr/DiscoLog/Monitoring/%s/" % server["name"]
    #     write_summary_to_server.set_message(text)
    #     write_summary_to_server.client.run(args.token)
    # else:
    #     write_summary_to_server.client.close()


if __name__ == '__main__':
    main()
