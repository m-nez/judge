# -*- coding: utf-8 -*-
# Copyright (C) 2016 Michał Nieznański
from __future__ import print_function
import subprocess
import shlex
import timeout
import atexit
import time
import sys
import os

def readline_timed(stream, t):
    result = -1
    with timeout.Timeout(t) as tout:
        result = stream.readline()
    return result

class Judge():
    def __init__(self, size, prog1, prog2, update_func = None, wait_time = 1):
        self.size = size
        self.update_func = update_func
        self.wait_time = wait_time
        self.prog1 = prog1
        self.prog2 = prog2
        self.array = [[ 0 for i in range(size) ] for j in range(size)]
        self.set = set((i, j) for i in range(size) for j in range(size))
    def next_move_possible(self):
        offset = [
                [-1, 0],
                [1, 0],
                [0, -1],
                [0, 1]
                ]
        to_rm = set()
        for e in self.set:
            for o in offset:
                if (e[0] + o[0], e[1] + o[1]) in self.set:
                    return True
            to_rm.add(e)
        self.set.difference_update(to_rm)
        return False
    def write(self, p, string):
        if p == 1:
            p = self.p1
        else:
            p = self.p2
        p.stdin.write(string)
        p.stdin.flush()
    def finish(self, win):
        try:
            if win == 1:
                self.write(1, "WYGRAŁEŚ")
                self.write(2, "PRZEGRAŁEŚ")
            elif win == 2:
                self.write(2, "WYGRAŁEŚ")
                self.write(1, "PRZEGRAŁEŚ")
            else:
                self.write(1, "WYGRAŁEŚ")
                self.write(2, "WYGRAŁEŚ")
        except:
            pass
        if win == 1 or win == 2:
            print("WIN:", win)
        if sys.platform.startswith("win"):
            os.system("taskkill /pid %d /F" % self.p1.pid)
            os.system("taskkill /pid %d /F" % self.p2.pid)
        else:
            self.p1.kill()
            self.p2.kill()
        return win

    def validate(self, string):
        strs = string.split()
        if len(strs) != 4:
            return 0
        try:
            ints = [int(i) for i in strs]
        except:
            return 0
        return ints

    def update(self, x0, y0, x1, y1, val):
        x0 -= 1
        x1 -= 1
        y0 -= 1
        y1 -= 1
        for i in (x0, x1, y0, y1):
            if i < 0 or i >= self.size:
                return 1
        if abs(x0 - x1) > 1 or abs(y0 - y1) > 1:
            return 1
        if x0 != x1 and y0 != y1:
            return 1
        if (x0, y0) == (x1, y1):
            return 1
        if self.array[y0][x0] != 0 or self.array[y1][x1] != 0:
            return 1
        self.array[y0][x0] = val
        self.array[y1][x1] = val
        self.set.remove((x0, y0))
        self.set.remove((x1, y1))
        return 0

    def play(self):
        if self.play_start() == None: # No return value means it's ok
            while True:
                r = self.play_step()
                if r != None:
                    return r

    def play_start(self):
        self.p1 = subprocess.Popen(
                shlex.split(self.prog1),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True)
        self.p2 = subprocess.Popen(
                shlex.split(self.prog2),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True)

        self.write(1, "PING\n")
        #print("SENT1:", "PING")
        self.write(2, "PING\n")
        #print("SENT2:", "PING")
        r = readline_timed(self.p1.stdout, self.wait_time)
        if r == -1:
            return self.finish(2)
        r = r.strip()
        #print("RECV1:",r)
        r = readline_timed(self.p2.stdout, self.wait_time)
        if r == -1:
            return self.finish(2)
        r = r.strip()
        #print("RECV2:",r)
        self.write(1, str(self.size) + "\n")
        #print("SENT1:", str(self.size))
        self.write(2, str(self.size) + "\n")
        #print("SENT2:", str(self.size))
        self.write(1, "ZACZYNAJ\n")
        #print("SENT1:", "ZACZYNAJ")

    def play_step(self):
        r = readline_timed(self.p1.stdout, self.wait_time)
        if r == -1:
            return self.finish(2)
        r = r.strip()
        #print("RECV1:", r)
        v = self.validate(r)
        if not v:
            return self.finish(2)
        if self.update(v[0], v[1], v[2], v[3], 1) != 0:
            return self.finish(2)
        if self.update_func != None:
            self.update_func(v[0], v[1], v[2], v[3], 1)

        if not self.next_move_possible():
            return self.finish(1)
        self.write(2, r + "\n")
        #print("SENT2:", r)
        r = readline_timed(self.p2.stdout, self.wait_time)
        if r == -1:
            return self.finish(1)
        r = r.strip()
        #print("RECV2:", r)
        v = self.validate(r)
        if not v:
            return self.finish(1)
        if self.update(v[0], v[1], v[2], v[3], 2) != 0:
            return self.finish(1)
        if self.update_func != None:
            self.update_func(v[0], v[1], v[2], v[3], 2)

        if not self.next_move_possible():
            return self.finish(2)
        self.write(1, r + "\n")
