# -*- coding: utf-8 -*-
#Copyright (C) 2016 Michał Nieznański
import signal
import os
import threading
import time

class TimeoutException(Exception):
    pass

def raise_timeout(signum, stacktrace):
    raise TimeoutException("SIGINT received")

class Timeout(threading.Thread):
    """
    Raise TimeoutError after *timeout* seconds.
    Use stop() to prevent the exception.
    >>> with Timeout(1) as t:
    ...     time.sleep(2)
    >>> t.timed_out
    True
    >>> with Timeout(1.5) as t:
    ...     time.sleep(1)
    >>> t.timed_out
    False
    """
    def __init__(self, timeout):
        threading.Thread.__init__(self)
        self.daemon = True
        self.timeout = timeout
        self.stopped = False
        self.timed_out = False
        signal.signal(signal.SIGINT, raise_timeout)
    def stop(self):
        self.stopped = True
    def run(self):
        time.sleep(self.timeout)
        if not self.stopped:
            os.kill(os.getpid(), signal.SIGINT)
    def __enter__(self):
        self.start()
        return self
    def __exit__(self, type, value, traceback):
        self.stop()
        if type == TimeoutException:
            self.timed_out = True
            return True
        else:
            return False
