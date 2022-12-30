from PySide2 import QtCore
import PySide2.QtGui as QtGui
from PySide2.QtCore import QPoint
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget
from pathlib import Path


class DarkBar(QWidget):
    """A custom dark title bar for a window, meant to replace the default windows titlebar"""
    # note QWidget functions don't use camelCase, don't change this

    def __init__(self, parent, title="", height=35, *args, **kwargs):
        """
        Args:
            parent (QWidget): The parent widget
            title (str): The title of the window
        """
        super().__init__(parent, *args, **kwargs)
        # self.parent = parent

        self.setMouseTracking(True)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self._height = height

        self.layout = QHBoxLayout()
        self.title = QLabel()  # believe this is a dummy to store the icon layout

        self.title.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)


        self.icon_layout = QHBoxLayout()

        self.btn_icon = QPushButton("♥")
        self.title_text = QLabel("   " + title)  # hack, add space instead of margin
        self.btn_close = QPushButton("🗙")
        self.btn_help = QPushButton("?")
        self.btn_minimize = QPushButton("🗕")
        self.btn_maximize = QPushButton("🗖")
        self.btn_restore = QPushButton("🗗")
        self.btn_restore.setVisible(False)

        # self._style_buttons_svg()

        self._connect_buttons()
        self._styling(height)

        self.layout.addWidget(self.title)
        # self.icon_layout.addStretch(-1)
        self.icon_layout.addWidget(self.btn_icon)
        self.icon_layout.addWidget(self.title_text)
        self.icon_layout.addStretch(-1)
        self.icon_layout.addWidget(self.btn_help)
        self.icon_layout.addWidget(self.btn_minimize)
        self.icon_layout.addWidget(self.btn_maximize)
        self.icon_layout.addWidget(self.btn_restore)
        self.icon_layout.addWidget(self.btn_close)
        self.title.setLayout(self.icon_layout)

        self.setLayout(self.layout)

        # init mouse tracking
        # self.start = QPoint(0, 0)
        # self.pressing = False

    @property
    def height(self):
        return self._height

    def _connect_buttons(self):
        self.btn_close.clicked.connect(self.close_parent)
        self.btn_minimize.clicked.connect(self.minimize_parent)
        self.btn_maximize.clicked.connect(self.maximize_parent)
        self.btn_restore.clicked.connect(self.maximize_parent)

    def _styling(self, height):
        """prettify the qt elements, run after creating all elements in init"""

        # unreal dark grey
        ue_grey = "#151515"
        ue_grey_white = "#c0c0c0"

        # remove padding layout
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.icon_layout.setSpacing(0)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)

        # style buttons
        for btn in [self.btn_icon, self.btn_close, self.btn_minimize, self.btn_maximize, self.btn_restore]:
            btn.setFixedSize(height, height)
            btn.setStyleSheet(f"background-color: transparent; font-size: 14px; color: {ue_grey_white};")
            btn.setFlat(True)  # remove frame from buttons

        # style title
        self.title.setFixedHeight(height)
        self.title.setAlignment(Qt.AlignCenter)
        # set padding

        self.title.setStyleSheet(f"""background-color: {ue_grey};""")
        self.title_text.setStyleSheet(f"""color: {ue_grey_white};""")

    def mousePressEvent(self, e):
        parent = self.parent()
        if e.button() == Qt.LeftButton:
            if parent._resizing:
                parent._resize()
            else:
                parent._move()
        parent.mousePressEvent(e)
        return super().mousePressEvent(e)

    # def mouseDoubleClickEvent(self, e):  # todo test
    #     self.parent().mouseDoubleClickEvent(e)
    #     return super().mouseDoubleClickEvent(e)

    def mouseMoveEvent(self, e):
        self.parent().mouseMoveEvent(e)
        return super().mouseMoveEvent(e)

    # prevent accumulated cursor shape bug
    def enterEvent(self, e):
        self.parent().enterEvent(e)
        return super().enterEvent(e)

    def close_parent(self):
        self.parent.close()

    def maximize_parent(self):
        # modified this func to support going back to normal
        if self.parent.windowState() & QtCore.Qt.WindowMaximized:
            self.parent.showNormal()
            self.btn_maximize.setVisible(True)
            self.btn_restore.setVisible(False)
        else:
            self.parent.showMaximized()
            self.btn_maximize.setVisible(False)
            self.btn_restore.setVisible(True)

    def minimize_parent(self):
        self.parent.showMinimized()

    # def setWindowFlag() # this wont work correctly
        # TODO implement this

    def setWindowFlags(self, flags):
        """
        WindowTitleHint:             show title
        WindowSystemMenuHint:        show icon
        WindowMinimizeButtonHint:    show minimize 🗕 button
        WindowMaximizeButtonHint:    show maximize 🗖🗗 buttons
        WindowCloseButtonHint:       show close 🗙 button
        WindowContextHelpButtonHint: show help ? button

        e.g. widget.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowMaximizeButtonHint)
        """
        # see https://doc.qt.io/qt-6/qt.html#WindowType-enum

        # default values
        show_title_bar = True
        show_close = True
        show_minim = True
        show_maxim = True
        show_help = False
        show_sys_hint = True  # icon
        full_screen = flags & Qt.WindowFullScreen
        frameless = flags & Qt.FramelessWindowHint

        # popup and dialog flags form a tool window together
        # otherwise Qt.Window triggers the Qt.Tool flag
        is_tool_window = bool(flags & 0x00000008) and bool(flags & 0x00000002)
        if is_tool_window:
            # hide all buttons if tool window, except title, title_text, and close button
            show_close = True
            show_minim = False
            show_maxim = False
            show_help = False
            show_sys_hint = False

        # set all to false, unless their flag is given
        # customise title bar overrides tool window, so run this after tool window logic
        if flags & QtCore.Qt.CustomizeWindowHint:
            show_title_bar = flags & QtCore.Qt.WindowTitleHint
            show_minim = flags & QtCore.Qt.WindowMinimizeButtonHint
            show_maxim = flags & QtCore.Qt.WindowMaximizeButtonHint
            show_close = flags & QtCore.Qt.WindowCloseButtonHint
            show_sys_hint = flags & QtCore.Qt.WindowSystemMenuHint
            show_help = flags & QtCore.Qt.WindowContextHelpButtonHint

        self.title.setVisible(not full_screen and not frameless and
                              (show_close or show_maxim or show_minim or show_title_bar or show_sys_hint or show_help))
        self.title_text.setVisible(show_title_bar)
        self.btn_minimize.setVisible(show_minim)
        self.btn_maximize.setVisible(show_maxim)
        self.btn_close.setVisible(show_close)
        self.btn_icon.setVisible(show_sys_hint)
        self.btn_help.setVisible(show_help)




class DarkBarUnreal(DarkBar):
    def __init__(self, parent, title="", height=35, *args, **kwargs):
        super().__init__(parent, title, height, *args, **kwargs)
        self._style_buttons_svg()

    def _style_buttons_svg(self):
        import unreal  # import unreal here to avoid import error in other dccs
        engine_content = Path(unreal.Paths.engine_content_dir())
        data = {
            self.btn_icon: engine_content / r"Slate\Starship\Common\unreal-small.svg",
            self.btn_close: engine_content / r"Slate\Starship\CoreWidgets\Window\close.svg",
            self.btn_minimize: engine_content / r"Slate\Starship\CoreWidgets\Window\minimize.svg",
            self.btn_maximize: engine_content / r"Slate\Starship\CoreWidgets\Window\maximize.svg",
            self.btn_restore: engine_content / r"Slate\Starship\CoreWidgets\Window\restore.svg",
        }
        for btn, icon_path in data.items():

            if not icon_path.exists():
                # use text as backup
                continue

            icon = QtGui.QIcon(str(icon_path))
            btn.setIcon(icon)
            btn.setIconSize(QtCore.QSize(self._height, self._height))
            btn.setText("")  # clear text if we set icon

        self.btn_icon.setIconSize(QtCore.QSize(self._height / 2, self._height / 2))


class FramelessWindow(QWidget):
    """
    A frameless window with a custom title bar.
    Devs can add their own widgets to self.content_layout
    """

    default_title_bar = DarkBar

    def __init__(self, parent=None, title="", title_bar=None, *args, **kwargs):
        """
        Args:
            parent: parent widget
            title: title of the window
            title_bar: custom title bar instance, if None, use self.default_title_bar()
        """
        self.show_original_title_bar = False  # debug flag

        super().__init__(parent=parent, *args, **kwargs)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.title_bar = self._set_title_bar(title_bar, title)
        self.content_layout = QVBoxLayout()

        layout.addWidget(self.title_bar)  # add title bar
        layout.addLayout(self.content_layout)
        layout.addStretch(-1)  # so the bar stays at top when scaling the window

        self._flags = Qt.Widget  # super().windowFlags()
        self.setWindowFlags(self._flags)

        # use CustomizeWindowHint when you want to support resizing
        self.layout().setContentsMargins(0, 0, 0, 0)
        # otherwise use MSWindowsFixedSizeDialogHint
        # self.setWindowFlags(Qt.Tool | Qt.MSWindowsFixedSizeDialogHint)
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

        self._initPosition()
        self._initVal()
        self.setMouseTracking(True)

    def _set_title_bar(self, title_bar, title):
        if not title_bar:
            title_bar = self.default_title_bar(self, title=title)
        return title_bar

    def setCentralWidget(self, widget):  # noqa: use same name convention as qmainwindow
        self.content_layout.addWidget(widget)
        return widget

    def centralWidget(self):
        return self.content_layout.itemAt(0).widget()

    def setWindowTitle(self, title):
        self.title_bar.title_text.setText(title)

    def windowTitle(self) -> str:
        return self.title_bar.title_text.text()

    def setWindowIcon(self, icon: QtGui.QIcon) -> None:
        size = self.title_bar.height * .5
        self.title_bar.btn_icon.setIcon(icon)
        self.title_bar.btn_icon.setIconSize(QtCore.QSize(size, size))

    def windowIcon(self) -> QtGui.QIcon:
        return self.title_bar.btn_icon.icon()

    def setWindowFlag(self, arg__1:QtCore.Qt.WindowType, on=True) -> None:
        flags = self.windowFlags()
        if on:
            flags |= arg__1
        else:
            flags &= ~arg__1
        self.setWindowFlags(flags)

    def setWindowFlags(self, flags:QtCore.Qt.WindowFlags) -> None:
        # pass window flags to the qt winodw as usual.
        # however when we say frameless window, hide both default and custom title bars
        # when we don't say frameless window, we only want to hide the qt default title bar but not our custom one

        self.title_bar.setWindowFlags(flags)

        flags_to_filter = (
            QtCore.Qt.CustomizeWindowHint,
            QtCore.Qt.WindowTitleHint,
            QtCore.Qt.WindowSystemMenuHint,
            QtCore.Qt.WindowMinimizeButtonHint,
            QtCore.Qt.WindowMaximizeButtonHint,
            QtCore.Qt.WindowCloseButtonHint,
            QtCore.Qt.WindowContextHelpButtonHint,
            QtCore.Qt.FramelessWindowHint,
            # QtCore.Qt.WindowFullScreen, # todo if windows fullscreen dont filter out
        )

        # filtered_flags = 0b00000000
        for flag in flags_to_filter:
            if flags & flag:
                # filtered_flags |= flag  # add flag to filtered flags
                flags ^= flag  # remove flag from flags

        if not self.show_original_title_bar:
            flags |= QtCore.Qt.FramelessWindowHint #CustomizeWindowHint

        super().setWindowFlags(flags)

        self._flags = flags

    def windowFlags(self):
        return self._flags

    def wrap_widget(self, widget):
        """set central widget and copy over settings from widget"""
        # wrap widget in a frameless window
        self.setCentralWidget(widget)

        # copy over settings from widget
        self.setWindowTitle(widget.windowTitle())
        self.setWindowIcon(widget.windowIcon())
        self.setWindowFlags(widget.windowFlags())
        self.resize(widget.size())
        # self.move(widget.pos())

    def showFullScreen(self):
        super().showFullScreen()
        # hide title bar, seems flags are not auto updated and called after showFullScreen
        self.title_bar.setVisible(False)
        # TODO support restore to normal size

    # ===== resize events =====

    # code from https://github.com/yjg30737/pyqt-frameless-window/blob/main/pyqt_frameless_window/base/baseWidget.py
    # init the edge direction for set correct reshape cursor based on it

    def _initVal(self):
        self._resizing = False
        self._resizable = True

        self._margin = 3
        self._cursor = QtGui.QCursor()
        self._pressToMove = False

        self._verticalExpandedEnabled = False
        self._verticalExpanded = False
        self._originalY = 0
        self._originalHeightBeforeExpand = 0

    def _initPosition(self):
        self._top = False
        self._bottom = False
        self._left = False
        self._right = False

    def _setCursorShapeForCurrentPoint(self, p):
        if self.isResizable():
            if self.isMaximized() or self.isFullScreen():
                pass
            else:
                # give the margin to reshape cursor shape
                rect = self.rect()
                rect.setX(self.rect().x() + self._margin)
                rect.setY(self.rect().y() + self._margin)
                rect.setWidth(self.rect().width() - self._margin * 2)
                rect.setHeight(self.rect().height() - self._margin * 2)

                self._resizing = rect.contains(p)
                if self._resizing:
                    # resize end
                    self.unsetCursor()
                    self._cursor = self.cursor()
                    self._initPosition()
                else:
                    # resize start
                    x = p.x()
                    y = p.y()

                    x1 = self.rect().x()
                    y1 = self.rect().y()
                    x2 = self.rect().width()
                    y2 = self.rect().height()

                    self._left = abs(x - x1) <= self._margin # if mouse cursor is at the almost far left
                    self._top = abs(y - y1) <= self._margin # far top
                    self._right = abs(x - (x2 + x1)) <= self._margin # far right
                    self._bottom = abs(y - (y2 + y1)) <= self._margin # far bottom

                    # set the cursor shape based on flag above
                    if self._top and self._left:
                        self._cursor.setShape(Qt.SizeFDiagCursor)
                    elif self._top and self._right:
                        self._cursor.setShape(Qt.SizeBDiagCursor)
                    elif self._bottom and self._left:
                        self._cursor.setShape(Qt.SizeBDiagCursor)
                    elif self._bottom and self._right:
                        self._cursor.setShape(Qt.SizeFDiagCursor)
                    elif self._left:
                        self._cursor.setShape(Qt.SizeHorCursor)
                    elif self._top:
                        self._cursor.setShape(Qt.SizeVerCursor)
                    elif self._right:
                        self._cursor.setShape(Qt.SizeHorCursor)
                    elif self._bottom:
                        self._cursor.setShape(Qt.SizeVerCursor)
                    self.setCursor(self._cursor)

                self._resizing = not self._resizing

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self._resizing:
                self._resize()
            else:
                if self._pressToMove:
                    self._move()
        return super().mousePressEvent(e)

    # def mouseDoubleClickEvent(self, e):  # todo test
    #     if self._verticalExpandedEnabled:
    #         p = e.pos()
    #
    #         rect = self.rect()
    #         rect.setX(self.rect().x() + self._margin)
    #         rect.setY(self.rect().y() + self._margin)
    #         rect.setWidth(self.rect().width() - self._margin * 2)
    #         rect.setHeight(self.rect().height() - self._margin * 2)
    #
    #         y = p.y()
    #
    #         y1 = self.rect().y()
    #         y2 = self.rect().height()
    #
    #         top = abs(y - y1) <= self._margin # far top
    #         bottom = abs(y - (y2 + y1)) <= self._margin # far bottom
    #
    #         ag = QtGui.QScreen().availableGeometry()
    #
    #         # fixme minor bug - resizing after expand can lead to inappropriate result when in comes to expanding again, it should be fixed
    #         # vertical expanding when double-clicking either top or bottom edge
    #         # back to normal
    #         if self._verticalExpanded:
    #             if top or bottom:
    #                 self.move(self.x(), self._originalY)
    #                 self.resize(self.width(), self._originalHeightBeforeExpand)
    #                 self._verticalExpanded = False
    #         # expand vertically
    #         else:
    #             if top or bottom:
    #                 self._verticalExpanded = True
    #                 min_size = self.minimumSize()
    #                 max_size = self.maximumSize()
    #                 geo = self.geometry()
    #                 self._originalY = geo.y()
    #                 self._originalHeightBeforeExpand = geo.height()
    #                 geo.moveTop(0)
    #                 self.setGeometry(geo)
    #                 self.setFixedHeight(ag.height()-2)
    #                 self.setMinimumSize(min_size)
    #                 self.setMaximumSize(max_size)
    #
    #     return super().mouseDoubleClickEvent(e)

    def mouseMoveEvent(self, e):
        self._setCursorShapeForCurrentPoint(e.pos())
        return super().mouseMoveEvent(e)

    # prevent accumulated cursor shape bug
    def enterEvent(self, e):
        self._setCursorShapeForCurrentPoint(e.pos())
        return super().enterEvent(e)

    def _resize(self):
        window = self.window().windowHandle()
        # reshape cursor for resize
        if self._cursor.shape() == Qt.SizeHorCursor:
            if self._left:
                window.startSystemResize(Qt.LeftEdge)
            elif self._right:
                window.startSystemResize(Qt.RightEdge)
        elif self._cursor.shape() == Qt.SizeVerCursor:
            if self._top:
                window.startSystemResize(Qt.TopEdge)
            elif self._bottom:
                window.startSystemResize(Qt.BottomEdge)
        elif self._cursor.shape() == Qt.SizeBDiagCursor:
            if self._top and self._right:
                window.startSystemResize(Qt.TopEdge | Qt.RightEdge)
            elif self._bottom and self._left:
                window.startSystemResize(Qt.BottomEdge | Qt.LeftEdge)
        elif self._cursor.shape() == Qt.SizeFDiagCursor:
            if self._top and self._left:
                window.startSystemResize(Qt.TopEdge | Qt.LeftEdge)
            elif self._bottom and self._right:
                window.startSystemResize(Qt.BottomEdge | Qt.RightEdge)

    def _move(self):
        window = self.window().windowHandle()
        window.startSystemMove()

    def setMargin(self, margin: int):
        self._margin = margin
        self.layout().setContentsMargins(self._margin, self._margin, self._margin, self._margin)

    def isResizable(self) -> bool:
        return self._resizable

    def setResizable(self, f: bool):
        self._resizable = f

    def isPressToMove(self) -> bool:
        return self._pressToMove

    def setPressToMove(self, f: bool):
        self._pressToMove = f




# ============

class FramelessWindowUnreal(FramelessWindow):
    default_title_bar = DarkBarUnreal


def wrap_widget_unreal(widget: QWidget) -> FramelessWindowUnreal:
    """helper function to wrap a widget in a frameless window with a custom title bar"""
    # wrap widget in a frameless window
    window = FramelessWindowUnreal()
    window.wrap_widget(widget)
    return window


# demo code
if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets
    flags = Qt.Tool
            #| Qt.WindowStaysOnTopHint works
    flags2 = flags

    app = QtWidgets.QApplication(sys.argv)
    w1 = FramelessWindow()
    w1.setWindowTitle("    Frameless Window")  # todo when no title provided, use default title from window
    w1.setWindowIcon(QtGui.QIcon("icon.png"))
    w1.setCentralWidget(QtWidgets.QPushButton("Hello World"))
    w1.setWindowFlags(flags)
    # w1.setWindowFlags(flags2)
    # set pos
    w1.move(100, 100)
    w1.show()

    # create a second default qt window
    w2 = QtWidgets.QWidget()
    w2.setWindowTitle("Default Window")
    w2.setWindowIcon(QtGui.QIcon("icon.png"))
    w2.setWindowFlags(flags)
    # w2.setWindowFlags(flags2)
    w2.show()

    sys.exit(app.exec_())

    # todo implement Qt.WindowSystemMenuHint dropdown menu when clicking on the icon
