from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication
import sys, os

app = QApplication(sys.argv)

APP_ICON = QPixmap(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\APP_ICON.png').scaled(30,30,transformMode=Qt.TransformationMode.SmoothTransformation)

CLOSE_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\CLOSE.png')

HIDE_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\HIDE.png')

FIXED_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\FIXED.png')

UNFIXED_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\UNFIXED.png')

HISTORY_ICON = QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\HISTORY.png')

CSS = '''
    #TitleBar {
        background-color: rgb(21, 21, 21);
        color: #FFF;
        font: 14px;
    }
    #MainWindow, QToolTip, #HistoryWindow, #btn_history {
        background-color: rgb(40, 40, 40);
        border: 1px solid rgb(21, 21, 21);
    }
    * {
        color: rgb(240, 240, 240);
        font-size: 14px;
    }
    QToolTip {
        font-size: 12px;
    }


    #btn_red_transp {
        background-color: rgba(200,0,0,0);
        border: 0px;
    }
    #btn_red_transp::hover {
        background-color: rgba(200,0,0,0.4);
    }
    #btn_red_transp::pressed {
        background-color: rgba(200,0,0,0.8);
    }
    #btn_standart_transp {
        background-color: rgba(60,60,60,0);
        border: 0px;
    }
    #btn_standart_transp::hover {
        background-color: rgba(60,60,60,0.4);
    }
    #btn_standart_transp::pressed {
        background-color: rgba(60,60,60,0.8);
    }
    #btn_standart {
        background-color: rgba(60,60,60,1);
        border: 0px;
        border-radius: 5px;
    }
    #btn_standart::hover {
        background-color: rgba(60,60,60,0.6);
    }
    #btn_standart::pressed {
        background-color: rgba(60,60,60,0.3);
    }
    #btn_red {
        background-color: rgba(200,0,0,1);
        border: 0px;
        border-radius: 5px;
    }
    #btn_red::hover {
        background-color: rgba(200,0,0,0.6);
    }
    #btn_red::pressed {
        background-color: rgba(200,0,0,0.3);
    }


    #entryArea {
        background-color: rgb(60,60,60);
        border: 0px;
        border-radius: 5px;
        color: rgb(255,255,255);
        selection-background-color: rgba(255,255,255,0.5);
    }
    #transpWidget {
        background-color: rgba(0,0,0,0);
        border: 0px;
    }


    #test {
        background-color: rgba(255,255,255,0);
        border: 1px solid rgb(255,0,0);
    }


    QScrollBar:vertical {
        background-color: rgba(0, 0, 0, 0);
        width: 7px;
    }
    QScrollBar::handle:vertical {
        background-color: rgb(40, 40, 40);
        border: 1px solid rgb(21, 21, 21);
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background-color: rgb(21, 21, 21);
    }    
'''