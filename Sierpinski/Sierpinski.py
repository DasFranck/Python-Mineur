#!/usr/bin/env python

from turtle import *
from time import sleep
from math import sqrt

bgcolor("white");
color("black");

size = 400;

xa = (-size)/2;
ya = (-size)/2;
xb = size/2;
yb = -size/2;
xc = 0;
yc = sqrt(3)/2 * size - size/2;

pu();
setpos(xa, ya);
pd();
for i in range(0, 4) :
    setpos(xa, ya);
    setpos(xb, yb);
    setpos(xc, yc);

input("Push Enter to exit the program");
