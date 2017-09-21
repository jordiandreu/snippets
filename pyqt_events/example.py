
from PyQt4 import Qt, QtCore, QtGui

class MyLineEdit(QtGui.QLineEdit):

    def __init__(self, *args):

        QtGui.QLineEdit.__init__(self,*args)

        self.last_value = "<value>"
        self.setStyleSheet("background-color: #aaa;")
        self.setText(self.last_value)

    def mousePressEvent(self,ev):
        self.last_value = self.text()
        self.setStyleSheet("background-color: #fff;")
        self.setText("")

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
           print "Key pressed", e.key()
           self.checkRestore()

        QtGui.QLineEdit.keyPressEvent(self, e)
    
    def focusOutEvent(self, ev):
        self.checkRestore()
        QtGui.QLineEdit.focusOutEvent(self, ev)

    def checkRestore(self):
        if str( self.text() ) == "":
            self.setText(self.last_value)
        self.setStyleSheet("background-color: #aaa;")

app = QtGui.QApplication([])
win = QtGui.QMainWindow()
but = MyLineEdit()
win.setCentralWidget(but)
win.show()
app.exec_()

