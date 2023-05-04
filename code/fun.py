import sys
  
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QPen)
from PySide2.QtWidgets import *
  
#IMPORT PYSIDE2EXTN WIDGET YOU USED IN THE QTDESIGNER FOR DESIGNING.
from PySide2extn.RoundProgressBar import roundProgressBar
import qdarkstyle
#UI FILE CONVERTED FROM .ui to python file ui.py
from app import *   

  
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

        self.show()
  
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())





    net_worker=Worker(self.network)

		net_worker.signals.result.connect(self.print_output)
		net_worker.signals.finished.connect(self.thread_complete)
		net_worker.signals.progress.connect(self.progress_fn)

		self.threadpool.start(net_worker)