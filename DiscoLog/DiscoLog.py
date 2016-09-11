#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Setting up some strings globals
NAME = "DiscoLog"

# Import modules with try and catch
try:
    import argparse
    import discord
    import getpass
    import os
    import sys
except ImportError as message:
    print("Missing package(s) for %s: %s" % (NAME, message))
    exit(12)

# Import classes
try:
    from classes import Logger
except ImportError as message:
    print("Missing python class(s) for %s: %s" % (NAME, message))
    exit(12)


client = discord.Client()
logger = Logger.Logger()


async def getrekt():
    if not (os.path.exists("chat_logs")):
        os.makedirs("chat_logs")

    # summary = open("chat_logs/summary.txt", 'w')
    for chan in client.private_channels:
        log_file = open("chat_logs/" + chan.id + ".log", 'w')

        log_file.write("Recipients: ")
        log_file.write(chan.me.name + ", ")
        for recipient in chan.recipients:
            log_file.write(recipient.name + ("\n" if recipient is chan.recipients[-1] else ", "))

        if (chan.type == discord.ChannelType.group):
            log_file.write("Chan name: " + chan.name + "\n")

        log_file.write(chan.created_at.strftime("Created at: %A %d %b %Y %H:%M:%S UTC\n\n"))

        messages = []
        async for item in client.logs_from(chan, limit=sys.maxsize):
            messages.append(item)

        print(type(messages))
        # Yeah I know the limit is maybe a bit too higher
        for msg in reversed(messages):
            log_file.write(msg.timestamp.strftime("%Y-%m-%d %H:%M:%S\t"))
            log_file.write(msg.author.name + "\t")
            log_file.write(msg.content + "\n")
        log_file.close()


@client.async_event
def on_ready():
    user = client.user
    logger.logger.info("Sucessfully connected as %s (%s)" % (user.name, user.id))
    logger.logger.info("------------")
    yield from getrekt()
    print("Done.")
    return


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("email")
    args = parser.parse_args()
    password = getpass.getpass()
    client.run(args.email, password)
    return


if __name__ == '__main__':
    main()
