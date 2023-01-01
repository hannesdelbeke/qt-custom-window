import qt_custom_window.qt_manager
from qt_custom_window.titlebar import TitleBar
# from qt_custom_window.qt_manager import QtCore, QtGui, QtWidgets
import qt_custom_window.qt_manager
QtCore = qt_custom_window.qt_manager.QtCore
QtGui = qt_custom_window.qt_manager.QtGui
QtWidgets = qt_custom_window.qt_manager.QtWidgets
Qt = QtCore.Qt
QVBoxLayout = QtWidgets.QVBoxLayout
QWidget = QtWidgets.QWidget


class FramelessWindow(QWidget):
    """
    A frameless window with a custom title bar.
    Devs can add their own widgets to self.content_layout
    """

    default_title_bar = TitleBar

    def __init__(self, parent=None, title="", title_bar=None, title_bar_height=35, *args, **kwargs):
        """
        Args:
            parent: parent widget
            title: title of the window
            title_bar: custom title bar instance, if None, use self.default_title_bar()
        """
        self.show_original_title_bar = False  # debug flag
        self.frameless = False

        super().__init__(parent=parent, *args, **kwargs)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.title_bar = self._set_title_bar(title_bar, title, height=title_bar_height)
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

    def _set_title_bar(self, title_bar, title, *args, **kwargs):
        if not title_bar:
            title_bar = self.default_title_bar(self, title=title, *args, **kwargs)
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
            if self.frameless:
                flags |= QtCore.Qt.FramelessWindowHint
            else:
                flags |= QtCore.Qt.CustomizeWindowHint

        super().setWindowFlags(flags)

        self._flags = flags

    def windowFlags(self):
        return self._flags

    def wrap_widget(self, widget):
        """set central widget and copy over settings from widget"""
        # wrap widget in a frameless window

        flags = widget.windowFlags() | Qt.Window
        self.setParent(widget.parent())
        # widget.setParent(self)

        self.setCentralWidget(widget)


        # copy over settings from widget
        self.setWindowTitle(widget.windowTitle())
        self.setWindowIcon(widget.windowIcon())
        # self.setWindowFlags(widget.windowFlags())
        self.setWindowFlags(flags)
        self.resize(widget.size())
        self.move(widget.pos())

    def showFullScreen(self):
        super().showFullScreen()
        # hide title bar, seems flags are not auto updated and called after showFullScreen
        self.title_bar.setVisible(False)
        # TODO support restore to normal size

    # ===== resize events =====
    # possibly replace with this, seems shorter
    # https://stackoverflow.com/questions/62807295/how-to-resize-a-window-from-the-edges-after-adding-the-property-qtcore-qt-framel

    # current code from https://github.com/yjg30737/pyqt-frameless-window/blob/main/pyqt_frameless_window/base/baseWidget.py
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
        if not self.frameless:
            return

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
        if not self.frameless:
            return

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
