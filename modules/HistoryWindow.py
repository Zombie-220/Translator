from PyQt6 import QtWidgets, QtCore, QtGui

from modules.GlobalVariables import CSS, CLOSE_ICON

from modules.SimpleModules import WindowTitleBar, Button

class HistoryWindow(QtWidgets.QMainWindow):
    data : list[str] = 0

    def __init__(self, parent: QtWidgets.QMainWindow):
        QtWidgets.QMainWindow.__init__(self)

        self.parent = parent
        self.title = f"{parent.title} | История"
        self.icon = parent.icon

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.move(10, 10)
        self.setFixedSize(500, 300)

        self.setObjectName("HistoryWindow")
        self.setStyleSheet(CSS)

        windowTitle = WindowTitleBar(self)
        btn_close = Button(self, CLOSE_ICON, self.width() - 30, 0, 30, 30, "btn_red_transp", self.close)
        btn_close.setToolTip("Закрыть окно")

        self.__scrollArea = QtWidgets.QScrollArea(self)
        self.__scrollArea.move(2, windowTitle.height())
        self.__scrollArea.setFixedSize(self. width() - 2, self.height() - windowTitle.height() - 1)
        self.__scrollArea.setObjectName("transpWidget")
        self.__scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__scrollArea.setWidgetResizable(True)
        self.__scrollArea.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__scrollArea.verticalScrollBar().rangeChanged.connect(self.scrollToBottom)

        self.__vBox = QtWidgets.QVBoxLayout()
        self.__vBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.__widget = QtWidgets.QWidget()
        self.__widget.setObjectName("transpWidget")

        self.__widget.setLayout(self.__vBox)
        self.__scrollArea.setWidget(self.__widget)

    def scrollToBottom(self, min, max):
        self.__scrollArea.verticalScrollBar().setValue(max)
