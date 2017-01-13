#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright (C) 2016 Michał Nieznański
from __future__ import print_function
try:
    #Python3
    import tkinter as tk
except:
    #Python2
    import Tkinter as tk
from judge import Judge
import argparse
import threading

class Board():
    def __init__(self, size, canvas, enum=False):
        """
        size : tuple (x, y)
        """
        self.enumerate = enum
        self.size = size[0]
        self.array = [ [ 0 for i in range(size[0]) ] for j in range(size[0])]
        self.canvas = canvas
        self.w = int(self.canvas["width"])
        self.h = int(self.canvas["height"])
        self.counter = 0
        self.restart()
    def restart(self):
        self.canvas.delete("all")
        self.draw_lines()
    def draw_lines(self):
        w = self.w
        h = self.h
        fill = "#000000"
        for i in range(1, self.size): # Horizontal lines
            self.canvas.create_line(
                    0, i * h / float(self.size),
                    w, i * h / float(self.size),
                    fill=fill
                    )
        for i in range(1, self.size): # Vertical lines
            self.canvas.create_line(
                    i * w / float(self.size), 0,
                    i * w / float(self.size), h,
                    fill=fill
                    )
    def add_elem(self, x0, y0, x1, y1, val):
        self.array[y0][x0] = val
        self.array[y1][x1] = val

        x_step = self.w / float(self.size)
        y_step = self.h / float(self.size)
        rx0 = min(x0, x1) * x_step + 1
        rx1 = (max(x0, x1) + 1 ) * x_step
        ry0 = min(y0, y1) * y_step + 1
        ry1 = (max(y0, y1) + 1) * y_step
        fill = "#FFFFFF" if val == 1 else "#808080"
        self.canvas.create_rectangle(rx0, ry0, rx1, ry1, fill=fill, width=0)
        if self.enumerate:
            self.counter += 1
            self.canvas.create_text((rx0 + rx1) / 2.0, (ry0 + ry1) / 2.0, text=str(self.counter),
                    font="-size %d" % int(0.4 * min(self.h, self.w) / self.size))
    def update_func(self, x0, y0, x1, y1, val):
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
        self.add_elem(x0, y0, x1, y1, val)
        self.canvas.update_idletasks()
        return 0


class Main(tk.Frame):
    def __init__(self, size, prog1, prog2, w=400, h=400, enum=False, wait_time=1, step=False):
        """
        size : int
        prog1 : str
        prog2 : str
        """
        self.step = step
        self.wait_time = wait_time
        tk.Frame.__init__(self)
        self.enumerate = enum
        self.width = w
        self.height = h
        self.size = size
        self.prog1 = prog1
        self.prog2 = prog2
        self.create_widgets()
        self.master.title("JudgeGUI")
        self.judge = Judge(self.size, self.prog1, self.prog2, self.board.update_func, self.wait_time)
        if self.step:
            if self.judge.play_start() == None: # No return value means it's ok
                self.master.protocol("WM_DELETE_WINDOW", self.on_quit)
                self.master.bind("<Key>", self.step_callback)
        else:
            self.master.after(1, self.judge.play)
    def on_quit(self):
        self.judge.finish(0)
        self.master.quit()
    def step_callback(self, key):
        if key.char == " ":
            self.judge.play_step()
    def play(self):
        self.judge = Judge(self.size, self.prog1, self.prog2, self.board.update_func, self.wait_time)
        self.judge.play()
    def create_widgets(self):
        self.grid()
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="#A0A040")
        self.board = Board((self.size, self.size), self.canvas, self.enumerate)
        self.canvas.grid(row=0)

def print_result(p_wins):
    print("PLAYER 1 WINS:", p_wins[1])
    print("PLAYER 2 WINS:", p_wins[2])


parser = argparse.ArgumentParser(description="Judge the game between two programs")
group = parser.add_mutually_exclusive_group()
group.add_argument("-g", "--gui", default=False, action="store_true", help="run with gui (not available with -f)")
group.add_argument("-f", "--file",  help="Play games on boards with sizes stated in the file")
parser.add_argument("prog1", help="first program")
parser.add_argument("prog2", help="second program")
parser.add_argument("-s", "--size", default=7, type=int, help="dimensions of the board")
parser.add_argument("-x", "--width", default=400, type=int, help="width of the gui")
parser.add_argument("-y", "--height", default=400, type=int, help="height of the gui")
parser.add_argument("-e", "--enumerate", default=False, action="store_true", help="enumerate placed blocks")
parser.add_argument("-t", "--timeout", default=1, type=float, help="maximal move time")
parser.add_argument("-p", "--step", default=False, action="store_true", help="Request the next step by pressing <Space>")
args = parser.parse_args()

p_wins = [0, 0, 0]
if args.file:
    with open(args.file) as f:
        for l in f:
            size = int(l)
            result = Judge(args.size, args.prog1, args.prog2, None, args.timeout).play()
            p_wins[result] += 1
        print_result(p_wins)
else:
    if args.gui:
        app = Main(args.size, args.prog1, args.prog2,
                args.width, args.height, args.enumerate, args.timeout, args.step)
        app.mainloop()
    else:
        result = Judge(args.size, args.prog1, args.prog2, None, args.timeout).play()
        p_wins[result] += 1
        print_result(p_wins)
