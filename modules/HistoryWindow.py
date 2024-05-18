from PyQt6 import QtWidgets, QtCore, QtGui
import sqlite3

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

        self.databaseConnect = sqlite3.connect("database.db")
        self.__databaseCursor = self.databaseConnect.cursor()

        self.__databaseData = self.readDatabase()
        for i in self.__databaseData:
            self.addHistoryButton(i[1], i[2])

    def dblClickEvent(self, row, column) -> None:
        self.__databaseCursor.execute('SELECT * FROM history WHERE id = ?', (row+1,))
        data = self.__databaseCursor.fetchone()
        self.parent.insertIntoEdit(f'{data[1]} - {data[2]} - {data[3]}')

    def scrollToBottom(self, min, max) -> None:
        self.__scrollArea.verticalScrollBar().setValue(max)

    def readDatabase(self) -> list[tuple]:
        self.__databaseCursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inputText TEXT NOT NULL,
                outputText TEXT NOT NULL,
                pronun TEXT NOT NULL,
                time INTEGER NOT NULL
            )""")
        self.__databaseCursor.execute("SELECT * FROM history ORDER BY time ASC")
        data = self.__databaseCursor.fetchall()
        return data

    def addDataLine(self, insertedText: str, outputText: str, pronun: str) -> None:
        if pronun != None: temp_pron = pronun
        else: temp_pron = "None"
        
        if len(self.__databaseData) >= 10:
                self.__databaseCursor.execute("""
                    UPDATE history SET inputText=?, outputText=?, pronun=?, time=DATETIME()
                    WHERE id = (SELECT id FROM history ORDER BY time ASC)
                """, (insertedText, outputText, temp_pron))
                self.__scrollArea.removeRow(0)
        else:
            self.__databaseCursor.execute("INSERT INTO history (inputText, outputText, pronun, time) VALUES (?,?,?,DATETIME())",
                                          (insertedText, outputText, temp_pron))
        self.databaseConnect.commit()
        self.addHistoryButton(int(self.__databaseCursor.execute('SELECT COUNT(*) FROM history').fetchone()[0]) - 1)

    def addHistoryButton(self, sourceLang, destLang) -> None:
        self.__scrollArea.insertRow(self.__scrollArea.rowCount())
        firstItem = QtWidgets.QTableWidgetItem(f"{sourceLang}")
        secondItem = QtWidgets.QTableWidgetItem(f"{destLang}")
        self.__scrollArea.setItem(self.__scrollArea.rowCount()-1, 0, firstItem)
        self.__scrollArea.setItem(self.__scrollArea.rowCount()-1, 1, secondItem)

    def closeDatabaseConnect(self) -> None:
        self.databaseConnect.close()