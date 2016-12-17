#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import yaml

import get_server_messages
import write_summary_to_server
from plotify import Plotify


def main():
    parser = argparse.ArgumentParser(description="BT-Monitor Script")
    parser.add_argument("config_file")
    parser.add_argument("--no-getlog", action='store_true', default=False)
    parser.add_argument("--no-plotify", action='store_true', default=False)
    parser.add_argument("--silent", action='store_true', default=False)
    args = parser.parse_args()

    with open(args.config_file, 'r') as file:
        config = yaml.load(file)

    if "servers" not in config:
        return (1)

    if not args.no_getlog:
        with open("chat_logs/summary.txt", 'w') as summary:
            get_server_messages.set_config(config["servers"], summary)
            get_server_messages.client.run(config["token"])
    else:
        get_server_messages.client.close()

    return
    if not args.no_plotify:
        with open("chat_logs/summary.txt", 'r') as summary:
            for line in summary:
                plotify = Plotify(config["output_dir"], line)
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
