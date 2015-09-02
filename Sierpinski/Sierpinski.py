#!/usr/bin/env python

import argparse
from turtle import *
from time import sleep
from math import sqrt

parser = argparse.ArgumentParser(description="Sierpinski's traingle drawer.");
parser.add_argument("-s", "--size", help="modify triangle size", type=int);
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true");
args = parser.parse_args();

def main():
    bgcolor("white");
    color("black");

    if (args.size):
        size = args.size;
    else:
        size = 400;
    xa = (-size)/2;
    ya = (-size)/2;
    xb = size/2;
    yb = (-size)/2;
    xc = 0;
    yc = sqrt(3)/2 * size - size/2;
    draw(xa, ya, xb, yb, xc, yc, 8);
    input("Push Enter to exit the program");

def draw(xa, ya, xb, yb, xc, yc, it):
    if (args.verbose):
        print(xa, ya, xb, yb, xc, yc);
    if (it != 0):
        pu();
        setpos(xa, ya);
        pd();
        setpos(xb, yb);
        setpos(xc, yc);
        setpos(xa, ya);
        draw(xa, ya, (xb - xa) / 2 + xa, yb, (xc - xa) / 2 + xa, (yc - ya) / 2 + ya, it - 1);
        draw((xb - xa) / 2 + xa, yb, xb, yb, xb - (xb - xc) / 2 , (yc - yb) / 2 + ya, it - 1);
        draw((xc - xa) / 2 + xa, (yc - ya) / 2 + ya, xb - (xb - xc) / 2, (yc - yb) / 2 + ya, xc, yc, it - 1);

if __name__ == '__main__':
        main();
