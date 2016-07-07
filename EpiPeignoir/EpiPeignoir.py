#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Name:    EpiPeignoir.py
## Desc:    Epitech Ranking by GPA
##
## Author:  "Das" Franck Hochstaetter
## Version: v0.2 (19/12/2015)
##
## Dependencies : - requests (pip install requests)
##    Requests is an Apache2 Licensed HTTP library, written in Python, for human beings.
##                - pandas (pip install pandas)
##    pandas is a library providing data structures and data analysis tools for Python.

import argparse
import pandas
import re
import requests
import sys
from configparser import ConfigParser

re_credits = re.compile("Total credits acquired.+\n.+?\">.*?(\d+).+", re.MULTILINE)
re_gpa = re.compile("G.P.A.+\n.+?(\d*\.*\d+).+", re.MULTILINE)

def main():
    parser = argparse.ArgumentParser(description="Epitech Ranking by GPA")
    parser.add_argument("-c", "--configfile", help="path to the config file", default="config.ini")
    parser.add_argument("-l", "--loginlist", help="path to the login list")
    parser.add_argument("-o", "--output", help="path to the txt output file")
    parser.add_argument("--csv", help="path to the csv output file")
    parser.add_argument("-q", "--quiet", help="Don't display anything except errors", action="store_true")
    parser.add_argument("-n", "--noresult", help="Don't display end result", action="store_true")
    args = parser.parse_args()
    df = pandas.DataFrame()
    EPITECH_INTRA_URL = "https://intra.epitech.eu/"
    config = ConfigParser()
    config.read(args.configfile)

    data = {"login": config["Credential"]["login"],
            "password": config["Credential"]["password"],
            "submit": "Connect"}

    login_list = ""
    if (args.loginlist):
        login_list = re.findall(r"([\w-]+)\n*", open(args.loginlist).read())
    else:
        while True:
            try:
                line = input()
                login_list += line + "\n"
            except:
                break
        login_list = re.findall(r"([\w-]+)\n*", login_list)
    for (i, login) in enumerate(login_list):
        try:
            r = requests.post(EPITECH_INTRA_URL + "user/" + login + "/", data=data)
            if (r.status_code == 403 or r.status_code == 404):
                print("Page not found, your creditentials or the target login maybe wrong (%s)." % login)
            elif (r.status_code == 200):
                html_page = r.text
                credits = float(re.search(re_credits, html_page).groups()[0]) if re.search(re_credits, html_page) else -42.0
                gpa = float(re.search(re_gpa, html_page).groups()[0]) if re.search(re_gpa, html_page) else -42.0
                if not (args.quiet):
                    print("%d/%d %s %s %s" % (i+1, len(login_list), login, gpa, credits))
                df.set_value(len(df), "login", login)
                df.set_value(len(df)-1, "gpa", gpa)
                df.set_value(len(df)-1, "credits", credits)
        except:
            pass
    df.sort_values(["gpa", "credits"], ascending=False, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df_str = df.to_string()
    if not (args.noresult or args.quiet):
        print(df_str)
    if (args.output):
        open(args.output, "w").write(df_str + "\n")
    if (args.csv):
        df.to_csv(args.csv, encoding="utf-8", sep=";")

if __name__ == "__main__":
    main()
