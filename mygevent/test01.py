import gevent
import signal

# Testing the gevent and greenlet basic functions

def foo(n):
    for i in range(n):
        gevent.sleep(1)
        print '[foo %s] counter is %s' % (n,i+1)
    return 'foo finished'


def fail():
    raise Exception('Failing at Fail')


def demo0():
    thread01 = Greenlet.spawn(foo, 10)
    thread01.start()
    thread02 = gevent.spawn(foo, 4)
    thread02.start()
    gevent.joinall([thread01, thread02])
    print 'done!'


def demo1():
    thread01 = gevent.spawn(foo, 10)
    thread02 = gevent.spawn(foo, 4)
    gevent.joinall([thread01, thread02])
    print 'done!'


from gevent import Greenlet

class MyGreenlet(Greenlet):
    def __init__(self, name, n):
        Greenlet.__init__(self)
        self.name = name
        self.n = n

    def _run(self):
        for i in range(self.n):
            gevent.sleep(1)
            print '[%s] counter is %s' % (self.name, i + 1)

        return "greenlet finished"


def demo2():
    g = MyGreenlet('greenlet foo', 10)
    b = MyGreenlet('greenlet bar', 4)
    g.start()
    b.start()
    print 'started'
    g.join()
    print 'g ended'
    b.join()
    print 'all ended'


def demo3():
    g = MyGreenlet('greenlet foo', 10)
    b = MyGreenlet('greenlet bar', 4)
    g.start()
    b.start()
    print 'started'
    g.join()
    print 'g ended'
    b.join()
    print 'all ended'


def demo4():
    g = MyGreenlet('greenlet foo', 10)
    g.start()
    print 'started and sleeping for 5 seconds'
    gevent.sleep(5)
    print 'awakening!'
    g.join()
    g.value
    print 'g ended'

# Greenlet States

def demo5():
    f = gevent.spawn(foo, 10)
#    e = gevent.spawn(fail)

    print 'f started = %s' % f.started
#    print 'e started = %s' % e.started

    print 'sleeping...'
    gevent.sleep(6)

    print 'foo ready = %s' % f.ready()
    print 'foo successful = %s' % f.successful()
    print 'foo value = %s' % f.value

    print 'continue sleeping...'
    gevent.sleep(6)

    print 'foo ready = %s' % f.ready()
    print 'foo successful = %s' % f.successful()
    print 'foo value = %s' % f.value

def demo6():

    # provide program shutdown (avoid ZOMBIE processes)
    gevent.signal(signal.SIGQUIT, gevent.kill)

    f = gevent.spawn(foo, 10)

    print 'f started = %s' % f.started
    print 'sleeping...'
    while not f.ready():

        gevent.sleep(1)
    print 'awakening!'
    print '##########################'
    print 'foo ready = %s' % f.ready()
    print 'foo successful = %s' % f.successful()
    print 'foo value = %s' % f.value



#demo0()
#demo1()
#demo2()
#demo3()
#demo4()
#demo5()
demo6()