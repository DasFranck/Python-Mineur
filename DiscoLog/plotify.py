#!/usr/bin/env python3

import argparse
import html
import itertools
import operator
import os
import plotly
import plotly.graph_objs as go
from datetime import date, datetime, timedelta as td
from yattag import Doc


def cumultative_sum(values, start=0):
    for v in values:
        start += v
        yield start


def get_date_array():
    d1 = date(2016, 9, 7)
    d2 = datetime.today().date()
    delta = d2 - d1

    date_array = []
    for i in range(delta.days):
        date_array.append(d1 + td(days=i))

    return [x.strftime("%Y-%m-%d") for x in date_array]


def get_log_content(args):
    text = ""
    meta_list = []
    with open(args.log_path, "r") as file:
        for line in file:
            text += line
            if (len(line.split("\t")) > 1):
                (date, author, _) = line.split("\t")
                meta_list.append((date, author))

    return (meta_list, text)


def generate_plot(graph_dict, file_path):
    plotly.offline.plot(graph_dict, filename=file_path, show_link=False, auto_open=False)
    return (plotly.offline.plot(graph_dict, filename=file_path, show_link=False, auto_open=False, output_type="div"))


def plot_1(date_array, msg_counts, cumul):
    msg_average = []
    for i, cum in enumerate(cumul):
        msg_average.append(int(cum / (i + 1)))

    line1 = go.Bar(x=date_array,
                   y=msg_counts,
                   name="Messages per day")

    line2 = go.Scatter(x=date_array,
                       y=msg_average,
                       name="Average messages per day")

    return (generate_plot({"data": [line1, line2],
                           "layout": go.Layout(title="Number of messages per day in #discussion (BreakTime)")},
                          "plots/PlotBT-msg.html"))


def plot_2(date_array, cumul):
    return (generate_plot({"data": [go.Scatter(x=date_array, y=cumul)],
                           "layout": go.Layout(title="Number of cumulatives messages in #discussion (BreakTime)")},
                          "plots/PlotBT-msgcumul.html"))


def top10_per_day(meta_list):
    # user_list = sort(list(set(([b for a,b in meta_list]))))
    text = "<pre>"
    meta_list = [(meta[0].split(" ")[0], meta[1]) for meta in meta_list]
    meta_sorted = sorted(meta_list, key=operator.itemgetter(0))
    meta_grouped = [list(group) for key, group in itertools.groupby(meta_sorted, operator.itemgetter(0))]
    for meta_per_date in meta_grouped:
        count_map = {}
        for t in meta_per_date:
            count_map[t[1]] = count_map.get(t[1], 0) + 1
        top_list = sorted(count_map.items(), key=operator.itemgetter(1), reverse=True)[0:10]

        text += "<b>" + meta_per_date[0][0] + "</b><br />"
        for (i, elem) in enumerate(top_list):
            text += "%d.\t%d\t%s<br />" % (i + 1, elem[1], html.escape(elem[0]))
        text += "<br />"
    text += "</pre>"
    return (text)


def write_html(pl1, pl2, tp1):
    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('head'):
            doc.asis('<meta http-equiv="content-type" content="text/html; charset=utf-8" />')
        with tag('body'):
            with tag('h1'):
                text("DiscoLog Monitoring for BreakTime")
            doc.asis(pl1)
            doc.asis(pl2)
            with tag('p'):
                doc.asis(tp1)
            text("html generated at %s" % datetime.now().strftime("%T the %F"))

    result = doc.getvalue()
    with open("plots/index.html", "w") as file:
        file.write(result)


def main():
    # Parsearg
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("log_path")
    args = parser.parse_args()

    if not (os.path.exists("plots")):
        os.makedirs("plots")

    date_array = get_date_array()
    meta_list, chat_log = get_log_content(args)

    counts = [chat_log.count(x) for x in date_array]
    cumul = list(cumultative_sum(counts))

    pl1 = plot_1(date_array, counts, cumul)
    pl2 = plot_2(date_array, cumul)
    tp1 = top10_per_day(meta_list)
    write_html(pl1, pl2, tp1)


if __name__ == '__main__':
    main()
