# coding=utf-8
import cv2
import numpy as np
import logging


class YUV(object):
    def __init__(self, w, h, packed=None):
        self.w = w
        self.h = h
        self.y_size = None
        self.u_size = None
        self.v_size = None
        self.u_offset = None
        self.v_offset = None
        self.uv0 = None
        self.uv1 = None
        self.packed = packed

    def extract(self, buffer):
        # Load the Y (luminance) data from the stream.
        # Load the UV (chrominance) data from the stream, and adjust size.
        if self.packed:
            frame = np.frombuffer(buffer, dtype=np.uint8)
            Y = frame[1:self.y_size*2:2].reshape(self.h, self.w)
            U = frame[0:self.y_size*2:4].repeat(self.uv1, axis=0).reshape(self.h, self.w)
            V = frame[2:self.y_size*2:4].repeat(self.uv1, axis=0).reshape(self.h, self.w)
        else:
            Y = np.frombuffer(buffer, dtype=np.uint8, count=self.y_size, offset=0).reshape(
                (self.h, self.w))
            U = np.frombuffer(buffer, dtype=np.uint8, count=self.u_size, offset=self.u_offset).reshape(
                (self.h/self.uv0, self.w/self.uv1)).repeat(self.uv0, axis=0).repeat(self.uv1, axis=1)
            V = np.frombuffer(buffer, dtype=np.uint8, count=self.v_size, offset=self.v_offset).reshape(
                (self.h/self.uv0, self.w/self.uv1)).repeat(self.uv0, axis=0).repeat(self.uv1, axis=1)
        return Y, U, V


    def stack(self, Y, U, V):
        # Stack the YUV channels together, crop the actual resolution, convert to
        # floating point for later calculations, and apply the standard biases
        YUV = np.dstack((Y, U, V))[:self.h, :self.w, :].astype(np.float)
        YUV[:, :, 0] = YUV[:, :, 0] - 16  # Offset Y by 16
        YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
        return YUV


class YUV420(YUV):
    def __init__(self, *args, **kwargs):
        YUV.__init__(self, *args, **kwargs)
        self.y_size = self.w * self.h
        self.u_size = self.w * self.h / 4
        self.v_size = self.u_size
        self.u_offset = self.y_size
        self.v_offset = self.u_offset + self.u_size
        self.uv0 = 2
        self.uv1 = 2


class YUV422(YUV):
    def __init__(self, *args, **kwargs):
        YUV.__init__(self, *args, **kwargs)
        self.y_size = self.w * self.h
        self.u_size = self.w * self.h / 2
        self.v_size = self.u_size
        self.u_offset = self.y_size
        self.v_offset = self.u_offset + self.u_size
        self.uv0 = 1
        self.uv1 = 2


class YUV444(YUV):
    def __init__(self, *args, **kwargs):
        YUV.__init__(self, *args, **kwargs)
        self.y_size = self.w * self.h
        self.u_size = self.y_size
        self.v_size = self.y_size
        self.u_offset = self.y_size
        self.v_offset = self.u_offset + self.u_size
        self.uv0 = 1
        self.uv1 = 1


def get_decoder(src, dst):
    # Initializes codec
    # Extract data and pack as matrix
    # Conversion to RGB

    # YUV conversion matrix from ITU-R BT.601 version (SDTV)
    # Note the swapped R and B planes!

    #              Y       U       V
    M_BGR = np.array([[1.164,  2.017,  0.000],    # B
                      [1.164, -0.392, -0.813],    # G
                      [1.164,  0.000,  1.596]])   # R

    #              Y       U       V
    M_RGB = np.array([[1.164, 0.000, 1.596],      # R
                      [1.164, -0.392, -0.813],    # G
                      [1.164, 2.017, 0.000]])     # B

    def YUV420toRGB(buffer, width, height):
        codec = YUV420(width, height)
        Y, U, V = codec.extract(buffer)
        YUV = codec.stack(Y, U, V)
        return YUV.dot(M_RGB.T).clip(0, 255).astype(np.uint8)

    def YUV420toBGR(buffer, width, height):
        codec = YUV420(width, height)
        Y, U, V = codec.extract(buffer)
        YUV = codec.stack(Y, U, V)
        return YUV.dot(M_BGR.T).clip(0, 255).astype(np.uint8)

    def YUV422toRGB(buffer, width, height):
        codec = YUV422(width, height)
        Y, U, V = codec.extract(buffer)
        YUV = codec.stack(Y, U, V)
        return YUV.dot(M_RGB.T).clip(0, 255).astype(np.uint8)

    def YUV422toBGR(buffer, width, height):
        codec = YUV422(width, height)
        Y, U, V = codec.extract(buffer)
        YUV = codec.stack(Y, U, V)
        return YUV.dot(M_BGR.T).clip(0, 255).astype(np.uint8)

    def YUV422ptoRGB(buffer, width, height):
        codec = YUV422(width, height, packed=True)
        Y, U, V = codec.extract(buffer)
        YUV = codec.stack(Y, U, V)
        return YUV.dot(M_RGB.T).clip(0, 255).astype(np.uint8)

    def YUV422ptoBGR(buffer, width, height):
        codec = YUV422(width, height, packed=True)
        Y, U, V = codec.extract(buffer)
        YUV = codec.stack(Y, U, V)
        return YUV.dot(M_BGR.T).clip(0, 255).astype(np.uint8)

    def YUV444toRGB(buffer, width, height):
        codec = YUV444(width, height)
        Y, U, V = codec.extract(buffer)
        YUV = codec.stack(Y, U, V)
        return YUV.dot(M_RGB.T).clip(0, 255).astype(np.uint8)

    def YUV444toBGR(buffer, width, height):
        codec = YUV444(width, height)
        Y, U, V = codec.extract(buffer)
        YUV = codec.stack(Y, U, V)
        return YUV.dot(M_BGR.T).clip(0, 255).astype(np.uint8)

    if src == 'YUV444':
        if dst is 'BGR':
            return YUV444toBGR
        elif dst is 'RGB':
            return YUV444toRGB
        else:
            logging.Logger().error('Invalid dst encoding value.')
    elif src == 'YUV422':
        if dst is 'BGR':
            return YUV422toBGR
        elif dst is 'RGB':
            return YUV422toRGB
        else:
            logging.Logger().error('Invalid dst encoding value.')
    elif src == 'YUV422p':
        if dst is 'BGR':
            return YUV422ptoBGR
        elif dst is 'RGB':
            return YUV422ptoRGB
        else:
            logging.Logger().error('Invalid dst encoding value.')
    elif src == 'YUV420':
        if dst is 'BGR':
            return YUV420toBGR
        elif dst is 'RGB':
            return YUV420toRGB
        else:
            logging.Logger().error('Invalid dst encoding value.')
    else:
        logging.Logger().error('Invalid src encoding value.')


################################################################################
#https://wiki.videolan.org/YUV/
#http://raspberrypi.stackexchange.com/questions/28033/reading-frames-of-uncompressed-yuv-video-file
#http://www.sunrayimage.com/examples.html
################################################################################

if __name__ == "__main__":
    import sys
    import argparse
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from itertools import cycle

    class PixmapWidget(QtGui.QWidget):

        def __init__(self, width, height):
            super(PixmapWidget, self).__init__()
            self.width = width
            self.height = height
            self.ctimer = QtCore.QTimer()
            QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.update_image)
            self.ctimer.start(1000)
            self.image_iter = cycle_iterator()
            self.pixmap = None
            self.init()

        def init(self):

            image, src, dst = self.image_iter.next()
            qimage = QtGui.QImage(image, self.width, self.height,
                                  self.width * 3, QtGui.QImage.Format_RGB888)
            self.pixmap = QtGui.QPixmap(qimage)
            self.graph = QtGui.QGraphicsScene()
            self.pixmap_item = self.graph.addPixmap(self.pixmap)
            self.view = QtGui.QGraphicsView(self.graph)
            self.view.setWindowTitle('%s/%s' % (src, dst))
            self.view.fitInView(QtCore.QRectF(0, 0, self.width, self.height),
                                QtCore.Qt.KeepAspectRatio)
            self.view.show()

        def update_image(self):
            image, src, dst = self.image_iter.next()
            qimage = QtGui.QImage(image, self.width, self.height, self.width * 3, QtGui.QImage.Format_RGB888)
            self.view.setWindowTitle('%s/%s' % (src, dst))
            self.pixmap = QtGui.QPixmap(qimage)
            self.pixmap_item.setPixmap(self.pixmap)


    def all_image_generator():
        width = 176
        height = 144
        file_420p = 'images/tulips_yuv420_prog_planar_qcif.yuv'
        file_422p = 'images/tulips_yuv422_prog_planar_qcif.yuv'
        file_444p = 'images/tulips_yuv444_prog_planar_qcif.yuv'
        file_422pp = 'images/tulips_uyvy422_prog_packed_qcif.yuv'

        files = [file_420p, file_422p, file_444p, file_422pp]
        srcs = ['YUV420', 'YUV422', 'YUV444', 'YUV422p']
        dsts = ['RGB', 'BGR']

        for fn, src in zip(files, srcs):
            for dst in dsts:
                f = open(fn, 'rb')
                frame = np.fromfile(f, dtype=np.uint8)
                decoder=get_decoder(src, dst)
                image = decoder(frame, width, height)
                f.close()
                print "%s, %s, %s" % (fn, src, dst)
                yield image, src, dst


    def image_generator():
        width = 176
        height = 144
        file_420p = 'images/tulips_yuv420_prog_planar_qcif.yuv'
        file_422p = 'images/tulips_yuv422_prog_planar_qcif.yuv'
        file_444p = 'images/tulips_yuv444_prog_planar_qcif.yuv'
        file_422pp = 'images/tulips_uyvy422_prog_packed_qcif.yuv'

        files = [file_422pp]
        srcs = ['YUV422p']
        dsts = ['RGB', 'BGR']

        import cv2

        for fn, src in zip(files, srcs):
            for dst in dsts:
                f = open(fn, 'rb')
                frame = np.fromfile(f, dtype=np.uint8)
                # USING OPENCV ENGINE!
                frame.resize(height, width, 2)
                image = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_UYVY)
                f.close()
                print "%s, %s, %s" % (fn, src, dst)
                yield image, src, dst
    def cycle_iterator():
        g = image_generator()
        for i in cycle(g):
            print "next image delivered!"
            yield i

    def opencv_display():
        # Display the image with OpenCV
        g = image_generator()
        #g = cycle_iterator()
        try:
            while True:
                image, src, dst  = g.next()
                cv2.imshow("%s/%s" % (src, dst), image)
                cv2.waitKey(0)
        except StopIteration:
            pass

    def qtgui_display():
        app = QtGui.QApplication(sys.argv)
        ww = PixmapWidget(176, 144)
        sys.exit(app.exec_())


################################################################################
    parser = argparse.ArgumentParser()
    parser.add_argument('viewer', type=str, choices=['qt', 'cv'], help='Visualization engine')
    args = parser.parse_args()

    if args.viewer == 'qt':
        qtgui_display()
    elif args.viewer == 'cv':
        opencv_display()
    else:
        print "Invalid viewer, use --help to see options."
