#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    SC2RA.py
## Desc:    StarCraft 2 Replay Analyser
##
## Author:  "Das" Franck Hochstaetter
## Version: V1.2 (03/09/2015)
##
## Dependencies : sc2reader (pip install sc2reader)
##    Python library for extracting information from various different Starcraft II resources.

import argparse
import sc2reader
from termcolor import cprint

def print_teams(replay):
    for team in replay.teams:
        print("Team %d:   (%s)" % (team.number, team.result));
        for player in team:
            print("        %s (%s)" % (player.name, player.pick_race))
        print("");

def display_normal(replay):
    print("");
    cprint("Replay Infos:", attrs=['bold']);
    if (replay.is_ladder):
        cprint("Ranked Game", attrs=['underline']);
    if (replay.is_private):
        cprint("Private Game", attrs=['underline']);
    print("Game type:     %s (%s)" % (replay.game_type, replay.expansion));
    print("Map Name:      %s" % replay.map_name);
    print("Game start:    %s" % replay.start_time.strftime("%A %d/%m/%Y %H:%M:%S"));
    print("Game end:      %s" % replay.end_time.strftime("%A %d/%m/%Y %H:%M:%S"));
    print("Game duration: %dm%02d" % (replay.real_length.seconds / 60, replay.real_length.seconds % 60));
    print("IG duration:   %dm%02d"  % (replay.game_length.seconds / 60, replay.game_length.seconds % 60));
    print("Game Speed:    %s" % replay.speed);
    print("Game version:  %s" % replay.release_string);
    print("");
    cprint("Teams Infos:", attrs=['bold']);
    print_teams(replay);


def main():
    parser = argparse.ArgumentParser(description="StarCraft 2 Replay Analyser");
    parser.add_argument("file_name", help="SC2 Replay file");
    args = parser.parse_args();
    replay = sc2reader.load_replay(args.file_name);
    display_normal(replay);

if __name__ == '__main__':
    main();
