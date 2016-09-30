import gevent
from gevent.queue import Queue
from gevent import getcurrent
from random import randint

TASKS_AT_START = 10
MAX_TREADS = 2

tasks = Queue()
results = Queue()
run_tasks = []
end_tasks = []


def boss_cb(g):
    print 'boss callback'


def worker_cb(g):
    print 'worker callback'


def job_cb(g):
    id = g.value[0]
    status = g.value[1]
    end_tasks.append(g)
    run_tasks.remove(g)
    print 'callback: job %s finished with status %s' % (id, status)


def job(worker_name, task_id):
    print 'Task %s is being executed by %s' % (task_id, worker_name)
    gevent.sleep(2)
    results.put((task_id, worker_name))
    status = True
    return task_id, status


def worker(name):
    while not g2.ready():

        while not tasks.empty():

            print 'tasks in queue: %s (empty = %s)' % (tasks.qsize(), tasks.empty())
            print 'boss is scheduling = %s' % (not g2.ready())

            if len(run_tasks) < MAX_TREADS:
                task_id = tasks.get()
                g = gevent.Greenlet(job, name, task_id)
                run_tasks.append(g)
                g.link(job_cb)
                g.start()
                print 'Starting task %s' % task_id
            else:
                # MANDATORY: we need to let the other process to run
                # The time determines how often the worker check for
                # new job in the tasks queue.
                gevent.sleep(0.5)

        print 'Queue empty, %s is going home!' % name


def init():
    for i in range(TASKS_AT_START):
        tasks.put_nowait(i+1)

i = gevent.spawn(init)
i.join()


def boss(extra_tasks):
    gevent.sleep(3)
    c=1
    while c <= extra_tasks:
        r = randint(0, 1)
        if r == 0:
            task_id = TASKS_AT_START + c
            tasks.put(task_id)
            print 'New task %s added (%s total)' % (task_id, tasks.qsize())
            c += 1
        # MANDATORY: we need to let the other process to run
        # This time determines how often the boss is trying to add a new task
        # to the tasks queue.
        gevent.sleep(1)
    return False


g2 = gevent.spawn(boss, 5)
g2.link(boss_cb)
j = gevent.spawn(worker, 'john')
j.link(worker_cb)

#####################
# Place here any code
#gevent.sleep(5)
#print 'awakening'
#####################

j.join()
gevent.joinall(end_tasks + run_tasks)
g2.join()

print 'rtasks size at end is %s' % len(run_tasks)
print 'ftasks size at end is %s' % len(end_tasks)

while not results.empty():
    print results.get_nowait()
