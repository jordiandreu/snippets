# coding=utf-8
from taurus import Attribute
from taurus.core import TaurusEventType

class Listener(object):

#    __pyqtSignals__ = ["onStateChanged"]

    def eventReceived(self, evt_src, evt_type, evt_value):
        if evt_type in (TaurusEventType.Change,):
#            logging.Logger().debug("Signal TaurusEventType.Change received")
            name = evt_value.name
            value = evt_value.value
            if value != []:
                print value
#                self.emit(Qt.SIGNAL("onStateChanged"), name, value)
#                logging.Logger().debug("Signal onStateChanged emitted, name = %s, "
#                             "value = %s received", name, value)


def main():
    attr_name = 'lab/el/acA1300-01-limaccds'
    listener = Listener()
    attr = Attribute(attr_name)
    attr.addListener(listener)
    import time
    while True:
        time.sleep(1)
