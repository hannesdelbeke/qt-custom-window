from pathlib import Path
from qt_custom_window.window import FramelessWindow
from qt_custom_window.titlebar import TitleBar
# from qt_custom_window.qt_manager import QtGui, QtCore, QtWidgets
import qt_custom_window.qt_manager
QtCore = qt_custom_window.qt_manager.QtCore
QtGui = qt_custom_window.qt_manager.QtGui
QtWidgets = qt_custom_window.qt_manager.QtWidgets
QWidget = QtWidgets.QWidget


class TitleBarUnreal(TitleBar):
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


class FramelessWindowUnreal(FramelessWindow):
    default_title_bar = TitleBarUnreal


def wrap_widget_unreal(widget: QWidget) -> FramelessWindowUnreal:
    """helper function to wrap a widget in a frameless window with a custom title bar"""
    # wrap widget in a frameless window
    window = FramelessWindowUnreal()
    window.wrap_widget(widget)
    return window
