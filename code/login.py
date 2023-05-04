import sys
import os
import typing

import PyQt5.sip

from PyQt5 import QtGui
from PyQt5 import QtCore
from pes import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec_())