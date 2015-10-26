import sys
from PyQt4.QtCore import *
 
class MyEmitter(QObject):
    def __init__(self):
        QObject.__init__(self)
 
    def femit(self):
        self.emit(SIGNAL("signal()"))

    def femitint(self, value):
        self.emit(SIGNAL("signalint(int)"), value)

    def femitpyobj(self, value):
        self.emit(SIGNAL("signalpyobj(PyQt_PyObject)"), value)

    def fslot(self):
        print "Hello world from my class."

    def fslotint(self, value):
        print "Hello World with value %s from my class" % value

    def fslotpyobj(self, value):
        print "Hello World with object value %s from my class" % repr(value)


def fslot():
    print "Hello World from global."

def fslotint(value):
    print "Hello World with value %s from global." % value

def fslotpyobj(value):
    print "Hello World with object value %s from global" % value


if __name__=="__main__":
    #app = QCoreApplication(sys.argv)
    obj = MyEmitter()

    # Old style
    QObject.connect(obj, SIGNAL("signal()"), fslot)
    QObject.connect(obj, SIGNAL("signal()"), obj.fslot)
    QObject.connect(obj, SIGNAL("signalint(int)"), fslotint)
    QObject.connect(obj, SIGNAL("signalint(int)"), obj.fslotint)
    QObject.connect(obj, SIGNAL("signalpyobj(PyQt_PyObject)"), fslotpyobj)
    QObject.connect(obj, SIGNAL("signalpyobj(PyQt_PyObject)"), obj.fslotpyobj)

    # New style
    obj.femit()
    obj.femitint(int(5))
    obj.femitpyobj(list([1,2,3]))

    #sys.exit(app.exec_())