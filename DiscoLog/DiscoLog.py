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
    import shlex
    import sys
    import os
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


# Get PM and write them in chat_logs/Private_Messages/{NAME}-{ID}.log
async def get_private_messages():

    summary = open("chat_logs/summary.txt", 'w')
    bar = progressbar.ProgressBar(redirect_stdout=True,
                                  widgets=[progressbar.Percentage(), " ",
                                           progressbar.Bar(), ' [', progressbar.Timer(), ']', ])

    for chan in bar(client.private_channels):
        recipients = chan.me.name + ", "
        for recipient in chan.recipients:
            recipients += recipient.name + ("" if recipient is chan.recipients[-1] else ", ")

        if (chan.name is not None):
            print("Fetching messages from the private channel \"" + chan.name + "\"")
            #log_file = open("chat_logs/" + chan.name + "-" + chan.id + ".log", 'w')
        else:
            print("Fecthing messages from a chat with " + recipients)
            #log_file = open("chat_logs/" + recipients + "-" + chan.id + ".log", 'w')

        log_file = open("chat_logs/" + chan.id + ".log", 'w')

        bar.update()

        # Get all messages
        messages = []
        async for item in client.logs_from(chan, limit=sys.maxsize):
            messages.append(item)

        # Make the header
        header = "ID: %s\n" % chan.id
        header += "Recipients:" + recipients + "\n"
        if (chan.name is not None):
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


# Launch the getter when the bot is ready
@client.async_event
def on_ready():
    user = client.user
    logger.log_info_print("Sucessfully connected as %s (%s)" % (user.name, user.id))
    logger.logger.info("------------")
    print()

    if not (os.path.exists("chat_logs")):
        os.makedirs("chat_logs")

    logger.log_info_print("Getting private messages")
    yield from get_private_messages()
    print("Done.")
    logger.logger.info("Done.")

    yield from client.logout()
    logger.logger.info("#--------------END--------------#")
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
