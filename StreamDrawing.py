#!/usr/bin/env python3
""" StreamDrawing

A tiny full screen drawing app - for streaming
Why? To be able to quickly draw mathematics, explain ideas, sketch on the fly

Requirements: tablet supported by PyQt5
Example: Wacom Intuos on Linux

Usage: buttons:
    f - toggles fullscreen
    q - quits
    Ctrl-s - save (creates a dir and dumps all .pngs - in background)
    a - add a new slide and jump to it
    page up / down - navigate between slides

Supports pen and eraser modes

PROBLEMS, BUGS, LIMITATIONS
- scenes the same as desktop resolution, not portable between resolutions for now
- no preview of brushes (eraser particularly)
- raster graphics - simple drawing on canvas
- save creates a directory in a current one, no feedback about success / failure

Author: Adam Lukomski, 2023
License: MIT
"""

import sys
import os
import datetime
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SlidesLibrary(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.addWidget( TabletDrawing() )
        self.updateTitle()
        self._fullscreen = True
        self.fullscreen(self._fullscreen)

    def addNewSlide(self):
        self.insertWidget( self.currentIndex()+1, TabletDrawing() )
        self.setCurrentIndex(self.currentIndex()+1)
        self.updateTitle()

    def keyPressEvent(self,event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_PageUp:
            if self.currentIndex() > 0:
                self.setCurrentIndex(self.currentIndex()-1)
                self.updateTitle()
        if event.key() == Qt.Key_PageDown:
            if self.currentIndex() < self.count()-1:
                self.setCurrentIndex(self.currentIndex()+1)
                self.updateTitle()
        if event.key() == Qt.Key_A:
            self.addNewSlide()
        if event.key() == Qt.Key_Q:
            app.closeAllWindows()
        if event.key() == Qt.Key_F:
            self.fullscreen( not self._fullscreen )
        if (event.modifiers() & Qt.ControlModifier) and event.key() == Qt.Key_S:
            self.save()

    def fullscreen(self,full=True):
        if full:
                self.setWindowState( Qt.WindowFullScreen )
                self._fullscreen = True
        else:
                self.setWindowState( Qt.WindowNoState )
                self._fullscreen = False

    def updateTitle(self):
        self.setWindowTitle("Slide {} of {}".format(self.currentIndex()+1,self.count()) )

    def save(self):
        dir1 = "saved_{}".format( datetime.datetime.now().strftime('%Y%m%d-%H%M%S') )
        os.mkdir( dir1 )
        for i in range(self.count()):
            self.widget(i).pixmap().save(os.path.join(dir1, 'image_{:03d}.png'.format(i)),'PNG')

class TabletDrawing(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.paint_count = 0
        self.pen_is_down = False
        self.pen_x = -1
        self.pen_y = -1
        self.pen_pressure = -1

        self.pen_x_last = -1
        self.pen_y_last = -1
        self.pen_size_pen = 12
        self.pen_size_eraser = 36
        self.pen_size = self.pen_size_pen

        self.pen1 = QPen(Qt.black, self.pen_size, Qt.SolidLine, Qt.RoundCap)

        width = app.desktop().frameGeometry().width()
        height = app.desktop().frameGeometry().height()
        self.resize(width, height)

        self.canvas1 = QPixmap(width, height)
        self.canvas1.fill(Qt.white)
        self.setPixmap(self.canvas1)

    def tabletEvent(self, event):
        self.pen_x_last = self.pen_x
        self.pen_y_last = self.pen_y
        self.pen_x = event.x()
        self.pen_y = event.y()
        self.pen_pressure = event.pressure()

        if event.type() == QTabletEvent.TabletPress:
            if event.pointerType() == QTabletEvent.Eraser:
                self.pen1.setColor( Qt.white )
                self.pen_size = self.pen_size_eraser
            else: # UnknownPointer, Pen, Cursor
                self.pen1.setColor( Qt.black )
                self.pen_size = self.pen_size_pen
        elif event.type() == QTabletEvent.TabletMove:
            pass
        elif event.type() == QTabletEvent.TabletRelease:
            self.pen_x = -1
            self.pen_y = -1
            self.pen_x_last = -1
            self.pen_y_last = -1

        if self.pen_x_last > 0 and self.pen_y_last > 0:
            self.paint_count += 1
            painter = QPainter(self.pixmap())
            self.pen1.setWidth( round(self.pen_size*self.pen_pressure) )
            painter.setPen( self.pen1 )
            painter.drawLine(self.pen_x_last, self.pen_y_last, self.pen_x, self.pen_y)
            painter.end()

        event.accept()
        self.update()

app = QApplication(sys.argv)
widget = SlidesLibrary()
widget.show()
app.exec()
