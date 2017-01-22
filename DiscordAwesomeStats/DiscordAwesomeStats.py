#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import yaml
from yattag import Doc, indent

import get_server_messages
import write_summary_to_server
from plotify import Plotify


def write_indexes_html(server_channel_dict, output_path):
    for id_server, server in server_channel_dict.items():
        doc, tag, text = Doc().tagtext()

        with tag('html'):
            # HEAD
            with tag('head'):
                doc.asis("<!DOCTYPE html>")
                doc.asis("<meta charset=\"UTF-8\">")
                doc.asis("<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">")
                doc.asis("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">")
                doc.asis("<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/css/bootstrap.min.css\" integrity=\"sha384-AysaV+vQoT3kOAXZkl02PThvDr8HYKPZhNT5h/CXfBThSRXQ6jW5DO2ekP5ViFdi\" crossorigin=\"anonymous\">")
                doc.asis("<link rel=\"stylesheet\" href=\"../css/own.css\">")
                with tag('title'):
                    text("Channel index for %s" % (server["Server name"]))
            with tag('body'):
                with tag('h1', klass="page-header"):
                    with tag('b'):
                        text("Channel index for %s" % (server["Server name"]))
                with tag("div", klass="container"):
                    with tag('h2'):
                        text("Channel List:")
                    with tag("ul", ("style", "list-style-type:none")):
                        for channel in server["Channels"]:
                            with tag("li"):
                                with tag('h4'):
                                    with tag('a', href=str(channel["Channel ID"])):
                                        text("#" + str(channel["Channel name"]))

        result = indent(doc.getvalue())
        with open(output_path + str(id_server) + "/index.html", "w") as file:
            file.write(result)

    doc, tag, text = Doc().tagtext()
    with tag('html'):
        # HEAD
        with tag('head'):
            doc.asis("<!DOCTYPE html>")
            doc.asis("<meta charset=\"UTF-8\">")
            doc.asis("<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">")
            doc.asis("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">")
            doc.asis("<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/css/bootstrap.min.css\" integrity=\"sha384-AysaV+vQoT3kOAXZkl02PThvDr8HYKPZhNT5h/CXfBThSRXQ6jW5DO2ekP5ViFdi\" crossorigin=\"anonymous\">")
            doc.asis("<link rel=\"stylesheet\" href=\"css/own.css\">")
            with tag('title'):
                text("DiscoLog Monitoring Index")
        with tag('body'):
            with tag('h1', klass="page-header"):
                with tag('b'):
                    text("DiscoLog Monitoring Index")
            with tag("div", klass="container"):
                with tag('h2'):
                    text("Server List:")
                with tag("ul", ("style", "list-style-type:none")):
                    for id_server, server in server_channel_dict.items():
                        with tag("li"):
                            with tag('h4'):
                                with tag('a', href=str(id_server)):
                                    text(server["Server name"])
    print(doc.getvalue())
    result = indent(doc.getvalue())
    with open(output_path + "index.html", "w") as file:
        file.write(result)


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
            server_channel_dict = {}
            for channel in summary_json:
                print("Doing plots for %s #%s" % (channel["Server name"], channel["Channel name"]))
                try:
                    plotify = Plotify(config["outputdir"], channel)
                except Plotify.EmptyChannelException:
                    print("Skipping it cause it's empty")
                else:
                    plotify.plotify()
                    plotify.write_standing_history_html()
                    plotify.write_all_plots_html()
                    plotify.write_channel_main_html()

                if (channel["Server ID"] not in server_channel_dict):
                    server_channel_dict[channel["Server ID"]] = {
                        "Server name": channel["Server name"],
                        "Channels": [{
                            "Channel name": channel["Channel name"],
                            "Channel ID": channel["Channel ID"]
                        }]}
                else:
                    server_channel_dict[channel["Server ID"]]["Channels"].append({
                        "Channel name": channel["Channel name"],
                        "Channel ID": channel["Channel ID"]
                    })
            print(server_channel_dict)
            write_indexes_html(server_channel_dict, config["outputdir"])

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
