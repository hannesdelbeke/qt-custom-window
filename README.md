# qt-custom-window
a customisable "frameless" window with move resize etc, no dependencies, and support for pyqt4 pyqt5 pyqt6 pyside2 pyside pyside6. make your own titlebar

# goals
- easy option to create custom titlebars (e.g. for dark themes)
- no dependencies (such as pywin32 in most other frameless windows)
- simple, to avoid advanced features like aero raising errors in Unreal or Maya
- support for pyqt4 pyqt5 pyqt6 pyside2 pyside pyside6
- stick to the qt docs. overloading existing methods from the QtWidget. 
- use windowsflags to control the window just like in qt

## credits
- used resize code from Jung Gyu Yoon [pyqt-frameless-window](https://github.com/yjg30737/pyqt-frameless-window) (added dev as commit author)
