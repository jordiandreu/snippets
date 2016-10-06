from taurus.external.qt import QtGui, QtCore
import sys
import logging


class XStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    messageWritten = QtCore.pyqtSignal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.messageWritten.emit(unicode(msg))

    @staticmethod
    def stdout():
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


class IDLabLogDialog(QtGui.QDialog):
    def __init__(self, add_handler_f):
        QtGui.QDialog.__init__(self)
        self.add_handler(add_handler_f)
        self.setWindowTitle('IDLab Log View')
        self._console = QtGui.QTextBrowser(self)
        self._btn_close = QtGui.QPushButton("Close", self)
        self._btn_close.setEnabled(False)

        self.create_layout()
        self.create_connects()
        self.setModal(True)
        self.show()

    def create_layout(self):
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self._console)
        layout.addWidget(self._btn_close)
        self.setGeometry(200, 200, 900, 300)

    def add_msg(self, msg):
        self._console.insertPlainText(msg)
        if msg.find('[done]') != -1:
            self._btn_close.setEnabled(True)

    def create_connects(self):
        self._btn_close.clicked.connect(self.done)
        XStream.stderr().messageWritten.connect(self.add_msg)
        XStream.stdout().messageWritten.connect(self.add_msg)

    def add_handler(self, f):
        class QtHandler(logging.Handler):
            def __init__(self):
                logging.Handler.__init__(self)

            def emit(self, record):
                record = self.format(record)
                if record:
                    XStream.stdout().write('%s\n' % record)

        handler = QtHandler()
        f(handler)


if __name__ == '__main__':
    from taurus.core.util.log import Logger
    import logging


    #   import taurus
    #   taurus.setLogLevel(taurus.Debug)

    class TestWidget(QtGui.QWidget):
        def __init__(self):
            QtGui.QWidget.__init__(self)
            #           self.logger = Logger('MyTaurusLogger')
            #           self.add_handler_f = self.logger.addRootLogHandler
            self.logger = logging.getLogger('MyLogger')
            self.add_handler_f = self.logger.addHandler

            self.logger.info("__init__()")

            self.setGeometry(100, 100, 200, 50)
            self.setWindowTitle('TestWidget')
            self.btn = QtGui.QPushButton(self)
            self.btn.setText('open log widget')
            self.log = None
            layout = QtGui.QVBoxLayout(self)
            layout.addWidget(self.btn)

            self.btn.clicked.connect(self.show_log)

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.print_msg)
            self.timer.start(1000)

            self.timer2 = QtCore.QTimer()
            self.timer2.timeout.connect(self.print_done)
            self.timer2.start(5000)

        def print_msg(self):
            self.logger.info('info message')

        def print_done(self):
            self.logger.info('[done]')

        def show_log(self):
            self.log = IDLabLogDialog(self.add_handler_f)


    def main():
        app = QtGui.QApplication(sys.argv)
        w = TestWidget()
        w.show()
        sys.exit(app.exec_())


    main()
