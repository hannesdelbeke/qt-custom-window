
qt_imported = False

QtGui = None
QtCore = None
QtWidgets = None

if not qt_imported:
    try:
        from PySide6 import QtGui, QtCore, QtWidgets
        qt_imported = True
    except ImportError:
        pass

if not qt_imported:
    try:
        from PySide2 import QtGui, QtCore, QtWidgets
        qt_imported = True
    except ImportError:
        pass

if not qt_imported:
    try:
        from PySide import QtGui, QtCore, QtWidgets
        qt_imported = True
    except ImportError:
        pass

if not qt_imported:
    try:
        from PyQt6 import QtGui, QtCore, QtWidgets
        qt_imported = True
    except ImportError:
        pass

if not qt_imported:
    try:
        from PyQt5 import QtGui, QtCore, QtWidgets
        qt_imported = True
    except ImportError:
        pass

if not qt_imported:
    try:
        from PyQt4 import QtGui, QtCore, QtWidgets
        qt_imported = True
    except ImportError:
        pass
