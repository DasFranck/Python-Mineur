#!/usr/bin/env python3

import argparse
import plotly
from datetime import date, datetime, timedelta as td
from plotly.graph_objs import Scatter, Layout


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
    with open(args.log_path, "r") as file:
        for line in file:
            text += line
    return text


def plot_1(date_array, msg_counts, cumul):
    msg_average = []
    for i, cum in enumerate(cumul):
        msg_average.append(int(cum / (i + 1)))

    line1 = Scatter(x=date_array,
                    y=msg_counts,
                    name="Messages per day",
                    fill="tozeroy")

    line2 = Scatter(x=date_array,
                    y=msg_average,
                    name="Average messages per day")

    plotly.offline.plot({"data": [line1, line2],
                         "layout": Layout(title="Number of messages per day in #discussion (BreakTime)")},
                        filename="PlotBT-msg.html",
                        auto_open=False)


def plot_2(date_array, cumul):
    plotly.offline.plot({"data": [Scatter(x=date_array, y=cumul)],
                         "layout": Layout(title="Number of cumulatives messages in #discussion (BreakTime)")},
                        filename="PlotBT-msgcumul.html",
                        auto_open=False)


def main():
    # Parsearg
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("log_path")
    args = parser.parse_args()

    date_array = get_date_array()
    chat_log = get_log_content(args)

    counts = [chat_log.count(x) for x in date_array]
    cumul = list(cumultative_sum(counts))

    plot_1(date_array, counts, cumul)
    plot_2(date_array, cumul)


if __name__ == '__main__':
    main()
