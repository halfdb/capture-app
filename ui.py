from ctypes.wintypes import MSG
import sys
import typing

from PyQt5 import sip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ocr


class MainWindow(QMainWindow):
    borderWidth = 10

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.brush = QBrush()
        self.startTimer(1000)

        self.windowPos = None
        self.mousePos = None

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.ActivationChange:
            if not self.isActiveWindow():
                self.close()

    def mouseDoubleClickEvent(self, event) -> None:
        self.close()

    def mousePressEvent(self, event):
        # Store the positions of mouse and window and
        # change the window position relative to them.
        self.windowPos = self.pos()
        self.mousePos = event.globalPos()
        super(MainWindow, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.move(self.windowPos + event.globalPos() - self.mousePos)
        super(MainWindow, self).mouseMoveEvent(event)

    def paintEvent(self, _: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setOpacity(0.2)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.black, MainWindow.borderWidth))
        painter.drawRect(self.rect())

    def nativeEvent(self, _, message: sip.voidptr) -> typing.Tuple[bool, int]:
        msg = MSG.from_address(message.__int__())
        if msg.message == 0x0084:
            pos = self.rect()
            pos.moveTo(self.pos())
            x = msg.lParam & 0x0000ffff
            y = (msg.lParam & 0xffff0000) >> 16
            h = 0
            if pos.left() < x < pos.left() + MainWindow.borderWidth:
                h = 1
            elif pos.right() - MainWindow.borderWidth < x < pos.right():
                h = 2
            v = 0
            if pos.top() < y < pos.top() + MainWindow.borderWidth:
                v = 1
            elif pos.bottom() - MainWindow.borderWidth < y < pos.bottom():
                v = 2
            res = 9 + 3 * v + h
            return res != 9, res
        return False, 0

    def timerEvent(self, _: 'QTimerEvent') -> None:
        pos = self.rect()
        pos.moveTo(self.pos())
        # print(pos)
        ocr.read(pos.x(), pos.y(), pos.width(), pos.height())
        print(ocr.lastResult())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.mainWindow = MainWindow()

    app.tray = QSystemTrayIcon(app.mainWindow)
    app.tray.setIcon(QIcon("icon.jfif"))

    # Creating the options
    app.menu = QMenu(app.mainWindow)

    show = QAction("&Show")
    show.triggered.connect(app.mainWindow.show)
    app.menu.addAction(show)

    # To quit the app
    quit_ = QAction("&Quit")
    quit_.triggered.connect(app.quit)
    app.menu.addAction(quit_)

    # Adding options to the System Tray
    app.tray.setContextMenu(app.menu)
    app.tray.show()

    app.mainWindow.show()
    sys.exit(app.exec_())
