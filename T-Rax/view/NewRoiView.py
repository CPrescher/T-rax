# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg


class NewRoiView(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(NewRoiView, self).__init__(*args, **kwargs)

        self._main_horizontal_layout = QtGui.QHBoxLayout()
        self._limits_layout = QtGui.QVBoxLayout()

        self._main_horizontal_layout.addWidget(QtGui.QWidget())# placeholder for image view

        self.img_widget = ImageWidget()

        self.us_roi_gb = RoiGroupBox('Upstream ROI')
        self.ds_roi_gb = RoiGroupBox('Downstream ROI')
        self._limits_layout.addWidget(self.us_roi_gb)
        self._limits_layout.addWidget(self.ds_roi_gb)
        self._limits_layout.addSpacerItem(QtGui.QSpacerItem(20,20,
                                                            QtGui.QSizePolicy.Expanding,
                                                            QtGui.QSizePolicy.Expanding))

        self._main_horizontal_layout.addWidget(self.img_widget)
        self._main_horizontal_layout.addLayout(self._limits_layout)

        self.setLayout(self._main_horizontal_layout)



class RoiGroupBox(QtGui.QGroupBox):
    def __init__(self, title):
        super(RoiGroupBox, self).__init__(title)
        self._grid_layout = QtGui.QGridLayout()

        self.x_min_txt = IntegerTextField('0')
        self.x_max_txt = IntegerTextField('0')
        self.y_min_txt = IntegerTextField('0')
        self.y_max_txt = IntegerTextField('0')

        self._grid_layout.addWidget(CenteredQLabel('min'), 0, 1)
        self._grid_layout.addWidget(CenteredQLabel('max'), 0, 2)

        self._grid_layout.addWidget(CenteredQLabel('X:'), 1, 0)
        self._grid_layout.addWidget(self.x_min_txt, 1, 1)
        self._grid_layout.addWidget(self.x_max_txt, 1, 2)

        self._grid_layout.addWidget(CenteredQLabel('Y:'), 2, 0)
        self._grid_layout.addWidget(self.y_min_txt, 2, 1)
        self._grid_layout.addWidget(self.y_max_txt, 2, 2)

        self.setLayout(self._grid_layout)

class CenteredQLabel(QtGui.QLabel):
    def __init__(self, *args, **kwargs):
        super(CenteredQLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

class IntegerTextField(QtGui.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(IntegerTextField, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.setValidator(QtGui.QIntValidator())
        
        
class ImageWidget(QtGui.QWidget):
    mouse_moved = QtCore.pyqtSignal(float, float)
    mouse_left_clicked = QtCore.pyqtSignal(float, float)
    mouse_left_double_clicked = QtCore.pyqtSignal(float, float)

    def __init__(self, *args, **kwargs):
        super(ImageWidget, self).__init__(*args, **kwargs)
        self.pg_widget = pg.GraphicsLayoutWidget()
        self.pg_layout = self.pg_widget.ci
        self.pg_layout.setContentsMargins(0,10,15,0)
        self.pg_viewbox = self.pg_layout.addViewBox(1, 1, lockAspect = False)

        self.bottom_axis = pg.AxisItem('bottom', linkView=self.pg_viewbox)
        self.left_axis = pg.AxisItem('left', linkView=self.pg_viewbox)

        self.pg_layout.addItem(self.bottom_axis, 2, 1)
        self.pg_layout.addItem(self.left_axis, 1,0)

        self.pg_img_item = pg.ImageItem()
        self.pg_viewbox.addItem(self.pg_img_item)

        self._layout = QtGui.QHBoxLayout()
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.addWidget(self.pg_widget)
        self.setLayout(self._layout)

        self.modify_mouse_behavior()

    def plot_image(self, data):
        self.pg_img_item.setImage(data)
        x_max, y_max = data.shape
        self.pg_viewbox.setLimits(xMin=0, xMax =x_max,
                                  yMin=0, yMax=y_max)
        self.img_data = data

    def mouseMoved(self, pos):
        pos = self.pg_img_item.mapFromScene(pos)
        self.mouse_moved.emit(pos.x(), pos.y())

    def modify_mouse_behavior(self):
        #different mouse handlers
        self.pg_viewbox.setMouseMode(self.pg_viewbox.RectMode)

        self.pg_layout.scene().sigMouseMoved.connect(self.mouseMoved)
        self.pg_viewbox.mouseClickEvent = self.myMouseClickEvent
        self.pg_viewbox.mouseDragEvent = self.myMouseDragEvent
        self.pg_viewbox.mouseDoubleClickEvent = self.myMouseDoubleClickEvent

    def myMouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and
                         ev.modifiers() & QtCore.Qt.ControlModifier):
            self.pg_viewbox.scaleBy(2)

        elif ev.button() == QtCore.Qt.LeftButton:
            pos = self.pg_viewbox.mapFromScene(ev.pos())
            y = pos.x()
            x = pos.y()
            self.mouse_left_clicked.emit(x, y)

    def myMouseDoubleClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.pg_viewbox.autoRange()
        if ev.button() == QtCore.Qt.LeftButton:
            pos = self.pg_viewbox.mapFromScene(ev.pos())
            self.mouse_left_double_clicked.emit(pos.x(), pos.y())

    def myMouseDragEvent(self, ev, axis=None):
        #most of this code is copied behavior of left click mouse drag from the original code
        ev.accept()
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif *= -1
        ## Ignore axes if mouse is disabled
        mouseEnabled = np.array(self.pg_viewbox.state['mouseEnabled'], dtype=np.float)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1 - axis] = 0.0

        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and \
                             ev.modifiers() & QtCore.Qt.ControlModifier):
            #determine the amount of translation
            tr = dif * mask
            tr = self.pg_viewbox.mapToView(tr) - self.pg_viewbox.mapToView(pg.Point(0, 0))
            x = tr.x()
            y = tr.y()

            self.pg_viewbox.translateBy(x=x, y=y)
            self.pg_viewbox.sigRangeChangedManually.emit(self.pg_viewbox.state['mouseEnabled'])
        else:
            if ev.isFinish():  ## This is the final move in the drag; change the view scale now
                #print "finish"
                self.pg_viewbox.rbScaleBox.hide()
                #ax = QtCore.QRectF(Point(self.pressPos), Point(self.mousePos))
                ax = QtCore.QRectF(pg.Point(ev.buttonDownPos(ev.button())), pg.Point(pos))
                ax = self.pg_viewbox.childGroup.mapRectFromParent(ax)
                self.pg_viewbox.showAxRect(ax)
                self.pg_viewbox.axHistoryPointer += 1
                self.pg_viewbox.axHistory = self.pg_viewbox.axHistory[:self.pg_viewbox.axHistoryPointer] + [ax]
            else:
                ## update shape of scale box
                self.pg_viewbox.updateScaleBox(ev.buttonDownPos(), ev.pos())


if __name__ == '__main__':
    import numpy as np
    app = QtGui.QApplication([])
    view = NewRoiView()

    data = np.identity(200)
    view.img_widget.plot_image(data)

    view.show()
    view.activateWindow()
    view.raise_()
    app.exec_()