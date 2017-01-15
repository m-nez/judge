# -*- coding: utf-8 -*-
# Copyright (C) 2016 Michał Nieznański

from time import sleep
import threading
try:
    from queue import Queue
except:
    # Python 2
    from Queue import Queue

def f(stream, q):
    l = stream.readline()
    q.put(l)

def readline_timed(stream, t):
    q = Queue()
    p = threading.Thread(
            target=f,
            args=[stream, q]
            )
    p.setDaemon(True)
    p.start()

    try:
        r = q.get(True, t)
    except:
        r = -1
    return r
