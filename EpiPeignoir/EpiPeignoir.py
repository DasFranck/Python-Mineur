#!/usr/bin/env python3

import argparse
import pandas
import re
import requests
import sys
from configparser import ConfigParser

re_credits = re.compile("Total credits acquired.+\n.+?(\d+).+", re.MULTILINE)
re_gpa = re.compile("G.P.A.+\n.+?(\d*\.*\d+).+", re.MULTILINE)

def main():
    df = pandas.DataFrame()
    EPITECH_INTRA_URL = "https://intra.epitech.eu/"
    config = ConfigParser()
    config.read("config.ini")

    data = {"login": config["Credential"]["login"],
            "password": config["Credential"]["password"],
            "submit": "Connect"}

    #login_list = re.findall(r"([\w-]+)\n*", open("ll.txt").read())
    login_list = re.findall(r"([\w-]+)\n*", open("pso2019").read())
    for (i, login) in enumerate(login_list):
        r = requests.post(EPITECH_INTRA_URL + "user/" + login + "/", data=data)
        if (r.status_code == 403 or r.status_code == 404):
            print("Page not found, your creditentials or the target login maybe wrong (%s)." % login)
        elif (r.status_code == 200):
            html_page = r.text
            credits = float(re.search(re_credits, html_page).groups()[0]) if re.search(re_credits, html_page) else -42.0
            gpa = float(re.search(re_gpa, html_page).groups()[0]) if re.search(re_gpa, html_page) else -42.0
            print("%d/%d %s %s %s" % (i+1, len(login_list), login, gpa, credits))
            df.set_value(len(df), "login", login)
            df.set_value(len(df)-1, "gpa", gpa)
            df.set_value(len(df)-1, "credits", credits)
    df.sort_values(["gpa", "credits"], ascending=False, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    df = df.to_string()
    print(df)

if __name__ == "__main__":
    main()
