#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getBTmessages
from plotify import Plotify

TOKEN = "MjQ1NjUzNTU3ODcxNjQwNTg0.CwpAXg.E-0gX1l3EXQ0c_YRyVWEBhltOxc"
LOG_PATH = "chat_logs/BreakTime-discussion.log"


def main():
    parser = argparse.ArgumentParser(description="BT-Monitor Script")
    parser.add_argument("--no-getlog", action='store_true')
    args = parser.parse_args()

    getBTmessages.client.run(TOKEN)
    plotify = Plotify(LOG_PATH)
    plotify.plotify()
    plotify.write_main_html()
    plotify.write_standing_history_html()


if __name__ == '__main__':
    main()
