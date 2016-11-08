#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Setting up some strings globals
NAME = "DiscoLog"

# Import modules with try and catch
try:
    import argparse
    import discord
    import getpass
    import progressbar
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


async def get_chat_logs():
    if not (os.path.exists("chat_logs")):
        os.makedirs("chat_logs")

    summary = open("chat_logs/summary.txt", 'w')
    bar = progressbar.ProgressBar(redirect_stdout=True,
                                  widgets=[progressbar.Percentage(), " ",
                                           progressbar.Bar(), ' [', progressbar.Timer(), ']', ])

    for chan in bar(client.private_channels):
        log_file = open("chat_logs/" + chan.id + ".log", 'w')

        recipients = chan.me.name + ", "
        for recipient in chan.recipients:
            recipients += recipient.name + ("" if recipient is chan.recipients[-1] else ", ")
        if (chan.type == discord.ChannelType.group):
            print("Fetching messages from the private channel " + chan.name + "\"")
        else:
            print("Fecthing messages from a chat with " + recipients)
        bar.update()

        # Get all messages
        messages = []
        async for item in client.logs_from(chan, limit=sys.maxsize):
            messages.append(item)

        # Make the header
        header = "ID: %s\n" % chan.id
        header += "Recipients:" + recipients + "\n"
        if (chan.type == discord.ChannelType.group):
            header += "Chan name: " + chan.name + "\n"
        header += chan.created_at.strftime("Created at: %A %d %b %Y %H:%M:%S UTC\n")
        header += "Length: %d messages\n\n" % len(messages)

        # Write the header in the summary and in the chat log file
        log_file.write(header)
        summary.write(header)

        # Yeah I know the limit is maybe a bit too higher
        for msg in reversed(messages):
            log_file.write(msg.timestamp.strftime("%Y-%m-%d %H:%M:%S\t"))
            log_file.write(msg.author.name + "\t")
            log_file.write(msg.content + "\n")
        log_file.close()
    summary.close()


async def get_logs_bt(client, channel):
    log_file = open("chat_logs/BREAKTEST.log", 'w')
    i = 0
    messages = []
    async for item in client.logs_from(channel, limit=sys.maxsize):
        i += 1
        if (i % 1000 == 0):
            print(i)
        messages.append(item)

    # Make the header
    header = "ID: %s\n" % channel.id
    if (channel.type == discord.ChannelType.group):
        header += "Chan name: " + channel.name + "\n"
    header += channel.created_at.strftime("Created at: %A %d %b %Y %H:%M:%S UTC\n")
    header += "Length: %d messages\n\n" % len(messages)

    log_file.write(header)
    for msg in reversed(messages):
        log_file.write(msg.timestamp.strftime("%Y-%m-%d %H:%M:%S\t"))
        log_file.write(msg.author.name + "\t")
        log_file.write(msg.content + "\n")
    log_file.close()


# Launch the getter when the bot is ready
@client.async_event
def on_ready():
    user = client.user
    print("Sucessfully connected as %s (%s)\n" % (user.name, user.id))
    logger.logger.info("Sucessfully connected as %s (%s)" % (user.name, user.id))
    logger.logger.info("------------")
    for server in client.servers:
        if "BreakTime" in server.name:
            for channel in server.channels:
                if channel.type == discord.ChannelType.text and "discussion" in channel.name:
                    yield from get_logs_bt(client, channel)

    print("Done.")
    logger.logger.info("Done.")
    logger.logger.info("#--------------END--------------#")
    yield from client.logout()
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
