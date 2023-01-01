from qt_custom_window.window import FramelessWindow
# from qt_custom_window.qt_manager import QtGui, QtCore, QtWidgets
import qt_custom_window.qt_manager
QtCore = qt_custom_window.qt_manager.QtCore
QtGui = qt_custom_window.qt_manager.QtGui
QtWidgets = qt_custom_window.qt_manager.QtWidgets
Qt = QtCore.Qt
QWidget = QtWidgets.QWidget


def wrap_widget(widget: QWidget, parent=None, **kwargs) -> FramelessWindow:
    """helper function to wrap a widget in a frameless window with a custom title bar"""
    window = FramelessWindow(**kwargs)
    window.wrap_widget(widget)

    # set parent seems to change window flags ## todo check out
    flags = widget.windowFlags()
    if parent:
        window.setParent(parent)
    window.setWindowFlags(flags)

    # window.setWindowFlags(QtCore.Qt.Window)
    return window

# todo close blender when clicking x