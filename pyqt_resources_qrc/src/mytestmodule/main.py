# coding=utf-8
import sys
from PyQt4.QtGui import QLabel, QPixmap, QApplication, QWidget
# DO NOT REMOVE: mandatory even not used explicitly
from resources import resources_rc


def show():
    """
    Simple function to show how to load an image from a resource file and
    add it to a widget.
    @return:
    """
    # Create window
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("PyQT4")
    # Create widget
    label = QLabel(w)
    image = ':/alba-logo.png'
    pixmap = QPixmap(image)
    label.setPixmap(pixmap)
    w.resize(pixmap.width(), pixmap.height())
    # Draw window
    w.show()
    sys.exit(app.exec_())
