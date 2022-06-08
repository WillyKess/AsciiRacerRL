#!/usr/bin/env python
from __future__ import absolute_import
import pprint
from queue import Queue
import threading
# import runpy
from time import sleep
from asciiracer.game import run
# from ascii_racer.asciiracer.game import run
# import ascii_racer.asciiracer as ar
# import sys
# import os.path
# ar_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#              + '/ascii_racer/asciiracer')
# sys.path.append(ar_dir)
statequeue: Queue[dict] = Queue()
keyqueue = Queue()


# def rungame():
#     run(squeue=statequeue, kqueue=keyqueue)


thread = threading.Thread(target=lambda: run(
    squeue=statequeue, kqueue=keyqueue), daemon=True)
thread.start()
sleep(2)
a = open("log.txt", "w")
print(statequeue.get())
# sleep(2)
a.write(pprint.pformat(statequeue.get()))
a.flush()
sleep(2)
print(statequeue.get())
sleep(0.5)
# a.write(str(statequeue.get()))
keyqueue.put(ord('q'))
a.close()
