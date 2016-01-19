#!/usr/bin/env python
#-*- coding:utf-8 -*-
#auther = Alan
import threading
import contextlib
import random
import time

doing = []
def num(argv):
    while True:
        print len(argv)
        time.sleep(1)
t = threading.Thread(target=num,args=(doing,))
t.start()

@contextlib.contextmanager
def fuc(item,argvs):
    item.append(argvs)
    yield
    item.remove(argvs)

def dask(argv):
    with fuc(doing,threading.current_thread()):
        print 'data'
        time.sleep(random.randint(1,5))

for i in xrange(30):
    t = threading.Thread(target=dask,args=(i,))
    t.start()