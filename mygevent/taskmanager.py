import gevent
from gevent.queue import Queue
import logging

import subprocess
from subprocess import Popen, PIPE, STDOUT

TASKS_AT_START = 10


fmt = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(format=fmt)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)


def push_event(id):
    return 'PUSHING EVENT, TASK %s ENDED' % id

class TaskManager(object):
    """
    Main class that encloses the mechanisms to process a dynamic set of
    subprocesses.
    """
    def __init__(self, concurrent):
        logger = logging.getLogger(__name__)
        logger.debug('initializing task manager')
        self._tasks = Queue()
        self._results = Queue()
        self.dispatcher = Dispatcher(self._tasks, self._results, concurrent,
                                     ext_cb=push_event)
        self.g_dispatcher = None
        self.scheduler = Scheduler(self._tasks)
        self.g_scheduler = None
        self.g_tm = None
        self.tasks_pending = None
        self.tasks_done = None

    def start(self):
        logger.debug('starting task manager')
        self.g_tm = gevent.spawn(self._start)

    def stop(self):
        logger.debug('stopping task manager')
        # TODO: review the sleep. Without, the call start/stop fails
        gevent.sleep(3)
        self.scheduler.stop()
        self.dispatcher.stop()
        self.g_tm.join()
        self.tasks_pending = self.get_tasks_pending()
        self.tasks_done = self.get_tasks_done()

    def _start(self):
        logger.debug('starting dispatcher')
        self.g_dispatcher = gevent.spawn(self.dispatcher.run)
        self.g_dispatcher.link(self._d_cb)

        self.g_dispatcher.join()

        while self.scheduler.state:
            logger.debug('scheduler state is %s' % self.scheduler.state)
            gevent.sleep(1)

        total_tasks = self.g_dispatcher.value
        gevent.joinall(total_tasks)

    def get_tasks_done(self):
        logger.debug('creating list of tasks done')
        return self._list(self._results)

    def get_tasks_pending(self):
        logger.debug('creating list of tasks pending')
        return self._list(self._tasks)

    def _d_cb(self, g):
        logger.debug('dispatcher callback')
        logger.debug('%s running tasks' % len(self.dispatcher.run_tasks))
        logger.debug('%s ended tasks' % len(self.dispatcher.end_tasks))

    def _list(self, q):
        _l = []
        while not q.empty():
            _l.append(q.get())
        return _l

    def summary(self):
        print 80*'#' + '\ntasks done:'
        self._show(self.tasks_done)
        print 80 * '#' + '\ntasks pending:'
        self._show(self.tasks_pending)

    def _show(self, l):
        for x in l:
            print repr(x)

class Dispatcher(object):
    """
    This class is the one in charge to schedule/launch the tasks queued.
    It also tracks the status of the tasks
    """
    def __init__(self, tasks, results, concurrent, ext_cb=None):

        logger.debug('initializing dispatcher')
        self.concurrent = concurrent
        self.tasks = tasks
        self.results = results
        self.state = True
        self.run_task = []

        self.run_tasks = []
        self.end_tasks = []

        self.ext_cb = ext_cb

    def run(self):
        while self.state:

            while not self.tasks.empty():

                logger.debug('%s tasks in queue' % self.tasks.qsize())

                if len(self.run_tasks) < self.concurrent:
                    task= self.tasks.get()
                    g = gevent.Greenlet(self._task, task)
                    self.run_tasks.append(g)
                    g.link(self._task_cb)
                    g.start()
                    logger.debug('starting task %s' % task.id)
                else:
                    # MANDATORY: we need to let the other process to run
                    # The time determines how often the worker check for
                    # new job in the tasks queue.
                    gevent.sleep(0.5)
            self.state = False
        logger.info('Queue empty, dispatcher is going down!')
        return self.end_tasks + self.run_tasks

    def _task(self, task):
        logger.info('task %s is being executed' % task.id)
        # TODO: implement here the function being executed as a task
        #gevent.sleep(2)
        task._run()
        self.results.put(task)
        return task

    def _task_cb(self, g):
        id = g.value.id
        success = g.value.success
        logger.debug('callback: job %s finished with status %s' % (id, success))
        self.end_tasks.append(g)
        self.run_tasks.remove(g)
        if self.ext_cb:
            logger.info(self.ext_cb(id))

    def stop(self):
        self.state = False


class Scheduler(object):
    def __init__(self, tasks):
        self.tasks = tasks
        self.new_task = None
        self.state = True
        self.ntasks = 0

#    def run(self):
#
#        while self.state:
#            if self.new_task:
#                self.addtask('auto')
#            else:
#                # This time determines how often the scheduler is trying to add
#                # a new task to the TaskManager tasks queue .
#                gevent.sleep(1)

    def stop(self):
        self.state = False

    def addtask(self, cmd):

        logger.debug('trying to add task %s with state %s' % (cmd, self.state))
        if self.state:
            if isinstance(cmd, str):
                task = SubprocessTask(cmd)
                task.id = self.ntasks +1
                self.tasks.put(task)
                self.ntasks += 1
                logger.info('New task %s added (%s total)' % (task.id, self.ntasks))
            else:
                logger.error('%s is not a valid string' % repr(cmd))
        else:
            logger.warning('scheduler is not accepting tasks, request on task '
                           '%s skipped.' % repr(cmd))


class SubprocessTask(object):
    def __init__(self, cmd):
        self.id = None
        self.cmd = cmd
        self.result = None
        self.success = None

    def run(self):

        process = subprocess.Popen(self.cmd, shell=True, stdout=PIPE)
        process.wait()
        data, err = process.communicate()
        print data
        self.result = data
        self.success = err
        return self.id, self.success, self.result

    def __repr__(self):
        return 'id: %s\t success: %s\t result: %s' % (self.id, self.success,
                                                      self.result)


def cmd_local():
    return 'ls -l'


def cmd_remote():
    host = 'opbl13@pcbl1305'
    cmd = 'ls -l'
    rem_cmd = 'ssh %s \"%s\"' % (host, cmd)
    return rem_cmd


def test01():
    tm = TaskManager(2)

    for i in range(10):
        tm.scheduler.addtask('command%s' % (i+1))

    tm.start()
    tm.stop()
    tm.summary()


def test02():
    tm = TaskManager(5)

    for i in range(10):
        tm.scheduler.addtask('command%s' % (i+1))

    tm.start()

    for i in range(10):
        tm.scheduler.addtask('command%s' % (i+10))
        gevent.sleep(1)
    tm.stop()
    tm.summary()


def test03():
    tm = TaskManager(2)

    for i in range(5):
        tm.scheduler.addtask(cmd_local())

    for i in range(5):
        tm.scheduler.addtask(cmd_remote())

    tm.start()

    # for i in range(10):
    #     tm.scheduler.addtask(cmd_local())
    #     gevent.sleep(.2)

    tm.stop()
    tm.summary()


if __name__ == "__main__":

    test03()

