#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    SC2RA.py
## Desc:    StarCraft 2 Replay Analyser
##
## Author:  "Das" Franck Hochstaetter
## Version: v0.1 (04/11/2015)
##
## Dependencies : sc2reader (pip install sc2reader)
##    Python library for extracting information from various different Starcraft II resources.

import argparse
import sc2reader

#To be less dirty... one day.
def init_colors(nocolors):
    global dict_colors
    global sc2_colors

    if (nocolors):
        dict_colors = {
            "BOLD":         "",
            "UNDERLINE":    "",
            "RESET_CLR":    "",
            "BLACK":        "",
            "BLUE":         "",
            "BROWN":        "",
            "DARKGREY":     "",
            "DARKGREEN":    "",
            "GREEN":        "",
            "LIGHTPINK":    "",
            "LIGHTGREY":    "",
            "LIGHTGREEN":   "",
            "ORANGE":       "",
            "PINK":         "",
            "PURPLE":       "",
            "RED":          "",
            "TEAL":         "",
            "VIOLET":       "",
            "YELLOW":       "",
            "WHITE":        "",
        }
    else:
        dict_colors = {
            "BOLD":         "\x1b[1m",
            "UNDERLINE":    "\x1b[4m",
            "RESET_CLR":    "\x1b[0m",
            "BLACK":        "\x1b[47;38;5;232m",
            "BLUE":         "\x1b[38;5;021m",
            "BROWN":        "\x1b[38;5;094m",
            "DARKGREY":     "\x1b[38;5;239m",
            "DARKGREEN":    "\x1b[38;5;022m",
            "GREEN":        "\x1b[38;5;028m",
            "LIGHTPINK":    "\x1b[38;5;141m",
            "LIGHTGREY":    "\x1b[38;5;243m",
            "LIGHTGREEN":   "\x1b[38;5;083m",
            "ORANGE":       "\x1b[38;5;208m",
            "PINK":         "\x1b[38;5;169m",
            "PURPLE":       "\x1b[38;5;054m",
            "RED":          "\x1b[38;5;160m",
            "TEAL":         "\x1b[38;5;030m",
            "VIOLET":       "\x1b[38;5;020m", #NOT SURE (constants.py/sc2reader)
            "YELLOW":       "\x1b[38;5;226m",
            "WHITE":        "\x1b[38;5;255m",
        }

    sc2_colors = {
        "Red":          dict_colors["RED"],
        "Blue":         dict_colors["BLUE"],
        "Teal":         dict_colors["TEAL"],
        "Yellow":       dict_colors["YELLOW"],
        "Purple":       dict_colors["PURPLE"],
        "Orange":       dict_colors["ORANGE"],
        "Green":        dict_colors["GREEN"],
        "Light Pink":   dict_colors["LIGHTPINK"],
        "Violet":       dict_colors["VIOLET"],
        "Light Grey":   dict_colors["LIGHTGREY"],
        "Dark Green":   dict_colors["DARKGREEN"],
        "Brown":        dict_colors["BROWN"],
        "Light Green":  dict_colors["LIGHTGREEN"],
        "Dark Grey":    dict_colors["DARKGREY"],
        "Pink":         dict_colors["PINK"],
        "White":        dict_colors["WHITE"],
        "Black":        dict_colors["BLACK"],
    }


def print_teams(replay):
    for team in replay.teams:
        if (team.result == "Win"):
            print("Team %d:   (%s%s%s)" % (team.number, dict_colors["GREEN"], team.result, dict_colors["RESET_CLR"]))
        else:
            print("Team %d:   (%s%s%s)" % (team.number, dict_colors["RED"], team.result, dict_colors["RESET_CLR"]))
        for player in team:
            print("\t%s%s%s (%s)" % (sc2_colors[player.color.name], player.name, dict_colors["RESET_CLR"], player.pick_race))
        print("")


def display_normal(replay):
    print("")
    print(dict_colors["BOLD"] + dict_colors["UNDERLINE"] + "Replay Infos:" + dict_colors["RESET_CLR"])
    if (replay.is_ladder):
        print(dict_colors["BLUE"] + "Ranked Game" + dict_colors["RESET_CLR"])
    if (replay.is_private):
        print(dict_colors["DARKGREY"] + "Private Game" + dict_colors["RESET_CLR"])
    print("Game type:     %s (%s)" % (replay.game_type, replay.expansion))
    print("Map Name:      %s" % replay.map_name)
    print("Game start:    %s" % replay.start_time.strftime("%A %d/%m/%Y %H:%M:%S"))
    print("Game end:      %s" % replay.end_time.strftime("%A %d/%m/%Y %H:%M:%S"))
    print("Game duration: %dm%02d" % (replay.real_length.seconds / 60, replay.real_length.seconds % 60))
    print("IG duration:   %dm%02d"  % (replay.game_length.seconds / 60, replay.game_length.seconds % 60))
    print("Game Speed:    %s" % replay.speed)
    print("Game version:  %s" % replay.release_string)
    print("")
    print(dict_colors["BOLD"] + dict_colors["UNDERLINE"] + "Teams Infos:" + dict_colors["RESET_CLR"])
    print_teams(replay)


def main():
    parser = argparse.ArgumentParser(description="StarCraft 2 Replay Analyser")
    parser.add_argument("file_name", help="SC2 Replay file")
    parser.add_argument("--nc", help="No color displayed", action="store_true")
    args = parser.parse_args()
    try:
        replay = sc2reader.load_replay(args.file_name)
    except UnicodeDecodeError:
        print("An error occured while parsing the Replay, please update sc2reader and try again.")
        exit(1)
    init_colors(args.nc)
    display_normal(replay)


if __name__ == '__main__':
    main()
