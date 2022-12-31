from qt_custom_window.window import FramelessWindow
# from qt_custom_window.qt_manager import QtGui, QtCore, QtWidgets
import qt_custom_window.qt_manager
QtCore = qt_custom_window.qt_manager.QtCore
QtGui = qt_custom_window.qt_manager.QtGui
QtWidgets = qt_custom_window.qt_manager.QtWidgets
Qt = QtCore.Qt
QWidget = QtWidgets.QWidget


def wrap_widget2(widget: QWidget) -> FramelessWindow:
    """helper function to wrap a widget in a frameless window with a custom title bar"""

    window = FramelessWindow()  # QWidget()  #
    window.wrap_widget(widget)
    window.show()
    return window
