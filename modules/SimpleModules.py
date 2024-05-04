from PyQt6 import QtWidgets, QtGui, QtCore

class Button(QtWidgets.QPushButton):
    def __init__(self, parent: QtWidgets.QMainWindow, content: str | QtGui.QIcon,
                 x: int, y: int, width: int, height: int,
                 objectName: str, func = None):
        
        QtWidgets.QPushButton.__init__(self, parent)
        
        self.setGeometry(x, y, width, height)
        self.setObjectName(objectName)

        if type(content) == str:
            self.setText(content)
        elif type(content) == QtGui.QIcon:
            self.setIcon(content) 

        if func != None:
            self.clicked.connect(func)



class Label(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QMainWindow,
                 x: int, y: int, width: int, height: int,
                 objectName: str, content: str | QtGui.QPixmap):
        
        QtWidgets.QLabel.__init__(self, parent)
        
        self.setGeometry(x, y, width, height)
        self.setObjectName(objectName)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        if type(content) == str:
            self.setText(content)
        elif type(content) == QtGui.QPixmap:
            self.setPixmap(content)



class Entry(QtWidgets.QLineEdit):
    def __init__(self, parent: QtWidgets.QMainWindow,
                 x: int, y: int, width: int, height: int,
                 placeholder: str, readOnly: bool, objectName: str):
        QtWidgets.QLineEdit.__init__(self, parent)

        self.setGeometry(x, y, width, height)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(objectName)
        self.setPlaceholderText(placeholder)

        if readOnly:
            self.setReadOnly(True)
        else:
            self.setReadOnly(False)



class TextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, parent: QtWidgets.QMainWindow,
                 x: int, y: int, width: int, height: int,
                 objectName: str):
        QtWidgets.QPlainTextEdit.__init__(self, parent)
        self.setFixedSize(width, height)
        self.move(x, y)
        self.setObjectName(objectName)



class WindowTitleBar(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QMainWindow) -> None:

        QtWidgets.QLabel.__init__(self, parent)
        
        self.icon = parent.icon

        self.parent = parent
        self.resize(parent.width(), 30)
        self.move(0,0)
        self.setObjectName("TitleBar")

        labelLogo = QtWidgets.QLabel(self)
        labelLogo.setPixmap(self.icon)
        labelLogo.setFixedSize(30,30)
        labelName = QtWidgets.QLabel(parent.title, self)
        labelName.setGeometry(35, 0, parent.width(), 30)
        labelName.setObjectName("label")

    def mousePressEvent(self, LeftButton) -> None:
        self.pos = LeftButton.pos()
        self.main_pos = self.parent.pos()

    def mouseMoveEvent(self, LeftButton) -> None:
        self.last_pos = LeftButton.pos() - self.pos
        self.main_pos += self.last_pos
        self.parent.move(self.main_pos)