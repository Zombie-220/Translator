from PyQt6 import QtWidgets, QtCore, QtGui

from modules.GlobalVariables import CSS, CLOSE_ICON

from modules.SimpleModules import WindowTitleBar, Button

class HistoryWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__()
        self.parent = parent
        self.title = f"{parent.title} | История"
        self.icon = parent.icon

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.move(50, 50)
        self.setFixedSize(parent.width(), parent.height())

        self.setObjectName("HistoryWindow")
        self.setStyleSheet(CSS)

        windowTitle = WindowTitleBar(self)
        btn_close = Button(self, CLOSE_ICON, self.width() - 30, 0, 30, 30, "btn_red_transp", self.close)
        btn_close.setToolTip("Закрыть окно")

        self.__scrollArea = QtWidgets.QTableWidget(0, 2, self)
        self.__scrollArea.move(2, windowTitle.height())
        self.__scrollArea.setFixedSize(self. width() - 2, self.height() - windowTitle.height() - 1)
        self.__scrollArea.verticalHeader().setVisible(False)
        self.__scrollArea.horizontalHeader().setVisible(False)
        self.__scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__scrollArea.setColumnWidth(0, int((self.__scrollArea.width() * 49.5) // 100))
        self.__scrollArea.setColumnWidth(1, int((self.__scrollArea.width() * 49.5) // 100))
        self.__scrollArea.setObjectName("transpWidget")
        self.__scrollArea.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.__scrollArea.horizontalHeader().setStretchLastSection(True)
        self.__scrollArea.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.__scrollArea.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.__scrollArea.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__scrollArea.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.__scrollArea.cellDoubleClicked.connect(self.dblClickEvent)

        self.databaseData = self.readDatabase()
        for i in range(len(self.databaseData)):
            if self.databaseData[i] != '':
                self.addHistoryButton(i)
        self.databaseData.pop(len(self.databaseData) - 1)

    def dblClickEvent(self, row, column) -> None:
        self.parent.insertIntoEdit(self.databaseData[row])

    def scrollToBottom(self, min, max) -> None:
        self.__scrollArea.verticalScrollBar().setValue(max)

    def readDatabase(self) -> list[str]:
        with open("history.txt", "r") as file:
            data = file.read()
            return data.split("\n")

    def addDataLine(self, data: str) -> None:
        self.databaseData.append(data)
        self.addHistoryButton(len(self.databaseData) - 1)

    def addHistoryButton(self, index: int) -> None:
        data = self.databaseData[index].split(" - ")
        self.__scrollArea.insertRow(self.__scrollArea.rowCount())
        firstItem = QtWidgets.QTableWidgetItem(f"{data[0]}")
        firstItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        secondItem = QtWidgets.QTableWidgetItem(f"{data[1]}")
        secondItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.__scrollArea.setItem(self.__scrollArea.rowCount()-1, 0, firstItem)
        self.__scrollArea.setItem(self.__scrollArea.rowCount()-1, 1, secondItem)

    def saveDatabase(self) -> None:
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