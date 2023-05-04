import shutil
import sys
import os
from PySide2 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qt_material import *
import psutil
import PySide2extn
from multiprocessing import cpu_count
import datetime
import platform
import speedtest
import GPUtil
from PySide2 import QtCore, QtGui, QtWidgets
from tabulate import tabulate
from time import sleep
# UI FILE CONVERTED FROM .ui to python file ui.py

from MAINUI import *

platforms = {'linux': 'Linux','linux1':'Linux','linux2':'Linux','darwin':'OS X','win32': 'Windows'}


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        apply_stylesheet(app, theme='dark_blue.xml')
        win = self.ui.centralwidget
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        '''self.setWindowFlags(QtCore.Qt.FramelessWindowHint)'''
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(3)
        self.shadow.setYOffset(3)
        self.shadow.setColor(QtGui.QColor(0, 92, 157, 550))

        win.setGraphicsEffect(self.shadow)

        self.setWindowIcon(QtGui.QIcon(":/Black/Icons/white/airplay.svg"))

        self.setWindowTitle("HEATSINK")
        QSizeGrip(self.ui.size_grip)
        # minimize window
        self.ui.Minimize_window_button.clicked.connect(
            lambda: self.showMinimized())

        # close window
        self.ui.Close_window_button.clicked.connect(lambda: self.close())

        # restore/maximize window
        self.ui.Restore_window_button.clicked.connect(
            lambda: self.resize_win())

        # Navigation#################################
        self.ui.CPU_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_bat))
        self.ui.RAM_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.memory))
        self.ui.Disk_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.rom))
        self.ui.Wifi_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.network))
        self.ui.GPU_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.gpu))
        self.ui.System_info.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.system_info))
        self.ui.act_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.activity))
        self.ui.sensor_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sensor))
        self.ui.battery_btn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.battery))

        # move bar
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        self.ui.Header_frame.mouseMoveEvent = moveWindow

        self.ui.menu.clicked.connect(lambda: self.slideLeftMenu())

        self.show()

        self.battery()
        self.cpu()
        self.memory()
        self.system_info()
        self.activity()
        self.storage()
        self.sensor()
        self.network()
        self.gpu()


    # all functions below
    # left slide

    def slideLeftMenu(self):

        # Get current left menu width

        width = self.ui.Left_menu_cont_frame.width()

        # If minimized

        if width == 110:

            # Expand menu

            newWidth = 300

        # If maximized

        else:

            # Restore menu

            newWidth = 110

        # Animate the transition

        self.animation = QPropertyAnimation(
            self.ui.Left_menu_cont_frame, b"minimumWidth")  # Animate minimumwidht
        self.animation.setDuration(250)
        # Start value is the current menu width
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    # mouse events
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    # minimized

    def resize_win(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.Restore_window_button.setIcon(
                QtGui.QIcon(u":/Black/Icons/white/plus-square.svg"))
        else:
            self.showMaximized()
            self.ui.Restore_window_button.setIcon(
                QtGui.QIcon(u":/Black/Icons/white/minus-square.svg"))

    # cpu and ram info
    ##########################################################################################
    ##########################################################################################
    def cpu(self):

        while True:
            core = cpu_count()
            self.ui.cpu_count.setText(str(core))

            cpuPer = psutil.cpu_percent()
            self.ui.cpu_per.setText(str(cpuPer)+" %")

            cpuMainCore = psutil.cpu_count(logical=False)
            self.ui.cpu_main_core.setText(str(cpuMainCore))


            # self.ui.cpu_percentage.rpb_setMaximum(100)
            # self.ui.cpu_percentage.rpb_setValue(cpuPer)
            # self.ui.cpu_percentage.rpb_setBarStyle('Hybrid2')
            # self.ui.cpu.percentage.rpb_setLineColor((255, 30, 99))
            # self.ui.cpu.percentage.rpb_setPieColor((45, 74, 83))
            # self.ui.cpu.percentage.rpb_setTextColor((255, 255, 255))
            # self.ui.cpu.percentage.rpb_setInitialPos('West')
            # self.ui.cpu.percentage.rpb_setTextFormat('Percentage')
            # self.ui.cpu.percentage.rpb_setTextFont('Arial')
            # self.ui.cpu.percentage.rpb_setLineWidth(15)
            # self.ui.cpu.percentage.rpb_setPathWidth(15)
            # self.ui.cpu_percentage.rpb_setLineCap('RoundCap')
            #
            # # setting min val
            # self.ui.ram_percentage.spb_setMinimum((0, 0, 0))
            #
            # # setting max value
            # self.ui.ram_percentage.spb_setMaximum((totalRam, totalRam, totalRam))
            #
            # # setting progress val
            # self.ui.ram_percentage.spb_setsetValue((availRam, ramUsed, ramFree))
            #
            # # set progress color
            # self.ui.ram_percentage.spb_lineColor(
            #     ((6, 233, 38), (6, 201, 38), (233, 6, 201)))
            #
            # self.ui.ram_percentage.spb_setInitialPos(('West', 'West', 'West'))
            #
            # self.ui.ram_percentage.spb_linewidth(15)
            # self.ui.ram_percentage.spb_setGap(15)
            # self.ui.ram_percentage.spb_LineStylep(
            #     ('SolidLine', 'SolidLine', 'SolidLine'))
            # self.ui.ram_percentage.spb_LineCap(
            #     ('RoundCap', 'RoundCap', 'RoundCap'))
            #
            # # hide the path
            # self.ui.ram_percentage.spb_setPathHidden(True)

            sleep(1)


    ##########################################################################################
    ##########################################################################################
        # system information

    def system_info(self):
            time = datetime.datetime.now().strftime("%I,%M,%S,%p")
            self.ui.system_date.setText(str(time))
            date = datetime.datetime.now().strftime("%Y-%m-%D")
            self.ui.system_time.setText(str(date))

            self.ui.system_machine.setText(platform.machine())
            self.ui.system_version.setText(platform.version())
            self.ui.system_platform.setText(platform.platform())
            self.ui.system_sytem.setText(platform.system())
            self.ui.system_processor.setText(platform.processor())

    ##########################################################################################
    ##########################################################################################

    # memory
    def memory(self):
        while True:
            totalRam = 1.0
            totalRam = psutil.virtual_memory()[0] * totalRam
            totalRam = totalRam / (1024 * 1024 * 1024)
            self.ui.total_ram.selfText(str("{:.4f}".format(availRam) + 'GB'))

            availRam = 1.0
            availRam = psutil.virtual_memory()[1] * availRam
            availRam = availRam / (1024 * 1024 * 1024)
            self.ui.available_ram.setText(str("{:.4f}".format(availRam)+'GB'))

            ramUsed = 1.0
            ramUsed = psutil.virtual_memory()[3] * ramUsed
            ramUsed = ramUsed / (1024 * 1024 * 1024)
            self.uiused_ram.setText(str("{:.4F}".format(ramUsed) + 'GB'))

            ramFree = 1.0
            ramFree = psutil.virtual_memory()[4] * ramFree
            ramFree = ramFree / (1024 * 1024 * 1024)
            self.ui.free_ram.setText(str("{:.4f}".format(ramFree)+'GB'))

            ramUsages = str(psutil.virtual_memory()[2]) + '%'
            self.ui.ram_usage.setText(str("{:.4f}".format(totalRam) + 'GB'))

            sleep(1)

    ##########################################################################################
    ##########################################################################################
    #GPU
    def gpu(self):
        gpus = GPUtil.getGPUs()
        while True:
            for x in gpus:
                load=x.load*100
                self.ui.loadd.setText(str(load))

                free_memory=x.memoryFree
                self.ui.freememory.setText(str(free_memory))

                total_memory = x.memoryTotal
                self.ui.totalmemory.setText(str(total_memory))

                used_memory = x.memoryUsed
                self.ui.usedmemory.setText(str(used_memory))

                temp = x.temperature
                self.ui.temperature.setText(str(temp))

                sleep(1)




    ##########################################################################################
    ##########################################################################################
    #network
    def network(self):
        speed_test = speedtest.Speedtest()

        while True:

            def bytes_to_mb(bytes):
                KB = 1024  # One Kilobyte is 1024 bytes
                MB = KB * 1024  # One MB is 1024 KB
                return int(bytes / MB)

            download_speed=bytes_to_mb(speed_test.download())
            self.ui.downloadspeed.setText(str(download_speed))

            upload_speed = bytes_to_mb(speed_test.upload())
            self.ui.upspeed.setText(str(upload_speed))

            total_speed = download_speed+upload_speed
            self.ui.totalspeed.setText(str(total_speed))

            sleep(1)

    ##########################################################################################
    ##########################################################################################
    #activity

    def create_table_widget(self,rowPosition,columnPosition,text,tableName):
            qtablewidgetitem=QTableWidgetItem()
            getattr(self.ui,tableName).setItem(rowPosition,columnPosition,qtablewidgetitem)
            qtablewidgetitem = getattr(self.ui,tableName).item(rowPosition,columnPosition)
            qtablewidgetitem.setText(text);

    def activity(self):
            for x in psutil.pids():
                rowPosition=self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rowPosition)
            try:
                process = psutil.Process(x)

                self.create_table_widget(rowPosition,0,str(process.pid),"tableWidget")
                self.create_table_widget(rowPosition, 1, str(process.name()), "tableWidget")
                self.create_table_widget(rowPosition, 2, str(process.status()), "tableWidget")
                self.create_table_widget(rowPosition, 3, str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S")), "tableWidget")


                suspend_btn=QPushButton(self.ui.tableWidget)
                suspend_btn.setText('Suspend')
                suspend_btn.setStyleSheet("color : brown")
                self.ui.tableWidget.setCellWidget(rowPosition,4,suspend_btn)

                resume_btn = QPushButton(self.ui.tableWidget)
                resume_btn.setText('Resume')
                resume_btn.setStyleSheet("color:green")
                self.ui.tableWidget.setCellWidget(rowPosition,6,resume_btn)

                terminate_btn = QPushButton(self.ui.tableWidget)
                terminate_btn.setText('Terminate')
                terminate_btn.setStyleSheet("color:orange")
                self.ui.tableWidget.setCellWidget(rowPosition, 5, terminate_btn)

                kill_btn = QPushButton(self.ui.tableWidget)
                kill_btn.setText('Kill')
                kill_btn.setStyleSheet("color:red")
                self.ui.tableWidget.setCellWidget(rowPosition, 7, kill_btn)
            except Exception as e:
                print(e)

            self.ui.activity_search.textChanged.connect(self.findName)

    def findName(self):
        name=self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            item=self.ui.tableWidget.item(row,1)
            self.ui.tableWidget.setRowHidden(row,name not in item.text().lower())

    ##########################################################################################
    ##########################################################################################
    #sensors
    def sensor(self):
        if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform=='linux2':
            for x in psutil.sensors_temperatures():
                for y in psutil.sensors_temperatures()[x]:
                    rowPosition = self.ui.sensor_table.rowCount()
                    self.ui.sensor_table.insertRow(rowPosition)
                    self.create_table_widget(rowPosition,0,x,"sensor_table")
                    self.create_table_widget(rowPosition, 1, y.label, "sensor_table")
                    self.create_table_widget(rowPosition, 2, str(y.current), "sensor_table")
                    self.create_table_widget(rowPosition, 3, str(y.high), "sensor_table")
                    self.create_table_widget(rowPosition, 4, str(y.critical), "sensor_table")

                    temp_per=(y.current/y.high)*100
                    progressBar = QProgressBar(self.ui.sensor_table)
                    progressBar.setObjectName(u"progressBar")
                    progressBar.setValue(temp_per)
                    self.ui.sensor_table.setCellWidget(rowPosition,5,progressBar)
        else:
            global platforms
            rowPosition=self.ui.sensor_table.rowCount()
            self.ui.sensor_table.insertRow(rowPosition)

            self.create_table_widget(rowPosition,0,"Function not supported on"+platforms[sys.platform],"sensor_table")
            self.create_table_widget(rowPosition, 1, "N/A" + platforms[sys.platform],"sensor_table")
            self.create_table_widget(rowPosition, 2, "N/A" + platforms[sys.platform], "sensor_table")
            self.create_table_widget(rowPosition, 3, "N/A" + platforms[sys.platform], "sensor_table")
            self.create_table_widget(rowPosition, 4, "N/A" + platforms[sys.platform], "sensor_table")
            self.create_table_widget(rowPosition, 5, "N/A" + platforms[sys.platform], "sensor_table")



    ##########################################################################################
    ##########################################################################################

    #storage
    def storage(self):
        global platforms
        storage_device=psutil.disk_usage(all=False)
        z=0
        for x in storage_device:
            rowPosition=self.ui.storageTable.rowCount()
            self.ui.storageTable.insertRow(rowPosition)
            self.create_table_widget(rowPosition,0,x.device,"storageTable")
            self.create_table_widget(rowPosition, 1, x.mountpoint, "storageTable")
            #self.create_table_widget(rowPosition, 3, x.opts, "storageTable")
            self.create_table_widget(rowPosition, 2, x.fstype, "storageTable")

        if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform=='linux2':
            self.create_table_widget(rowPosition, 3,str(x.maxfile), "storageTable")
            self.create_table_widget(rowPosition, 4, str(x.maxpath), "storageTable")
        else:
            self.create_table_widget(rowPosition,3,"Function not available on "+ platforms[sys.platform],"storageTable")
            self.create_table_widget(rowPosition, 4, "Function not available on " + platforms[sys.platform],
                                     "storageTable")
        disk_usage = shutil.disk_usage(x.mountpoint)
        self.create_table_widget(rowPosition,5,str((disk_usage.total/(1024*1024*1024)))+"GB","storageTable")
        self.create_table_widget(rowPosition, 6, str((disk_usage.used / (1024 * 1024 * 1024))) + "GB", "storageTable")
        self.create_table_widget(rowPosition, 7, str((disk_usage.free/ (1024 * 1024 * 1024))) + "GB", "storageTable")

        # full_disk = (disk_usage.used/disk_usage.total)*100
        # progressBar = QProgressBar(self.ui.storageTable)
        # progressBar=setObjectName(u"progressBar")
        # progressBar.setValue(full_disk)
        # self.ui.storageTable.setCellWidget(rowPosition,9,progressBar)

    ##########################################################################################
    ##########################################################################################

    def secs2hours(self, secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d (H:M:S)" % (hh, mm, ss)

    # battery info
    def battery(self):
        while True:
            batt = psutil.sensors_battery()
            if not hasattr(psutil,"sensors_battery"):
                    self.ui.battery_status.setText("Platform not supported")

            if batt is None:
                    self.ui.battery_status.setText("No battery installed")

            if batt.power_plugged:
                    self.ui.battery_charge.setText(str(round(batt.percent, 2))+"%")
                    self.ui.battery_time_left.setText("N/A")
                    if batt.percent < 100:
                        self.ui.battery_status.setText("Charging")
                    else:
                        self.ui.battery_status.setText("Fully Charged")
                    self.ui.battery_plugged.setText("Yes")

            else:
                    self.ui.battery_charge.setText(str(round(batt.percent, 2))+"%")
                    self.ui.battery_time_left.setText(self.secs2hours(batt.secsleft))
                    if batt.percent < 100:
                        self.ui.battery_status.setText("Discharging")
                    else:
                        self.ui.battery_status.setText("Fully Charged")
                    self.ui.battery_plugged.setText("No")
            # battery power indicator
            #     self.ui.battery_usage.rpb_setaaMaximum(100)
            #     self.ui.battery_usage.rpb_setValue(batt.percent)
            #     self.ui.battery_usage.rpb_setBarStyle('Hybrid2')
            #     self.ui.battery_usage.rpb_setLineColor((255, 30, 99))
            #     self.ui.battery_usage.rpb_setPieColor((45, 74, 83))
            #     self.ui.battery_usage.rpb_setTextColor((255, 255, 255))
            #     self.ui.battery_usage.rpb_setInitialPos('West')
            #     self.ui.battery_usage.rpb_setTextFormat('Percentage')
            #     self.ui.battery_usage.rpb_setLineWidth(15)
            #     self.ui.battery_usage.rpb_setPathWidth(15)
            #     self.ui.battery_usage.rpb_setLineCap('RoundCap')
                    sleep(1)

##########################################################################################
##########################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
