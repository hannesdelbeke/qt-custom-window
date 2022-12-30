import sys
from qt_custom_window.window import FramelessWindow
from qt_custom_window.qt_manager import QtGui, QtCore, QtWidgets
Qt = QtCore.Qt


# demo code
if __name__ == "__main__":

    flags = Qt.Tool
    flags2 = flags
    app = QtWidgets.QApplication(sys.argv)
    w1 = FramelessWindow()
    w2 = QtWidgets.QWidget()

    #| Qt.WindowStaysOnTopHint works

    w1.setWindowTitle("    Frameless Window")  # todo when no title provided, use default title from window
    w1.setWindowIcon(QtGui.QIcon("icon.png"))
    w1.setCentralWidget(QtWidgets.QPushButton("Hello World"))
    w1.setWindowFlags(flags)
    # w1.setWindowFlags(flags2)
    # set pos
    w1.move(100, 100)
    w1.show()

    # create a second default qt window
    w2.setWindowTitle("Default Window")
    w2.setWindowIcon(QtGui.QIcon("icon.png"))
    w2.setWindowFlags(flags)
    # w2.setWindowFlags(flags2)
    w2.show()

    sys.exit(app.exec_())

    # todo implement Qt.WindowSystemMenuHint dropdown menu when clicking on the icon
