#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord


client = discord.Client()

msg = ""


def set_message(text):
    global msg
    msg = text


@client.async_event
def on_ready():
    for server in client.servers:
        if "BreakTime" in server.name:
            for channel in server.channels:
                if "discussion" in channel.name:
                    yield from client.send_message(channel, msg)
    yield from client.logout()
    return
