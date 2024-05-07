from PyQt6 import QtWidgets, QtCore, QtGui

from modules.GlobalVariables import CSS, CLOSE_ICON

from modules.SimpleModules import WindowTitleBar, Button

class HistoryWindow(QtWidgets.QMainWindow):
    data : list[str] = 0

    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__()

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

        self.databaseData = self.readDatabase()
        for i in range(len(self.databaseData)):
            if self.databaseData[i] != '':
                self.addHistoryButton(i)

    def scrollToBottom(self, min, max) -> None:
        self.__scrollArea.verticalScrollBar().setValue(max)

    def readDatabase(self) -> list[str]:
        with open("history.txt", "r") as file:
            data = file.read()
            return data.split("\n")
        
    def addToDatabase(self, data: str) -> None:
        self.databaseData.append(data)
        self.addHistoryButton(len(self.databaseData) - 1)

    def addHistoryButton(self, index: int) -> None:
        btnData = self.databaseData[index].split(" - ")
        btnText = f"{btnData[0]} - {btnData[1]}"
        btn = Button(self, btnText, 0, 0, 0, 0, "btn_history", lambda ch, x=index: [self.parent.insertIntoEdit(self.databaseData[x])])
        self.__vBox.addWidget(btn)
        self.__scrollArea.setWidget(self.__widget)

    def saveDatabase(self):
        data = self.databaseData
        if len(data) > 50:
            while len(data) > 50:
                data.pop(0)
        x = ""
        for i in range(len(data)):
            if data[i] != '':
                x += f"{data[i]}\n"
        with open("history.txt", "w") as file:
            file.write(x)
