#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Setting up some strings globals
NAME = "DiscoLog"

import discord
import os
import sys
from datetime import timedelta


async def get_logs_from_channel(client, channel, cfg, summary):
    if not (os.path.exists("chat_logs")):
        os.makedirs("chat_logs")

    log_file = open("chat_logs/%s-%s.log" % (str(cfg["id"]), channel.id), 'w')
    i = 0
    messages = []
    async for item in client.logs_from(channel, limit=sys.maxsize):
        i += 1
        if (i % 1000 == 0):
            print("\t\t" + str(i))
        messages.append(item)

    # Make the header
    header = "Server name: " + cfg["name"] + "\n"
    header += "Server ID: " + str(cfg["id"]) + "\n"
    header += "Channel name: " + channel.name + "\n"
    header += "Channel ID: " + channel.id + "\n"
    header += channel.created_at.strftime("Created at: %A %d %b %Y %H:%M:%S UTC\n")
    header += "Length: %d messages\n\n" % len(messages)

    log_file.write(header)
    for msg in reversed(messages):
        log_file.write((msg.timestamp + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S\t"))
        log_file.write(msg.author.name + "\t")
        log_file.write(msg.content + "\n")
    log_file.close()

    summary.append({
        "Server name": cfg["name"],
        "Server ID": str(cfg["id"]),
        "Channel name": channel.name,
        "Channel ID": str(channel.id),
        "Length": len(messages),
        "Log path": "chat_logs/%s-%s.log" % (str(cfg["id"]), channel.id)
    })


# Launch the getter when the bot is ready
async def get_server_messages(client, logger, config):
    summary = []
    print("Sucessfully connected as %s (%s)\n" % (client.user.name, client.user.id))
    logger.logger.info("Sucessfully connected as %s (%s)" % (client.user.name, client.user.id))
    logger.logger.info("------------")
    # yield from client.change_status(game=discord.Game(name="Ketchup Splash Simulator"))
    for cfg in config["servers"]:
        for server in client.servers:
            if server.id == str(cfg["id"]):
                print("{} ({})".format(server.name, server.id))
                for channel in server.channels:
                    if (channel.type != discord.ChannelType.voice and
                        ("channels" not in cfg or
                         channel.id in [str(i["id"]) for i in cfg["channels"]])):
                        try:
                            print("\t{} ({})".format(channel.name, channel.id))
                            await get_logs_from_channel(client, channel, cfg, summary)
                        except discord.errors.Forbidden:
                            pass
                print()

    print("Done.")
    logger.logger.info("Done.")
    logger.logger.info("#--------------END--------------#")
    return summary
