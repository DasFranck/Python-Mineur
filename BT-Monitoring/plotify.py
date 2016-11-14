#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import html
import itertools
import operator
import os
import plotly
import plotly.graph_objs as go
import re
from collections import Counter, OrderedDict
from datetime import date, datetime, timedelta as td
from yattag import Doc


# UTILS
def generate_plot(graph_dict, file_path):
    plotly.offline.plot(graph_dict, filename=file_path, show_link=False, auto_open=False)
    return (plotly.offline.plot(graph_dict, filename=file_path, show_link=False, auto_open=False, output_type="div"))


def cumultative_sum(values, start=0):
    for v in values:
        start += v
        yield start


# Plotify class
class Plotify():
    def __init__(self, log_path):
        if not (os.path.exists("plots")):
            os.makedirs("plots")
        self.get_date_array()
        self.get_log_content(log_path)
        self.counts = [self.chat_log.count(x) for x in self.date_array]
        self.cumul = list(cumultative_sum(self.counts))

    def get_date_array(self):
        d1 = date(2016, 9, 7)
        d2 = datetime.today().date()
        delta = d2 - d1

        date_array = []
        for i in range(delta.days):
            date_array.append(d1 + td(days=i))
        self.date_array = [x.strftime("%Y-%m-%d") for x in date_array]

    def get_log_content(self, log_path):
        text = ""
        meta_list = []
        with open(log_path, "r") as file:
            for line in file:
                text += line
                if (len(line.split("\t")) > 1):
                    (date, author, _) = line.split("\t")
                    meta_list.append((date, author))
        self.chat_log = text
        self.meta_list = meta_list
        print("OK")

    def plotify(self):
        self.plots = OrderedDict()
        self.plots["msgperday"] = (plot_msgperday(self, "PlotBT-msg.html"), "PlotBT-msg.html", "Number of messages per day")
        self.plots["msgcumul"] = (plot_msgcumul(self, "PlotBT-msgcumul.html"), "PlotBT-msgcumul.html", "Number of cumulatives messages")
        self.plots["top10"] = (plot_usertopx(self, 10, "PlotBT-top10.html"), "PlotBT-top10.html", "Number of cumulatives messages for the Top 10 users")
        self.plots["top20"] = (plot_usertopx(self, 20, "PlotBT-top20.html"), "PlotBT-top20.html", "Number of cumulatives messages for the Top 20 users")
        self.stats = OrderedDict()
        self.stats["top10perday"] = (top10_per_day(self, "StatsBT-top10perday.html"), "StatsBT-top10perday.html", "Standings history")
        top10yesterday_html, self.top10yesterday = top10_yesterday(self, "Stats-top10yesterday.html")
        self.stats["top10yesterday"] = (top10yesterday_html, None, None)

    def write_main_html(self):
        doc, tag, text = Doc().tagtext()

        with tag('html'):
            with tag('head'):
                doc.asis('<meta http-equiv="content-type" content="text/html; charset=utf-8" />')
            with tag('body'):
                with tag('h1'):
                    text("DiscoLog Monitoring for BreakTime (#discussion)")
                # Standing of yesterday
                with tag('h2'):
                    text("Standings of yesterday")
                with tag('h3'):
                    doc.asis(self.stats["top10yesterday"][0])
                # Graphs
                with tag('h2'):
                    text("Graphs")
                doc.asis("<ul style=\"list-style-type:none\">")
                for _, plot in self.plots.items():
                    if plot[1] and plot[2]:
                        doc.asis("<li>")
                        with tag('a', href=plot[1]):
                            text(plot[2])
                        doc.asis("</li>")
                doc.asis("</ul>")
                # Stats
                with tag('h2'):
                    text("Stats")
                doc.asis("<ul style=\"list-style-type:none\">")
                for _, stat in self.stats.items():
                    if stat[1] and stat[2]:
                        doc.asis("<li>")
                        with tag('a', href=stat[1]):
                            text(stat[2])
                        doc.asis("</li>")
                doc.asis("</ul>")
                # Footer
                text("Page generated at %s" % datetime.now().strftime("%T the %F"))

        result = doc.getvalue()
        with open("plots/index.html", "w") as file:
            file.write(result)

    def write_standing_history_html(self):
        doc, tag, text = Doc().tagtext()

        with tag('html'):
            with tag('head'):
                doc.asis('<meta http-equiv="content-type" content="text/html; charset=utf-8" />')
            with tag('body'):
                doc.asis(self.stats["top10perday"][0])
                doc.asis("<br />")
                doc.asis("<br />")
                text("Page generated at %s" % datetime.now().strftime("%T the %F"))

        result = doc.getvalue()
        with open("plots/standinghistory.html", "w") as file:
            file.write(result)

    def write_raw_text_in_html(self, content, path):
        doc, tag, text = Doc().tagtext()

        with tag('html'):
            with tag('head'):
                doc.asis('<meta http-equiv="content-type" content="text/html; charset=utf-8" />')
            with tag('body'):
                doc.asis(content)

        result = doc.getvalue()
        with open("plots/" + path, "w") as file:
            file.write(result)


def plot_msgperday(plotify, path):
    msg_average = []
    for i, cum in enumerate(plotify.cumul):
        msg_average.append(int(cum / (i + 1)))

    line1 = go.Bar(x=plotify.date_array,
                   y=plotify.counts,
                   name="Messages per day")

    line2 = go.Scatter(x=plotify.date_array,
                       y=msg_average,
                       name="Average messages per day")

    return (generate_plot({"data": [line1, line2],
                           "layout": go.Layout(title="Number of messages per day in #discussion (BreakTime)")},
                          "plots/" + path))


def plot_msgcumul(plotify, path):
    return (generate_plot({"data": [go.Scatter(x=plotify.date_array, y=plotify.cumul)],
                           "layout": go.Layout(title="Number of cumulatives messages in #discussion (BreakTime)")},
                          "plots/" + path))


def plot_usertopx(plotify, max, path):
    top = Counter(elem[1] for elem in plotify.meta_list).most_common(max)
    top_users = [elem[0] for elem in top]
    users_line = []
    for i, user in enumerate(top_users):
        print(i + 1)
        counts = [len(re.findall(r'%s.+\t%s' % (re.escape(x), re.escape(user)), plotify.chat_log)) for x in plotify.date_array]
        cumul = list(cumultative_sum(counts))
        line = go.Scatter(x=plotify.date_array,
                          y=cumul,
                          name=user)
        users_line.append(line)
    return (generate_plot({"data": users_line,
                           "layout": go.Layout(title="Number of cumulatives messages for the Top %d users in #discussion (BreakTime)" % max)},
                          "plots/" + path))


def top10_per_day(plotify, path):
    # user_list = sort(list(set(([b for a,b in meta_list]))))
    text = "<pre>"
    meta_list = [(meta[0].split(" ")[0], meta[1]) for meta in plotify.meta_list]
    meta_sorted = sorted(meta_list, key=operator.itemgetter(0))
    meta_grouped = [list(group) for key, group in itertools.groupby(meta_sorted, operator.itemgetter(0))]
    for meta_per_date in reversed(meta_grouped[:-1]):
        count_map = {}
        for t in meta_per_date:
            count_map[t[1]] = count_map.get(t[1], 0) + 1
        top_list = sorted(count_map.items(), key=operator.itemgetter(1), reverse=True)[0:10]

        text += "<b>" + meta_per_date[0][0] + "</b><br />"
        for (i, elem) in enumerate(top_list):
            text += "%d.\t%d\t%s<br />" % (i + 1, elem[1], html.escape(elem[0]))
        if meta_per_date is not meta_grouped[0]:
            text += "<br />"
    text += "</pre>"
    plotify.write_raw_text_in_html(text, path)
    return (text)


def top10_yesterday(plotify, path):
    # user_list = sort(list(set(([b for a,b in meta_list]))))
    text = "<ol type=\"1\">"
    plain = ""
    meta_list = [(meta[0].split(" ")[0], meta[1]) for meta in plotify.meta_list]
    meta_sorted = sorted(meta_list, key=operator.itemgetter(0))
    meta_grouped = [list(group) for key, group in itertools.groupby(meta_sorted, operator.itemgetter(0))]
    meta_yesterday = meta_grouped[-2]
    count_map = {}
    for t in meta_yesterday:
        count_map[t[1]] = count_map.get(t[1], 0) + 1
    top_list = sorted(count_map.items(), key=operator.itemgetter(1), reverse=True)[0:10]

    for (i, elem) in enumerate(top_list):
        text += "<li><pre>%d\t%s</pre></li>" % (elem[1], html.escape(elem[0]))
        plain += "%d.\t%d\t%s\n" % (i + 1, elem[1], elem[0])
    text += "</ol>"
    plotify.write_raw_text_in_html(text, path)
    return (text, plain)


def main():
    # Parsearg
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("log_path")
    args = parser.parse_args()

    plotify = Plotify(args.log_path)
    plotify.plotify()
    plotify.write_main_html()
    plotify.write_standing_history_html()


if __name__ == '__main__':
    main()
