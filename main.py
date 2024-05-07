from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout
import sys, os
from googletrans import Translator

from modules.SimpleModules import *
from modules.GlobalVariables import *

from modules.HistoryWindow import HistoryWindow

class MainWindow(QMainWindow):
    def __init__(self, title: str, icon:QPixmap):
        QMainWindow.__init__(self)
        self.setFixedSize(720, 470)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowIcon(QIcon(APP_ICON))

        self.__windowOnTop = False
        self.title = title
        self.icon = icon
        self.setObjectName("MainWindow")
        self.setStyleSheet(CSS)
        self.setWindowIcon(QIcon(self.icon))

        self.historyWindow = HistoryWindow(self)

        windowTitle = WindowTitleBar(self)
        btn_close = Button(self, CLOSE_ICON, self.width() - 30, 0, 30, 30, "btn_red_transp", self.closeEvent)
        btn_close.setToolTip("Закрыть окно")
        btn_hide = Button(self, HIDE_ICON, self.width() - 60, 0, 30, 30, "btn_standart_transp", self.hide)
        btn_hide.setToolTip("Свернуть окно")
        self.__btn_changeFlag = Button(self, UNFIXED_ICON ,self.width() - 90, 0, 30, 30, "btn_standart_transp", self.changeWindowFlag)
        self.__btn_changeFlag.setToolTip("Закрепить окно")
        btn_openHistoryWindow = Button(self, HISTORY_ICON, self.width() - 120, 0, 30, 30, "btn_standart_transp", self.openHistoryWindow)
        btn_openHistoryWindow.setToolTip("Открыть историю")

        self.__edit_fromLang = TextEdit(self, 5, windowTitle.height() + 5, self.width() - 10, 170, "entryArea")

        btn_rusLang = Button(self, "Русский", 0, 0, 0, 0, "btn_standart", lambda: [self.translate('ru')])
        btn_engLang = Button(self, "Английский", 0, 0, 0, 0, "btn_standart", lambda: [self.translate('en')])
        btn_deuLang = Button(self, "Немецкий", 0, 0, 0, 0, "btn_standart", lambda: [self.translate('de')])
        btn_japLang = Button(self, "Японский", 0, 0, 0, 0, "btn_standart", lambda: [self.translate('ja')])
        btn_clear = Button(self, "Очистить", 0, 0, 0, 0, "btn_red", self.clearEditArea)
        labelForButtons = Label(self, 5, self.__edit_fromLang.pos().y() + self.__edit_fromLang.height() + 5, self.width() - 10, 40, "label", "")
        vBox = QHBoxLayout()
        vBox.addWidget(btn_rusLang)
        vBox.addWidget(btn_engLang)
        vBox.addWidget(btn_deuLang)
        vBox.addWidget(btn_japLang)
        vBox.addWidget(btn_clear)
        labelForButtons.setLayout(vBox)

        self.__edit_toLang = TextEdit(self, 5, labelForButtons.pos().y() + labelForButtons.height() + 5, self.width() - 10, 170, "entryArea")
        self.__edit_pron = TextEdit(self, 5, self.__edit_toLang.pos().y() + self.__edit_toLang.height() + 5, self.width() - 10, 30, "entryArea")

    def closeEvent(self, event) -> None:
        self.historyWindow.close()
        self.close()
        self.historyWindow.saveDatabase()

    def openHistoryWindow(self) -> None:
        if self.historyWindow.isVisible():
            self.historyWindow.hide()
        else:
            self.historyWindow.show()

    def changeWindowFlag(self) -> None:
        self.__windowOnTop = not self.__windowOnTop
        self.hide()
        if self.__windowOnTop:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            self.__btn_changeFlag.setToolTip("Открепить окно")
            self.__btn_changeFlag.setIcon(FIXED_ICON)
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.__btn_changeFlag.setToolTip("Закрепить окно")
            self.__btn_changeFlag.setIcon(UNFIXED_ICON)
        self.show()

    def clearEditArea(self) -> None:
        self.__edit_fromLang.clear()
        self.__edit_toLang.clear()
        self.__edit_pron.clear()

    def insertIntoEdit(self, data: str) -> None:
        self.clearEditArea()
        temp_data = data.split(" - ")
        self.__edit_fromLang.setPlainText(temp_data[0])
        self.__edit_toLang.setPlainText(temp_data[1])
        try:
            if temp_data[2] != "None":
                self.__edit_pron.setPlainText(temp_data[2])
        except Exception as ex: print(ex)

    def translate(self, dest_lang) -> None:
        txt = self.__edit_fromLang.toPlainText()
        if txt != '':
            try:
                translatedText = trn.translate(txt, dest=dest_lang)
            except Exception as exp:
                translatedText = f"Что-то пошло не так >_<\n{exp}"

            self.__edit_toLang.setPlainText(translatedText.text)
            self.__edit_pron.setPlainText(translatedText.pronunciation)
            self.historyWindow.addToDatabase(f"{txt} - {translatedText.text} - {translatedText.pronunciation}")

        else:
            self.__edit_toLang.setPlainText("Там нечего переводить, хехе")

if __name__ == "__main__":
    trn = Translator()
    app = QApplication(sys.argv)
    window = MainWindow("Переводчик", APP_ICON)
    window.show()
    sys.exit(app.exec())