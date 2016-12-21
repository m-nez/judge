# -*- coding: UTF-8 -*-
#Copyright (C) 2016 Michał Nieznański
from sys import argv
from time import sleep
from sys import stdout, stderr, stdin
from random import randint
import numpy

def move(array):
    offset = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for y, r in enumerate(array):
        for x, e in enumerate(r):
            if e == 0:
                for o in offset:
                    size = array.shape[0]
                    if size > y + o[1] >= 0 and size > x + o[0] >= 0:
                        if array[y + o[1]][x + o[0]] == 0:
                            return "%d %d %d %d" % (
                                    x + 1,
                                    y + 1,
                                    x + 1 + o[0],
                                    y + 1 + o[1]
                                    )
    return "1 1 1 2"

def make_move(array, m, v):
    ints = [int(i) - 1 for i in m.split()]
    array[ints[1]][ints[0]] = v
    array[ints[3]][ints[2]] = v

ping = input()
print("PONG")
stdout.flush()
size = input()
size = int(size)

array = numpy.zeros((size, size), numpy.uint8)

first = input()
if first == "ZACZYNAJ":
    m = move(array)
    make_move(array, m, 1)
    print(m)
else:
    m = first
    make_move(array, m, 2)
    m = move(array)
    make_move(array, m, 1)
    print(m)
while True:
    m = input()
    sleep(0.02)
    make_move(array, m, 2)
    m = move(array)
    make_move(array, m, 1)
    print(m)
