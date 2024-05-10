from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QMainWindow, QApplication, QWidget, QPlainTextEdit
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import sys, os
from googletrans import Translator

class Button(QPushButton):
    def __init__(self, parent:QWidget, width:int, height:int, x_move:int, y_move:int, content:str|QIcon, objectName:str, command=None):
        QPushButton.__init__(self,parent)
        self.setFixedSize(width,height)
        self.move(x_move,y_move)
        self.setObjectName(objectName)
        if type(content) == str:
            self.setText(content)
        elif type(content) == QIcon:
            self.setIcon(content)
        if command != None:
            self.clicked.connect(command)

class Label(QLabel):
    def __init__(self,parent, width:int, height:int, x_move:int, y_move:int, text:str):
        QLabel.__init__(self,parent)
        self.setText(text)
        self.setFixedSize(width,height)
        self.move(x_move,y_move)

class Entry(QPlainTextEdit):
    def __init__(self,parent, width:int, height:int, x_move:int, y_move:int):
        QPlainTextEdit.__init__(self,parent)
        self.setFixedSize(width,height)
        self.move(x_move,y_move)

class WindowTopHat(QLabel):
    css = '''
    * {
        background-color: rgb(21,21,21);
        color: #FFF;
        font: 14px;
    }
    '''
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.icon = QPixmap(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\icon.png').scaled(30,30,transformMode=Qt.TransformationMode.SmoothTransformation)
        self.parent=parent
        self.resize(parent.width(), 32)
        self.move(0,0)
        self.setStyleSheet(self.css)

        self.labelLogo = QLabel(self)
        self.labelLogo.setPixmap(self.icon)
        self.labelLogo.setFixedSize(35,32)
        self.labelName = Label(self,parent.width(),32,35,0,'Переводчик')

    def mousePressEvent(self, LeftButton):
        self.pos = LeftButton.pos()
        self.main_pos = self.parent.pos()

    def mouseMoveEvent(self, LeftButton):
        self.last_pos = LeftButton.pos() - self.pos
        self.main_pos += self.last_pos
        self.parent.move(self.main_pos)

class TranscriptionLine(QLabel):
    def __init__(self, parent, name:str, y_move:int):
        QLabel.__init__(self,parent)
        self.chek(name)
        self.move(15, y_move - self.height() + 4)
        self.setText(f'{name} язык')
        self.setFixedSize(150,28)
        self.setStyleSheet(parent.css)

        self.ent = Entry(parent, parent.width()-182, 92, 10, y_move)
        self.trnTo = Label(parent, 150, 30, parent.width()-160, y_move-30, 'Перевести на:')
        self.trnTo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_Clear = Button(parent, 75, 20, parent.width()-247, y_move - self.height() + 4, self.names[3], 'btn_light_red', self.ent.clear)
        self.btn0 = Button(parent, 150, 30, parent.width()-160, y_move, self.names[0], 'btn_ligth_grey')
        self.btn1 = Button(parent, 150, 30, parent.width()-160, y_move+31, self.names[1], 'btn_ligth_grey')
        self.btn2 = Button(parent, 150, 30, parent.width()-160, y_move+62, self.names[2], 'btn_ligth_grey')

    def chek(self, name):
        if name == 'Русский':
            self.names = ['Английский', 'Немецкий', 'Японский', 'Очистить']
        elif name == 'Английский':
            self.names = ['Русский', 'Немецкий', 'Японский', 'Очистить']
        elif name == 'Немецкий':
            self.names = ['Русский', 'Английский', 'Японский', 'Очистить']
        elif name == 'Японский':
            self.names = ['Русский', 'Английский', 'Немецкий', 'Очистить']

class MainWindow(QMainWindow):
    css = '''
    QMainWindow {
        background: rgb(38,38,38);
        border: 2px solid rgb(21,21,21);
    }
    QLabel {
        color: #FFF;
        font-size: 16px;
    }
    Entry, QLineEdit {
        color: #FFF;
        font-size: 16px;
        background: rgb(50,50,50);
        border-radius: 5px;
        padding: 0px 5px 0px;
        border: 1px solid rgb(21,21,21);
        selection-background-color: rgb(21,21,21);
    }
    #btn_light_red {
        background: rgba(200,0,0,1);
        border-radius: 5px;
        border: 1px solid rgb(21,21,21);
    }
    #btn_light_red:hover {
        background: rgba(200,0,0,0.7);
    }
    #btn_light_red:pressed {
        background: rgba(200,0,0,0.4);
    }
    #btn_ligth_grey {
        background: rgba(50,50,50,1);
        color: rgb(255,255,255);
        border-radius: 5px;
        border: 1px solid rgb(21,21,21);
    }
    #btn_ligth_grey:hover {
        background: rgba(50,50,50,0.7);
    }
    #btn_ligth_grey:pressed {
        background: rgba(50,50,50,0.4);
    }
    QScrollBar:vertical {
        background: #151515;
        width: 7px;
    }
    QScrollBar::handle:vertical {
        background: rgba(255,255,255,1);
        border-radius: 3px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: #151515;
    }
    '''
    def __init__(self, translator:Translator):
        QMainWindow.__init__(self)
        self.icon = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\icon.png')
        self.fixed_btn = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\office_button.png')
        self.unfixed_btn = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\no_office_button.png')
        self.close_icon = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\close.png')
        self.hide_icon = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\hide.png')

        self.screenSize = QApplication.primaryScreen().availableGeometry()
        self.setGeometry((self.screenSize.width()//2)-(self.width()//2), (self.screenSize.height()//2)-(self.height()//2), 700, 565)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle('Переводчик')
        self.setWindowIcon(self.icon)
        self.setStyleSheet(self.css)

        self.hat = WindowTopHat(self)
        self.btnClose = Button(self,28,28,self.width()-30,2,self.close_icon,'btn_light_red',self.close)
        self.btnClose.setIconSize(QSize(12,12))
        self.btnHide = Button(self, 28,28,self.width()-60,2,self.hide_icon,'btn_ligth_grey',self.showMinimized)
        self.btnHide.setIconSize(QSize(20,20))
        self.btnFixed = Button(self,28,28,self.width()-90,2,self.unfixed_btn,'btn_ligth_grey',self.fix_unfix)

        self.trn_line1 = TranscriptionLine(self, 'Русский',65)
        self.trn_line2 = TranscriptionLine(self, 'Английский',197)
        self.trn_line3 = TranscriptionLine(self, 'Немецкий',329)

        self.trn_line4 = TranscriptionLine(self, 'Японский',461)
        self.trn_line4.ent.setFixedSize(self.trn_line4.ent.width(), 62)
        self.jap_lab = Label(self, 150,25,15,self.height()-37,'Произношение:')
        self.jap_pron = QLineEdit(self)
        self.jap_pron.setFixedSize(self.width()-332, 28)
        self.jap_pron.move(self.width()-540, self.height()-40)
        self.trn_line4.btn_Clear.clicked.connect(self.jap_pron.clear)

        self.trn_line1.btn0.clicked.connect(lambda: [self.translate(self.trn_line1.ent, 'en','ru')])
        self.trn_line1.btn1.clicked.connect(lambda: [self.translate(self.trn_line1.ent, 'de','ru')])
        self.trn_line1.btn2.clicked.connect(lambda: [self.translate(self.trn_line1.ent, 'ja','ru')])
        self.trn_line2.btn0.clicked.connect(lambda: [self.translate(self.trn_line2.ent, 'ru','en')])
        self.trn_line2.btn1.clicked.connect(lambda: [self.translate(self.trn_line2.ent, 'de','en')])
        self.trn_line2.btn2.clicked.connect(lambda: [self.translate(self.trn_line2.ent, 'ja','en')])
        self.trn_line3.btn0.clicked.connect(lambda: [self.translate(self.trn_line3.ent, 'ru','de')])
        self.trn_line3.btn1.clicked.connect(lambda: [self.translate(self.trn_line3.ent, 'en','de')])
        self.trn_line3.btn2.clicked.connect(lambda: [self.translate(self.trn_line3.ent, 'ja','de')])
        self.trn_line4.btn0.clicked.connect(lambda: [self.translate(self.trn_line4.ent, 'ru','ja')])
        self.trn_line4.btn1.clicked.connect(lambda: [self.translate(self.trn_line4.ent, 'en','ja')])
        self.trn_line4.btn2.clicked.connect(lambda: [self.translate(self.trn_line4.ent, 'de','ja')])

    def translate(self, text_label, dest_language, lang):
        txt = text_label.toPlainText()
        try:
            if dest_language == "ru":
                self.trn_line1.ent.setPlainText(myTranslator.translate(txt, src=lang, dest=dest_language).text)
            elif dest_language == "en":
                self.trn_line2.ent.setPlainText(myTranslator.translate(txt, src=lang, dest=dest_language).text)
            elif dest_language == "de":
                self.trn_line3.ent.setPlainText(myTranslator.translate(txt, src=lang, dest=dest_language).text)
            elif dest_language == "ja":
                self.trn_line4.ent.setPlainText(myTranslator.translate(txt, src=lang, dest=dest_language).text)
                self.jap_pron.setText(myTranslator.translate(txt, src=lang, dest=dest_language).pronunciation)
        except Exception as exp:
            text_label.setPlainText(str(exp))

    def fix_unfix(self):
        if self.windowFlags() == 2049:
            self.hide()
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            self.btnFixed.setIcon(self.fixed_btn)
            self.show()
        else:
            self.hide()
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            self.btnFixed.setIcon(self.unfixed_btn)
            self.show()

if __name__ == '__main__':
    myTranslator = Translator()

    app = QApplication(sys.argv)
    window = MainWindow(myTranslator)
    window.show()
    sys.exit(app.exec())

# cd Desktop\Python\translator && pyinstaller -w -F -i"images\icon.ico" main.py