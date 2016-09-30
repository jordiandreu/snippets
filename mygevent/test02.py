import gevent
from gevent.queue import Queue

tasks = Queue()
results = Queue()


def job(worker, task):
    gevent.sleep(3)
    results.put_nowait('Task set %s executed  by %s' % (task, worker))
    print '%s remaining tasks' % tasks.qsize()


def worker(name):
    while not tasks.empty():
        task = tasks.get()
        print('Worker %s got task %s' % (name, task))
        job(name, task)
    print 'Queue empty, %s is going home!' % name


def boss(n):
    for i in range(n):
        tasks.put_nowait(i)

gevent.spawn(boss, 10).join()

# Number of workers...number of concurrent tasks
j = gevent.spawn(worker, 'john')
s = gevent.spawn(worker, 'steve')
b = gevent.spawn(worker, 'bob')

#####################
# Place here any code
gevent.sleep(5)
print 'awakening'
#####################
gevent.joinall([j,s,b])

while not results.empty():
    print results.get_nowait()
