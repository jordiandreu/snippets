import gevent
from gevent.queue import Queue
import time
from random import randint

TASK0 = 10

tasks = Queue()
results = Queue()

def cb(a):
    print 'I am %s' % a
    print 'callback'

def job(worker, task):
    gevent.sleep(3)
    results.put('Task set %s executed  by %s' % (task, worker))
    print '%s remaining tasks' % tasks.qsize()


def worker(name):
    while not tasks.empty():
        task = tasks.get()
        print('Worker %s got task %s' % (name, task))
        job(name, task)
    print 'Queue empty, %s is going home!' % name


def boss():
    for i in range(TASK0):
        tasks.put_nowait(i)

g = gevent.spawn(boss)
g.link(cb)
g.join()


def boss2():
    c=1
    while True:
        r = randint(0, 1)
        if r ==0:
            tasks.put(TASK0 + c)
            print 'task %s added' % (TASK0 + c)
        c += 1
        gevent.sleep(3)

g2 = gevent.spawn(boss2)

# Number of workers...number of concurrent tasks
j = gevent.spawn(worker, 'john')
s = gevent.spawn(worker, 'steve')
b = gevent.spawn(worker, 'bob')

print type(j)

#####################
# Place here any code
gevent.sleep(5)
print 'awakening'
#####################

gevent.joinall([j,s,b])

while not results.empty():
    print results.get_nowait()
