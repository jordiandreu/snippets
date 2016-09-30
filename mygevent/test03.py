import gevent
from gevent import Greenlet


def cb():
    print 'FOOOOOOOOOO'


def foo():
    print 'foo'
    return 'foooooo'


g = Greenlet.spawn(foo)
g.link(cb)
print g.successful()
g.join()
print g.successful()
