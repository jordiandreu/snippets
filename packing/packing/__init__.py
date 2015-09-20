__all__=['fooA','ClassA']

def fooA():
    print 'foo A'

def fooB():
    print 'foo B'

class ClassA:
    def __init__(self):
        print 'instance class A'

class ClassB:
    def __init__(self):
        print 'instance class B'

if __name__ == '__main__':
    print 'testing module'
    fooA()
    A = ClassA()
    fooB()
    B = ClassB()

    AB = ClassAB()

    A()
    B()

#    ClassA().display()
#    ClassB().display()

#    A
#    print A

