
def make_f():
    def f():
        print 'This is function f'
    return f

def g():
    print 'This is function g'


def o():
    print "This function overrides!"


class DynamicContainer(object):

    def __init__(self, f, g):
        self.foo = f
        self.goo = g

    def f(self):
        print "This is member function f"

A = DynamicContainer('hello','bye')

setattr(A, "I_say_%s" % A.foo, A.f)
setattr(A, A.foo, make_f())
setattr(A, A.goo, g)

A.hello()
A.bye()
A.I_say_hello()

A.f=o
A.I_say_hello()




