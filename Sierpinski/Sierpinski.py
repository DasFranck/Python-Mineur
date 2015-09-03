#!/usr/bin/env python

## Name:    Sierpinski.py
## Desc:    Sierpinski's traingle drawer using the turtle lib.
##
## Author:  "Das" Franck Hochstaetter
## Version: V1.2 (03/09/2015)

import argparse
from turtle import *
from time import sleep
from math import sqrt

parser = argparse.ArgumentParser(description="Sierpinski's traingle drawer.");
parser.add_argument("-c", "--cursor", help="show the cursor", action="store_true");
parser.add_argument("-i", "--iteration", help="modify the number of iterations", default=4, type=int);
parser.add_argument("-o", "--orange", help="better colors", action="store_true");
parser.add_argument("-s", "--size", help="modify triangle size", default=400, type=int);
parser.add_argument("--speed", help="modify the cursor speed (see turtle.speed for more informations)", default=6, type=int);
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true");
args = parser.parse_args();

def main():
    print("\033c");

    if (args.orange):
        bgcolor("black");
        color("orange");
    if (args.cursor == 0):
        ht();

    size = args.size;
    it = args.iteration;
    speed(args.speed);
    xa = (-size)/2;
    ya = (-size)/2;
    xb = size/2;
    yb = (-size)/2;
    xc = 0;
    yc = sqrt(3)/2 * size - size/2;
    draw(xa, ya, xb, yb, xc, yc, it);
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
