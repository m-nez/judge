import multiprocessing
from time import sleep
from sys import stdin
import os

def f(fd, q):
    fl = open(fd, "r")
    l = fl.readline()
    q.put(l)

def readline_timed(stream, t):
    q = multiprocessing.Queue()
    p = multiprocessing.Process(
            target=f,
            args=[os.dup(stream.fileno()), q],
            daemon=True
            )
    p.start()

    try:
        r = q.get(True, t)
    except Exception:
        r = -1
    p.terminate()
    return r
