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
        super(DarkBar, self).__init__(*args, **kwargs)
        self.parent = parent

        self._height = height

        self.layout = QHBoxLayout()
        self.title = QLabel()  # believe this is a dummy to store the icon layout
        self.icon_layout = QHBoxLayout()

        self.btn_icon = QPushButton("♥")
        self.title_text = QLabel("   " + title)  # hack, add space instead of margin
        self.btn_close = QPushButton("🗙")
        self.btn_minimize = QPushButton("🗕")
        self.btn_maximize = QPushButton("🗖")
        self.btn_restore = QPushButton("🗗", )
        self.btn_restore.setVisible(False)

        # self._style_buttons_svg()

        self._connect_buttons()
        self._styling(height)

        self.layout.addWidget(self.title)
        # self.icon_layout.addStretch(-1)
        self.icon_layout.addWidget(self.btn_icon)
        self.icon_layout.addWidget(self.title_text)
        self.icon_layout.addStretch(-1)
        self.icon_layout.addWidget(self.btn_minimize)
        self.icon_layout.addWidget(self.btn_maximize)
        self.icon_layout.addWidget(self.btn_restore)
        self.icon_layout.addWidget(self.btn_close)
        self.title.setLayout(self.icon_layout)

        self.setLayout(self.layout)

        # init mouse tracking
        self.start = QPoint(0, 0)
        self.pressing = False

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


    # resizing is not implemented
    # def resizeEvent(self, QResizeEvent):
    #     super(MyBar, self).resizeEvent(QResizeEvent)
    #     self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

        window = self.parent.windowHandle()
        window.startSystemMove()

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

        show_title = False
        show_minim = False
        show_maxim = False
        show_close = False
        show_help = False
        show_sys_hint = False  # icon
        full_screen = flags & Qt.WindowFullScreen

        # hide all buttons if tool window, except title, title_text, and close button
        show_close = flags & QtCore.Qt.Tool

        # TODO frameless hides this. don't pass other flags to this
        # self.title.setVisible(not flags & QtCore.Qt.CustomizeWindowHint)

        # set all to false, unless their flag is given
        # customise title bar overrides tool window, so run this after tool window logic
        if flags & QtCore.Qt.CustomizeWindowHint:

            show_title = flags & QtCore.Qt.WindowTitleHint
            show_minim = flags & QtCore.Qt.WindowMinimizeButtonHint
            show_maxim = flags & QtCore.Qt.WindowMaximizeButtonHint
            show_close = flags & QtCore.Qt.WindowCloseButtonHint
            show_sys_hint = flags & QtCore.Qt.WindowSystemMenuHint

        self.title.setVisible(not full_screen and (show_close or show_maxim or show_minim or show_title or show_sys_hint))
        self.title_text.setVisible(True)
        self.btn_minimize.setVisible(show_minim)
        self.btn_maximize.setVisible(show_maxim)
        self.btn_close.setVisible(show_close)
        self.btn_icon.setVisible(show_sys_hint)

        # TODO add support for
        # Qt.WindowContextHelpButtonHint




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

        self._flags = super().windowFlags()
        self.setWindowFlags(self._flags)

        # use CustomizeWindowHint when you want to support resizing
        self.layout().setContentsMargins(0, 0, 0, 0)
        # otherwise use MSWindowsFixedSizeDialogHint
        # self.setWindowFlags(Qt.Tool | Qt.MSWindowsFixedSizeDialogHint)
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

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
        super().setWindowFlag(arg__1, on)
    # TODO if flags affect title bar pass along to title bar
    #     self._process_flags()

    def setWindowFlags(self, flags:QtCore.Qt.WindowFlags) -> None:
        # pass window flags to the qt winodw as usual.
        # however when we say frameless window, hide both default and custom title bars
        # when we don't say frameless window, we only want to hide the qt default title bar but not our custom one

        # filter following flags
        # WindowTitleHint:             show title
        # WindowSystemMenuHint:        show icon
        # WindowMinimizeButtonHint:    show minimize 🗕 button
        # WindowMaximizeButtonHint:    show maximize 🗖🗗 buttons
        # WindowCloseButtonHint:       show close 🗙 button
        # WindowContextHelpButtonHint: show help ? button
        flags_to_filter = (
            QtCore.Qt.CustomizeWindowHint,
            QtCore.Qt.WindowTitleHint,
            QtCore.Qt.WindowSystemMenuHint,
            QtCore.Qt.WindowMinimizeButtonHint,
            QtCore.Qt.WindowMaximizeButtonHint,
            QtCore.Qt.WindowCloseButtonHint,
            QtCore.Qt.WindowContextHelpButtonHint,
        )

        filtered_flags = 0b10000000
        for flag in flags_to_filter:
            if flags & flag:
                filtered_flags |= flag  # add flag to filtered flags
                flags ^= flag  # remove flag from flags

        if not self.show_original_title_bar:
            flags |= QtCore.Qt.CustomizeWindowHint

        super().setWindowFlags(flags)

        self.title_bar.setWindowFlags(filtered_flags)
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
    flags = Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint \
            #| Qt.WindowStaysOnTopHint works
    flags2 = flags

    app = QtWidgets.QApplication(sys.argv)
    w1 = FramelessWindow()
    w1.setWindowTitle("    Frameless Window")  # todo when no title provided, use default title from window
    w1.setWindowIcon(QtGui.QIcon("icon.png"))
    w1.setCentralWidget(QtWidgets.QPushButton("Hello World"))
    w1.setWindowFlags(flags)
    w1.setWindowFlags(flags2)
    w1.show()

    # create a second default qt window
    w2 = QtWidgets.QMainWindow()
    w2.setWindowTitle("Default Window")
    w2.setWindowIcon(QtGui.QIcon("icon.png"))
    w2.setWindowFlags(flags)
    w2.setWindowFlags(flags2)
    w2.show()


    sys.exit(app.exec_())

    # todo implement Qt.WindowSystemMenuHint dropdown menu when clicking on the icon
