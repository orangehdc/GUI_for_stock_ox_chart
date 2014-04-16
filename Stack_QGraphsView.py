# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 13:16:59 2014
http://stackoverflow.com/questions/11250110/
connecting-slider-to-graphics-view-in-pyqt
@author: Administrator
"""
from PyQt4 import QtCore, QtGui

class Graph_view(QtGui.QWidget):

    def __init__(self, jpg_name,parent=None):
        super(Graph_view, self).__init__(parent)
        self.resize(640,480)
        self.layout = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.view = QtGui.QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.image = QtGui.QGraphicsPixmapItem()
        self.scene.addItem(self.image)
        self.view.centerOn(self.image)

        self._images = [
            QtGui.QPixmap("D:/demo/jpg/"+jpg_name),
            QtGui.QPixmap('')
        ]
        
        self.slider = QtGui.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        # max is the last index of the image list
        self.slider.setMaximum(len(self._images)-1)
        self.layout.addWidget(self.slider)

        # set it to the first image, if you want.
        self.sliderMoved(0)

        self.slider.sliderMoved.connect(self.sliderMoved)
        
    def sliderMoved(self, val):
        print "Slider moved to:", val
        try:
            self.image.setPixmap(self._images[val])
        except IndexError:
            print "Error: No image at index", val


if __name__ == "__main__":
    app = QtGui.QApplication([])
    jpg_name = 'stock600805.png'
    w = Graph_view(jpg_name)
    w.show()
    #w.raise_()
    app.exec_()