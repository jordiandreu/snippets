# coding=utf-8
import sys
from PyQt4.QtGui import QLabel, QPixmap, QApplication, QWidget

from pkg_resources import Requirement, resource_filename


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
    image = resource_filename(Requirement.parse("setuptools_resource_example_pkg"), "mypkg/resources/alba-logo.png")
    pixmap = QPixmap(image)
    label.setPixmap(pixmap)
    w.resize(pixmap.width(), pixmap.height())
    # Draw window
    w.show()
    sys.exit(app.exec_())
