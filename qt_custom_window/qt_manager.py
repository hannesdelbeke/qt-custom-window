
qt_imported = False

if not qt_imported:
    try:
        from PyQt6 import *
        qt_imported = True
    except:
        pass

if not qt_imported:
    try:
        from PyQt5 import *
        qt_imported = True
    except:
        pass

if not qt_imported:
    try:
        from PyQt4 import *
        qt_imported = True
    except:
        pass

if not qt_imported:
    try:
        from PySide6 import *
        qt_imported = True
    except:
        pass

if not qt_imported:
    try:
        from PySide2 import *
        qt_imported = True
    except:
        pass

if not qt_imported:
    try:
        from PySide import *
        qt_imported = True
    except:
        pass
