from PyQt4 import QtCore
from PyQt4 import QtGui
from Lima import Core
from Lima import Basler


class BaslerCamera(object):

    def __init__(self, ip_str):
        self.ip = ip_str
        #self.filename = None

        self.camera = None
        self.interface = None
        self.control = None
        self.video = None

        self.width = None
        self.height = None

        self.sensor_width = None
        self.sensor_height = None

        self.init()


    def init(self):
        self.camera = Basler.Camera(self.ip)
        self.height = self.camera.getRoi().getSize().getHeight()
        self.width = self.camera.getRoi().getSize().getWidth()

#        roi = camera.getRoi() <244,184>-<900x670>
#        size = roi.getSize() <900x670>
#        height = size.getHeight() 670
#        width = size.getWidth() 900

#        camera.getDetectorImageSize() <1390x1038>
        self.sensor_width = self.camera.getDetectorImageSize().getWidth()
        self.sensor_height = self.camera.getDetectorImageSize().getHeight()

        print 'sensor size = %s' % (self.sensor_width * self.sensor_height)
        print 'frame size (AOI) = %s' % (self.width * self.height)


    def prepare(self, video_mode):
        self.interface = Basler.Interface(self.camera)
        self.control = Core.CtControl(self.interface)
        self.video = self.control.video()

        # See Lima enum for video modes available for each camera
        # YUV422 = 16
        # Y8 = 0
        if video_mode == 'Y8':
            m = 0
        elif video_mode == 'YUV422':
            m = 16
        else:
            raise Exception('Invalid video mode!')

        self.video.setMode(m)
        self.video.startLive()

    def get_image_from_file(self, filename='test.png'):
        #self.filename = filename
        qimage = QtGui.QPixmap(filename)
        return qimage


    def get_new_image(self):
        import time
        image = self.video.getLastImage()
        while image.frameNumber() == -1:
            image = self.video.getLastImage()
            time.sleep(1)

        if image.frameNumber() > -1:
            raw_buffer = image.buffer()
            rgb = self.Y8toRGB888(raw_buffer)
            print image.width(), image.height()
            print rgb.size
            qimage = QtGui.QImage(rgb, image.width(), image.height(), QtGui.QImage.Format_RGB888)

            #import numpy as np
            #y8 = np.fromstring(raw_buffer, dtype=np.uint16)
            #y8.resize(self.height, self.width, 1)
            #qimage = QtGui.QImage(y8, image.width(), image.height(), QtGui.QImage.Format_MonoLSB)
            #qimage = QtGui.QImage(rgb_buffer, image.width(), image.height(), image.width()*3, QtGui.QImage.Format_RGB888)



            #if self.cam_mirror is not None:
            #    qimage = qimage.mirrored(self.cam_mirror[0], self.cam_mirror[1])

            #qpixmap = QtGui.QPixmap(qimage)
            #self.emit("imageReceived", qpixmap)
            #return qimage

            qpixmap = QtGui.QPixmap(qimage)
            return qpixmap

    def Y8toRGB888(self, raw_buffer):
        import cv2
        import numpy as np
        y8 = np.fromstring(raw_buffer, dtype=np.uint8)
        y8.resize(self.height, self.width, 1)
        rgb888 = cv2.cvtColor(y8, cv2.COLOR_GRAY2RGB)
        #cv2.imshow('Y8 format', y8)
        #cv2.waitKey()
        return rgb888

    def save_snapshot(self, image_type='PNG'):
        qimage = self.get_new_image()
        qimage.save('image.png', image_type)



def YUV422toRGB888(raw_buffer):
    import cv2
    import numpy as np
    print "input buffer type is %s" % type(raw_buffer)
    raw_image = np.fromstring(raw_buffer, dtype=np.uint8)
    print "raw image type is %s, size = %s" % (type(raw_image), raw_image.size)
    raw_image.resize(670, 900, 1)
#    raw_image.resize(670, 900, 3)
    yuv = raw_image
    print yuv
    cv2.imshow('YUV', yuv)
    cv2.waitKey()

#    rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
#    print rgb
#    cv2.imshow('rgb', rgb)
#    cv2.waitKey()


    #print "yuv buffer type is %s" % type(img_yuv)
    #img = cv2.cvtColor(array, cv2.COLOR_YUV2BGR)
    #print "output buffer type is %s" % type(img)

    yuv = cv2.cvtColor(raw_image, cv2.COLOR_GRAY2RGB)

    img = yuv
    return img


class PixmapWidget(QtGui.QWidget):

    def __init__(self, ip, filename=None):
        super(PixmapWidget, self).__init__()

        self.camera = BaslerCamera(ip)
        self.camera.prepare('Y8')

        if filename:
            # create a QPixmap from image file:
            self.pixmap = self.camera.get_image_from_file(filename)
        else:
            self.pixmap = self.camera.get_new_image()
            self.camera.save_snapshot()
        #import time
        #time.sleep(5)
        width = self.camera.width
        height = self.camera.height
        self.graph = QtGui.QGraphicsScene(0, 0, width, height)
        self.graph.addPixmap(self.pixmap)
        #self.graph.addPixmap(self.camera.get_new_image())
        self.view = QtGui.QGraphicsView(self.graph)
        self.view.fitInView(QtCore.QRectF(0, 0, width, height), QtCore.Qt.KeepAspectRatio)
        self.view.show()

# Need to be tested
#    def addIMage(self, pixmap):
#        self.graph.addPixmap(pixmap)
#        #self.view = QtGui.QGraphicsView(self.graph)
#        self.view.show()

if __name__ == "__main__":

    import sys
    app = QtGui.QApplication(sys.argv)
    w = PixmapWidget("84.89.227.6") # ccd110-bl13
    #w = PixmapWidget("10.0.35.10")  # ccd110
    #w = PixmapWidget("84.89.227.72")  # bl13 oav
    sys.exit(app.exec_())
