from PyQt4 import QtGui, Qt, QtCore
from PyQt4.QtCore import QThread, SIGNAL, pyqtSignal
import sys
import time


class MyWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setGeometry(100, 100, 200, 50)
        self.setWindowTitle('PyQt')
        self.btn = QtGui.QPushButton(self)
        self.btn.setText('push')
        self.log = None
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.btn)

        self.btn.clicked.connect(self.show_log)

        self.emitter = Emitter()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.emitter.emit_message)
        self.timer.start(1000)

    def show_log(self):
        self.log = MyLogView()
        self.emitter.on_signal_emitted.connect(self.log.write_log)


class MyLogView(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setGeometry(100, 100, 200, 50)
        self.setWindowTitle('LogView')
        self.text = QtGui.QTextEdit(self)
        self.text.setText('Init the log')
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.text)
        self.setModal(True)
        self.show()
        #self.exec_()

    def write_log(self, msg):
        self.text.append(str(msg))


class Emitter(Qt.QObject):

    on_signal_emitted = pyqtSignal(str, name='OnSignalEmitted')

    def __init__(self):
        Qt.QObject.__init__(self)

    def emit_message(self):
        msg = time.ctime()
        print str(msg)
        self.on_signal_emitted.emit(str(msg))



def window():
   app = QtGui.QApplication(sys.argv)
   w = MyWidget()
   w.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()