# from qt_custom_window.qt_manager import QtCore, QtWidgets
import qt_custom_window.qt_manager
QtCore = qt_custom_window.qt_manager.QtCore
QtGui = qt_custom_window.qt_manager.QtGui
QtWidgets = qt_custom_window.qt_manager.QtWidgets
Qt = QtCore.Qt
QWidget = QtWidgets.QWidget
QHBoxLayout = QtWidgets.QHBoxLayout
QLabel = QtWidgets.QLabel
QPushButton = QtWidgets.QPushButton


class TitleBar(QWidget):
    """A custom dark title bar for a window, meant to replace the default windows titlebar"""
    # note QWidget functions don't use camelCase, don't change this

    def __init__(self, parent, title=None, height=35, *args, **kwargs):
        """
        Args:
            parent (QWidget): The parent widget
            title (str): The title of the window
        """

        title = title or ""
        super().__init__(parent, *args, **kwargs)
        # self.parent = parent

        self.setMouseTracking(True)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self._height = height

        self.layout = QHBoxLayout()
        self.title = QWidget()  # believe this is a dummy to store the icon layout

        # self.title.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)  # better resize cursor handling but can't click buttons


        self.icon_layout = QHBoxLayout()

        self.btn_icon = QPushButton()
        self.title_text = QLabel("   " + title)  # hack, add space instead of margin
        self.btn_close = QPushButton("🗙")
        self.btn_help = QPushButton("?")
        self.btn_minimize = QPushButton("🗕")
        self.btn_maximize = QPushButton("🗖")
        self.btn_restore = QPushButton("🗗")
        self.btn_restore.setVisible(False)

        # self.title_text.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
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

    @height.setter
    def height(self, value):
        self._height = value
        self._styling(value)

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
        for btn in [self.btn_icon, self.btn_close, self.btn_minimize, self.btn_maximize, self.btn_restore, self.btn_help]:
            btn.setFixedSize(height, height)
            btn.setStyleSheet(f"background-color: transparent; "
                              f"font-size: 14px; "
                              f"color: {ue_grey_white}; "
                              "border: none;"
                              "padding-top: 0px;"
                              "text-align: center;")
            btn.setFlat(True)  # remove frame from buttons

        # style title
        self.title.setFixedHeight(height)
        # self.title.setAlignment(Qt.AlignCenter)
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
        self.parent().close()

    def maximize_parent(self):
        # modified this func to support going back to normal
        if self.parent().windowState() & QtCore.Qt.WindowMaximized:
            self.parent().showNormal()
            self.btn_maximize.setVisible(True)
            self.btn_restore.setVisible(False)
        else:
            self.parent().showMaximized()
            self.btn_maximize.setVisible(False)
            self.btn_restore.setVisible(True)

    def minimize_parent(self):
        self.parent().showMinimized()

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
