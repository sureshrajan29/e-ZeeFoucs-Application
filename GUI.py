"""
This module is responsible for setting up the application's entire user interface.
"""
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget
import os
from PyQt5.QtWidgets import *
from qtwidgets import Toggle
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import *
import sys
from logger import logger
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.image import imread


class HoverButton(QPushButton):
    """
      This class is used to convert button into Q-menubar.
      param lists: None
      return: Bool
    """

    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self.machine_menu = QMenu(self)

            self.machine_menu.setStyleSheet(
                "background-color:rgb(49, 77, 162);\n"
                "color:rgb(255, 255, 255);\n"
                "border-radius: 10px;")

            self.setStyleSheet("QPushButton:enabled{\n"
                               "background-color:rgb(49, 77, 162);\n"
                               "color:rgb(255, 255, 255);\n"
                               "border-radius: 10px;\n"
                               "}"
                               "QPushButton:Pressed{\n"
                               "background-color: #1a5276;\n"
                               "}"
                               "QPushButton:disabled"
                               "{"
                               "border-radius: 10px;\n"
                               "background-color:#95a5a6;"
                               "}")

            self.installEventFilter(self)
            self.machine_menu.installEventFilter(self)

            self.check_cursor_timer = QTimer(self)
            self.check_cursor_timer.timeout.connect(self.check_cursor_position)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at GUI HoverButton class : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def eventFilter(self, source, event):
        try:
            if source == self and event.type() == QEvent.Enter:
                if self.isEnabled():
                    self.machine_menu.popup(self.mapToGlobal(self.rect().topRight()))
                self.check_cursor_timer.start(100)
            elif source == self.machine_menu and event.type() == QEvent.Leave:
                QTimer.singleShot(100, self.check_cursor_position)
            return super().eventFilter(source, event)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at GUI HoverButton eventFilter : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def check_cursor_position(self):
        try:
            if not (self.rect().contains(self.mapFromGlobal(QCursor.pos())) or
                    self.machine_menu.rect().contains(self.machine_menu.mapFromGlobal(QCursor.pos()))):
                if self.isEnabled():
                    self.machine_menu.hide()
                self.check_cursor_timer.stop()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at GUI HoverButton check_cursor_position : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno,
                                                                                      e))


class AnimatedLineEdit(QLineEdit):
    """
    A QLineEdit subclass with a custom integer property 'xPos'
    that controls the widget's x-coordinate.
    """

    def __init__(self, *args, **kwargs):
        super(AnimatedLineEdit, self).__init__(*args, **kwargs)

    def getX(self):
        return self.x()

    def setX(self, x):
        self.move(x, self.y())

    xPos = pyqtProperty(int, fget=getX, fset=setX)


class Animatedbutton(QPushButton):
    """
    A QLineEdit subclass with a custom integer property 'xPos'
    that controls the widget's x-coordinate.
    """

    def __init__(self, *args, **kwargs):
        super(Animatedbutton, self).__init__(*args, **kwargs)
        self.setStyleSheet("QPushButton {"
                            "background-color: #a2d2ff;"
                            "border-radius: 5px;"
                            "}"
                            "QPushButton:hover {"
                            "background-color: #bde0fe;"
                            "}"
                            "QPushButton:pressed {"
                            "padding-left: 5px;"
                            "padding-top: 5px;"
                            "background-color: #00b4d8;"
                            "}"
                        )
    def getX(self):
        return self.x()

    def setX(self, x):
        self.move(x, self.y())

    xPos = pyqtProperty(int, fget=getX, fset=setX)


class combobox(QtWidgets.QComboBox):
    try:
        stepChanged = QtCore.pyqtSignal()

        def wheelEvent(self, event):
            event.ignore()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("Error at GUI combo box class : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))


class Password_LineEdit(QtWidgets.QLineEdit):
    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Copy) or event.matches(QtGui.QKeySequence.Paste):
            return
        super().keyPressEvent(event)


class graph_widget(QtWidgets.QWidget):
    try:
        def __init__(self, image):
            super().__init__()
            self.image = image

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.image)
            print("dl")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("Error at GUI graph_widget class : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))


class CustomCheckBox(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
                            QCheckBox {
                                color: black;
                                font-size: 14px;
                            }
                            QCheckBox::indicator {
                                width: 10px;
                                height: 10px;
                            }
                            QCheckBox::indicator:unchecked {
                                background-color: white;
                                border: 1px solid black;
                                border-radius: 5px;
                            }
                            QCheckBox::indicator:indeterminate {
                                background-color: orange;
                                border: 1px solid black;
                                border-radius: 5px;
                            }
                            QCheckBox::indicator:checked {
                                background-color: green;
                                border: 1px solid black;
                                border-radius: 5px;
                            }
                            """)
        self.setTristate(True)
    def mousePressEvent(self, event):
        pass


class MyDialog(QDialog):
    try:
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Curved Dialog")
            self.resize(400, 350)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setStyleSheet("""
                        QDialog {
                            background-color: rgba(196,236,236,255);
                            color: rgba(255, 255, 255, 210);
                            border: 2px solid rgba(255, 255, 255, 180);
                            border-radius: 15px;
                            padding: 10px;
                        }
                    """)
            self.layout = QVBoxLayout()
            self.layout.setSpacing(20)
            self.setLayout(self.layout)

        def mousePressEvent(self, event):
            pass

        def closeEvent(self, event):
            # Prevent closing with Alt+F4
            event.ignore()

        def keyPressEvent(self, event):
            # Prevent closing with the Esc key
            if event.key() == Qt.Key_Escape:
                event.ignore()

        def dialog_close(self):
            self.accept()
            self.close()

        def paintEvent(self, event):
            """ Override paint event to create a curved dialog """
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            rect = self.rect()
            painter.setBrush(QColor("#8ab0ab"))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, 15, 15)  # 15px curve

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("Error at MyDialog class : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))


class UiMainWindow(object):
    def __init__(self):
        self.relay_x_axis_current_position_value = None
        self.btn_fingerprint_create = None
        self.fixture_txt_box = None
        self.collimator_azimuth_lndt = None
        self.collimator_dy_offset_tolerence_lndt = None
        self.collimator_dy_offset_tolerence_lbl = None
        self.collimator_dx_offset_tolerence_lndt = None
        self.collimator_dx_offset_tolerence_lbl = None
        self.collimator_details_chart_check_btn = None
        self.collimator_details_offset_check_btn = None
        self.relay_chart_check_btn = None
        self.relay_lens_offset_check_btn = None
        self.user_setting = None
        self.menu = None
        self.delete_user = None
        self.edit_user = None
        self.delete_recipe = None
        self.gluing_dispenser_type_lbl = None
        self.gluing_dispenser_type_cmb = None
        self.front_door_close_btn = None
        self.front_door_open_btn = None
        self.collimator_tl_chartintensity_lbl = None
        self.gluing_z_axis_actual_lbl = None
        self.gluing_cntrl_homing_btn = None
        self.user_icon_lbl = None
        self.user_login_lbl = None
        self.emp_id_txtbox = None
        self.progress_bar = None
        self.econ_logo = None
        self.current_lbl_geomentry = None
        self.btn_save_recipe = None
        self.btn_prev = None
        self.btn_next = None
        self.btn_save = None
        self.window_height = None
        self.window_width = None
        self.create_recipe = None
        self.create_user = None
        self.horizontalLayout = None
        self.horizontalLayoutWidget = None
        self.btn_station_1 = None
        self.btn_station_2 = None
        self.btn_station_3 = None
        self.btn_station_4 = None
        self.btn_station_5 = None
        self.btn_station_6 = None
        self.verticalLayout_2 = None
        self.verticalLayoutWidget = None
        self.lbl_station_6 = None
        self.station_6_layout = None
        self.edit_recipe = None
        self.lbl_station_5 = None
        self.lbl_station_4 = None
        self.station_4_layout = None
        self.lbl_station_3 = None
        self.station_3_layout = None
        self.lbl_station_2 = None
        self.station_2_layout = None
        self.lbl_station_1 = None
        self.radioButton_edit = None
        self.station_1_layout = None
        self.radioButton_create = None
        self.btn_user_create = None
        self.lbl_set_password_2 = None
        self.lnedt_set_password_2 = None
        self.lbl_set_password = None
        self.lnedt_set_password = None
        self.lnedt_name = None
        self.lbl_user = None
        self.station_5_layout = None
        self.lbl_user_name = None
        self.user_create_layout = None
        self.stackedWidget = None
        self.statusbar = None
        self.central_widget = None
        self.pwd_txtbox = None
        self.init_all_lbl = None
        self.init_grpbox = None
        self.init_lbl = None
        self.name_txtbox = None
        self.name_lbl = None
        self.user_lgn_all_lbl = None
        self.title_lbl = None
        self.verison_lbl = None
        self.user_logn_lbl = None
        self.userr_lgn_grp_box = None
        self.screen_resolution = None
        self.current_lbl_geomentry = None
        self.window_height = None
        self.window_width = None
        self.label = None
        self.app_close_btn = None
        self.btn_start = None
        self.dry_run_btn = None
        self.step_run_btn = None
        self.machine_cntrl_btn = None
        self.select_recipe_btn = None
        self.init_btn = None
        self.btn_mode = None
        self.line = None
        self.app_version = "4.0.0"
        self.application_name = "e-ZeeFocus Application"

    def login_setupUi(self, user_login_window):
        try:
            """
                  This method is used to create the login page.
                  param lists: None
                  return: Bool
                """
            user_login_window.setObjectName("user_login_window")
            for i in self.screen_resolution:
                if self.screen_resolution[i][0] == user_login_window.geometry().width() and \
                        self.screen_resolution[i][1] >= user_login_window.geometry().height():
                    self.window_width, self.window_height = self.screen_resolution[i][0], self.screen_resolution[i][1]
                    user_login_window.resize(self.window_width, self.window_height)
                    user_login_window.setFixedSize(self.window_width, self.window_height)
                    break
            else:
                user_login_window.showMaximized()
                user_login_window.showMinimized()
                user_login_window.showMaximized()

            if self.window_width != 0:
                user_login_window.setAutoFillBackground(False)
                user_login_window.setStyleSheet("")
                user_login_window.setWindowTitle(f"Lens Focusing and Gluing Automation {self.app_version}")
                user_login_window.setWindowIcon(QtGui.QIcon(r".\media\e-con-systems-logo.png"))
                user_login_window.setDocumentMode(False)
                self.central_widget = QtWidgets.QWidget(user_login_window)
                self.central_widget.setMinimumSize(QtCore.QSize(self.window_width, self.window_height))
                self.central_widget.setMaximumSize(QtCore.QSize(self.window_width, self.window_height))
                self.central_widget.setObjectName("central_widget")

            self.econ_logo = QtWidgets.QLabel(self.central_widget)
            self.econ_logo.setGeometry(QtCore.QRect(0, 0, 250, 100))
            self.econ_logo.setStyleSheet("background-color:rgba(255, 255, 255, 0);")
            self.econ_logo.setText("")
            self.econ_logo.setPixmap(QtGui.QPixmap(r".\media\e-con-systems-logo.png"))
            self.econ_logo.setScaledContents(True)
            self.econ_logo.setWordWrap(False)
            self.econ_logo.setObjectName("econ_logo")

            self.verison_lbl = QtWidgets.QLabel(self.central_widget)
            if self.window_height < 1085:

                self.current_lbl_geomentry = QtCore.QRect((self.window_width - 140), 20, 120, 20)
                self.verison_lbl.setGeometry(self.current_lbl_geomentry)
            elif self.window_height < 1610:
                self.current_lbl_geomentry = QtCore.QRect((self.window_width - 140), 20, 120, 30)
                self.verison_lbl.setGeometry(self.current_lbl_geomentry)
            elif self.window_height < 2165:
                self.current_lbl_geomentry = QtCore.QRect((self.window_width - 140), 20, 120, 40)
                self.verison_lbl.setGeometry(self.current_lbl_geomentry)
            self.verison_lbl.setStyleSheet("background-color:rgba(255, 255, 255, 0);"
                                           "color: rgb(0, 0, 0);\n"
                                           "border-radius: 10px")
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.verison_lbl.setFont(font)
            self.verison_lbl.setObjectName("verison_lbl")

            self.title_lbl = QtWidgets.QLabel(self.central_widget)
            if self.window_height < 1085:
                self.current_lbl_geomentry = QtCore.QRect((self.window_width // 2 - 190), 20, 800, 50)
                self.title_lbl.setGeometry(self.current_lbl_geomentry)
            elif self.window_height < 1610:
                self.current_lbl_geomentry = QtCore.QRect((self.window_width // 2 - 375), 40, 800, 50)
                self.title_lbl.setGeometry(self.current_lbl_geomentry)
            elif self.window_height < 2165:
                self.current_lbl_geomentry = QtCore.QRect((self.window_width // 2 - 375), 50, 800, 50)
                self.title_lbl.setGeometry(self.current_lbl_geomentry)
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(18)
            font.setBold(True)
            self.title_lbl.setFont(font)
            self.title_lbl.setCursor(QtGui.QCursor(Qt.ArrowCursor))
            self.title_lbl.setStyleSheet("background-color:rgba(255, 255, 255, 0);"
                                         "color: rgb(0, 0, 0);\n"
                                         "border-radius: 10px"
                                         )
            self.title_lbl.setObjectName("title_lbl")

            self.widget = QtWidgets.QWidget(self.central_widget)
            self.widget.setGeometry(QtCore.QRect(450, 230, 1000, 1000))
            self.widget.setObjectName("widget")

            self.label = QtWidgets.QLabel(self.widget)
            self.label.setGeometry(QtCore.QRect(60, 30, 490, 425))
            self.label.setPixmap(QtGui.QPixmap(r".\media\Automation-blog.jpg"))
            self.label.setScaledContents(True)
            self.label.setStyleSheet("")
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setText("")
            self.label.setObjectName("label")

            self.img_lbl = QtWidgets.QLabel(self.widget)
            self.img_lbl.setGeometry(QtCore.QRect(40, 30, 600, 430))
            self.img_lbl.setStyleSheet("border-top-left-radius: 50px;")
            self.img_lbl.setText("")
            self.img_lbl.setObjectName("img_lbl")

            self.login_bg_lbl = QtWidgets.QLabel(self.widget)
            self.login_bg_lbl.setGeometry(QtCore.QRect(450, 30, 490, 425))
            self.login_bg_lbl.setStyleSheet("background-color:rgba(255, 255, 255, 255);\n"
                                            "border-bottom-right-radius: 50px;")
            self.login_bg_lbl.setText("")
            self.login_bg_lbl.setObjectName("login_bg_lbl")

            self.user_login_lbl = QtWidgets.QLabel(self.widget)
            self.user_login_lbl.setGeometry(QtCore.QRect(650, 70, 100, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(14)
            font.setBold(True)
            self.user_login_lbl.setFont(font)
            self.user_login_lbl.setStyleSheet("color:rgba(0, 0, 0, 200);")
            self.user_login_lbl.setObjectName("user_login_lbl")

            self.emp_id_txtbox = QtWidgets.QLineEdit(self.widget)
            self.emp_id_txtbox.setGeometry(QtCore.QRect(600, 150, 200, 40))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.emp_id_txtbox.setFont(font)
            self.emp_id_txtbox.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                             "border:none;\n"
                                             "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                             "color:rgba(0, 0, 0, 240);\n"
                                             "padding-bottom:7px;")
            regx = QRegExp('^\d{0,9}$')
            emp_id_txtbox = QRegExpValidator(regx, self.emp_id_txtbox)
            self.emp_id_txtbox.setValidator(emp_id_txtbox)
            self.emp_id_txtbox.setObjectName("lineEdit")

            self.pwd_txtbox = AnimatedLineEdit(self.widget)
            self.pwd_txtbox.setGeometry(QtCore.QRect(600, 215, 200, 40))
            font = QtGui.QFont()
            font.setPointSize(12)
            self.pwd_txtbox.setFont(font)
            self.pwd_txtbox.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                          "border:none;\n"
                                          "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                          "color:rgba(0, 0, 0, 240);\n"
                                          "padding-bottom:7px;")
            self.pwd_txtbox.setEchoMode(QLineEdit.Password)
            self.pwd_txtbox.setPlaceholderText("Enter Password")
            self.pwd_txtbox.move(-200, 215)

            self.login_btn = Animatedbutton(self.widget)
            self.login_btn.setGeometry(QtCore.QRect(600, 295, 200, 40))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(14)
            font.setBold(True)
            self.login_btn.setFont(font)
            self.login_btn.move(-200, 295)
            self.login_btn.setObjectName("pushButton")

            self.fingerprint_lbl = QtWidgets.QLabel(self.widget)
            self.fingerprint_lbl.setGeometry(QtCore.QRect(570, 250, 230, 200))
            self.fingerprint_lbl.setScaledContents(True)
            self.fingerprint_lbl.setStyleSheet("color: rgb(255, 255, 255);\n"
                                               "background-color:rgba(255, 255, 255, 0);"
                                               "font: 87 11pt \"Arial Black\";\n"
                                               "\n"
                                               "border-radius: 100px")
            movie = QtGui.QMovie(r".\media\fingerprint_1.gif")
            self.fingerprint_lbl.setMovie(movie)
            movie.setSpeed(75)
            movie.start()
            self.fingerprint_lbl.hide()
            self.fingerprint_lbl.setObjectName("pwd_lbl")

            self.move_login_btn = QtWidgets.QPushButton(self.widget)
            self.move_login_btn.setGeometry(QtCore.QRect(650, 240, 100, 80))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.move_login_btn.setFont(font)
            self.move_login_btn.setStyleSheet("QPushButton:Pressed{\n"
                                              "padding-left:15px;\n"
                                              "}"
                                              "QPushButton::icon {"
                                              "padding-right: 1px;}"
                                              "QPushButton{"
                                              "border-radius: 25px;}")
            self.move_login_btn.setText("")
            icon10 = QtGui.QIcon()
            icon10.addPixmap(QtGui.QPixmap(r".\media\login icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.move_login_btn.setIcon(icon10)
            self.move_login_btn.setIconSize(QtCore.QSize(55, 55))
            self.move_login_btn.setObjectName("move_login_btn")
            self.login_btn.hide()
            user_login_window.setCentralWidget(self.central_widget)

            self.login_retranslateUi(user_login_window)
            QtCore.QMetaObject.connectSlotsByName(user_login_window)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(

                "Error at GUI login_setupUI function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def login_retranslateUi(self, user_login_window):
        try:
            _translate = QtCore.QCoreApplication.translate
            user_login_window.setWindowTitle(
                _translate("user_login_window", f"{self.application_name}_{self.app_version}"))
            self.verison_lbl.setText(_translate("user_login_window", f"Version {self.app_version}"))
            self.title_lbl.setText(_translate("user_login_window", "e-ZeeFocus Application"))
            self.user_login_lbl.setText(_translate("user_login_window", "L O G  I N"))
            self.emp_id_txtbox.setPlaceholderText(_translate("user_login_window", "E  m  p    I  d"))
            self.emp_id_txtbox.setText(_translate("user_login_window", ""))
            self.pwd_txtbox.setPlaceholderText(_translate("user_login_window", "P  a  s  s  w  o  r  d"))
            self.login_btn.setText(_translate("user_login_window", "Login"))

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at GUI login_re_translateUi function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def setupUi(self, MainWindow, mode='Auto'):
        try:
            """
              This method is used to create the Main page and recipe creation page.
              param lists: None
              return: Bool
            """
            MainWindow.setObjectName("MainWindow")
            for i in self.screen_resolution:
                if self.screen_resolution[i][0] == MainWindow.geometry().width() and \
                        self.screen_resolution[i][1] >= MainWindow.geometry().height():
                    self.window_width, self.window_height = self.screen_resolution[i][0], self.screen_resolution[i][1]
                    MainWindow.resize(self.window_width, self.window_height)
                    MainWindow.setFixedSize(self.window_width, self.window_height)
                    break
            else:
                MainWindow.showMaximized()
                MainWindow.showMinimized()
                MainWindow.showMaximized()

            if self.window_width != 0 and self.window_height != 0:
                MainWindow.setAutoFillBackground(False)
                MainWindow.setDocumentMode(False)

                self.central_widget = QtWidgets.QWidget(MainWindow)
                self.central_widget.setObjectName("central_widget")
                self.central_widget.setMinimumSize(QtCore.QSize(self.window_width, self.window_height))
                self.central_widget.setMaximumSize(QtCore.QSize(self.window_width, self.window_height))
                self.central_widget.setStyleSheet("QWidget {background-color:rgb(255, 255, 255)}")

                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)
                self.user_setting = HoverButton(self.central_widget)
                self.create_user = self.user_setting.machine_menu.addAction(QIcon(r".\media\signup-icon.png"),
                                                                            'Create User')
                self.edit_user = self.user_setting.machine_menu.addAction(QIcon(r".\media\edit_user.png"),
                                                                          'Edit User')
                self.delete_user = self.user_setting.machine_menu.addAction(QIcon(r".\media\user_delete_icon.png"),
                                                                            'Delete User')
                self.create_recipe = self.user_setting.machine_menu.addAction(
                    QIcon(r".\media\create_recipe.png"), 'Create Recipe')
                self.edit_recipe = self.user_setting.machine_menu.addAction(
                    QIcon(r".\media\edit_recipe.png"), 'Edit Recipe')

                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.user_setting.sizePolicy().hasHeightForWidth())
                self.user_setting.setSizePolicy(sizePolicy)
                font = QtGui.QFont()
                font.setPointSize(15)
                self.user_setting.setFont(font)
                self.user_setting.setEnabled(False)
                self.user_setting.setObjectName("user_setting")

                self.progress_bar = QtWidgets.QProgressBar(self.central_widget)
                if self.window_height < 1085:
                    self.progress_bar.setGeometry(QtCore.QRect(315, self.window_height - 110, 260, 30))
                elif self.window_height < 1610:
                    self.progress_bar.setGeometry(
                        QtCore.QRect(340, (self.window_height - 125), 260, 30))
                elif self.window_height < 2165:
                    self.progress_bar.setGeometry(
                        QtCore.QRect(340, (self.window_height - 140), 260, 30))
                self.progress_bar.setMinimum(0)
                self.progress_bar.setMaximum(100)
                self.progress_bar.hide()
                self.progress_bar.setObjectName("progress_bar")

                if mode == 'Auto':
                    self.user_setting.setGeometry(QtCore.QRect(50, 830, 180, 60))
                    self.econ_logo = QtWidgets.QLabel(self.central_widget)
                    self.econ_logo.setGeometry(QtCore.QRect(0, 0, 300, 100))
                    self.econ_logo.setText("")
                    self.econ_logo.setPixmap(QtGui.QPixmap(r".\media\e-con-systems-logo.png"))
                    self.econ_logo.setScaledContents(True)
                    self.econ_logo.setWordWrap(False)
                    self.econ_logo.setObjectName("econ_logo")
                    self.right_frame = QtWidgets.QFrame(self.central_widget)
                    self.right_frame.setGeometry(QtCore.QRect(310, 10, self.window_width - 420, 200))
                    self.right_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                    self.right_frame.setObjectName("right_frame")
                    self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.right_frame)
                    self.verticalLayout_2.setObjectName("verticalLayout_2")

                    self.station_frame = QtWidgets.QFrame(self.right_frame)
                    self.station_frame.setStyleSheet("border-radius:20px;\n"
                                                     "background-color: rgb(3, 97, 45);")
                    self.station_frame.setFrameShape(QtWidgets.QFrame.Box)
                    self.station_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                    self.station_frame.setFixedHeight(130)
                    self.station_frame.setObjectName("station_frame")
                    self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.station_frame)
                    self.horizontalLayout_3.setObjectName("horizontalLayout_3")
                    self.load_frame = QtWidgets.QFrame(self.station_frame)
                    self.load_frame.setMaximumSize(QtCore.QSize(150, 120))
                    self.load_frame.setStyleSheet("")
                    self.load_frame.setFrameShape(QtWidgets.QFrame.Box)
                    self.load_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                    self.load_frame.setObjectName("load_frame")
                    self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.load_frame)
                    self.verticalLayout_4.setObjectName("verticalLayout_4")
                    self.loadinglbl = QtWidgets.QLabel(self.load_frame)
                    self.loadinglbl.setStyleSheet("border:0px;")
                    self.loadinglbl.setText("")
                    self.loadinglbl.setPixmap(QtGui.QPixmap(r".\media\load_lbl.png"))
                    self.loadinglbl.setScaledContents(True)
                    self.loadinglbl.setObjectName("loadinglbl")
                    self.verticalLayout_4.addWidget(self.loadinglbl)
                    self.loading_txt = QtWidgets.QLabel(self.load_frame)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.loading_txt.setFont(font)
                    self.loading_txt.setStyleSheet("border:0px;\n"
                                                   "color: white;\n"
                                                   "qproperty-alignment: AlignCenter;")
                    self.loading_txt.setScaledContents(False)
                    self.loading_txt.setWordWrap(True)
                    self.loading_txt.setObjectName("loading_txt")
                    self.verticalLayout_4.addWidget(self.loading_txt)
                    self.horizontalLayout_3.addWidget(self.load_frame)
                    self.h_sensor_frame = QtWidgets.QFrame(self.station_frame)
                    self.h_sensor_frame.setMaximumSize(QtCore.QSize(150, 120))
                    self.h_sensor_frame.setObjectName("h_sensor_frame")
                    self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.h_sensor_frame)
                    self.verticalLayout_7.setObjectName("verticalLayout_7")
                    self.h_sensor_lbl = QtWidgets.QLabel(self.h_sensor_frame)
                    self.h_sensor_lbl.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    self.h_sensor_lbl.setStyleSheet("border:0px;\n")
                    self.h_sensor_lbl.setText("")
                    self.h_sensor_lbl.setPixmap(QtGui.QPixmap(r".\media\h_sensor.png"))
                    self.h_sensor_lbl.setScaledContents(True)
                    self.h_sensor_lbl.setObjectName("h_sensor_lbl")
                    self.verticalLayout_7.addWidget(self.h_sensor_lbl)
                    self.h_sensor_txt = QtWidgets.QLabel(self.h_sensor_frame)
                    self.h_sensor_txt.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.h_sensor_txt.setFont(font)
                    self.h_sensor_txt.setStyleSheet("color: white;\n"
                                                    "border:0px;\n"
                                                    "qproperty-alignment: AlignCenter;")
                    self.h_sensor_txt.setScaledContents(False)
                    self.h_sensor_txt.setWordWrap(True)
                    self.h_sensor_txt.setObjectName("h_sensor_txt")
                    self.verticalLayout_7.addWidget(self.h_sensor_txt)
                    self.horizontalLayout_3.addWidget(self.h_sensor_frame)

                    self.collimator_frame = QtWidgets.QFrame(self.station_frame)
                    self.collimator_frame.setMaximumSize(QtCore.QSize(150, 120))
                    self.collimator_frame.setObjectName("collimator_frame")
                    self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.collimator_frame)
                    self.verticalLayout_11.setObjectName("verticalLayout_11")
                    self.collimator_lbl = QtWidgets.QLabel(self.collimator_frame)
                    self.collimator_lbl.setStyleSheet("border:0px;")
                    self.collimator_lbl.setText("")
                    self.collimator_lbl.setPixmap(QtGui.QPixmap(r".\media\collimator.png"))
                    self.collimator_lbl.setScaledContents(True)
                    self.collimator_lbl.setObjectName("collimator_lbl")
                    self.verticalLayout_11.addWidget(self.collimator_lbl)
                    self.collimator_txt = QtWidgets.QLabel(self.collimator_frame)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.collimator_txt.sizePolicy().hasHeightForWidth())
                    self.collimator_txt.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_txt.setFont(font)
                    self.collimator_txt.setFont(font)
                    self.collimator_txt.setStyleSheet("color: white;\n"
                                                      "border:0px;\n"
                                                      "qproperty-alignment: AlignCenter;")
                    self.collimator_txt.setWordWrap(True)
                    self.collimator_txt.setObjectName("collimator_txt")
                    self.verticalLayout_11.addWidget(self.collimator_txt)
                    self.horizontalLayout_3.addWidget(self.collimator_frame)

                    self.relay_frame = QtWidgets.QFrame(self.station_frame)
                    self.relay_frame.setMaximumSize(QtCore.QSize(150, 130))
                    self.relay_frame.setObjectName("ralay_frame")
                    self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.relay_frame)
                    self.verticalLayout_9.setObjectName("verticalLayout_9")
                    self.relay_lbl = QtWidgets.QLabel(self.relay_frame)
                    self.relay_lbl.setStyleSheet("border:0px;\n")
                    self.relay_lbl.setText("")
                    self.relay_lbl.setPixmap(QtGui.QPixmap(r".\media\relay.png"))
                    self.relay_lbl.setScaledContents(True)
                    self.relay_lbl.setObjectName("relay_lbl")
                    self.verticalLayout_9.addWidget(self.relay_lbl)
                    self.relay_txt = QtWidgets.QLabel(self.relay_frame)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_txt.setFont(font)
                    self.relay_txt.setStyleSheet("color: white;\n"
                                                 "border:0px;\n"
                                                 "qproperty-alignment: AlignCenter;")
                    self.relay_txt.setObjectName("relay_txt")
                    self.verticalLayout_9.addWidget(self.relay_txt)
                    self.horizontalLayout_3.addWidget(self.relay_frame)

                    self.gluing_frame = QtWidgets.QFrame(self.station_frame)
                    self.gluing_frame.setMaximumSize(QtCore.QSize(150, 120))
                    self.gluing_frame.setObjectName("gluing_frame")
                    self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.gluing_frame)
                    self.verticalLayout_13.setObjectName("verticalLayout_13")
                    self.gluing_lbl = QtWidgets.QLabel(self.gluing_frame)
                    self.gluing_lbl.setStyleSheet("border:0px;")
                    self.gluing_lbl.setText("")
                    self.gluing_lbl.setPixmap(QtGui.QPixmap(r".\media\gluing.png"))
                    self.gluing_lbl.setScaledContents(True)
                    self.gluing_lbl.setObjectName("gluing_lbl")
                    self.verticalLayout_13.addWidget(self.gluing_lbl)
                    self.gluing_txt = QtWidgets.QLabel(self.gluing_frame)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_txt.setFont(font)
                    self.gluing_txt.setStyleSheet("color: white;\n"
                                                  "border:0px;\n"
                                                  "qproperty-alignment: AlignCenter;")
                    self.gluing_txt.setObjectName("gluing_txt")
                    self.verticalLayout_13.addWidget(self.gluing_txt)
                    self.horizontalLayout_3.addWidget(self.gluing_frame)

                    self.curing_frame = QtWidgets.QFrame(self.station_frame)
                    self.curing_frame.setMaximumSize(QtCore.QSize(150, 120))
                    self.curing_frame.setFrameShape(QtWidgets.QFrame.Box)
                    self.curing_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                    self.curing_frame.setObjectName("curing_frame")
                    self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.curing_frame)
                    self.verticalLayout_15.setObjectName("verticalLayout_15")
                    self.curing_lbl = QtWidgets.QLabel(self.curing_frame)
                    self.curing_lbl.setStyleSheet("border:0px;")
                    self.curing_lbl.setText("")
                    self.curing_lbl.setPixmap(QtGui.QPixmap(r".\media\curing.png"))
                    self.curing_lbl.setScaledContents(True)
                    self.curing_lbl.setObjectName("curing_lbl")
                    self.verticalLayout_15.addWidget(self.curing_lbl)
                    self.curing_txt = QtWidgets.QLabel(self.curing_frame)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.curing_txt.setFont(font)
                    self.curing_txt.setStyleSheet("color: white;\n"
                                                  "border:0px;\n"
                                                  "qproperty-alignment: AlignCenter;")
                    self.curing_txt.setObjectName("curing_txt")
                    self.verticalLayout_15.addWidget(self.curing_txt)
                    self.horizontalLayout_3.addWidget(self.curing_frame)
                    self.verticalLayout_2.addWidget(self.station_frame)

                    self.init_btn = QtWidgets.QPushButton(self.central_widget)
                    self.init_btn.setGeometry(QtCore.QRect(50, 100, 180, 60))
                    font = QtGui.QFont()
                    font.setPointSize(15)

                    self.init_btn.setFont(font)
                    self.init_btn.setStyleSheet("QPushButton:enabled{\n"
                                                "background-color:rgb(49, 77, 162);\n"
                                                "color:rgb(255, 255, 255);\n"
                                                "border-radius: 10px;\n"
                                                "}"
                                                "QPushButton:Pressed{\n"
                                                "background-color: #1a5276;\n"
                                                "}"
                                                "QPushButton:disabled"
                                                "{"
                                                "border-radius: 10px;\n"
                                                "background-color:#95a5a6;"
                                                "}"
                                                )

                    self.init_btn.setDefault(False)
                    self.init_btn.setDisabled(True)
                    self.init_btn.setFlat(False)
                    self.init_btn.setObjectName("init_btn")
                    self.init_btn.setFocusPolicy(Qt.NoFocus)
                    self.init_btn.setText("INIT")

                    self.user_name_lbl = QtWidgets.QLabel(self.central_widget)
                    self.user_name_lbl.setGeometry(QtCore.QRect(350, 10, 300, 30))
                    self.user_name_lbl.setAlignment(Qt.AlignLeft)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setFamily("Segoe UI")
                    font.setBold(True)
                    self.user_name_lbl.setFont(font)
                    self.user_name_lbl.setText("")
                    self.user_name_lbl.setScaledContents(True)
                    self.user_name_lbl.setObjectName("user_name_lbl")

                    self.config_name_lbl = QtWidgets.QLabel(self.central_widget)
                    self.config_name_lbl.setGeometry(QtCore.QRect(850, 10, 400, 30))
                    self.config_name_lbl.setAlignment(Qt.AlignLeft)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setFamily("Segoe UI")
                    font.setBold(True)
                    self.config_name_lbl.setFont(font)
                    self.config_name_lbl.setText("")
                    self.config_name_lbl.setScaledContents(True)
                    self.config_name_lbl.setObjectName("config_name_lbl")

                    self.product_name_lbl = QtWidgets.QLabel(self.central_widget)
                    self.product_name_lbl.setGeometry(QtCore.QRect(self.window_width - 500, 10, 450, 30))
                    self.product_name_lbl.setAlignment(Qt.AlignLeft)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setFamily("Segoe UI")
                    font.setBold(True)
                    self.product_name_lbl.setFont(font)
                    self.product_name_lbl.setText("")
                    self.product_name_lbl.setScaledContents(True)
                    self.product_name_lbl.setObjectName("product_name_lbl")

                    self.select_recipe_btn = QtWidgets.QPushButton(self.central_widget)
                    self.select_recipe_btn.setGeometry(QtCore.QRect(50, 410, 180, 60))
                    font = QtGui.QFont()
                    font.setPointSize(15)
                    self.select_recipe_btn.setFont(font)
                    self.select_recipe_btn.setStyleSheet("QPushButton:enabled{\n"
                                                         "background-color:rgb(49, 77, 162);\n"
                                                         "color:rgb(255, 255, 255);\n"
                                                         "border-radius: 10px;\n"
                                                         "}"
                                                         "QPushButton:Pressed{\n"
                                                         "background-color: #1a5276;\n"
                                                         "}"
                                                         "QPushButton:disabled"
                                                         "{"
                                                         "border-radius: 10px;\n"
                                                         "background-color:#95a5a6;"
                                                         "}"
                                                         )

                    self.select_recipe_btn.setDefault(False)
                    self.select_recipe_btn.setDisabled(True)
                    self.select_recipe_btn.setFlat(False)
                    self.select_recipe_btn.setObjectName("select_recipe_btn")
                    self.select_recipe_btn.setFocusPolicy(Qt.NoFocus)
                    self.select_recipe_btn.setText("Select Recipe")

                    self.btn_start = QtWidgets.QPushButton(self.central_widget)
                    self.btn_start.setGeometry(QtCore.QRect(50, 490, 180, 60))
                    self.btn_start.setDisabled(True)
                    font = QtGui.QFont()
                    font.setPointSize(15)
                    self.btn_start.setFont(font)
                    self.btn_start.setStyleSheet("QPushButton:enabled{\n"
                                                 "background-color:rgb(49, 77, 162);\n"
                                                 "color:rgb(255, 255, 255);\n"
                                                 "border-radius: 10px;\n"
                                                 "}"
                                                 "QPushButton:Pressed{\n"
                                                 "background-color: #1a5276;\n"
                                                 "}"
                                                 "QPushButton:disabled"
                                                 "{"
                                                 "border-radius: 10px;\n"
                                                 "background-color:#95a5a6;"
                                                 "}"
                                                 )
                    self.btn_start.setDefault(False)
                    self.btn_start.setFlat(False)
                    self.btn_start.setObjectName("btn_start")
                    self.btn_start.setFocusPolicy(Qt.NoFocus)
                    self.btn_start.setText("START")

                    self.line = QtWidgets.QFrame(self.central_widget)
                    self.line.setGeometry(QtCore.QRect(30, 570, 250, 1))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.line.setFont(font)
                    self.line.setFrameShadow(QtWidgets.QFrame.Plain)
                    self.line.setLineWidth(3)
                    self.line.setFrameShape(QtWidgets.QFrame.HLine)
                    self.line.setFocusPolicy(Qt.NoFocus)
                    self.line.setObjectName("line")

                    self.glue_teach_btn = QtWidgets.QPushButton(self.central_widget)
                    self.glue_teach_btn.setStyleSheet("QPushButton:enabled{\n"
                                                      "background-color:rgb(49, 77, 162);\n"
                                                      "color:rgb(255, 255, 255);\n"
                                                      "border-radius: 10px;\n"
                                                      "}"
                                                      "QPushButton:Pressed{\n"
                                                      "background-color: #1a5276;\n"
                                                      "}"
                                                      "QPushButton:disabled"
                                                      "{"
                                                      "border-radius: 10px;\n"
                                                      "background-color:#95a5a6;"
                                                      "}"
                                                      )
                    font = QtGui.QFont()
                    font.setPointSize(15)
                    self.glue_teach_btn.setFont(font)
                    self.glue_teach_btn.setEnabled(False)
                    self.glue_teach_btn.setText('Glue Purge')
                    self.glue_teach_btn.setGeometry(QtCore.QRect(50, 590, 180, 60))
                    self.glue_teach_btn.setObjectName("glue_teach_btn")
                    self.glue_teach_btn.raise_()

                    self.step_run_btn = QtWidgets.QPushButton(self.central_widget)
                    self.step_run_btn.setGeometry(QtCore.QRect(50, 670, 180, 60))
                    self.step_run_btn.setDisabled(True)
                    font = QtGui.QFont()
                    font.setPointSize(15)
                    self.step_run_btn.setFont(font)
                    self.step_run_btn.setStyleSheet("QPushButton:enabled{\n"
                                                    "background-color:rgb(49, 77, 162);\n"
                                                    "color:rgb(255, 255, 255);\n"
                                                    "border-radius: 10px;\n"
                                                    "}"
                                                    "QPushButton:Pressed{\n"
                                                    "background-color: #1a5276;\n"
                                                    "}"
                                                    "QPushButton:disabled"
                                                    "{"
                                                    "border-radius: 10px;\n"
                                                    "background-color:#95a5a6;"
                                                    "}"
                                                    )

                    self.step_run_btn.setDefault(False)
                    self.step_run_btn.setFlat(False)
                    self.step_run_btn.setObjectName("step_run_btn")
                    self.step_run_btn.setFocusPolicy(Qt.NoFocus)
                    self.step_run_btn.setText("Step Run")

                    self.machine_cntrl_btn = HoverButton(self.central_widget)
                    self.machine_cntrl_btn.setGeometry(QtCore.QRect(50, 750, 180, 60))
                    self.machine_cntrl_btn.setDefault(False)
                    self.machine_cntrl_btn.setDisabled(True)
                    self.machine_cntrl_btn.setFlat(False)
                    self.i_o_check = self.machine_cntrl_btn.machine_menu.addAction(QIcon(".\media\input_output.png"),
                                                                                   'I/o Check')
                    self.port_connection = self.machine_cntrl_btn.machine_menu.addAction(
                        QIcon(r".\media\port_connect.png"),
                        'Port Connection')
                    self.diagnostics = self.machine_cntrl_btn.machine_menu.addAction(QIcon(r".\media\diagnostic.png"),
                                                                                     'Diagnostics Screen')
                    self.bypass = self.machine_cntrl_btn.machine_menu.addAction(QIcon(r".\media\machine_cntl.png"),
                                                                                'Bypass screen')

                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.machine_cntrl_btn.sizePolicy().hasHeightForWidth())
                    self.machine_cntrl_btn.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(15)
                    self.machine_cntrl_btn.setFont(font)
                    self.machine_cntrl_btn.setText("Machine Control")
                    self.machine_cntrl_btn.setFocusPolicy(Qt.NoFocus)
                    self.machine_cntrl_btn.setObjectName("machine_cntrl_btn")

                    self.logout_btn = QtWidgets.QPushButton(self.central_widget)
                    self.logout_btn.setStyleSheet("QPushButton:enabled{\n"
                                                  "background-color:rgb(49, 77, 162);\n"
                                                  "color:rgb(255, 255, 255);\n"
                                                  "border-radius: 10px;\n"
                                                  "}"
                                                  "QPushButton:Pressed{\n"
                                                  "background-color: #1a5276;\n"
                                                  "}"
                                                  "QPushButton:disabled"
                                                  "{"
                                                  "border-radius: 10px;\n"
                                                  "background-color:#95a5a6;"
                                                  "}"
                                                  )
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.logout_btn.setFont(font)
                    self.logout_btn.setGeometry(QtCore.QRect(self.window_width - 110, 55, 100, 40))
                    self.logout_btn.setObjectName("logout_btn")
                    self.logout_btn.setDisabled(True)
                    self.logout_btn.setFocusPolicy(Qt.NoFocus)
                    self.logout_btn.raise_()

                    self.main_page_abort_btn = QtWidgets.QPushButton(self.central_widget)
                    self.main_page_abort_btn.setStyleSheet("QPushButton:enabled{\n"
                                                           "background-color:rgb(49, 77, 162);\n"
                                                           "color:rgb(255, 255, 255);\n"
                                                           "border-radius: 10px;\n"
                                                           "}"
                                                           "QPushButton:Pressed{\n"
                                                           "background-color: #1a5276;\n"
                                                           "}"
                                                           "QPushButton:disabled"
                                                           "{"
                                                           "border-radius: 10px;\n"
                                                           "background-color:#95a5a6;"
                                                           "}"
                                                           )
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.main_page_abort_btn.setFont(font)
                    self.main_page_abort_btn.setGeometry(QtCore.QRect(self.window_width - 110, 120, 100, 40))
                    self.main_page_abort_btn.setObjectName("main_page_abort_btn")
                    self.main_page_abort_btn.setDisabled(True)
                    self.main_page_abort_btn.setText("Abort")
                    self.main_page_abort_btn.raise_()

                    self.homing_dialog_box = MyDialog()
                    self.homing_header_lbl = QtWidgets.QLabel(self.homing_dialog_box)
                    self.homing_header_lbl.setAlignment(Qt.AlignCenter)
                    self.homing_header_lbl.setText("Machine Homing")
                    self.homing_header_lbl.setAlignment(Qt.AlignCenter)
                    self.homing_header_lbl.setStyleSheet("""
                                QLabel {
                                    background-color: #3e505b;
                                    color: white;
                                    padding: 10px;
                                    border-radius: 10px;
                                    font-size: 18px;
                                    font-weight: bold;
                                    text-align: center;
                                    box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.2);
                                }
                            """)
                    self.homing_header_lbl.setObjectName("homing_header_lbl")
                    self.homing_dialog_box.layout.addWidget(self.homing_header_lbl)

                    self.gluing_homing = CustomCheckBox()
                    self.gluing_homing.setText("Gluing Homing")
                    font = QFont("Arial", 9)
                    font.setBold(True)
                    font.setWeight(QFont.Black)
                    self.gluing_homing.setFont(font)
                    self.gluing_homing.setObjectName("gluing_homing")
                    self.gluing_homing.setCheckState(Qt.Unchecked)
                    self.homing_dialog_box.layout.addWidget(self.gluing_homing)

                    self.z_curing_homing = CustomCheckBox()
                    font = QFont("Arial", 9)
                    font.setBold(True)
                    font.setWeight(QFont.Black)
                    self.z_curing_homing.setFont(font)
                    self.z_curing_homing.setText("Z Axis Actuator - Curing")
                    self.z_curing_homing.setObjectName("z_curing_homing")
                    self.z_curing_homing.setCheckState(Qt.Unchecked)
                    self.homing_dialog_box.layout.addWidget(self.z_curing_homing)

                    self.z_gluing_homing = CustomCheckBox()
                    font = QFont("Arial", 9)
                    font.setBold(True)
                    font.setWeight(QFont.Black)
                    self.z_gluing_homing.setFont(font)
                    self.z_gluing_homing.setText("Z Axis Actuator - Gluing")
                    self.z_gluing_homing.setObjectName("z_gluing_homing")
                    self.z_gluing_homing.setCheckState(Qt.Unchecked)
                    self.homing_dialog_box.layout.addWidget(self.z_gluing_homing)

                    self.z_relay_homing = CustomCheckBox()
                    font = QFont("Arial", 9)
                    font.setBold(True)
                    font.setWeight(QFont.Black)
                    self.z_relay_homing.setFont(font)
                    self.z_relay_homing.setText("Z Axis Actuator - Relay")
                    self.z_relay_homing.setObjectName("z_relay_homing")
                    self.z_relay_homing.setCheckState(Qt.Unchecked)
                    self.homing_dialog_box.layout.addWidget(self.z_relay_homing)

                    self.y_axis_homing = CustomCheckBox()
                    self.y_axis_homing.setChecked(False)
                    self.y_axis_homing.setText("Y-axis actuator")
                    font = QFont("Arial", 9)
                    font.setBold(True)
                    font.setWeight(QFont.Black)
                    self.y_axis_homing.setFont(font)
                    self.y_axis_homing.setObjectName("y_axis_homing")
                    self.y_axis_homing.setCheckState(Qt.Unchecked)
                    self.homing_dialog_box.layout.addWidget(self.y_axis_homing)

                    self.x_axis_homing = CustomCheckBox()
                    self.x_axis_homing.setText("X-axis actuator")
                    font = QFont("Arial", 9)
                    font.setBold(True)
                    font.setWeight(QFont.Black)
                    self.x_axis_homing.setFont(font)
                    self.x_axis_homing.setObjectName("x_axis_homing")
                    self.x_axis_homing.setCheckState(Qt.Unchecked)
                    self.homing_dialog_box.layout.addWidget(self.x_axis_homing)

                    self.plc_initialize_homing = CustomCheckBox()
                    self.plc_initialize_homing.setText("Plc initialize")
                    font = QFont("Arial", 9)
                    font.setBold(True)
                    font.setWeight(QFont.Black)
                    self.plc_initialize_homing.setFont(font)
                    self.plc_initialize_homing.setObjectName("plc_initialize_homing")
                    self.plc_initialize_homing.setCheckState(Qt.Unchecked)
                    self.homing_dialog_box.layout.addWidget(self.plc_initialize_homing)

                    self.front_door_homing = CustomCheckBox()
                    self.front_door_homing.setText("Front door open")
                    font = QFont("Arial", 9)
                    font.setBold(True)
                    font.setWeight(QFont.Black)
                    self.front_door_homing.setFont(font)
                    self.front_door_homing.setObjectName("front_door_homing")
                    self.front_door_homing.setCheckState(Qt.Unchecked)
                    self.homing_dialog_box.layout.addWidget(self.front_door_homing)

                    self.mod_serial_lbl = QtWidgets.QLabel(self.central_widget)
                    self.mod_serial_lbl.setStyleSheet("border:0px;")
                    self.mod_serial_lbl.setText("ModBoard Serial No")
                    self.mod_serial_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.mod_serial_lbl.setFont(font)
                    self.mod_serial_lbl.setGeometry(QtCore.QRect(25, 190, 250, 15))
                    self.mod_serial_lbl.setObjectName("mod_serial_lbl")

                    self.mod_serial_lnedt = QtWidgets.QLineEdit(self.central_widget)
                    self.mod_serial_lnedt.setGeometry(QtCore.QRect(25, 210, 250, 40))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(75)
                    self.mod_serial_lnedt.setFont(font)
                    self.mod_serial_lnedt.setReadOnly(True)
                    self.mod_serial_lnedt.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
                    self.mod_serial_lnedt.setAutoFillBackground(False)
                    self.mod_serial_lnedt.setStyleSheet("\n"
                                                        "QLineEdit {\n"
                                                        "border-width: 3px; border-style: solid; border-color: rgb("
                                                        "105,105,105);}\n "
                                                        "QLineEdit::hover {\n"
                                                        "border-color:  rgb(49, 77, 162);\n"
                                                        "}")
                    self.mod_serial_lnedt.setText("")
                    self.mod_serial_lnedt.setObjectName("Module Serial No.")
                    self.mod_serial_lnedt.setPlaceholderText("Enter the Mod Serial No.")

                    self.base_serial_lbl = QtWidgets.QLabel(self.central_widget)
                    self.base_serial_lbl.setStyleSheet("border:0px;")
                    self.base_serial_lbl.setText("BaseBoard Serial No")
                    self.base_serial_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.base_serial_lbl.setFont(font)
                    self.base_serial_lbl.setGeometry(QtCore.QRect(25, 260, 250, 15))
                    self.base_serial_lbl.setObjectName("base_serial_lbl")

                    self.base_serial_lnedt = QtWidgets.QLineEdit(self.central_widget)
                    self.base_serial_lnedt.setGeometry(QtCore.QRect(25, 280, 250, 40))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(75)
                    self.base_serial_lnedt.setFont(font)
                    self.base_serial_lnedt.setText("E")
                    self.base_serial_lnedt.setFont(font)
                    self.base_serial_lnedt.setReadOnly(True)
                    self.base_serial_lnedt.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
                    self.base_serial_lnedt.setAutoFillBackground(False)
                    self.base_serial_lnedt.setStyleSheet("\n"
                                                         "QLineEdit {\n"
                                                         "border-width: 3px; border-style: solid; border-color: rgb(105,105,105);}\n"
                                                         "QLineEdit::hover {\n"
                                                         "border-color:  rgb(49, 77, 162);\n"
                                                         "}")
                    self.base_serial_lnedt.setText("")
                    self.base_serial_lnedt.setObjectName("Base Serial No.")
                    self.base_serial_lnedt.setPlaceholderText("Enter the base Serial No.")

                    self.product_serial_lbl = QtWidgets.QLabel(self.central_widget)
                    self.product_serial_lbl.setStyleSheet("border:0px;")
                    self.product_serial_lbl.setText("Product Serial No")
                    self.product_serial_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.product_serial_lbl.setFont(font)
                    self.product_serial_lbl.setGeometry(QtCore.QRect(25, 330, 250, 15))
                    self.product_serial_lbl.setObjectName("product_serial_lbl")

                    self.product_serial_lnedt = QtWidgets.QLineEdit(self.central_widget)
                    self.product_serial_lnedt.setGeometry(QtCore.QRect(25, 350, 250, 40))
                    self.product_serial_lnedt.setPlaceholderText("Enter the Product Serial No.")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    self.product_serial_lnedt.setReadOnly(True)
                    font.setWeight(75)
                    self.product_serial_lnedt.setFont(font)
                    self.product_serial_lnedt.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
                    self.product_serial_lnedt.setAutoFillBackground(False)
                    self.product_serial_lnedt.setStyleSheet("\n"
                                                            "QLineEdit {\n"
                                                            "border-width: 3px; border-style: solid; border-color: "
                                                            "rgb(105,105,105);}\n "
                                                            "QLineEdit::hover {\n"
                                                            "border-color:  rgb(49, 77, 162);\n"
                                                            "}")
                    self.product_serial_lnedt.setText("")
                    self.product_serial_lnedt.setObjectName("Product Serial No.")

                    self.image_preview = QtWidgets.QLabel(self.central_widget)
                    if self.window_height < 1085:
                        self.image_preview.setGeometry(QtCore.QRect(310, 210,
                                                                    (self.window_width - 950),
                                                                    (self.window_height - 340)))

                    elif self.window_height < 1610:
                        self.image_preview.setGeometry(QtCore.QRect(310, 210, (self.window_width - 320),
                                                                    (self.window_height - 360)))
                    elif self.window_height < 2165:
                        self.image_preview.setGeometry(QtCore.QRect(310, 210, (self.window_width - 320),
                                                                    (self.window_height - 380)))

                    self.image_preview.setText("")
                    self.image_preview.setPixmap(QtGui.QPixmap(r".\media\No-Preview-Available.jpg"))
                    self.image_preview.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.image_preview.setFrameShadow(QtWidgets.QFrame.Plain)
                    self.image_preview.setAlignment(Qt.AlignCenter)
                    self.image_preview.setObjectName("image_preview")

                    self.mtf_grpah_widget = QtWidgets.QWidget(self.central_widget)
                    self.mtf_grpah_widget.setObjectName("mtf_grpah_widget")
                    self.mtf_grpah_widget.setGeometry(QtCore.QRect(1300, 210, 600, 500))
                    self.mtf_graph_verticalLayout = QtWidgets.QVBoxLayout()
                    self.figure = plt.figure()
                    self.canvas = FigureCanvas(self.figure)
                    self.ax = self.figure.add_subplot(111)
                    image_path = r".\media\plot_graph.png"
                    preview = imread(image_path)
                    self.ax.imshow(preview)
                    self.ax.set_title('MTF graph')
                    self.ax.axis('off')
                    self.mtf_graph_verticalLayout.addWidget(self.canvas)
                    self.mtf_grpah_widget.setLayout(self.mtf_graph_verticalLayout)
                    self.mtf_graph_verticalLayout.setObjectName("verticalLayout_3")

                    self.tableWidget = QTableWidget(self.central_widget)
                    self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                    self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

                    self.tableWidget.setGeometry(
                        QtCore.QRect(1440, (self.window_height - 325), 350, 120))
                    self.tableWidget.setRowCount(4)
                    self.tableWidget.setColumnCount(2)
                    self.tableWidget.setFont(QtGui.QFont('Arial', 13))

                    item = QtWidgets.QTableWidgetItem(str("Overall Running"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(0, 100, 255))
                    self.tableWidget.setItem(0, 0, item)

                    item = QtWidgets.QTableWidgetItem(str("NA"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(0, 100, 255))
                    self.tableWidget.setItem(0, 1, item)

                    item = QtWidgets.QTableWidgetItem(str("Passed Count"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(0, 153, 76))
                    self.tableWidget.setItem(1, 0, item)

                    item = QtWidgets.QTableWidgetItem(str("NA"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(0, 153, 76))
                    self.tableWidget.setItem(1, 1, item)

                    item = QtWidgets.QTableWidgetItem(str("Failed Count"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(255, 0, 0))
                    self.tableWidget.setItem(2, 0, item)

                    item = QtWidgets.QTableWidgetItem(str("NA"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(255, 0, 0))
                    self.tableWidget.setItem(2, 1, item)

                    item = QtWidgets.QTableWidgetItem(str("Validation"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(245, 100, 20))
                    self.tableWidget.setItem(3, 0, item)

                    item = QtWidgets.QTableWidgetItem(str("NA"))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(245, 100, 20))
                    self.tableWidget.setItem(3, 1, item)

                    self.tableWidget.setColumnWidth(0, 200)
                    self.tableWidget.setColumnWidth(1, 150)
                    self.tableWidget.verticalHeader().setVisible(False)
                    self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                    self.tableWidget.horizontalHeader().setVisible(False)

                else:
                    self.stackedWidget = QtWidgets.QStackedWidget(self.central_widget)
                    self.stackedWidget.setGeometry(QtCore.QRect(10, 50, 420, 900))
                    self.stackedWidget.setObjectName("stackedWidget")

                    self.btn_mode = QtWidgets.QPushButton(self.central_widget)
                    self.btn_mode.setGeometry(QtCore.QRect(self.window_width - 50, 15, 40, 40))
                    font = QtGui.QFont()
                    font.setPointSize(14)
                    self.btn_mode.setFont(font)
                    self.btn_mode.setStyleSheet("""
                                QPushButton {
                                    border-radius: 20px;
                                    border: 2px solid transparent;
                                }
                                QPushButton:hover {
                                    border: 5px solid #555;
                                    background-color: rgba(255, 255, 255, 0.5);
                                }
                            """)
                    self.btn_mode.setText("")
                    icon10 = QtGui.QIcon()
                    icon10.addPixmap(QtGui.QPixmap(r".\media\window_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.btn_mode.setIcon(icon10)
                    self.btn_mode.setIconSize(QtCore.QSize(40, 40))
                    self.btn_mode.setObjectName("btn_mode")

                    self.stackedWidget_title_lbl = QtWidgets.QLabel(self.central_widget)
                    self.stackedWidget_title_lbl.setGeometry(QtCore.QRect(70, 0, 290, 40))
                    self.stackedWidget_title_lbl.setText('Create User')
                    font = QtGui.QFont()
                    font.setPointSize(16)
                    self.stackedWidget_title_lbl.setFont(font)
                    self.stackedWidget_title_lbl.setAlignment(Qt.AlignCenter)
                    self.stackedWidget_title_lbl.setObjectName("stackedWidget_title_lbl")

                    self.stackedWidget_main_title_lbl = QtWidgets.QLabel(self.central_widget)
                    self.stackedWidget_main_title_lbl.setGeometry(QtCore.QRect(960, 0, 290, 40))
                    self.stackedWidget_main_title_lbl.setText('Recipe Creation')
                    font = QtGui.QFont()
                    font.setPointSize(16)
                    self.stackedWidget_main_title_lbl.setFont(font)
                    self.stackedWidget_main_title_lbl.hide()
                    self.stackedWidget_main_title_lbl.setAlignment(Qt.AlignCenter)
                    self.stackedWidget_main_title_lbl.setObjectName("stackedWidget_main_title_lbl")

                    self.user_create_layout = QtWidgets.QWidget()
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.user_create_layout.sizePolicy().hasHeightForWidth())
                    self.user_create_layout.setSizePolicy(sizePolicy)
                    self.user_create_layout.setMinimumSize(QtCore.QSize(420, 1000))
                    self.user_create_layout.setMaximumSize(QtCore.QSize(420, 1000))
                    self.user_create_layout.setStyleSheet("Background-color:RGB(240, 240, 240)")
                    self.user_create_layout.setObjectName("user_create_layout")

                    self.lbl_emp_id = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_emp_id.setGeometry(QtCore.QRect(20, 30, 60, 35))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_emp_id.sizePolicy().hasHeightForWidth())
                    self.lbl_emp_id.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lbl_emp_id.setFont(font)
                    self.lbl_emp_id.setObjectName("lbl_emp_id")
                    self.lnedt_emp_id = Password_LineEdit(self.user_create_layout)
                    self.lnedt_emp_id.setGeometry(QtCore.QRect(170, 30, 201, 31))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lnedt_emp_id.setFont(font)
                    regx = QRegExp('^[1-9]\d{0,8}$')
                    lnedt_emp_id = QRegExpValidator(regx, self.lnedt_emp_id)
                    self.lnedt_emp_id.setValidator(lnedt_emp_id)
                    self.lnedt_emp_id.setObjectName("lnedt_emp_id")

                    self.lbl_warning_emp_id = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_warning_emp_id.setGeometry(QtCore.QRect(170, 55, 200, 35))
                    self.lbl_warning_emp_id.setText("*Employee id Already exists")
                    self.lbl_warning_emp_id.setStyleSheet("color:red")
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_warning_emp_id.sizePolicy().hasHeightForWidth())
                    self.lbl_warning_emp_id.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lbl_warning_emp_id.setFont(font)
                    self.lbl_warning_emp_id.hide()
                    self.lbl_warning_emp_id.setObjectName("lbl_warning_emp_id")

                    self.lbl_user_name = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_user_name.setGeometry(QtCore.QRect(20, 110, 60, 35))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_user_name.sizePolicy().hasHeightForWidth())
                    self.lbl_user_name.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lbl_user_name.setFont(font)
                    self.lbl_user_name.setObjectName("lbl_user_name")
                    self.lnedt_name = Password_LineEdit(self.user_create_layout)
                    self.lnedt_name.setGeometry(QtCore.QRect(170, 110, 201, 31))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lnedt_name.setFont(font)
                    regx = QRegExp('^[a-zA-Z\sa-zA-Z]{3,20}$')
                    lnedt_name = QRegExpValidator(regx, self.lnedt_name)
                    self.lnedt_name.setValidator(lnedt_name)
                    self.lnedt_name.setObjectName("lnedt_name")

                    self.lbl_set_password = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_set_password.setGeometry(QtCore.QRect(20, 190, 120, 35))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_set_password.sizePolicy().hasHeightForWidth())
                    self.lbl_set_password.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lbl_set_password.setFont(font)
                    self.lbl_set_password.setLayoutDirection(QtCore.Qt.LeftToRight)
                    self.lbl_set_password.setObjectName("lbl_set_password")
                    self.lnedt_set_password = Password_LineEdit(self.user_create_layout)
                    self.lnedt_set_password.setGeometry(QtCore.QRect(170, 190, 201, 31))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lnedt_set_password.setFont(font)
                    self.lnedt_set_password.setMaxLength(15)
                    self.lnedt_set_password.setEchoMode(QtWidgets.QLineEdit.Normal)
                    self.lnedt_set_password.setObjectName("lnedt_set_password")

                    self.lbl_warning_password = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_warning_password.setGeometry(QtCore.QRect(170, 215, 200, 35))
                    self.lbl_warning_password.setText("*Minimum 8 character are only allowed")
                    self.lbl_warning_password.setStyleSheet("color:red")
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_warning_password.sizePolicy().hasHeightForWidth())
                    self.lbl_warning_password.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lbl_warning_password.setFont(font)
                    self.lbl_warning_password.hide()
                    self.lbl_warning_password.setObjectName("lbl_warning_password_2")

                    self.lbl_set_password_2 = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_set_password_2.setGeometry(QtCore.QRect(20, 270, 160, 35))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_set_password_2.sizePolicy().hasHeightForWidth())
                    self.lbl_set_password_2.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lbl_set_password_2.setFont(font)
                    self.lbl_set_password_2.setLayoutDirection(QtCore.Qt.LeftToRight)
                    self.lbl_set_password_2.setObjectName("lbl_set_password_2")
                    self.lnedt_set_password_2 = Password_LineEdit(self.user_create_layout)
                    self.lnedt_set_password_2.setGeometry(QtCore.QRect(170, 270, 200, 30))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lnedt_set_password_2.setFont(font)
                    self.lnedt_set_password_2.setMaxLength(15)
                    self.lnedt_set_password_2.setEchoMode(QtWidgets.QLineEdit.Normal)
                    self.lnedt_set_password_2.setObjectName("lnedt_set_password_2")

                    self.lbl_warning_password_2 = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_warning_password_2.setGeometry(QtCore.QRect(170, 295, 200, 35))
                    self.lbl_warning_password_2.setText("*Confirm password doesn't match")
                    self.lbl_warning_password_2.setStyleSheet("color:red")
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_warning_password_2.sizePolicy().hasHeightForWidth())
                    self.lbl_warning_password_2.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lbl_warning_password_2.setFont(font)
                    self.lbl_warning_password_2.hide()
                    self.lbl_warning_password_2.setObjectName("lbl_warning_password_2")

                    self.cmb_user_permission = combobox(self.user_create_layout)
                    self.cmb_user_permission.setGeometry(QtCore.QRect(170, 350, 200, 30))
                    self.cmb_user_permission.addItem("--Select--")
                    self.cmb_user_permission.addItem("Operator")
                    self.cmb_user_permission.addItem("Supervisor")
                    self.cmb_user_permission.addItem("Admin")
                    self.cmb_user_permission.addItem("Superuser")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.cmb_user_permission.setFont(font)
                    self.cmb_user_permission.setObjectName("cmb_user_permission")

                    self.lbl_user_permission = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_user_permission.setGeometry(QtCore.QRect(20, 350, 145, 35))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_user_permission.sizePolicy().hasHeightForWidth())
                    self.lbl_user_permission.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lbl_user_permission.setFont(font)
                    self.lbl_user_permission.setLayoutDirection(QtCore.Qt.LeftToRight)
                    self.lbl_user_permission.setObjectName("lbl_user_permission")

                    self.lbl_privilege = QtWidgets.QLabel(self.user_create_layout)
                    self.lbl_privilege.setGeometry(QtCore.QRect(20, 430, 145, 35))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_privilege.sizePolicy().hasHeightForWidth())
                    self.lbl_privilege.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lbl_privilege.setFont(font)
                    self.lbl_privilege.setLayoutDirection(QtCore.Qt.LeftToRight)
                    self.lbl_privilege.setObjectName("lbl_privilege")

                    self.cmb_user_privilege = combobox(self.user_create_layout)
                    self.cmb_user_privilege.setGeometry(QtCore.QRect(170, 430, 200, 30))
                    self.cmb_user_privilege.addItem("No")
                    self.cmb_user_privilege.addItem("Yes")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.cmb_user_privilege.setFont(font)
                    self.cmb_user_privilege.setObjectName("cmb_user_privilege")

                    self.create_fingerprint = QtWidgets.QLabel(self.user_create_layout)
                    self.create_fingerprint.setGeometry(QtCore.QRect(20, 510, 145, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.create_fingerprint.setFont(font)
                    self.create_fingerprint.setObjectName("create_fingerprint")

                    self.btn_fingerprint_create = QtWidgets.QPushButton(self.user_create_layout)
                    self.btn_fingerprint_create.setGeometry(QtCore.QRect(150, 510, 120, 40))
                    font = QtGui.QFont()
                    font.setPointSize(14)
                    self.btn_fingerprint_create.setFont(font)
                    self.btn_fingerprint_create.setStyleSheet("QPushButton { color: blue; "
                                                              "text-decoration: underline; "
                                                              "border: none; "
                                                              "background: none; }")
                    self.btn_fingerprint_create.setCursor(QCursor(Qt.PointingHandCursor))
                    self.btn_fingerprint_create.setObjectName("btn_fingerprint_create")

                    self.scanning_lbl = QtWidgets.QLabel(self.user_create_layout)
                    self.scanning_lbl.setGeometry(QtCore.QRect(80, 680, 210, 200))
                    movie = QtGui.QMovie(r".\media\fingerprint_1.gif")
                    self.scanning_lbl.setMovie(movie)
                    movie.setSpeed(75)
                    movie.start()
                    self.scanning_lbl.hide()
                    self.scanning_lbl.setScaledContents(True)

                    self.btn_user_create = QtWidgets.QPushButton(self.user_create_layout)
                    self.btn_user_create.setGeometry(QtCore.QRect(120, 600, 120, 40))
                    font = QtGui.QFont()
                    font.setPointSize(14)
                    self.btn_user_create.setFont(font)
                    self.btn_user_create.setStyleSheet("QPushButton{\n"
                                                       "background-color:rgb(49, 77, 162);\n"
                                                       "color:rgb(255, 255, 255);\n"
                                                       "border-radius: 10px;\n"
                                                       "}"
                                                       "QPushButton:Pressed{\n"
                                                       "border: 3px solid;\n"
                                                       "}"
                                                       )
                    self.btn_user_create.setObjectName("btn_user_create")
                    self.user_create_layout.setObjectName("user_create_layout")
                    self.stackedWidget.addWidget(self.user_create_layout)

                    self.station_1_layout = QtWidgets.QWidget()
                    self.station_1_layout.setObjectName("station_1_layout")
                    self.loading_scrollarea = QtWidgets.QScrollArea(self.station_1_layout)
                    self.loading_scrollarea.setGeometry(QtCore.QRect(0, 0, 420, 900))
                    self.loading_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.loading_scrollarea.setWidgetResizable(True)
                    self.loading_scrollarea.setObjectName("loading_scrollarea")
                    self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
                    self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 401, 1142))
                    self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
                    self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
                    self.verticalLayout_2.setObjectName("verticalLayout_2")

                    self.device_details_grpbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.device_details_grpbox.sizePolicy().hasHeightForWidth())
                    self.device_details_grpbox.setSizePolicy(sizePolicy)
                    self.device_details_grpbox.setMinimumSize(QtCore.QSize(0, 425))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.device_details_grpbox.setFont(font)
                    self.device_details_grpbox.setStyleSheet("Background-color:RGB(240, 240, 240)")
                    self.device_details_grpbox.setObjectName("device_details_grpbox")

                    self.path_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.path_lbl.setGeometry(QtCore.QRect(10, 30, 120, 25))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.path_lbl.setFont(font)
                    self.path_lbl.setObjectName("path_lbl")
                    self.path_txt_box = QtWidgets.QLineEdit(self.device_details_grpbox)
                    self.path_txt_box.setGeometry(QtCore.QRect(90, 30, 200, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.path_txt_box.setReadOnly(True)
                    self.path_txt_box.setFont(font)
                    self.path_txt_box.setObjectName("path_txt_box")
                    self.path_btn = QtWidgets.QPushButton(self.device_details_grpbox)
                    self.path_btn.setGeometry(QtCore.QRect(300, 30, 75, 30))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.path_btn.setFont(font)
                    self.path_btn.setStyleSheet("QPushButton{\n"
                                                "background-color:rgb(49, 77, 162);\n"
                                                "color:rgb(255, 255, 255);\n"
                                                "border-radius: 10px;\n"
                                                "}"
                                                "QPushButton:Pressed{\n"
                                                "border: 3px solid;\n"
                                                "}"
                                                )
                    self.path_btn.setObjectName("path_btn")

                    self.get_device_btn = QtWidgets.QPushButton(self.device_details_grpbox)
                    self.get_device_btn.setGeometry(QtCore.QRect(300, 80, 75, 30))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.get_device_btn.setFont(font)
                    self.get_device_btn.setStyleSheet("QPushButton:enabled{\n"
                                                      "background-color:rgb(49, 77, 162);\n"
                                                      "color:rgb(255, 255, 255);\n"
                                                      "border-radius: 10px;\n"
                                                      "}"
                                                      "QPushButton:Pressed{\n"
                                                      "background-color: #1a5276;\n"
                                                      "}"
                                                      "QPushButton:disabled"
                                                      "{"
                                                      "background-color:#95a5a6;"
                                                      "border-radius: 10px;\n"
                                                      "}"
                                                      )
                    self.get_device_btn.setObjectName("get_device_btn")
                    self.device_name_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.device_name_lbl.setGeometry(QtCore.QRect(10, 75, 120, 35))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.device_name_lbl.setFont(font)
                    self.device_name_lbl.setObjectName("device_name_lbl")
                    self.device_name_box = QtWidgets.QLabel(self.device_details_grpbox)
                    self.device_name_box.setGeometry(QtCore.QRect(90, 80, 200, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.device_name_box.setFont(font)
                    self.device_name_box.setText('No Devices')
                    self.device_name_box.setAlignment(Qt.AlignCenter)
                    self.device_name_box.setObjectName("device_name_box")

                    self.firmware_title_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.firmware_title_lbl.setGeometry(QtCore.QRect(10, 125, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.firmware_title_lbl.setFont(font)
                    self.firmware_title_lbl.setText("FW Version")
                    self.firmware_title_lbl.setObjectName("firmware_title_lbl")

                    self.firmware_value_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.firmware_value_lbl.setGeometry(QtCore.QRect(90, 130, 200, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.firmware_value_lbl.setFont(font)
                    self.firmware_value_lbl.setText("None")
                    self.firmware_value_lbl.setAlignment(Qt.AlignCenter)
                    self.firmware_value_lbl.setObjectName("firmware_value_lbl")

                    self.resolution_lbl_name = QtWidgets.QLabel(self.device_details_grpbox)
                    self.resolution_lbl_name.setGeometry(QtCore.QRect(10, 175, 60, 35))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.resolution_lbl_name.setFont(font)
                    self.resolution_lbl_name.setObjectName("resolution_lbl_name")
                    self.resolution_box = combobox(self.device_details_grpbox)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.resolution_box.setFont(font)
                    self.resolution_box.setGeometry(QtCore.QRect(90, 180, 200, 30))
                    self.resolution_box.setObjectName("resolution_box")

                    self.exposure_Lbl_name = QtWidgets.QLabel(self.device_details_grpbox)
                    self.exposure_Lbl_name.setGeometry(QtCore.QRect(10, 225, 60, 35))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.exposure_Lbl_name.setFont(font)
                    self.exposure_Lbl_name.setObjectName("exposure_Lbl_name")
                    self.exposure_box = combobox(self.device_details_grpbox)
                    self.exposure_box.setGeometry(QtCore.QRect(90, 230, 200, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.exposure_box.setFont(font)
                    self.exposure_box.setObjectName("exposure_box")

                    self.mod_board_check_box = QtWidgets.QCheckBox("Mod board", self.device_details_grpbox)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.mod_board_check_box.setFont(font)
                    self.mod_board_check_box.setGeometry(QtCore.QRect(10, 270, 100, 30))

                    self.base_board_check_box = QtWidgets.QCheckBox("Base board", self.device_details_grpbox)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.base_board_check_box.setFont(font)
                    self.base_board_check_box.setGeometry(QtCore.QRect(120, 270, 100, 30))

                    self.product_board_check_box = QtWidgets.QCheckBox("Product Serial", self.device_details_grpbox)
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.product_board_check_box.setFont(font)
                    self.product_board_check_box.setGeometry(QtCore.QRect(230, 270, 100, 30))

                    self.product_sr_no_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.product_sr_no_lbl.setStyleSheet("border:0px;")
                    self.product_sr_no_lbl.setText("Product Serial No.")
                    self.product_sr_no_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    self.product_sr_no_lbl.setFont(font)
                    self.product_sr_no_lbl.setGeometry(QtCore.QRect(10, 300, 200, 30))
                    self.product_sr_no_lbl.hide()
                    self.product_sr_no_lbl.setObjectName("product_sr_no_lbl")

                    self.product_sr_no_box = QtWidgets.QLineEdit(self.device_details_grpbox)
                    self.product_sr_no_box.setGeometry(QtCore.QRect(10, 325, 280, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.product_sr_no_box.setFont(font)
                    self.product_sr_no_box.hide()
                    self.product_sr_no_box.setObjectName("product_sr_no_box")

                    self.product_sr_no_len_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.product_sr_no_len_lbl.setStyleSheet("border:0px;")
                    self.product_sr_no_len_lbl.setText("Serial No.length")
                    self.product_sr_no_len_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    self.product_sr_no_len_lbl.setFont(font)
                    self.product_sr_no_len_lbl.setGeometry(QtCore.QRect(10, 300, 200, 30))
                    self.product_sr_no_len_lbl.hide()
                    self.product_sr_no_len_lbl.setObjectName("product_sr_no_lbl")

                    self.product_sr_no_len_box = QtWidgets.QLineEdit(self.device_details_grpbox)
                    self.product_sr_no_len_box.setGeometry(QtCore.QRect(10, 325, 280, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.product_sr_no_len_box.setFont(font)
                    validator = QIntValidator(0, 100, self.product_sr_no_len_box)
                    self.product_sr_no_len_box.setValidator(validator)
                    self.product_sr_no_len_box.hide()
                    self.product_sr_no_len_box.setObjectName("product_sr_no_len_box")

                    self.mod_sr_no_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.mod_sr_no_lbl.setStyleSheet("border:0px;")
                    self.mod_sr_no_lbl.setText("Modboard Serial No.")
                    self.mod_sr_no_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    self.mod_sr_no_lbl.setFont(font)
                    self.mod_sr_no_lbl.setGeometry(QtCore.QRect(10, 360, 200, 30))
                    self.mod_sr_no_lbl.hide()
                    self.mod_sr_no_lbl.setObjectName("mod_sr_no_lbl")

                    self.mod_Serial_No_box = QtWidgets.QLineEdit(self.device_details_grpbox)
                    self.mod_Serial_No_box.setGeometry(QtCore.QRect(10, 385, 280, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.mod_Serial_No_box.setFont(font)
                    self.mod_Serial_No_box.hide()
                    self.mod_Serial_No_box.setObjectName("mod_Serial_No_box")

                    self.mod_sr_no_len_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.mod_sr_no_len_lbl.setStyleSheet("border:0px;")
                    self.mod_sr_no_len_lbl.setText("Serial No.length")
                    self.mod_sr_no_len_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    self.mod_sr_no_len_lbl.setFont(font)
                    self.mod_sr_no_len_lbl.setGeometry(QtCore.QRect(10, 360, 200, 30))
                    self.mod_sr_no_len_lbl.hide()
                    self.mod_sr_no_len_lbl.setObjectName("mod_sr_no_len_lbl")

                    self.mod_Serial_No_len_box = QtWidgets.QLineEdit(self.device_details_grpbox)
                    self.mod_Serial_No_len_box.setGeometry(QtCore.QRect(10, 385, 280, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.mod_Serial_No_len_box.setFont(font)
                    validator = QIntValidator(0, 100, self.mod_Serial_No_len_box)
                    self.mod_Serial_No_len_box.setValidator(validator)
                    self.mod_Serial_No_len_box.hide()
                    self.mod_Serial_No_len_box.setObjectName("mod_Serial_No_len_box")

                    self.base_sr_no_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.base_sr_no_lbl.setStyleSheet("border:0px;")
                    self.base_sr_no_lbl.setText("Baseboard Serial No.")
                    self.base_sr_no_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    self.base_sr_no_lbl.setFont(font)
                    self.base_sr_no_lbl.hide()
                    self.base_sr_no_lbl.setGeometry(QtCore.QRect(10, 420, 200, 30))
                    self.base_sr_no_lbl.setObjectName("base_sr_no_lbl")

                    self.base_Serial_No_box = QtWidgets.QLineEdit(self.device_details_grpbox)
                    self.base_Serial_No_box.setGeometry(QtCore.QRect(10, 445, 250, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.base_Serial_No_box.setFont(font)
                    self.base_Serial_No_box.hide()
                    self.base_Serial_No_box.setObjectName("base_Serial_No_box")

                    self.base_sr_no_len_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.base_sr_no_len_lbl.setStyleSheet("border:0px;")
                    self.base_sr_no_len_lbl.setText("Serial No.length")
                    self.base_sr_no_len_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    self.base_sr_no_len_lbl.setFont(font)
                    self.base_sr_no_len_lbl.hide()
                    self.base_sr_no_len_lbl.setGeometry(QtCore.QRect(250, 420, 200, 30))
                    self.base_sr_no_len_lbl.setObjectName("base_sr_no_len_lbl")

                    self.base_Serial_No_len_box = QtWidgets.QLineEdit(self.device_details_grpbox)
                    self.base_Serial_No_len_box.setGeometry(QtCore.QRect(250, 445, 100, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.base_Serial_No_len_box.setFont(font)
                    validator = QIntValidator(0, 100, self.base_Serial_No_len_box)
                    self.base_Serial_No_len_box.setValidator(validator)
                    self.base_Serial_No_len_box.hide()
                    self.base_Serial_No_len_box.setObjectName("base_Serial_No_len_box")

                    self.product_name_lbl = QtWidgets.QLabel(self.device_details_grpbox)
                    self.product_name_lbl.setStyleSheet("border:0px;")
                    self.product_name_lbl.setText("Product Name")
                    self.product_name_lbl.setScaledContents(True)
                    font = QtGui.QFont()
                    self.product_name_lbl.setFont(font)
                    self.product_name_lbl.setGeometry(QtCore.QRect(10, 300, 200, 30))
                    self.product_name_lbl.setObjectName("mod_serial_lbl")

                    self.product_name_box = QtWidgets.QLineEdit(self.device_details_grpbox)
                    self.product_name_box.setGeometry(QtCore.QRect(10, 325, 280, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.product_name_box.setFont(font)
                    self.product_name_box.setObjectName("product_name_box")
                    self.verticalLayout_2.addWidget(self.device_details_grpbox)

                    self.loading_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.loading_groupbox.sizePolicy().hasHeightForWidth())
                    self.loading_groupbox.setSizePolicy(sizePolicy)
                    self.loading_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.loading_groupbox.setFont(font)
                    self.loading_groupbox.setObjectName("loading_groupbox")

                    self.loading_init_lbl = QtWidgets.QLabel(self.loading_groupbox)
                    self.loading_init_lbl.setGeometry(QtCore.QRect(10, 20, 150, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.loading_init_lbl.setFont(font)
                    self.loading_init_lbl.setObjectName("loading_init_lbl")
                    self.loading_init_btn = QtWidgets.QPushButton(self.loading_groupbox)
                    self.loading_init_btn.setGeometry(QtCore.QRect(150, 15, 70, 30))
                    self.loading_init_btn.setAccessibleName("loading init")
                    self.loading_init_btn.setText("Init")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    font.setBold(True)
                    self.loading_init_btn.setFont(font)
                    self.loading_init_btn.setStyleSheet("QPushButton{\n"
                                                        "background-color:rgb(49, 77, 162);\n"
                                                        "color:rgb(255, 255, 255);\n"
                                                        "border-radius: 10px;\n"
                                                        "}"
                                                        "QPushButton:Pressed{\n"
                                                        "border: 3px solid;\n"
                                                        "}"
                                                        )
                    self.loading_init_btn.setObjectName("loading_init_btn")

                    self.loading_overall_homing_btn = QtWidgets.QPushButton(self.loading_groupbox)
                    self.loading_overall_homing_btn.setGeometry(QtCore.QRect(280, 15, 90, 30))
                    self.loading_overall_homing_btn.setText("Machine Homing")
                    self.loading_overall_homing_btn.setAccessibleName("overall_homing")
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    font.setBold(True)
                    self.loading_overall_homing_btn.setFont(font)
                    self.loading_overall_homing_btn.hide()
                    self.loading_overall_homing_btn.setStyleSheet("QPushButton{\n"
                                                                  "background-color:rgb(49, 77, 162);\n"
                                                                  "color:rgb(255, 255, 255);\n"
                                                                  "border-radius: 10px;\n"
                                                                  "}"
                                                                  "QPushButton:Pressed{\n"
                                                                  "border: 3px solid;\n"
                                                                  "}"
                                                                  )
                    self.loading_overall_homing_btn.setObjectName("loading_overall_homing_btn")

                    self.loading_door_lbl = QtWidgets.QLabel(self.loading_groupbox)
                    self.loading_door_lbl.setGeometry(QtCore.QRect(10, 60, 90, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.loading_door_lbl.setFont(font)
                    self.loading_door_lbl.setObjectName("loading_door_lbl")

                    self.front_door_open_lbl = QtWidgets.QLabel(self.loading_groupbox)
                    self.front_door_open_lbl.setGeometry(QtCore.QRect(250, 60, 90, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.front_door_open_lbl.setFont(font)
                    self.front_door_open_lbl.setObjectName("front_door_open_lbl")
                    self.front_door_open_btn = QtWidgets.QPushButton(self.loading_groupbox)
                    self.front_door_open_btn.setGeometry(QtCore.QRect(290, 60, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(28)
                    font.setBold(True)
                    font.setWeight(75)
                    self.front_door_open_btn.setFont(font)
                    self.front_door_open_btn.setStyleSheet("QPushButton{\n"
                                                           "background-color:rgb(49, 77, 162);\n"
                                                           "color:rgb(255, 255, 255);\n"
                                                           "border-radius: 25px;\n"
                                                           "}"
                                                           "QPushButton:Pressed{\n"
                                                           "border: 3px solid;\n"
                                                           "}"
                                                           )
                    self.front_door_open_btn.setText("")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\open.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
                    self.front_door_open_btn.setIcon(icon)
                    self.front_door_open_btn.setIconSize(QtCore.QSize(65, 65))
                    self.front_door_open_btn.setFlat(True)
                    self.front_door_open_btn.setObjectName("front_door_open_btn")

                    self.front_door_close_lbl = QtWidgets.QLabel(self.loading_groupbox)
                    self.front_door_close_lbl.setGeometry(QtCore.QRect(110, 60, 60, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.front_door_close_lbl.setFont(font)
                    self.front_door_close_lbl.setObjectName("front_door_close_lbl")
                    self.front_door_close_btn = QtWidgets.QPushButton(self.loading_groupbox)
                    self.front_door_close_btn.setGeometry(QtCore.QRect(150, 60, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(28)
                    font.setBold(True)
                    font.setWeight(75)
                    self.front_door_close_btn.setFont(font)
                    self.front_door_close_btn.setStyleSheet("QPushButton{\n"
                                                            "background-color:rgb(49, 77, 162);\n"
                                                            "color:rgb(255, 255, 255);\n"
                                                            "border-radius: 25px;\n"
                                                            "}"
                                                            "QPushButton:Pressed{\n"
                                                            "border: 3px solid;\n"
                                                            "}"
                                                            )
                    self.front_door_close_btn.setText("")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\close.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
                    self.front_door_close_btn.setIcon(icon)
                    self.front_door_close_btn.setIconSize(QtCore.QSize(65, 65))
                    self.front_door_close_btn.setFlat(True)
                    self.front_door_close_btn.setObjectName("front_door_close_btn")

                    self.loading_part_load_lbl = QtWidgets.QLabel(self.loading_groupbox)
                    self.loading_part_load_lbl.setGeometry(QtCore.QRect(10, 100, 90, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.loading_part_load_lbl.setFont(font)
                    self.loading_part_load_lbl.setObjectName("loading_part_load_lbl")

                    self.loading_part_load_open_lbl = QtWidgets.QLabel(self.loading_groupbox)
                    self.loading_part_load_open_lbl.setGeometry(QtCore.QRect(250, 100, 90, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.loading_part_load_open_lbl.setFont(font)
                    self.loading_part_load_open_lbl.setObjectName("loading_part_load_open_lbl")

                    self.loading_part_load_close_lbl = QtWidgets.QLabel(self.loading_groupbox)
                    self.loading_part_load_close_lbl.setGeometry(QtCore.QRect(110, 100, 60, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.loading_part_load_close_lbl.setFont(font)
                    self.loading_part_load_close_lbl.setObjectName("loading_part_load_close_lbl")

                    self.loading_part_load_close_btn = QtWidgets.QPushButton(self.loading_groupbox)
                    self.loading_part_load_close_btn.setGeometry(QtCore.QRect(150, 100, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(28)
                    font.setBold(True)
                    font.setWeight(75)
                    self.loading_part_load_close_btn.setFont(font)
                    self.loading_part_load_close_btn.setStyleSheet("QPushButton{\n"
                                                                   "background-color:rgb(49, 77, 162);\n"
                                                                   "color:rgb(255, 255, 255);\n"
                                                                   "border-radius: 25px;\n"
                                                                   "}"
                                                                   "QPushButton:Pressed{\n"
                                                                   "border: 3px solid;\n"
                                                                   "}"
                                                                   )
                    self.loading_part_load_close_btn.setText("")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\open.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
                    self.loading_part_load_close_btn.setIcon(icon)
                    self.loading_part_load_close_btn.setIconSize(QtCore.QSize(65, 65))
                    self.loading_part_load_close_btn.setFlat(True)
                    self.loading_part_load_close_btn.setObjectName("loading_part_load_close_btn")

                    self.loading_part_load_open_btn = QtWidgets.QPushButton(self.loading_groupbox)
                    self.loading_part_load_open_btn.setGeometry(QtCore.QRect(290, 100, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(28)
                    font.setBold(True)
                    font.setWeight(75)
                    self.loading_part_load_open_btn.setFont(font)
                    self.loading_part_load_open_btn.setStyleSheet("QPushButton{\n"
                                                                  "background-color:rgb(49, 77, 162);\n"
                                                                  "color:rgb(255, 255, 255);\n"
                                                                  "border-radius: 25px;\n"
                                                                  "}"
                                                                  "QPushButton:Pressed{\n"
                                                                  "border: 3px solid;\n"
                                                                  "}"
                                                                  )
                    self.loading_part_load_open_btn.setText("")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\close.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
                    self.loading_part_load_open_btn.setIcon(icon)
                    self.loading_part_load_open_btn.setIconSize(QtCore.QSize(65, 65))
                    self.loading_part_load_open_btn.setFlat(True)
                    self.loading_part_load_open_btn.setObjectName("loading_part_load_open_btn")
                    self.verticalLayout_2.addWidget(self.loading_groupbox)

                    self.loading_x_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.loading_x_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.loading_x_axis_groupbox.setSizePolicy(sizePolicy)
                    self.loading_x_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.loading_x_axis_groupbox.setFont(font)
                    self.loading_x_axis_groupbox.setObjectName("loading_x_axis_groupbox")

                    self.loading_x_axis_mini_lbl = QtWidgets.QLabel(self.loading_x_axis_groupbox)
                    self.loading_x_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_x_axis_mini_lbl.setFont(font)
                    self.loading_x_axis_mini_lbl.setObjectName("loading_x_axis_mini_lbl")
                    self.loading_x_axis_mini_lndt = QtWidgets.QLineEdit(self.loading_x_axis_groupbox)
                    self.loading_x_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(\d|[1-9]\d)(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.loading_x_axis_mini_lndt)
                    self.loading_x_axis_mini_lndt.setValidator(validator)
                    self.loading_x_axis_mini_lndt.setObjectName("loading_x_axis_mini_lndt")

                    self.loading_x_axis_speed_lbl = QtWidgets.QLabel(self.loading_x_axis_groupbox)
                    self.loading_x_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_x_axis_speed_lbl.setFont(font)
                    self.loading_x_axis_speed_lbl.setText("Speed")
                    self.loading_x_axis_speed_lbl.setObjectName("loading_x_axis_speed_lbl")
                    self.loading_x_axis_speed_lndt = QtWidgets.QLineEdit(self.loading_x_axis_groupbox)
                    self.loading_x_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 5000, self.loading_x_axis_speed_lndt)
                    self.loading_x_axis_speed_lndt.setValidator(validator)
                    self.loading_x_axis_speed_lndt.setToolTip("The X-Actuator speed is limited to a range of 0 to 2000")
                    self.loading_x_axis_speed_lndt.setObjectName("loading_x_axis_speed_lndt")

                    self.loading_x_axis_current_position_lbl = QtWidgets.QLabel(self.loading_x_axis_groupbox)
                    self.loading_x_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.loading_x_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.loading_x_axis_current_position_lbl.setFont(font)
                    self.loading_x_axis_current_position_lbl.setObjectName("loading_x_axis_current_position_lbl")
                    self.loading_x_axis_current_position_value = QtWidgets.QLabel(self.loading_x_axis_groupbox)
                    self.loading_x_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.loading_x_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.loading_x_axis_current_position_value.setFont(font)
                    self.loading_x_axis_current_position_value.setObjectName("loading_x_axis_current_position_value")

                    self.loading_x_axis_run_btn = QtWidgets.QPushButton(self.loading_x_axis_groupbox)
                    self.loading_x_axis_run_btn.setAccessibleName('loading_x_axis_run_btn')
                    self.loading_x_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.loading_x_axis_run_btn.setFont(font)
                    self.loading_x_axis_run_btn.setText("Run")
                    self.loading_x_axis_run_btn.setFlat(True)
                    self.loading_x_axis_run_btn.setFont(font)
                    self.loading_x_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                              "background-color:rgb(49, 77, 162);\n"
                                                              "color:rgb(255, 255, 255);\n"
                                                              "border-radius: 10px;\n"
                                                              "}"
                                                              "QPushButton:Pressed{\n"
                                                              "border: 3px solid;\n"
                                                              "}"
                                                              )
                    self.loading_x_axis_run_btn.setObjectName("loading_x_axis_run_btn")

                    self.loading_x_axis_homing_btn = QtWidgets.QPushButton(self.loading_x_axis_groupbox)
                    self.loading_x_axis_homing_btn.setGeometry(QtCore.QRect(270, 100, 100, 40))
                    self.loading_x_axis_homing_btn.setAccessibleName('loading x_axis_homing btn')
                    self.loading_x_axis_homing_btn.setText("Homing")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.loading_x_axis_homing_btn.setFont(font)
                    self.loading_x_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                                 "background-color:rgb(49, 77, 162);\n"
                                                                 "color:rgb(255, 255, 255);\n"
                                                                 "border-radius: 10px;\n"
                                                                 "}"
                                                                 "QPushButton:Pressed{\n"
                                                                 "border: 3px solid;\n"
                                                                 "}"
                                                                 )
                    self.loading_x_axis_homing_btn.setObjectName("loading_x_axis_homing_btn")
                    self.verticalLayout_2.addWidget(self.loading_x_axis_groupbox)

                    self.loading_y_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.loading_y_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.loading_y_axis_groupbox.setSizePolicy(sizePolicy)
                    self.loading_y_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.loading_y_axis_groupbox.setFont(font)
                    self.loading_y_axis_groupbox.setObjectName("loading_y_axis_groupbox")

                    self.loading_y_axis_mini_lbl = QtWidgets.QLabel(self.loading_y_axis_groupbox)
                    self.loading_y_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_y_axis_mini_lbl.setFont(font)
                    self.loading_y_axis_mini_lbl.setObjectName("loading_y_axis_mini_lbl")
                    self.loading_y_axis_mini_lndt = QtWidgets.QLineEdit(self.loading_y_axis_groupbox)
                    self.loading_y_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.loading_y_axis_mini_lndt)
                    self.loading_y_axis_mini_lndt.setValidator(validator)
                    self.loading_y_axis_mini_lndt.setObjectName("loading_y_axis_mini_lndt")

                    self.loading_y_axis_speed_lbl = QtWidgets.QLabel(self.loading_y_axis_groupbox)
                    self.loading_y_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_y_axis_speed_lbl.setFont(font)
                    self.loading_y_axis_speed_lbl.setText("Speed")
                    self.loading_y_axis_speed_lbl.setObjectName("loading_y_axis_speed_lbl")
                    self.loading_y_axis_speed_lndt = QtWidgets.QLineEdit(self.loading_y_axis_groupbox)
                    self.loading_y_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 15000, self.loading_y_axis_speed_lndt)
                    self.loading_y_axis_speed_lndt.setValidator(validator)
                    self.loading_y_axis_speed_lndt.setToolTip(
                        "The Y-Actuator speed is limited to a range of 0 to 15000")
                    self.loading_y_axis_speed_lndt.setObjectName("loading_y_axis_speed_lndt")

                    self.loading_y_axis_current_position_lbl = QtWidgets.QLabel(self.loading_y_axis_groupbox)
                    self.loading_y_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.loading_y_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.loading_y_axis_current_position_lbl.setFont(font)
                    self.loading_y_axis_current_position_lbl.setObjectName("loading_y_axis_current_position_lbl")
                    self.loading_y_axis_current_position_value = QtWidgets.QLabel(self.loading_y_axis_groupbox)
                    self.loading_y_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.loading_y_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.loading_y_axis_current_position_value.setFont(font)
                    self.loading_y_axis_current_position_value.setObjectName("loading_y_axis_current_position_value")

                    self.loading_y_axis_run_btn = QtWidgets.QPushButton(self.loading_y_axis_groupbox)
                    self.loading_y_axis_run_btn.setAccessibleName('loading_y_axis_run_btn')
                    self.loading_y_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.loading_y_axis_run_btn.setFont(font)
                    self.loading_y_axis_run_btn.setText("Run")
                    self.loading_y_axis_run_btn.setFlat(True)
                    self.loading_y_axis_run_btn.setFont(font)
                    self.loading_y_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                              "background-color:rgb(49, 77, 162);\n"
                                                              "color:rgb(255, 255, 255);\n"
                                                              "border-radius: 10px;\n"
                                                              "}"
                                                              "QPushButton:Pressed{\n"
                                                              "border: 3px solid;\n"
                                                              "}"
                                                              )
                    self.loading_y_axis_run_btn.setObjectName("loading_y_axis_run_btn")

                    self.loading_y_axis_homing_btn = QtWidgets.QPushButton(self.loading_y_axis_groupbox)
                    self.loading_y_axis_homing_btn.setGeometry(QtCore.QRect(270, 100, 100, 40))
                    self.loading_y_axis_homing_btn.setAccessibleName('loading y_axis_homing btn')
                    self.loading_y_axis_homing_btn.setText("Homing")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.loading_y_axis_homing_btn.setFont(font)
                    self.loading_y_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                                 "background-color:rgb(49, 77, 162);\n"
                                                                 "color:rgb(255, 255, 255);\n"
                                                                 "border-radius: 10px;\n"
                                                                 "}"
                                                                 "QPushButton:Pressed{\n"
                                                                 "border: 3px solid;\n"
                                                                 "}"
                                                                 )
                    self.loading_y_axis_homing_btn.setObjectName("loading_x_axis_homing_btn")
                    self.verticalLayout_2.addWidget(self.loading_y_axis_groupbox)

                    self.loading_slider_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.loading_slider_groupbox.sizePolicy().hasHeightForWidth())
                    self.loading_slider_groupbox.setSizePolicy(sizePolicy)
                    self.loading_slider_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.loading_slider_groupbox.setFont(font)
                    self.loading_slider_groupbox.setObjectName("loading_slider_groupbox")

                    self.loading_slider_mini_lbl = QtWidgets.QLabel(self.loading_slider_groupbox)
                    self.loading_slider_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_slider_mini_lbl.setFont(font)
                    self.loading_slider_mini_lbl.setObjectName("loading_slider_mini_lbl")
                    self.loading_slider_mini_lndt = QtWidgets.QLineEdit(self.loading_slider_groupbox)
                    self.loading_slider_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(\d|[1-9]\d)(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.loading_slider_mini_lndt)
                    self.loading_slider_mini_lndt.setValidator(validator)
                    self.loading_slider_mini_lndt.setObjectName("loading_slider_mini_lndt")

                    self.loading_slider_current_position_lbl = QtWidgets.QLabel(self.loading_slider_groupbox)
                    self.loading_slider_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.loading_slider_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.loading_slider_current_position_lbl.setFont(font)
                    self.loading_slider_current_position_lbl.setObjectName("loading_slider_current_position_lbl")
                    self.loading_slider_current_position_value = QtWidgets.QLabel(self.loading_slider_groupbox)
                    self.loading_slider_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.loading_slider_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.loading_slider_current_position_value.setFont(font)
                    self.loading_slider_current_position_value.setObjectName("loading_slider_current_position_value")

                    self.loading_slider_run_btn = QtWidgets.QPushButton(self.loading_slider_groupbox)
                    self.loading_slider_run_btn.setAccessibleName('loading_slider_run_btn')
                    self.loading_slider_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.loading_slider_run_btn.setFont(font)
                    self.loading_slider_run_btn.setStyleSheet("QPushButton{\n"
                                                              "background-color:rgb(49, 77, 162);\n"
                                                              "color:rgb(255, 255, 255);\n"
                                                              "border-radius: 10px;\n"
                                                              "}"
                                                              "QPushButton:Pressed{\n"
                                                              "border: 3px solid;\n"
                                                              "}"
                                                              )
                    self.loading_slider_run_btn.setText("Run")
                    self.loading_slider_run_btn.setFlat(True)
                    self.loading_slider_run_btn.setFont(font)
                    self.loading_slider_run_btn.setObjectName("loading_slider_run_btn")

                    self.loading_slider_init_btn = QtWidgets.QPushButton(self.loading_slider_groupbox)
                    self.loading_slider_init_btn.setGeometry(QtCore.QRect(270, 100, 100, 40))
                    self.loading_slider_init_btn.setAccessibleName('loading slider_homing btn')
                    self.loading_slider_init_btn.setText("Init")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.loading_slider_init_btn.setFont(font)
                    self.loading_slider_init_btn.setStyleSheet("QPushButton{\n"
                                                               "background-color:rgb(49, 77, 162);\n"
                                                               "color:rgb(255, 255, 255);\n"
                                                               "border-radius: 10px;\n"
                                                               "}"
                                                               "QPushButton:Pressed{\n"
                                                               "border: 3px solid;\n"
                                                               "}"
                                                               )
                    self.loading_slider_init_btn.setObjectName("loading_slider_init_btn")
                    self.verticalLayout_2.addWidget(self.loading_slider_groupbox)

                    self.loading_gripper_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.loading_gripper_groupbox.sizePolicy().hasHeightForWidth())
                    self.loading_gripper_groupbox.setSizePolicy(sizePolicy)
                    self.loading_gripper_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.loading_gripper_groupbox.setFont(font)
                    self.loading_gripper_groupbox.setObjectName("loading_gripper_groupbox")

                    self.loading_gripper_mini_lbl = QtWidgets.QLabel(self.loading_gripper_groupbox)
                    self.loading_gripper_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_gripper_mini_lbl.setFont(font)
                    self.loading_gripper_mini_lbl.setObjectName("loading_gripper_mini_lbl")
                    self.loading_gripper_mini_lndt = QtWidgets.QLineEdit(self.loading_gripper_groupbox)
                    self.loading_gripper_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(\d|[1-9]\d)(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.loading_gripper_mini_lndt)
                    self.loading_gripper_mini_lndt.setValidator(validator)
                    self.loading_gripper_mini_lndt.setObjectName("loading_gripper_mini_lndt")

                    self.loading_gripper_current_position_lbl = QtWidgets.QLabel(self.loading_gripper_groupbox)
                    self.loading_gripper_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.loading_gripper_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.loading_gripper_current_position_lbl.setFont(font)
                    self.loading_gripper_current_position_lbl.setObjectName("loading_gripper_current_position_lbl")
                    self.loading_gripper_current_position_value = QtWidgets.QLabel(self.loading_gripper_groupbox)
                    self.loading_gripper_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.loading_gripper_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.loading_gripper_current_position_value.setFont(font)
                    self.loading_gripper_current_position_value.setObjectName("loading_gripper_current_position_value")

                    self.loading_gripper_run_btn = QtWidgets.QPushButton(self.loading_gripper_groupbox)
                    self.loading_gripper_run_btn.setAccessibleName('loading_gripper_run_btn')
                    self.loading_gripper_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.loading_gripper_run_btn.setFont(font)
                    self.loading_gripper_run_btn.setText("Run")
                    self.loading_gripper_run_btn.setFlat(True)
                    self.loading_gripper_run_btn.setFont(font)
                    self.loading_gripper_run_btn.setStyleSheet("QPushButton{\n"
                                                               "background-color:rgb(49, 77, 162);\n"
                                                               "color:rgb(255, 255, 255);\n"
                                                               "border-radius: 10px;\n"
                                                               "}"
                                                               "QPushButton:Pressed{\n"
                                                               "border: 3px solid;\n"
                                                               "}"
                                                               )
                    self.loading_gripper_run_btn.setObjectName("loading_y_axis_run_btn")

                    self.loading_gripper_open_btn = QtWidgets.QPushButton(self.loading_gripper_groupbox)
                    self.loading_gripper_open_btn.setGeometry(QtCore.QRect(270, 100, 100, 40))
                    self.loading_gripper_open_btn.setAccessibleName('loading gripper_homing btn')
                    self.loading_gripper_open_btn.setText("Gripper open")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.loading_gripper_open_btn.setFont(font)
                    self.loading_gripper_open_btn.setStyleSheet("QPushButton{\n"
                                                                "background-color:rgb(49, 77, 162);\n"
                                                                "color:rgb(255, 255, 255);\n"
                                                                "border-radius: 10px;\n"
                                                                "}"
                                                                "QPushButton:Pressed{\n"
                                                                "border: 3px solid;\n"
                                                                "}"
                                                                )
                    self.loading_gripper_open_btn.setObjectName("loading_gripper_open_btn")
                    self.verticalLayout_2.addWidget(self.loading_gripper_groupbox)

                    self.loading_rotation_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.loading_rotation_groupbox.sizePolicy().hasHeightForWidth())
                    self.loading_rotation_groupbox.setSizePolicy(sizePolicy)
                    self.loading_rotation_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.loading_rotation_groupbox.setFont(font)
                    self.loading_rotation_groupbox.setObjectName("loading_rotation_groupbox")

                    self.loading_rotation_stepvalue_lbl = QtWidgets.QLabel(self.loading_rotation_groupbox)
                    self.loading_rotation_stepvalue_lbl.setGeometry(QtCore.QRect(10, 30, 55, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_rotation_stepvalue_lbl.setFont(font)
                    self.loading_rotation_stepvalue_lbl.setObjectName("loading_rotation_stepvalue_lbl")
                    self.loading_rotation_stepvalue_lndt = QtWidgets.QLineEdit(self.loading_rotation_groupbox)
                    regx = QRegExp(r"^(0?\.[0-9]{2}|[1-9]?\d\.[0-9]{2}|[12]\d{2}\.[0-9]{2}|3[0-5]\d\.[0-9]{2}|360)$")
                    loading_rotation_stepvalue_lndt = QRegExpValidator(regx,
                                                                       self.loading_rotation_stepvalue_lndt)
                    self.loading_rotation_stepvalue_lndt.setValidator(loading_rotation_stepvalue_lndt)
                    self.loading_rotation_stepvalue_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    self.loading_rotation_stepvalue_lndt.setObjectName("loading_rotation_stepvalue_lndt")

                    self.loading_rotation_clkwise_btn = QtWidgets.QPushButton(self.loading_rotation_groupbox)
                    self.loading_rotation_clkwise_btn.setGeometry(QtCore.QRect(10, 100, 70, 40))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_rotation_clkwise_btn.setFont(font)
                    self.loading_rotation_clkwise_btn.setStyleSheet("QPushButton{\n"
                                                                    "background-color:rgb(49, 77, 162);\n"
                                                                    "color:rgb(255, 255, 255);\n"
                                                                    "border-radius: 10px;\n"
                                                                    "}"
                                                                    "QPushButton:Pressed{\n"
                                                                    "border: 3px solid;\n"
                                                                    "}"
                                                                    )
                    self.loading_rotation_clkwise_btn.setText("")
                    self.loading_rotation_clkwise_btn.setAccessibleName('lens_rotator_clockwise')
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.loading_rotation_clkwise_btn.setIcon(icon)
                    self.loading_rotation_clkwise_btn.setIconSize(QtCore.QSize(40, 40))
                    self.loading_rotation_clkwise_btn.setObjectName("loading_rotation_clkwise_btn")

                    self.loading_rotation_aclkwise_btn = QtWidgets.QPushButton(self.loading_rotation_groupbox)
                    self.loading_rotation_aclkwise_btn.setGeometry(QtCore.QRect(110, 100, 70, 40))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.loading_rotation_aclkwise_btn.setFont(font)
                    self.loading_rotation_aclkwise_btn.setStyleSheet("QPushButton{\n"
                                                                     "background-color:rgb(49, 77, 162);\n"
                                                                     "color:rgb(255, 255, 255);\n"
                                                                     "border-radius: 10px;\n"
                                                                     "}"
                                                                     "QPushButton:Pressed{\n"
                                                                     "border: 3px solid;\n"
                                                                     "}"
                                                                     )
                    self.loading_rotation_aclkwise_btn.setText("")
                    self.loading_rotation_aclkwise_btn.setAccessibleName('lens_rotator_anti_clockwise')
                    icon1 = QtGui.QIcon()
                    icon1.addPixmap(QtGui.QPixmap(r".\media\anti-clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.loading_rotation_aclkwise_btn.setIcon(icon1)
                    self.loading_rotation_aclkwise_btn.setIconSize(QtCore.QSize(40, 40))
                    self.loading_rotation_aclkwise_btn.setObjectName("loading_rotation_aclkwise_btn")
                    self.verticalLayout_2.addWidget(self.loading_rotation_groupbox)
                    self.loading_scrollarea.setWidget(self.scrollAreaWidgetContents_2)
                    self.stackedWidget.addWidget(self.station_1_layout)

                    self.station_2_layout = QtWidgets.QWidget()
                    self.station_2_layout.setObjectName("station_2_layout")
                    self.lens_rotator_scrollarea = QtWidgets.QScrollArea(self.station_2_layout)
                    self.lens_rotator_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.lens_rotator_scrollarea.setGeometry(QtCore.QRect(0, 0, 420, 900))
                    self.lens_rotator_scrollarea.setWidgetResizable(True)
                    self.lens_rotator_scrollarea.setObjectName("lens_rotator_scrollarea")
                    self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
                    self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 418, 898))
                    self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
                    self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
                    self.verticalLayout_3.setObjectName("verticalLayout_3")

                    self.lens_rotator_enable_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lens_rotator_enable_groupbox.sizePolicy().hasHeightForWidth())
                    self.lens_rotator_enable_groupbox.setSizePolicy(sizePolicy)
                    self.lens_rotator_enable_groupbox.setMinimumSize(QtCore.QSize(0, 80))
                    self.lens_rotator_enable_groupbox.setStyleSheet("border:0px")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lens_rotator_enable_groupbox.setFont(font)
                    self.lens_rotator_enable_groupbox.setObjectName("lens_rotator_enable_groupbox")
                    self.lens_rotator_enable_lbl = QLabel(self.lens_rotator_enable_groupbox)
                    self.lens_rotator_enable_lbl.setGeometry(QtCore.QRect(80, 25, 150, 15))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lens_rotator_enable_lbl.setFont(font)
                    self.lens_rotator_enable_lbl.setText('Station Enable')
                    self.lens_rotator_enable_lbl.setObjectName("lens_rotator_enable_lbl")
                    self.lens_rotator_toggle = Toggle(self.lens_rotator_enable_groupbox)
                    self.lens_rotator_toggle.setChecked(True)
                    self.lens_rotator_toggle.setGeometry(QtCore.QRect(210, 17, 70, 35))
                    self.verticalLayout_3.addWidget(self.lens_rotator_enable_groupbox)

                    self.lens_rotator_x_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lens_rotator_x_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.lens_rotator_x_axis_groupbox.setSizePolicy(sizePolicy)
                    self.lens_rotator_x_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lens_rotator_x_axis_groupbox.setFont(font)
                    self.lens_rotator_x_axis_groupbox.setObjectName("lens_rotator_x_axis_groupbox")

                    self.lens_rotator_x_axis_mini_lbl = QtWidgets.QLabel(self.lens_rotator_x_axis_groupbox)
                    self.lens_rotator_x_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lens_rotator_x_axis_mini_lbl.setFont(font)
                    self.lens_rotator_x_axis_mini_lbl.setObjectName("lens_rotator_x_axis_mini_lbl")
                    self.lens_rotator_x_axis_mini_lndt = QtWidgets.QLineEdit(self.lens_rotator_x_axis_groupbox)
                    self.lens_rotator_x_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(\d|[1-9]\d)(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.lens_rotator_x_axis_mini_lndt)
                    self.lens_rotator_x_axis_mini_lndt.setValidator(validator)
                    self.lens_rotator_x_axis_mini_lndt.setObjectName("lens_rotator_x_axis_mini_lndt")

                    self.lens_rotator_x_axis_speed_lbl = QtWidgets.QLabel(self.lens_rotator_x_axis_groupbox)
                    self.lens_rotator_x_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lens_rotator_x_axis_speed_lbl.setFont(font)
                    self.lens_rotator_x_axis_speed_lbl.setText("Speed")
                    self.lens_rotator_x_axis_speed_lbl.setObjectName("lens_rotator_x_axis_speed_lbl")
                    self.lens_rotator_x_axis_speed_lndt = QtWidgets.QLineEdit(self.lens_rotator_x_axis_groupbox)
                    self.lens_rotator_x_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 5000, self.lens_rotator_x_axis_speed_lndt)
                    self.lens_rotator_x_axis_speed_lndt.setValidator(validator)
                    self.lens_rotator_x_axis_speed_lndt.setToolTip(
                        "The X-Actuator speed is limited to a range of 0 to 2000")
                    self.lens_rotator_x_axis_speed_lndt.setObjectName("lens_rotator_x_axis_speed_lndt")

                    self.lens_rotator_x_axis_current_position_lbl = QtWidgets.QLabel(self.lens_rotator_x_axis_groupbox)
                    self.lens_rotator_x_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.lens_rotator_x_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.lens_rotator_x_axis_current_position_lbl.setFont(font)
                    self.lens_rotator_x_axis_current_position_lbl.setObjectName(
                        "lens_rotator_x_axis_current_position_lbl")
                    self.lens_rotator_x_axis_current_position_value = QtWidgets.QLabel(
                        self.lens_rotator_x_axis_groupbox)
                    self.lens_rotator_x_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.lens_rotator_x_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.lens_rotator_x_axis_current_position_value.setFont(font)
                    self.lens_rotator_x_axis_current_position_value.setObjectName(
                        "lens_rotator_x_axis_current_position_value")

                    self.lens_rotator_x_axis_run_btn = QtWidgets.QPushButton(self.lens_rotator_x_axis_groupbox)
                    self.lens_rotator_x_axis_run_btn.setAccessibleName('lens_rotator_x_axis_run_btn')
                    self.lens_rotator_x_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.lens_rotator_x_axis_run_btn.setFont(font)
                    self.lens_rotator_x_axis_run_btn.setText("Run")
                    self.lens_rotator_x_axis_run_btn.setFlat(True)
                    self.lens_rotator_x_axis_run_btn.setFont(font)
                    self.lens_rotator_x_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                                   "background-color:rgb(49, 77, 162);\n"
                                                                   "color:rgb(255, 255, 255);\n"
                                                                   "border-radius: 10px;\n"
                                                                   "}"
                                                                   "QPushButton:Pressed{\n"
                                                                   "border: 3px solid;\n"
                                                                   "}"
                                                                   )
                    self.lens_rotator_x_axis_run_btn.setObjectName("lens_rotator_x_axis_run_btn")

                    self.lens_rotator_x_axis_homing_btn = QtWidgets.QPushButton(self.lens_rotator_x_axis_groupbox)
                    self.lens_rotator_x_axis_homing_btn.setGeometry(QtCore.QRect(270, 100, 90, 40))
                    self.lens_rotator_x_axis_homing_btn.setAccessibleName('lens_rotator_x_axis_homing_btn')
                    self.lens_rotator_x_axis_homing_btn.setText("Homing")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.lens_rotator_x_axis_homing_btn.setFont(font)
                    self.lens_rotator_x_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                                      "background-color:rgb(49, 77, 162);\n"
                                                                      "color:rgb(255, 255, 255);\n"
                                                                      "border-radius: 10px;\n"
                                                                      "}"
                                                                      "QPushButton:Pressed{\n"
                                                                      "border: 3px solid;\n"
                                                                      "}"
                                                                      )
                    self.lens_rotator_x_axis_homing_btn.setObjectName("lens_rotator_x_axis_homing_btn")
                    self.verticalLayout_3.addWidget(self.lens_rotator_x_axis_groupbox)

                    self.lens_rotator_y_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lens_rotator_y_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.lens_rotator_y_axis_groupbox.setSizePolicy(sizePolicy)
                    self.lens_rotator_y_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lens_rotator_y_axis_groupbox.setFont(font)
                    self.lens_rotator_y_axis_groupbox.setObjectName("lens_rotator_y_axis_groupbox")

                    self.lens_rotator_y_axis_mini_lbl = QtWidgets.QLabel(self.lens_rotator_y_axis_groupbox)
                    self.lens_rotator_y_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lens_rotator_y_axis_mini_lbl.setFont(font)
                    self.lens_rotator_y_axis_mini_lbl.setObjectName("lens_rotator_y_axis_mini_lbl")
                    self.lens_rotator_y_axis_mini_lndt = QtWidgets.QLineEdit(self.lens_rotator_y_axis_groupbox)
                    self.lens_rotator_y_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.lens_rotator_y_axis_mini_lndt)
                    self.lens_rotator_y_axis_mini_lndt.setValidator(validator)
                    self.lens_rotator_y_axis_mini_lndt.setObjectName("lens_rotator_y_axis_mini_lndt")

                    self.lens_rotator_y_axis_speed_lbl = QtWidgets.QLabel(self.lens_rotator_y_axis_groupbox)
                    self.lens_rotator_y_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lens_rotator_y_axis_speed_lbl.setFont(font)
                    self.lens_rotator_y_axis_speed_lbl.setText("Speed")
                    self.lens_rotator_y_axis_speed_lbl.setObjectName("lens_rotator_y_axis_speed_lbl")
                    self.lens_rotator_y_axis_speed_lndt = QtWidgets.QLineEdit(self.lens_rotator_y_axis_groupbox)
                    self.lens_rotator_y_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 15000, self.lens_rotator_y_axis_speed_lndt)
                    self.lens_rotator_y_axis_speed_lndt.setValidator(validator)
                    self.lens_rotator_y_axis_speed_lndt.setToolTip(
                        "The Y-Actuator speed is limited to a range of 0 to 15000")
                    self.lens_rotator_y_axis_speed_lndt.setObjectName("lens_rotator_y_axis_speed_lndt")

                    self.lens_rotator_y_axis_current_position_lbl = QtWidgets.QLabel(self.lens_rotator_y_axis_groupbox)
                    self.lens_rotator_y_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.lens_rotator_y_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.lens_rotator_y_axis_current_position_lbl.setFont(font)
                    self.lens_rotator_y_axis_current_position_lbl.setObjectName(
                        "lens_rotator_y_axis_current_position_lbl")
                    self.lens_rotator_y_axis_current_position_value = QtWidgets.QLabel(
                        self.lens_rotator_y_axis_groupbox)
                    self.lens_rotator_y_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.lens_rotator_y_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.lens_rotator_y_axis_current_position_value.setFont(font)
                    self.lens_rotator_y_axis_current_position_value.setObjectName(
                        "lens_rotator_y_axis_current_position_value")

                    self.lens_rotator_y_axis_run_btn = QtWidgets.QPushButton(self.lens_rotator_y_axis_groupbox)
                    self.lens_rotator_y_axis_run_btn.setAccessibleName('lens_rotator_y_axis_run_btn')
                    self.lens_rotator_y_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.lens_rotator_y_axis_run_btn.setFont(font)
                    self.lens_rotator_y_axis_run_btn.setText("Run")
                    self.lens_rotator_y_axis_run_btn.setFlat(True)
                    self.lens_rotator_y_axis_run_btn.setFont(font)
                    self.lens_rotator_y_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                                   "background-color:rgb(49, 77, 162);\n"
                                                                   "color:rgb(255, 255, 255);\n"
                                                                   "border-radius: 10px;\n"
                                                                   "}"
                                                                   "QPushButton:Pressed{\n"
                                                                   "border: 3px solid;\n"
                                                                   "}"
                                                                   )
                    self.lens_rotator_y_axis_run_btn.setObjectName("lens_rotator_y_axis_run_btn")

                    self.lens_rotator_y_axis_homing_btn = QtWidgets.QPushButton(self.lens_rotator_y_axis_groupbox)
                    self.lens_rotator_y_axis_homing_btn.setGeometry(QtCore.QRect(270, 100, 90, 40))
                    self.lens_rotator_y_axis_homing_btn.setAccessibleName('lens_rotator_y_axis_homing_btn')
                    self.lens_rotator_y_axis_homing_btn.setText("Homing")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.lens_rotator_y_axis_homing_btn.setFont(font)
                    self.lens_rotator_y_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                                      "background-color:rgb(49, 77, 162);\n"
                                                                      "color:rgb(255, 255, 255);\n"
                                                                      "border-radius: 10px;\n"
                                                                      "}"
                                                                      "QPushButton:Pressed{\n"
                                                                      "border: 3px solid;\n"
                                                                      "}"
                                                                      )
                    self.lens_rotator_y_axis_homing_btn.setObjectName("lens_rotator_y_axis_homing_btn")
                    self.verticalLayout_3.addWidget(self.lens_rotator_y_axis_groupbox)

                    self.lens_rotator_gripper_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lens_rotator_gripper_groupbox.sizePolicy().hasHeightForWidth())
                    self.lens_rotator_gripper_groupbox.setSizePolicy(sizePolicy)
                    self.lens_rotator_gripper_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lens_rotator_gripper_groupbox.setFont(font)
                    self.lens_rotator_gripper_groupbox.setObjectName("lens_rotator_gripper_groupbox")

                    self.lens_rotator_gripper_stepvalue_lbl = QtWidgets.QLabel(self.lens_rotator_gripper_groupbox)
                    self.lens_rotator_gripper_stepvalue_lbl.setGeometry(QtCore.QRect(10, 30, 55, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lens_rotator_gripper_stepvalue_lbl.setFont(font)
                    self.lens_rotator_gripper_stepvalue_lbl.setObjectName("lens_rotator_gripper_stepvalue_lbl")
                    self.lens_rotator_gripper_stepvalue_lndt = QtWidgets.QLineEdit(self.lens_rotator_gripper_groupbox)
                    regx = QRegExp(r"^(0?\.[0-9]{2}|[1-9]?\d\.[0-9]{2}|[12]\d{2}\.[0-9]{2}|3[0-5]\d\.[0-9]{2}|360)$")
                    lens_rotator_gripper_stepvalue_lndt = QRegExpValidator(regx,
                                                                           self.lens_rotator_gripper_stepvalue_lndt)
                    self.lens_rotator_gripper_stepvalue_lndt.setValidator(lens_rotator_gripper_stepvalue_lndt)
                    self.lens_rotator_gripper_stepvalue_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    self.lens_rotator_gripper_stepvalue_lndt.setObjectName("lens_rotator_gripper_stepvalue_lndt")

                    self.lens_rotator_gripper_clkwise_btn = QtWidgets.QPushButton(self.lens_rotator_gripper_groupbox)
                    self.lens_rotator_gripper_clkwise_btn.setGeometry(QtCore.QRect(10, 100, 70, 40))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lens_rotator_gripper_clkwise_btn.setFont(font)
                    self.lens_rotator_gripper_clkwise_btn.setStyleSheet("QPushButton{\n"
                                                                        "background-color:rgb(49, 77, 162);\n"
                                                                        "color:rgb(255, 255, 255);\n"
                                                                        "border-radius: 10px;\n"
                                                                        "}"
                                                                        "QPushButton:Pressed{\n"
                                                                        "border: 3px solid;\n"
                                                                        "}"
                                                                        )
                    self.lens_rotator_gripper_clkwise_btn.setText("")
                    self.lens_rotator_gripper_clkwise_btn.setAccessibleName('lens_rotator_clockwise')
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.lens_rotator_gripper_clkwise_btn.setIcon(icon)
                    self.lens_rotator_gripper_clkwise_btn.setIconSize(QtCore.QSize(40, 40))
                    self.lens_rotator_gripper_clkwise_btn.setObjectName("lens_rotator_gripper_clkwise_btn")

                    self.lens_rotator_gripper_aclkwise_btn = QtWidgets.QPushButton(self.lens_rotator_gripper_groupbox)
                    self.lens_rotator_gripper_aclkwise_btn.setGeometry(QtCore.QRect(110, 100, 70, 40))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.lens_rotator_gripper_aclkwise_btn.setFont(font)
                    self.lens_rotator_gripper_aclkwise_btn.setStyleSheet("QPushButton{\n"
                                                                         "background-color:rgb(49, 77, 162);\n"
                                                                         "color:rgb(255, 255, 255);\n"
                                                                         "border-radius: 10px;\n"
                                                                         "}"
                                                                         "QPushButton:Pressed{\n"
                                                                         "border: 3px solid;\n"
                                                                         "}"
                                                                         )
                    self.lens_rotator_gripper_aclkwise_btn.setText("")
                    self.lens_rotator_gripper_aclkwise_btn.setAccessibleName('lens_rotator_anti_clockwise')
                    icon1 = QtGui.QIcon()
                    icon1.addPixmap(QtGui.QPixmap(r".\media\anti-clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.lens_rotator_gripper_aclkwise_btn.setIcon(icon1)
                    self.lens_rotator_gripper_aclkwise_btn.setIconSize(QtCore.QSize(40, 40))
                    self.lens_rotator_gripper_aclkwise_btn.setObjectName("lens_rotator_gripper_aclkwise_btn")
                    self.verticalLayout_3.addWidget(self.lens_rotator_gripper_groupbox)

                    self.lens_rotator_sensor_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lens_rotator_sensor_groupbox.sizePolicy().hasHeightForWidth())
                    self.lens_rotator_sensor_groupbox.setSizePolicy(sizePolicy)
                    self.lens_rotator_sensor_groupbox.setMinimumSize(QtCore.QSize(0, 100))
                    self.lens_rotator_sensor_groupbox.setStyleSheet("border-radius: 10px;")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.lens_rotator_sensor_groupbox.setFont(font)
                    self.lens_rotator_sensor_groupbox.setObjectName("lens_rotator_sensor_groupbox")

                    self.lens_rotator_sensor_value_lbl = QtWidgets.QLabel(self.lens_rotator_sensor_groupbox)
                    self.lens_rotator_sensor_value_lbl.setGeometry(QtCore.QRect(50, 50, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    self.lens_rotator_sensor_value_lbl.setFont(font)
                    self.lens_rotator_sensor_value_lbl.setObjectName("lens_rotator_sensor_value_lbl")
                    self.lens_rotator_sensor_value = QtWidgets.QLabel(self.lens_rotator_sensor_groupbox)
                    self.lens_rotator_sensor_value.setGeometry(QtCore.QRect(150, 40, 180, 30))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    self.lens_rotator_sensor_value.setFont(font)
                    self.lens_rotator_sensor_value.setText("10")
                    self.lens_rotator_sensor_value.setObjectName("lens_rotator_sensor_value")
                    self.verticalLayout_3.addWidget(self.lens_rotator_sensor_groupbox)
                    self.lens_rotator_scrollarea.setWidget(self.scrollAreaWidgetContents_3)
                    self.stackedWidget.addWidget(self.station_2_layout)

                    self.station_3_layout = QtWidgets.QWidget()
                    self.station_3_layout.setObjectName("station_3_layout")
                    self.collimator_scrollarea = QtWidgets.QScrollArea(self.station_3_layout)
                    self.collimator_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.collimator_scrollarea.setGeometry(QtCore.QRect(0, 0, 420, 900))
                    self.collimator_scrollarea.setWidgetResizable(True)
                    self.collimator_scrollarea.setObjectName("collimator_scrollarea")
                    self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
                    self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 418, 898))
                    self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
                    self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
                    self.verticalLayout_4.setObjectName("verticalLayout_4")

                    self.collimator_enable_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_4)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.collimator_enable_groupbox.sizePolicy().hasHeightForWidth())
                    self.collimator_enable_groupbox.setSizePolicy(sizePolicy)
                    self.collimator_enable_groupbox.setMinimumSize(QtCore.QSize(0, 80))
                    self.collimator_enable_groupbox.setStyleSheet("border:0px")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.collimator_enable_groupbox.setFont(font)
                    self.collimator_enable_groupbox.setObjectName("collimator_enable_groupbox")
                    self.collimator_enable_lbl = QLabel(self.collimator_enable_groupbox)
                    self.collimator_enable_lbl.setGeometry(QtCore.QRect(80, 25, 150, 15))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.collimator_enable_lbl.setFont(font)
                    self.collimator_enable_lbl.setText('Station Enable')
                    self.collimator_enable_lbl.setObjectName("collimator_enable_lbl")
                    self.collimator_toggle = Toggle(self.collimator_enable_groupbox)
                    self.collimator_toggle.setChecked(True)
                    self.collimator_toggle.setGeometry(QtCore.QRect(210, 17, 70, 35))
                    self.verticalLayout_4.addWidget(self.collimator_enable_groupbox)

                    self.collimator_x_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_4)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.collimator_x_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.collimator_x_axis_groupbox.setSizePolicy(sizePolicy)
                    self.collimator_x_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.collimator_x_axis_groupbox.setFont(font)
                    self.collimator_x_axis_groupbox.setObjectName("collimator_x_axis_groupbox")

                    self.collimator_x_axis_mini_lbl = QtWidgets.QLabel(self.collimator_x_axis_groupbox)
                    self.collimator_x_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_x_axis_mini_lbl.setFont(font)
                    self.collimator_x_axis_mini_lbl.setObjectName("collimator_x_axis_mini_lbl")
                    self.collimator_x_axis_mini_lndt = QtWidgets.QLineEdit(self.collimator_x_axis_groupbox)
                    self.collimator_x_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(\d|[1-9]\d)(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.collimator_x_axis_mini_lndt)
                    self.collimator_x_axis_mini_lndt.setValidator(validator)
                    self.collimator_x_axis_mini_lndt.setObjectName("collimator_x_axis_mini_lndt")

                    self.collimator_x_axis_speed_lbl = QtWidgets.QLabel(self.collimator_x_axis_groupbox)
                    self.collimator_x_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_x_axis_speed_lbl.setFont(font)
                    self.collimator_x_axis_speed_lbl.setText("Speed")
                    self.collimator_x_axis_speed_lbl.setObjectName("collimator_x_axis_speed_lbl")
                    self.collimator_x_axis_speed_lndt = QtWidgets.QLineEdit(self.collimator_x_axis_groupbox)
                    self.collimator_x_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 5000, self.collimator_x_axis_speed_lndt)
                    self.collimator_x_axis_speed_lndt.setValidator(validator)
                    self.collimator_x_axis_speed_lndt.setToolTip(
                        "The X-Actuator speed is limited to a range of 0 to 2000")
                    self.collimator_x_axis_speed_lndt.setObjectName("collimator_x_axis_speed_lndt")

                    self.collimator_x_axis_current_position_lbl = QtWidgets.QLabel(self.collimator_x_axis_groupbox)
                    self.collimator_x_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.collimator_x_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.collimator_x_axis_current_position_lbl.setFont(font)
                    self.collimator_x_axis_current_position_lbl.setObjectName("collimator_x_axis_current_position_lbl")
                    self.collimator_x_axis_current_position_value = QtWidgets.QLabel(self.collimator_x_axis_groupbox)
                    self.collimator_x_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.collimator_x_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.collimator_x_axis_current_position_value.setFont(font)
                    self.collimator_x_axis_current_position_value.setObjectName(
                        "collimator_x_axis_current_position_value")

                    self.collimator_x_axis_run_btn = QtWidgets.QPushButton(self.collimator_x_axis_groupbox)
                    self.collimator_x_axis_run_btn.setAccessibleName('collimator_x_axis_run_btn')
                    self.collimator_x_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.collimator_x_axis_run_btn.setFont(font)
                    self.collimator_x_axis_run_btn.setText("Run")
                    self.collimator_x_axis_run_btn.setFlat(True)
                    self.collimator_x_axis_run_btn.setFont(font)
                    self.collimator_x_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                                 "background-color:rgb(49, 77, 162);\n"
                                                                 "color:rgb(255, 255, 255);\n"
                                                                 "border-radius: 10px;\n"
                                                                 "}"
                                                                 "QPushButton:Pressed{\n"
                                                                 "border: 3px solid;\n"
                                                                 "}"
                                                                 )
                    self.collimator_x_axis_run_btn.setObjectName("collimator_x_axis_run_btn")

                    self.collimator_x_axis_homing_btn = QtWidgets.QPushButton(self.collimator_x_axis_groupbox)
                    self.collimator_x_axis_homing_btn.setGeometry(QtCore.QRect(270, 100, 90, 40))
                    self.collimator_x_axis_homing_btn.setAccessibleName('collimator_x_axis_homing_btn')
                    self.collimator_x_axis_homing_btn.setText("Homing")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.collimator_x_axis_homing_btn.setFont(font)
                    self.collimator_x_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                                    "background-color:rgb(49, 77, 162);\n"
                                                                    "color:rgb(255, 255, 255);\n"
                                                                    "border-radius: 10px;\n"
                                                                    "}"
                                                                    "QPushButton:Pressed{\n"
                                                                    "border: 3px solid;\n"
                                                                    "}"
                                                                    )
                    self.collimator_x_axis_homing_btn.setObjectName("collimator_x_axis_homing_btn")
                    self.verticalLayout_4.addWidget(self.collimator_x_axis_groupbox)

                    self.collimator_y_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_4)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.collimator_y_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.collimator_y_axis_groupbox.setSizePolicy(sizePolicy)
                    self.collimator_y_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.collimator_y_axis_groupbox.setFont(font)
                    self.collimator_y_axis_groupbox.setObjectName("collimator_y_axis_groupbox")

                    self.collimator_y_axis_mini_lbl = QtWidgets.QLabel(self.collimator_y_axis_groupbox)
                    self.collimator_y_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_y_axis_mini_lbl.setFont(font)
                    self.collimator_y_axis_mini_lbl.setObjectName("collimator_y_axis_mini_lbl")
                    self.collimator_y_axis_mini_lndt = QtWidgets.QLineEdit(self.collimator_y_axis_groupbox)
                    self.collimator_y_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.collimator_y_axis_mini_lndt)
                    self.collimator_y_axis_mini_lndt.setValidator(validator)
                    self.collimator_y_axis_mini_lndt.setObjectName("collimator_y_axis_mini_lndt")

                    self.collimator_y_axis_speed_lbl = QtWidgets.QLabel(self.collimator_y_axis_groupbox)
                    self.collimator_y_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_y_axis_speed_lbl.setFont(font)
                    self.collimator_y_axis_speed_lbl.setText("Speed")
                    self.collimator_y_axis_speed_lbl.setObjectName("collimator_y_axis_speed_lbl")
                    self.collimator_y_axis_speed_lndt = QtWidgets.QLineEdit(self.collimator_y_axis_groupbox)
                    self.collimator_y_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 15000, self.collimator_y_axis_speed_lndt)
                    self.collimator_y_axis_speed_lndt.setValidator(validator)
                    self.collimator_y_axis_speed_lndt.setToolTip(
                        "The Y-Actuator speed is limited to a range of 0 to 15000")
                    self.collimator_y_axis_speed_lndt.setObjectName("collimator_y_axis_speed_lndt")

                    self.collimator_y_axis_current_position_lbl = QtWidgets.QLabel(self.collimator_y_axis_groupbox)
                    self.collimator_y_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.collimator_y_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.collimator_y_axis_current_position_lbl.setFont(font)
                    self.collimator_y_axis_current_position_lbl.setObjectName("collimator_y_axis_current_position_lbl")
                    self.collimator_y_axis_current_position_value = QtWidgets.QLabel(self.collimator_y_axis_groupbox)
                    self.collimator_y_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.collimator_y_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.collimator_y_axis_current_position_value.setFont(font)
                    self.collimator_y_axis_current_position_value.setObjectName(
                        "collimator_y_axis_current_position_value")

                    self.collimator_y_axis_run_btn = QtWidgets.QPushButton(self.collimator_y_axis_groupbox)
                    self.collimator_y_axis_run_btn.setAccessibleName('collimator_y_axis_run_btn')
                    self.collimator_y_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.collimator_y_axis_run_btn.setFont(font)
                    self.collimator_y_axis_run_btn.setText("Run")
                    self.collimator_y_axis_run_btn.setFlat(True)
                    self.collimator_y_axis_run_btn.setFont(font)
                    self.collimator_y_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                                 "background-color:rgb(49, 77, 162);\n"
                                                                 "color:rgb(255, 255, 255);\n"
                                                                 "border-radius: 10px;\n"
                                                                 "}"
                                                                 "QPushButton:Pressed{\n"
                                                                 "border: 3px solid;\n"
                                                                 "}"
                                                                 )
                    self.collimator_y_axis_run_btn.setObjectName("collimator_y_axis_run_btn")

                    self.collimator_y_axis_homing_btn = QtWidgets.QPushButton(self.collimator_y_axis_groupbox)
                    self.collimator_y_axis_homing_btn.setGeometry(QtCore.QRect(270, 100, 90, 40))
                    self.collimator_y_axis_homing_btn.setAccessibleName('collimator_y_axis_homing_btn')
                    self.collimator_y_axis_homing_btn.setText("Homing")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.collimator_y_axis_homing_btn.setFont(font)
                    self.collimator_y_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                                    "background-color:rgb(49, 77, 162);\n"
                                                                    "color:rgb(255, 255, 255);\n"
                                                                    "border-radius: 10px;\n"
                                                                    "}"
                                                                    "QPushButton:Pressed{\n"
                                                                    "border: 3px solid;\n"
                                                                    "}"
                                                                    )
                    self.collimator_y_axis_homing_btn.setObjectName("collimator_y_axis_homing_btn")
                    self.verticalLayout_4.addWidget(self.collimator_y_axis_groupbox)

                    self.collimator_gripper_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_4)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.collimator_gripper_groupbox.sizePolicy().hasHeightForWidth())
                    self.collimator_gripper_groupbox.setSizePolicy(sizePolicy)
                    self.collimator_gripper_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.collimator_gripper_groupbox.setFont(font)
                    self.collimator_gripper_groupbox.setObjectName("collimator_gripper_groupbox")

                    self.collimator_gripper_stepvalue_lndt = QtWidgets.QLineEdit(self.collimator_gripper_groupbox)
                    self.collimator_gripper_stepvalue_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r"^(0?\.[0-9]{2}|[1-9]?\d\.[0-9]{2}|[12]\d{2}\.[0-9]{2}|3[0-5]\d\.[0-9]{2}|360)$")
                    collimator_gripper_stepvalue_lndt = QRegExpValidator(regx,
                                                                         self.collimator_gripper_stepvalue_lndt)
                    self.collimator_gripper_stepvalue_lndt.setValidator(collimator_gripper_stepvalue_lndt)
                    self.collimator_gripper_stepvalue_lndt.setObjectName("collimator_gripper_stepvalue_lndt")
                    self.collimator_gripper_stepvalue_lbl = QtWidgets.QLabel(self.collimator_gripper_groupbox)
                    self.collimator_gripper_stepvalue_lbl.setGeometry(QtCore.QRect(10, 30, 55, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_gripper_stepvalue_lbl.setFont(font)
                    self.collimator_gripper_stepvalue_lbl.setObjectName("collimator_gripper_stepvalue_lbl")

                    self.collimator_gripper_clkwise_btn = QtWidgets.QPushButton(self.collimator_gripper_groupbox)
                    self.collimator_gripper_clkwise_btn.setGeometry(QtCore.QRect(10, 100, 70, 40))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_gripper_clkwise_btn.setFont(font)
                    self.collimator_gripper_clkwise_btn.setStyleSheet("QPushButton{\n"
                                                                      "background-color:rgb(49, 77, 162);\n"
                                                                      "color:rgb(255, 255, 255);\n"
                                                                      "border-radius: 10px;\n"
                                                                      "}"
                                                                      "QPushButton:Pressed{\n"
                                                                      "border: 3px solid;\n"
                                                                      "}"
                                                                      )
                    self.collimator_gripper_clkwise_btn.setText("")
                    self.collimator_gripper_clkwise_btn.setAccessibleName('collimator_clockwise_btn')
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.collimator_gripper_clkwise_btn.setIcon(icon)
                    self.collimator_gripper_clkwise_btn.setIconSize(QtCore.QSize(40, 40))
                    self.collimator_gripper_clkwise_btn.setObjectName("collimator_gripper_clkwise_btn")

                    self.collimator_gripper_aclkwise_btn = QtWidgets.QPushButton(self.collimator_gripper_groupbox)
                    self.collimator_gripper_aclkwise_btn.setGeometry(QtCore.QRect(110, 100, 70, 40))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_gripper_aclkwise_btn.setFont(font)
                    self.collimator_gripper_aclkwise_btn.setStyleSheet("QPushButton{\n"
                                                                       "background-color:rgb(49, 77, 162);\n"
                                                                       "color:rgb(255, 255, 255);\n"
                                                                       "border-radius: 10px;\n"
                                                                       "}"
                                                                       "QPushButton:Pressed{\n"
                                                                       "border: 3px solid;\n"
                                                                       "}"
                                                                       )
                    self.collimator_gripper_aclkwise_btn.setText("")
                    self.collimator_gripper_aclkwise_btn.setAccessibleName('collimator_anti_clockwise_btn')
                    icon1 = QtGui.QIcon()
                    icon1.addPixmap(QtGui.QPixmap(r".\media\anti-clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.collimator_gripper_aclkwise_btn.setIcon(icon1)
                    self.collimator_gripper_aclkwise_btn.setIconSize(QtCore.QSize(40, 40))
                    self.collimator_gripper_aclkwise_btn.setObjectName("collimator_gripper_aclkwise_btn")
                    self.verticalLayout_4.addWidget(self.collimator_gripper_groupbox)

                    self.Collimator_chart_details_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_4)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(
                        self.Collimator_chart_details_groupbox.sizePolicy().hasHeightForWidth())
                    self.Collimator_chart_details_groupbox.setSizePolicy(sizePolicy)
                    self.Collimator_chart_details_groupbox.setMinimumSize(QtCore.QSize(0, 580))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.Collimator_chart_details_groupbox.setFont(font)
                    self.Collimator_chart_details_groupbox.setStyleSheet("Background-color:RGB(240, 240, 240)")
                    self.Collimator_chart_details_groupbox.setObjectName("Collimator_chart_details_groupbox")

                    self.collimator_azimuth_lndt = QtWidgets.QLineEdit(self.Collimator_chart_details_groupbox)
                    self.collimator_azimuth_lndt.setGeometry(QtCore.QRect(120, 30, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_azimuth_lndt = QRegExpValidator(regx, self.collimator_azimuth_lndt)
                    self.collimator_azimuth_lndt.setValidator(collimator_azimuth_lndt)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_azimuth_lndt.setFont(font)
                    self.collimator_azimuth_lndt.setPlaceholderText("in deg")
                    self.collimator_azimuth_lndt.setObjectName("collimator_azimuth_lndt")
                    self.collimator_azimuth_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_azimuth_lbl.setGeometry(QtCore.QRect(20, 35, 90, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_azimuth_lbl.setFont(font)
                    self.collimator_azimuth_lbl.setObjectName("collimator_azimuth_lbl")

                    self.collimator_radius_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_radius_lbl.setGeometry(QtCore.QRect(210, 35, 90, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_radius_lbl.setFont(font)
                    self.collimator_radius_lbl.setObjectName("collimator_radius_lbl")
                    self.collimator_radius_lndt = QtWidgets.QLineEdit(self.Collimator_chart_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_radius_lndt = QRegExpValidator(regx, self.collimator_radius_lndt)
                    self.collimator_radius_lndt.setValidator(collimator_radius_lndt)
                    self.collimator_radius_lndt.setGeometry(QtCore.QRect(300, 30, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_radius_lndt.setFont(font)
                    self.collimator_radius_lndt.setObjectName("collimator_radius_lndt")

                    self.collimator_width_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_width_lbl.setGeometry(QtCore.QRect(20, 85, 90, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_width_lbl.setFont(font)
                    self.collimator_width_lbl.setObjectName("collimator_width_lbl")
                    self.collimator_width_lndt = QtWidgets.QLineEdit(self.Collimator_chart_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_width_lndt = QRegExpValidator(regx, self.collimator_width_lndt)
                    self.collimator_width_lndt.setValidator(collimator_width_lndt)
                    self.collimator_width_lndt.setGeometry(QtCore.QRect(120, 80, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_width_lndt.setFont(font)
                    self.collimator_width_lndt.setObjectName("collimator_width_lndt")

                    self.collimator_height_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_height_lbl.setGeometry(QtCore.QRect(210, 85, 90, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_height_lbl.setFont(font)
                    self.collimator_height_lbl.setObjectName("collimator_height_lbl")
                    self.collimator_height_lndt = QtWidgets.QLineEdit(self.Collimator_chart_details_groupbox)
                    self.collimator_height_lndt.setGeometry(QtCore.QRect(300, 80, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_height_lndt = QRegExpValidator(regx, self.collimator_height_lndt)
                    self.collimator_height_lndt.setValidator(collimator_height_lndt)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_height_lndt.setFont(font)
                    self.collimator_height_lndt.setObjectName("collimator_height_lndt")

                    self.collimator_black_lvl_value_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_black_lvl_value_lbl.setGeometry(QtCore.QRect(20, 135, 100, 30))
                    self.collimator_black_lvl_value_lbl.setText("Black level")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_black_lvl_value_lbl.setFont(font)
                    self.collimator_black_lvl_value_lbl.setObjectName("collimator_black_lvl_value_lbl")
                    self.collimator_black_lvl_value_lndt = QtWidgets.QLineEdit(
                        self.Collimator_chart_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_black_lvl_value_lndt = QRegExpValidator(regx, self.collimator_black_lvl_value_lndt)
                    self.collimator_black_lvl_value_lndt.setValidator(collimator_black_lvl_value_lndt)
                    self.collimator_black_lvl_value_lndt.setGeometry(QtCore.QRect(120, 130, 70, 30))
                    self.collimator_black_lvl_value_lndt.setObjectName("collimator_black_lvl_value_lndt")

                    self.collimator_median_frame_cnt_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_median_frame_cnt_lbl.setGeometry(QtCore.QRect(210, 130, 100, 30))
                    self.collimator_median_frame_cnt_lbl.setText("Median frame\ncount")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_median_frame_cnt_lbl.setFont(font)
                    self.collimator_median_frame_cnt_lbl.setObjectName("collimator_median_frame_cnt_lbl")
                    self.collimator_median_frame_cnt_lndt = QtWidgets.QLineEdit(
                        self.Collimator_chart_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_median_frame_cnt_lndt = QRegExpValidator(regx, self.collimator_median_frame_cnt_lndt)
                    self.collimator_median_frame_cnt_lndt.setValidator(collimator_median_frame_cnt_lndt)
                    self.collimator_median_frame_cnt_lndt.setGeometry(QtCore.QRect(300, 130, 70, 30))
                    self.collimator_median_frame_cnt_lndt.setObjectName("collimator_median_frame_cnt_lndt")

                    self.collimator_red_value_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_red_value_lbl.setGeometry(QtCore.QRect(20, 185, 100, 30))
                    self.collimator_red_value_lbl.setText("Red value")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_red_value_lbl.setFont(font)
                    self.collimator_red_value_lbl.setObjectName("collimator_red_value_lbl")
                    self.collimator_red_value_lndt = QtWidgets.QLineEdit(
                        self.Collimator_chart_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_red_value_lndt = QRegExpValidator(regx, self.collimator_red_value_lndt)
                    self.collimator_red_value_lndt.setValidator(collimator_red_value_lndt)
                    self.collimator_red_value_lndt.setGeometry(QtCore.QRect(120, 180, 70, 30))
                    self.collimator_red_value_lndt.setObjectName("collimator_red_value_lndt")

                    self.collimator_green_value_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_green_value_lbl.setGeometry(QtCore.QRect(210, 185, 100, 30))
                    self.collimator_green_value_lbl.setText("Green value")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_green_value_lbl.setFont(font)
                    self.collimator_green_value_lbl.setObjectName("collimator_green_value_lbl")
                    self.collimator_green_value_lndt = QtWidgets.QLineEdit(
                        self.Collimator_chart_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_green_value_lndt = QRegExpValidator(regx, self.collimator_green_value_lndt)
                    self.collimator_green_value_lndt.setValidator(collimator_green_value_lndt)
                    self.collimator_green_value_lndt.setGeometry(QtCore.QRect(300, 180, 70, 30))
                    self.collimator_green_value_lndt.setObjectName("collimator_green_value_lndt")

                    self.collimator_blue_value_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_blue_value_lbl.setGeometry(QtCore.QRect(20, 235, 100, 30))
                    self.collimator_blue_value_lbl.setText("Blue value")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_blue_value_lbl.setFont(font)
                    self.collimator_blue_value_lbl.setObjectName("collimator_blue_value_lbl")
                    self.collimator_blue_value_lndt = QtWidgets.QLineEdit(
                        self.Collimator_chart_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    collimator_blue_value_lndt = QRegExpValidator(regx, self.collimator_blue_value_lndt)
                    self.collimator_blue_value_lndt.setValidator(collimator_blue_value_lndt)
                    self.collimator_blue_value_lndt.setGeometry(QtCore.QRect(120, 230, 70, 30))
                    self.collimator_blue_value_lndt.setObjectName("collimator_blue_value_lndt")

                    self.collimator_details_save_frame_btn = QtWidgets.QPushButton(
                        self.Collimator_chart_details_groupbox)
                    self.collimator_details_save_frame_btn.setGeometry(QtCore.QRect(210, 235, 100, 30))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_details_save_frame_btn.setFont(font)
                    self.collimator_details_save_frame_btn.setText("Save Frame")
                    self.collimator_details_save_frame_btn.setAccessibleName('Save Frame')
                    self.collimator_details_save_frame_btn.setStyleSheet("QPushButton{\n"
                                                                         "background-color:rgb(49, 77, 162);\n"
                                                                         "color:rgb(255, 255, 255);\n"
                                                                         "border-radius: 10px;\n"
                                                                         "}"
                                                                         "QPushButton:Pressed{\n"
                                                                         "border: 3px solid;\n"
                                                                         "}"
                                                                         "QPushButton:enabled{\n"
                                                                         "background-color: rgb(49, "
                                                                         "77, 162); }\n"
                                                                         )
                    self.collimator_details_save_frame_btn.setObjectName("collimator_details_save_frame_btn")

                    self.img_frmt_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.img_frmt_lbl.setGeometry(QtCore.QRect(20, 285, 60, 35))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.img_frmt_lbl.setFont(font)
                    self.img_frmt_lbl.setText("Format type")
                    self.img_frmt_lbl.setObjectName("img_frmt_lbl")
                    self.img_frmt_box = combobox(self.Collimator_chart_details_groupbox)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.img_frmt_box.setFont(font)
                    self.img_frmt_box.addItem("Monochrome")
                    self.img_frmt_box.addItem("CN")
                    self.img_frmt_box.addItem("No")
                    self.img_frmt_box.addItem("DB, RG")
                    self.img_frmt_box.addItem("DB, BG")
                    self.img_frmt_box.addItem("DB, GR")
                    self.img_frmt_box.addItem("DB, GB")
                    self.img_frmt_box.setGeometry(QtCore.QRect(120, 285, 185, 30))
                    self.img_frmt_box.setObjectName("img_frmt_box")

                    self.collimator_details_update_btn = QtWidgets.QPushButton(self.Collimator_chart_details_groupbox)
                    self.collimator_details_update_btn.setGeometry(QtCore.QRect(150, 345, 80, 30))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_details_update_btn.setFont(font)
                    self.collimator_details_update_btn.setStyleSheet("QPushButton{\n"
                                                                     "background-color:rgb(49, 77, 162);\n"
                                                                     "color:rgb(255, 255, 255);\n"
                                                                     "border-radius: 10px;\n"
                                                                     "}"
                                                                     "QPushButton:Pressed{\n"
                                                                     "border: 3px solid;\n"
                                                                     "}"
                                                                     "QPushButton:enabled{\n"
                                                                     "background-color: rgb(49, "
                                                                     "77, 162); }\n"
                                                                     )
                    self.collimator_details_update_btn.setObjectName("collimator_details_update_btn")

                    self.collimator_details_simulate_btn = QtWidgets.QPushButton(self.Collimator_chart_details_groupbox)
                    self.collimator_details_simulate_btn.setGeometry(QtCore.QRect(30, 345, 80, 30))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_details_simulate_btn.setFont(font)
                    self.collimator_details_simulate_btn.setStyleSheet("QPushButton{\n"
                                                                       "background-color:rgb(49, 77, 162);\n"
                                                                       "color:rgb(255, 255, 255);\n"
                                                                       "border-radius: 10px;\n"
                                                                       "}"
                                                                       "QPushButton:Pressed{\n"
                                                                       "border: 3px solid;\n"
                                                                       "}"
                                                                       )
                    self.collimator_details_simulate_btn.setObjectName("collimator_details_simulate_btn")

                    self.collimator_details_chart_check_btn = QtWidgets.QPushButton(
                        self.Collimator_chart_details_groupbox)
                    self.collimator_details_chart_check_btn.setGeometry(QtCore.QRect(270, 345, 80, 30))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.collimator_details_chart_check_btn.setFont(font)
                    self.collimator_details_chart_check_btn.setStyleSheet("QPushButton{\n"
                                                                          "background-color:rgb(49, 77, 162);\n"
                                                                          "color:rgb(255, 255, 255);\n"
                                                                          "border-radius: 10px;\n"
                                                                          "}"
                                                                          "QPushButton:Pressed{\n"
                                                                          "border: 3px solid;\n"
                                                                          "}"
                                                                          )
                    self.collimator_details_chart_check_btn.setObjectName("collimator_details_chart_check_btn")

                    self.collimator_after_gluing_focus_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_after_gluing_focus_lbl.setGeometry(QtCore.QRect(20, 400, 170, 35))
                    self.collimator_after_gluing_focus_lbl.setText("Do you need to \n"
                                                                   "check focus after gluing ?")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_after_gluing_focus_lbl.setFont(font)
                    self.collimator_after_gluing_focus_lbl.setObjectName("collimator_after_gluing_focus_lbl")

                    self.collimator_after_gluing_focus_cmb = combobox(self.Collimator_chart_details_groupbox)
                    self.collimator_after_gluing_focus_cmb.setGeometry(QtCore.QRect(180, 405, 100, 30))
                    self.collimator_after_gluing_focus_cmb.addItem("No")
                    self.collimator_after_gluing_focus_cmb.addItem("Yes")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.collimator_after_gluing_focus_cmb.setFont(font)
                    self.collimator_after_gluing_focus_cmb.setObjectName("collimator_after_gluing_focus_cmb")

                    self.collimator_after_curing_focus_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_after_curing_focus_lbl.setGeometry(QtCore.QRect(20, 450, 170, 35))
                    self.collimator_after_curing_focus_lbl.setText("Do you need to check\n"
                                                                   "focus after curing ?")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_after_curing_focus_lbl.setFont(font)
                    self.collimator_after_curing_focus_lbl.setObjectName("collimator_after_curing_focus_lbl")

                    self.collimator_after_curing_focus_cmb = combobox(self.Collimator_chart_details_groupbox)
                    self.collimator_after_curing_focus_cmb.setGeometry(QtCore.QRect(180, 455, 100, 30))
                    self.collimator_after_curing_focus_cmb.addItem("No")
                    self.collimator_after_curing_focus_cmb.addItem("Yes")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.collimator_after_curing_focus_cmb.setFont(font)
                    self.collimator_after_curing_focus_cmb.setObjectName("collimator_after_curing_focus_cmb")

                    self.collimator_raw_save_option_lbl = QtWidgets.QLabel(self.Collimator_chart_details_groupbox)
                    self.collimator_raw_save_option_lbl.setGeometry(QtCore.QRect(20, 500, 110, 35))
                    self.collimator_raw_save_option_lbl.setText("Do you need Save\n"
                                                                "raw frame ?")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_raw_save_option_lbl.setFont(font)
                    self.collimator_raw_save_option_lbl.setObjectName("collimator_raw_save_option_lbl")

                    self.collimator_raw_save_option_cmb = combobox(self.Collimator_chart_details_groupbox)
                    self.collimator_raw_save_option_cmb.setGeometry(QtCore.QRect(180, 505, 100, 30))
                    self.collimator_raw_save_option_cmb.addItem("No")
                    self.collimator_raw_save_option_cmb.addItem("Yes")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.collimator_raw_save_option_cmb.setFont(font)
                    self.collimator_raw_save_option_cmb.setObjectName("collimator_raw_save_option_cmb")

                    self.verticalLayout_4.addWidget(self.Collimator_chart_details_groupbox)
                    self.collimator_scrollarea.setWidget(self.scrollAreaWidgetContents_4)

                    self.Collimator_details_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_4)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.Collimator_details_groupbox.sizePolicy().hasHeightForWidth())
                    self.Collimator_details_groupbox.setSizePolicy(sizePolicy)
                    self.Collimator_details_groupbox.setMinimumSize(QtCore.QSize(0, 330))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.Collimator_details_groupbox.setFont(font)
                    self.Collimator_details_groupbox.setStyleSheet("Background-color:RGB(240, 240, 240)")
                    self.Collimator_details_groupbox.setObjectName("Collimator_details_groupbox")

                    self.collimator_type_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_type_lbl.setGeometry(QtCore.QRect(20, 35, 90, 20))
                    self.collimator_type_lbl.setText("Collimator Type")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_type_lbl.setFont(font)
                    self.collimator_type_lbl.setObjectName("collimator_type_lbl")

                    self.collimator_type_cmb = combobox(self.Collimator_details_groupbox)
                    self.collimator_type_cmb.setGeometry(QtCore.QRect(150, 30, 150, 30))
                    self.collimator_type_cmb.addItem("Old Collimator")
                    self.collimator_type_cmb.addItem("New Collimator")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.collimator_type_cmb.setFont(font)
                    self.collimator_type_cmb.setObjectName("collimator_type_cmb")

                    self.collimator_light_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_light_lbl.setGeometry(QtCore.QRect(20, 85, 90, 20))
                    self.collimator_light_lbl.setText("Light Type")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_light_lbl.setFont(font)
                    self.collimator_light_lbl.setObjectName("collimator_light_lbl")

                    self.collimator_light_cmb = combobox(self.Collimator_details_groupbox)
                    self.collimator_light_cmb.setGeometry(QtCore.QRect(150, 80, 150, 30))
                    self.collimator_light_cmb.addItem("Visible")
                    self.collimator_light_cmb.addItem("IR850")
                    self.collimator_light_cmb.addItem("IR940")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.collimator_light_cmb.setFont(font)
                    self.collimator_light_cmb.setObjectName("collimator_light_cmb")

                    self.collimator_wd_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_wd_lbl.setGeometry(QtCore.QRect(20, 135, 110, 40))
                    self.collimator_wd_lbl.setText("Working Distance & \nFov")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_wd_lbl.setFont(font)
                    self.collimator_wd_lbl.hide()
                    self.collimator_wd_lbl.setObjectName("collimator_wd_lbl")

                    self.collimator_wd_cmb = combobox(self.Collimator_details_groupbox)
                    self.collimator_wd_cmb.setGeometry(QtCore.QRect(150, 130, 150, 30))
                    self.collimator_wd_cmb.addItem("80 & 15")
                    self.collimator_wd_cmb.addItem("100 & 12")
                    self.collimator_wd_cmb.addItem("120 & 07")
                    self.collimator_wd_cmb.addItem("120 & 09")
                    self.collimator_wd_cmb.addItem("150 & 06")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.collimator_wd_cmb.setFont(font)
                    self.collimator_wd_cmb.hide()
                    self.collimator_wd_cmb.setObjectName("collimator_wd_cmb")

                    self.collimator_cct_lndt = QtWidgets.QLineEdit(self.Collimator_details_groupbox)
                    self.collimator_cct_lndt.setGeometry(QtCore.QRect(150, 180, 150, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_cct_lndt.setFont(font)
                    self.collimator_cct_lndt.setText("4500")
                    self.collimator_cct_lndt.hide()
                    self.collimator_cct_lndt.setObjectName("collimator_cct_lndt")
                    self.collimator_cct_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_cct_lbl.setGeometry(QtCore.QRect(20, 185, 110, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_cct_lbl.setFont(font)
                    self.collimator_cct_lbl.hide()
                    self.collimator_cct_lbl.setText("Color Temperature")
                    self.collimator_cct_lbl.setObjectName("collimator_cct_lbl")

                    self.collimator_chartdistance_lndt = QtWidgets.QLineEdit(self.Collimator_details_groupbox)
                    self.collimator_chartdistance_lndt.setGeometry(QtCore.QRect(150, 130, 150, 30))
                    regx = QRegExp(r"^([6-8][0-9][0-9]|5[1-9][0-9]|50[0-9]|9[0-8][0-9]|99[0-9]|[2-8][0-9][0-9][0-9]|1"
                                   r"[1-9][0-9][0-9]|10[1-9][0-9]|100[0-9]|9[0-8][0-9][0-9]|99[0-8][0-9]|999[0-9]|"
                                   r"[2-8][0-9][0-9][0-9][0-9]|1[1-9][0-9][0-9][0-9]|10[1-9][0-9][0-9]|100[1-9][0-9]"
                                   r"|1000[0-9]|9[0-8][0-9][0-9][0-9]|99[0-8][0-9][0-9]|999[0-8][0-9]|9999[0-9]|[2-8]"
                                   r"[0-9][0-9][0-9][0-9][0-9]|1[1-9][0-9][0-9][0-9][0-9]|10[1-9][0-9][0-9][0-9]"
                                   r"|100[1-9][0-9][0-9]|1000[1-9][0-9]|10000[0-9]|9[0-8][0-9][0-9][0-9][0-9]|99[0-8]"
                                   r"[0-9][0-9][0-9]|999[0-8][0-9][0-9]|9999[0-8][0-9]|99999[0-9]|[2-8][0-9][0-9]["
                                   r"0-9][0-9][0-9][0-9]|1[1-9][0-9][0-9][0-9][0-9][0-9]|10[1-9][0-9][0-9][0-9]["
                                   r"0-9]|100[1-9][0-9][0-9][0-9]|1000[1-9][0-9][0-9]|10000[1-9][0-9]|100000[0-9]|9["
                                   r"0-8][0-9][0-9][0-9][0-9][0-9]|99[0-8][0-9][0-9][0-9][0-9]|999[0-8][0-9][0-9]["
                                   r"0-9]|9999[0-8][0-9][0-9]|99999[0-8][0-9]|999999[0-9]|[2-8][0-9][0-9][0-9][0-9]["
                                   r"0-9][0-9][0-9]|1[1-9][0-9][0-9][0-9][0-9][0-9][0-9]|10[1-9][0-9][0-9][0-9][0-9]["
                                   r"0-9]|100[1-9][0-9][0-9][0-9][0-9]|1000[1-9][0-9][0-9][0-9]|10000[1-9][0-9]["
                                   r"0-9]|100000[1-9][0-9]|1000000[0-9]|9[0-8][0-9][0-9][0-9][0-9][0-9][0-9]|99[0-8]["
                                   r"0-9][0-9][0-9][0-9][0-9]|999[0-8][0-9][0-9][0-9][0-9]|9999[0-8][0-9][0-9]["
                                   r"0-9]|99999[0-8][0-9][0-9]|999999[0-8][0-9]|9999999[0-9]|[2-8][0-9][0-9][0-9]["
                                   r"0-9][0-9][0-9][0-9][0-9]|1[1-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]|10[1-9][0-9]["
                                   r"0-9][0-9][0-9][0-9][0-9]|100[1-9][0-9][0-9][0-9][0-9][0-9]|1000[1-9][0-9][0-9]["
                                   r"0-9][0-9]|10000[1-9][0-9][0-9][0-9]|100000[1-9][0-9][0-9]|1000000[1-9]["
                                   r"0-9]|10000000[0-9]|9[0-8][0-9][0-9][0-9][0-9][0-9][0-9][0-9]|99[0-8][0-9][0-9]["
                                   r"0-9][0-9][0-9][0-9]|999[0-8][0-9][0-9][0-9][0-9][0-9]|9999[0-8][0-9][0-9][0-9]["
                                   r"0-9]|99999[0-8][0-9][0-9][0-9]|999999[0-8][0-9][0-9]|9999999[0-8][0-9]|99999999["
                                   r"0-9]|1000000000)$")
                    collimator_chartdistance_lndt = QRegExpValidator(regx, self.collimator_chartdistance_lndt)
                    self.collimator_chartdistance_lndt.setValidator(collimator_chartdistance_lndt)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_chartdistance_lndt.setFont(font)
                    self.collimator_chartdistance_lndt.setObjectName("collimator_chartdistance_lndt")
                    self.collimator_chartdistance_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_chartdistance_lbl.setGeometry(QtCore.QRect(20, 135, 90, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_chartdistance_lbl.setFont(font)
                    self.collimator_chartdistance_lbl.setObjectName("collimator_chartdistance_lbl")

                    self.collimator_chartintensity_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_chartintensity_lbl.setGeometry(QtCore.QRect(20, 175, 100, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    font.setBold(True)
                    self.collimator_chartintensity_lbl.setFont(font)
                    self.collimator_chartintensity_lbl.setObjectName("collimator_chartintensity_lbl")

                    self.collimator_tl_chartintensity_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_tl_chartintensity_lbl.setGeometry(QtCore.QRect(20, 220, 50, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_tl_chartintensity_lbl.setFont(font)
                    self.collimator_tl_chartintensity_lbl.setObjectName("collimator_tl_chartintensity_lbl")

                    self.collimator_tl_chartintensity_lndt = QtWidgets.QLineEdit(self.Collimator_details_groupbox)
                    self.collimator_tl_chartintensity_lndt.setGeometry(QtCore.QRect(55, 215, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    regx = QRegExp(r"^([0-9]|[2-8][0-9]|1[0-9]|9[0-9]|1[1-9][0-9]|10[0-9]|2[0-4][0-9]|25[0-5])$")
                    collimator_tl_chartintensity_lndt = QRegExpValidator(regx, self.collimator_tl_chartintensity_lndt)
                    self.collimator_tl_chartintensity_lndt.setValidator(collimator_tl_chartintensity_lndt)
                    self.collimator_tl_chartintensity_lndt.setFont(font)
                    self.collimator_tl_chartintensity_lndt.setPlaceholderText("")
                    self.collimator_tl_chartintensity_lndt.setToolTip("The lux value ranges from 0 to 255")
                    self.collimator_tl_chartintensity_lndt.setObjectName("collimator_tl_chartintensity_lndt")

                    self.collimator_tr_chartintensity_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_tr_chartintensity_lbl.setGeometry(QtCore.QRect(20, 275, 50, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_tr_chartintensity_lbl.setFont(font)
                    self.collimator_tr_chartintensity_lbl.setObjectName("collimator_tr_chartintensity_lbl")

                    self.collimator_tr_chartintensity_lndt = QtWidgets.QLineEdit(self.Collimator_details_groupbox)
                    self.collimator_tr_chartintensity_lndt.setGeometry(QtCore.QRect(55, 265, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_tr_chartintensity_lndt.setFont(font)
                    regx = QRegExp(r"^([0-9]|[2-8][0-9]|1[0-9]|9[0-9]|1[1-9][0-9]|10[0-9]|2[0-4][0-9]|25[0-5])$")
                    collimator_tr_chartintensity_lndt = QRegExpValidator(regx, self.collimator_tr_chartintensity_lndt)
                    self.collimator_tr_chartintensity_lndt.setValidator(collimator_tr_chartintensity_lndt)
                    self.collimator_tr_chartintensity_lndt.setPlaceholderText("")
                    self.collimator_tr_chartintensity_lndt.setToolTip("The lux value ranges from 0 to 255")
                    self.collimator_tr_chartintensity_lndt.setObjectName("collimator_tr_chartintensity_lndt")

                    self.collimator_bl_chartintensity_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_bl_chartintensity_lbl.setGeometry(QtCore.QRect(145, 220, 50, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_bl_chartintensity_lbl.setFont(font)
                    self.collimator_bl_chartintensity_lbl.setObjectName("collimator_bl_chartintensity_lbl")

                    self.collimator_bl_chartintensity_lndt = QtWidgets.QLineEdit(self.Collimator_details_groupbox)
                    self.collimator_bl_chartintensity_lndt.setGeometry(QtCore.QRect(180, 215, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_bl_chartintensity_lndt.setFont(font)
                    self.collimator_bl_chartintensity_lndt.setPlaceholderText("")
                    regx = QRegExp(r"^([0-9]|[2-8][0-9]|1[0-9]|9[0-9]|1[1-9][0-9]|10[0-9]|2[0-4][0-9]|25[0-5])$")
                    collimator_bl_chartintensity_lndt = QRegExpValidator(regx, self.collimator_bl_chartintensity_lndt)
                    self.collimator_bl_chartintensity_lndt.setToolTip("The lux value ranges from 0 to 255")
                    self.collimator_bl_chartintensity_lndt.setValidator(collimator_bl_chartintensity_lndt)
                    self.collimator_bl_chartintensity_lndt.setObjectName("collimator_bl_chartintensity_lndt")

                    self.collimator_br_chartintensity_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_br_chartintensity_lbl.setGeometry(QtCore.QRect(145, 275, 50, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_br_chartintensity_lbl.setFont(font)
                    self.collimator_br_chartintensity_lbl.setObjectName("collimator_br_chartintensity_lbl")

                    self.collimator_br_chartintensity_lndt = QtWidgets.QLineEdit(self.Collimator_details_groupbox)
                    self.collimator_br_chartintensity_lndt.setGeometry(QtCore.QRect(180, 270, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_br_chartintensity_lndt.setFont(font)
                    regx = QRegExp(r"^([0-9]|[2-8][0-9]|1[0-9]|9[0-9]|1[1-9][0-9]|10[0-9]|2[0-4][0-9]|25[0-5])$")
                    collimator_br_chartintensity_lndt = QRegExpValidator(regx, self.collimator_br_chartintensity_lndt)
                    self.collimator_br_chartintensity_lndt.setValidator(collimator_br_chartintensity_lndt)
                    self.collimator_br_chartintensity_lndt.setPlaceholderText("")
                    self.collimator_br_chartintensity_lndt.setToolTip("The lux value ranges from 0 to 255")
                    self.collimator_br_chartintensity_lndt.setObjectName("collimator_br_chartintensity_lndt")

                    self.collimator_c_chartintensity_lbl = QtWidgets.QLabel(self.Collimator_details_groupbox)
                    self.collimator_c_chartintensity_lbl.setGeometry(QtCore.QRect(265, 220, 50, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_c_chartintensity_lbl.setFont(font)
                    self.collimator_c_chartintensity_lbl.setObjectName("collimator_c_chartintensity_lbl")

                    self.collimator_c_chartintensity_lndt = QtWidgets.QLineEdit(self.Collimator_details_groupbox)
                    self.collimator_c_chartintensity_lndt.setGeometry(QtCore.QRect(300, 215, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.collimator_c_chartintensity_lndt.setFont(font)
                    self.collimator_c_chartintensity_lndt.setPlaceholderText("")
                    regx = QRegExp(r"^([0-9]|[2-8][0-9]|1[0-9]|9[0-9]|1[1-9][0-9]|10[0-9]|2[0-4][0-9]|25[0-5])$")
                    collimator_c_chartintensity_lndt = QRegExpValidator(regx, self.collimator_c_chartintensity_lndt)
                    self.collimator_c_chartintensity_lndt.setValidator(collimator_c_chartintensity_lndt)
                    self.collimator_c_chartintensity_lndt.setToolTip("The lux value ranges from 0 to 255")
                    self.collimator_c_chartintensity_lndt.setObjectName("collimator_c_chartintensity_lndt")

                    self.collimator_chart_detail_update_btn = QtWidgets.QPushButton(self.Collimator_details_groupbox)
                    self.collimator_chart_detail_update_btn.setGeometry(QtCore.QRect(280, 270, 90, 40))
                    self.collimator_chart_detail_update_btn.setAccessibleName("Collimator_chart_update_btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.collimator_chart_detail_update_btn.setFont(font)
                    self.collimator_chart_detail_update_btn.setStyleSheet("QPushButton{\n"
                                                                          "background-color:rgb(49, 77, 162);\n"
                                                                          "color:rgb(255, 255, 255);\n"
                                                                          "border-radius: 10px;\n"
                                                                          "}"
                                                                          "QPushButton:Pressed{\n"
                                                                          "border: 3px solid;\n"
                                                                          "}"
                                                                          )
                    self.collimator_chart_detail_update_btn.setObjectName("collimator_chart_detail_update_btn")
                    self.verticalLayout_4.addWidget(self.Collimator_details_groupbox)
                    self.stackedWidget.addWidget(self.station_3_layout)

                    self.station_4_layout = QtWidgets.QWidget()
                    self.station_4_layout.setObjectName("station_4_layout")
                    self.relay_scrollarea = QtWidgets.QScrollArea(self.station_4_layout)
                    self.relay_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.relay_scrollarea.setGeometry(QtCore.QRect(0, 0, 420, 900))
                    self.relay_scrollarea.setWidgetResizable(True)
                    self.relay_scrollarea.setObjectName("relay_scrollarea")
                    self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
                    self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 401, 1242))
                    self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
                    self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_5)
                    self.verticalLayout_5.setObjectName("verticalLayout_5")

                    self.relay_enable_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.relay_enable_groupbox.sizePolicy().hasHeightForWidth())
                    self.relay_enable_groupbox.setSizePolicy(sizePolicy)
                    self.relay_enable_groupbox.setMinimumSize(QtCore.QSize(0, 80))
                    self.relay_enable_groupbox.setStyleSheet("border:0px")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_enable_groupbox.setFont(font)
                    self.relay_enable_groupbox.setObjectName("relay_enable_groupbox")
                    self.relay_enable_lbl = QLabel(self.relay_enable_groupbox)
                    self.relay_enable_lbl.setGeometry(QtCore.QRect(80, 25, 150, 15))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_enable_lbl.setFont(font)
                    self.relay_enable_lbl.setText('Station Enable')
                    self.relay_enable_lbl.setObjectName("relay_enable_lbl")
                    self.relay_toggle = Toggle(self.relay_enable_groupbox)
                    self.relay_toggle.setChecked(True)
                    self.relay_toggle.setGeometry(QtCore.QRect(210, 17, 70, 35))
                    self.verticalLayout_5.addWidget(self.relay_enable_groupbox)

                    self.relay_x_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.relay_x_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.relay_x_axis_groupbox.setSizePolicy(sizePolicy)
                    self.relay_x_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_x_axis_groupbox.setFont(font)
                    self.relay_x_axis_groupbox.setObjectName("relay_x_axis_groupbox")

                    self.relay_x_axis_mini_lbl = QtWidgets.QLabel(self.relay_x_axis_groupbox)
                    self.relay_x_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_x_axis_mini_lbl.setFont(font)
                    self.relay_x_axis_mini_lbl.setObjectName("relay_x_axis_mini_lbl")
                    self.relay_x_axis_mini_lndt = QtWidgets.QLineEdit(self.relay_x_axis_groupbox)
                    self.relay_x_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(\d|[1-9]\d)(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.relay_x_axis_mini_lndt)
                    self.relay_x_axis_mini_lndt.setValidator(validator)
                    self.relay_x_axis_mini_lndt.setObjectName("relay_x_axis_mini_lndt")

                    self.relay_x_axis_speed_lbl = QtWidgets.QLabel(self.relay_x_axis_groupbox)
                    self.relay_x_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_x_axis_speed_lbl.setFont(font)
                    self.relay_x_axis_speed_lbl.setText("Speed")
                    self.relay_x_axis_speed_lbl.setObjectName("relay_x_axis_speed_lbl")
                    self.relay_x_axis_speed_lndt = QtWidgets.QLineEdit(self.relay_x_axis_groupbox)
                    self.relay_x_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 5000, self.relay_x_axis_speed_lndt)
                    self.relay_x_axis_speed_lndt.setValidator(validator)
                    self.relay_x_axis_speed_lndt.setToolTip("The X-Actuator speed is limited to a range of 0 to 2000")
                    self.relay_x_axis_speed_lndt.setObjectName("relay_x_axis_speed_lndt")

                    self.relay_x_axis_current_position_lbl = QtWidgets.QLabel(self.relay_x_axis_groupbox)
                    self.relay_x_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.relay_x_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.relay_x_axis_current_position_lbl.setFont(font)
                    self.relay_x_axis_current_position_lbl.setObjectName("relay_x_axis_current_position_lbl")
                    self.relay_x_axis_current_position_value = QtWidgets.QLabel(self.relay_x_axis_groupbox)
                    self.relay_x_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.relay_x_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.relay_x_axis_current_position_value.setFont(font)
                    self.relay_x_axis_current_position_value.setObjectName("relay_x_axis_current_position_value")

                    self.relay_x_axis_run_btn = QtWidgets.QPushButton(self.relay_x_axis_groupbox)
                    self.relay_x_axis_run_btn.setAccessibleName('relay_x_axis_run_btn')
                    self.relay_x_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.relay_x_axis_run_btn.setFont(font)
                    self.relay_x_axis_run_btn.setText("Run")
                    self.relay_x_axis_run_btn.setFlat(True)
                    self.relay_x_axis_run_btn.setFont(font)
                    self.relay_x_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                            "background-color:rgb(49, 77, 162);\n"
                                                            "color:rgb(255, 255, 255);\n"
                                                            "border-radius: 10px;\n"
                                                            "}"
                                                            "QPushButton:Pressed{\n"
                                                            "border: 3px solid;\n"
                                                            "}"
                                                            )
                    self.relay_x_axis_run_btn.setObjectName("relay_x_axis_run_btn")

                    self.relay_x_axis_homing_btn = QtWidgets.QPushButton(self.relay_x_axis_groupbox)
                    self.relay_x_axis_homing_btn.setGeometry(QtCore.QRect(270, 100, 90, 40))
                    self.relay_x_axis_homing_btn.setAccessibleName('relay_x_axis_homing_btn')
                    self.relay_x_axis_homing_btn.setText("Homing")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.relay_x_axis_homing_btn.setFont(font)
                    self.relay_x_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                               "background-color:rgb(49, 77, 162);\n"
                                                               "color:rgb(255, 255, 255);\n"
                                                               "border-radius: 10px;\n"
                                                               "}"
                                                               "QPushButton:Pressed{\n"
                                                               "border: 3px solid;\n"
                                                               "}"
                                                               )
                    self.relay_x_axis_homing_btn.setObjectName("relay_x_axis_homing_btn")
                    self.verticalLayout_5.addWidget(self.relay_x_axis_groupbox)

                    self.relay_y_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.relay_y_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.relay_y_axis_groupbox.setSizePolicy(sizePolicy)
                    self.relay_y_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_y_axis_groupbox.setFont(font)
                    self.relay_y_axis_groupbox.setObjectName("relay_y_axis_groupbox")

                    self.relay_y_axis_mini_lbl = QtWidgets.QLabel(self.relay_y_axis_groupbox)
                    self.relay_y_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_y_axis_mini_lbl.setFont(font)
                    self.relay_y_axis_mini_lbl.setObjectName("relay_y_axis_mini_lbl")
                    self.relay_y_axis_mini_lndt = QtWidgets.QLineEdit(self.relay_y_axis_groupbox)
                    self.relay_y_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.relay_y_axis_mini_lndt)
                    self.relay_y_axis_mini_lndt.setValidator(validator)
                    self.relay_y_axis_mini_lndt.setObjectName("relay_y_axis_mini_lndt")

                    self.relay_y_axis_speed_lbl = QtWidgets.QLabel(self.relay_y_axis_groupbox)
                    self.relay_y_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_y_axis_speed_lbl.setFont(font)
                    self.relay_y_axis_speed_lbl.setText("Speed")
                    self.relay_y_axis_speed_lbl.setObjectName("relay_y_axis_speed_lbl")
                    self.relay_y_axis_speed_lndt = QtWidgets.QLineEdit(self.relay_y_axis_groupbox)
                    self.relay_y_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 15000, self.relay_y_axis_speed_lndt)
                    self.relay_y_axis_speed_lndt.setValidator(validator)
                    self.relay_y_axis_speed_lndt.setToolTip("The Y-Actuator speed is limited to a range of 0 to 15000")
                    self.relay_y_axis_speed_lndt.setObjectName("relay_y_axis_speed_lndt")

                    self.relay_y_axis_current_position_lbl = QtWidgets.QLabel(self.relay_y_axis_groupbox)
                    self.relay_y_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.relay_y_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.relay_y_axis_current_position_lbl.setFont(font)
                    self.relay_y_axis_current_position_lbl.setObjectName("relay_y_axis_current_position_lbl")
                    self.relay_y_axis_current_position_value = QtWidgets.QLabel(self.relay_y_axis_groupbox)
                    self.relay_y_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.relay_y_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.relay_y_axis_current_position_value.setFont(font)
                    self.relay_y_axis_current_position_value.setObjectName("relay_y_axis_current_position_value")

                    self.relay_y_axis_run_btn = QtWidgets.QPushButton(self.relay_y_axis_groupbox)
                    self.relay_y_axis_run_btn.setAccessibleName('relay_y_axis_run_btn')
                    self.relay_y_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.relay_y_axis_run_btn.setFont(font)
                    self.relay_y_axis_run_btn.setText("Run")
                    self.relay_y_axis_run_btn.setFlat(True)
                    self.relay_y_axis_run_btn.setFont(font)
                    self.relay_y_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                            "background-color:rgb(49, 77, 162);\n"
                                                            "color:rgb(255, 255, 255);\n"
                                                            "border-radius: 10px;\n"
                                                            "}"
                                                            "QPushButton:Pressed{\n"
                                                            "border: 3px solid;\n"
                                                            "}"
                                                            )
                    self.relay_y_axis_run_btn.setObjectName("relay_y_axis_run_btn")

                    self.relay_y_axis_homing_btn = QtWidgets.QPushButton(self.relay_y_axis_groupbox)
                    self.relay_y_axis_homing_btn.setGeometry(QtCore.QRect(270, 100, 90, 40))
                    self.relay_y_axis_homing_btn.setAccessibleName('relay_y_axis_homing_btn')
                    self.relay_y_axis_homing_btn.setText("Homing")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.relay_y_axis_homing_btn.setFont(font)
                    self.relay_y_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                               "background-color:rgb(49, 77, 162);\n"
                                                               "color:rgb(255, 255, 255);\n"
                                                               "border-radius: 10px;\n"
                                                               "}"
                                                               "QPushButton:Pressed{\n"
                                                               "border: 3px solid;\n"
                                                               "}"
                                                               )
                    self.relay_y_axis_homing_btn.setObjectName("relay_y_axis_homing_btn")
                    self.verticalLayout_5.addWidget(self.relay_y_axis_groupbox)

                    self.relay_gripper_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.relay_gripper_groupbox.sizePolicy().hasHeightForWidth())
                    self.relay_gripper_groupbox.setSizePolicy(sizePolicy)
                    self.relay_gripper_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_gripper_groupbox.setFont(font)
                    self.relay_gripper_groupbox.setObjectName("relay_gripper_groupbox")

                    self.relay_gripper_stepvalue_lndt = QtWidgets.QLineEdit(self.relay_gripper_groupbox)
                    self.relay_gripper_stepvalue_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r"^(0?\.[0-9]{2}|[1-9]?\d\.[0-9]{2}|[12]\d{2}\.[0-9]{2}|3[0-5]\d\.[0-9]{2}|360)$")
                    relay_gripper_stepvalue_lndt = QRegExpValidator(regx,
                                                                    self.relay_gripper_stepvalue_lndt)
                    self.relay_gripper_stepvalue_lndt.setValidator(relay_gripper_stepvalue_lndt)
                    self.relay_gripper_stepvalue_lndt.setObjectName("relay_gripper_stepvalue_lndt")
                    self.relay_gripper_stepvalue_lbl = QtWidgets.QLabel(self.relay_gripper_groupbox)
                    self.relay_gripper_stepvalue_lbl.setGeometry(QtCore.QRect(10, 30, 55, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_gripper_stepvalue_lbl.setFont(font)
                    self.relay_gripper_stepvalue_lbl.setObjectName("relay_gripper_stepvalue_lbl")

                    self.relay_gripper_clkwise_btn = QtWidgets.QPushButton(self.relay_gripper_groupbox)
                    self.relay_gripper_clkwise_btn.setGeometry(QtCore.QRect(10, 100, 70, 40))
                    self.relay_gripper_clkwise_btn.setAccessibleName('relay_clockwise_btn')
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_gripper_clkwise_btn.setFont(font)
                    self.relay_gripper_clkwise_btn.setStyleSheet("QPushButton{\n"
                                                                 "background-color:rgb(49, 77, 162);\n"
                                                                 "color:rgb(255, 255, 255);\n"
                                                                 "border-radius: 10px;\n"
                                                                 "}"
                                                                 "QPushButton:Pressed{\n"
                                                                 "border: 3px solid;\n"
                                                                 "}"
                                                                 )
                    self.relay_gripper_clkwise_btn.setText("")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.relay_gripper_clkwise_btn.setIcon(icon)
                    self.relay_gripper_clkwise_btn.setIconSize(QtCore.QSize(40, 40))
                    self.relay_gripper_clkwise_btn.setObjectName("relay_aclockwise_btn")

                    self.relay_gripper_aclkwise_btn = QtWidgets.QPushButton(self.relay_gripper_groupbox)
                    self.relay_gripper_aclkwise_btn.setGeometry(QtCore.QRect(110, 100, 70, 40))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_gripper_aclkwise_btn.setFont(font)
                    self.relay_gripper_aclkwise_btn.setAccessibleName('relay_anti_clockwise_btn')
                    self.relay_gripper_aclkwise_btn.setStyleSheet("QPushButton{\n"
                                                                  "background-color:rgb(49, 77, 162);\n"
                                                                  "color:rgb(255, 255, 255);\n"
                                                                  "border-radius: 10px;\n"
                                                                  "}"
                                                                  "QPushButton:Pressed{\n"
                                                                  "border: 3px solid;\n"
                                                                  "}"
                                                                  )
                    self.relay_gripper_aclkwise_btn.setText("")
                    icon1 = QtGui.QIcon()
                    icon1.addPixmap(QtGui.QPixmap(r".\media\anti-clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.relay_gripper_aclkwise_btn.setIcon(icon1)
                    self.relay_gripper_aclkwise_btn.setIconSize(QtCore.QSize(40, 40))
                    self.relay_gripper_aclkwise_btn.setObjectName("relay_gripper_aclkwise_btn")
                    self.verticalLayout_5.addWidget(self.relay_gripper_groupbox)

                    self.relay_light_panel_actuator_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(
                        self.relay_light_panel_actuator_groupbox.sizePolicy().hasHeightForWidth())
                    self.relay_light_panel_actuator_groupbox.setSizePolicy(sizePolicy)
                    self.relay_light_panel_actuator_groupbox.setMinimumSize(QtCore.QSize(0, 360))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_light_panel_actuator_groupbox.setFont(font)
                    self.relay_light_panel_actuator_groupbox.setStyleSheet("Background-color:RGB(240, 240, 240)")
                    self.relay_light_panel_actuator_groupbox.setObjectName("relay_light_panel_actuator_groupbox")

                    self.relay_light_panel_actuator_mini_lbl = QtWidgets.QLabel(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_actuator_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_light_panel_actuator_mini_lbl.setFont(font)
                    self.relay_light_panel_actuator_mini_lbl.setObjectName("relay_light_panel_actuator_mini_lbl")
                    self.relay_light_panel_actuator_mini_lndt = QtWidgets.QLineEdit(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_actuator_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.relay_light_panel_actuator_mini_lndt)
                    self.relay_light_panel_actuator_mini_lndt.setValidator(validator)
                    self.relay_light_panel_actuator_mini_lndt.setObjectName("relay_light_panel_actuator_mini_lndt")

                    self.relay_light_panel_actuator_speed_lbl = QtWidgets.QLabel(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_actuator_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_light_panel_actuator_speed_lbl.setFont(font)
                    self.relay_light_panel_actuator_speed_lbl.setText("Speed")
                    self.relay_light_panel_actuator_speed_lbl.setObjectName("relay_light_panel_actuator_speed_lbl")
                    self.relay_light_panel_actuator_speed_lndt = QtWidgets.QLineEdit(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_actuator_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 15000, self.relay_y_axis_speed_lndt)
                    self.relay_y_axis_speed_lndt.setValidator(validator)
                    self.relay_light_panel_actuator_speed_lndt.setToolTip(
                        "The Z-Actuator speed is limited to a range of 0 to 2000")
                    self.relay_light_panel_actuator_speed_lndt.setObjectName("relay_light_panel_actuator_speed_lndt")

                    self.relay_light_panel_actuator_current_position_lbl = QtWidgets.QLabel(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_actuator_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.relay_light_panel_actuator_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.relay_light_panel_actuator_current_position_lbl.setFont(font)
                    self.relay_light_panel_actuator_current_position_lbl.setObjectName(
                        "relay_light_panel_actuator_current_position_lbl")
                    self.relay_light_panel_actuator_current_position_value = QtWidgets.QLabel(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_actuator_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.relay_light_panel_actuator_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.relay_light_panel_actuator_current_position_value.setFont(font)
                    self.relay_light_panel_actuator_current_position_value.setObjectName(
                        "relay_light_panel_actuator_current_position_value")

                    self.relay_light_panel_actuator_run_btn = QtWidgets.QPushButton(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_actuator_run_btn.setAccessibleName('relay_light_panel_actuator_run_btn')
                    self.relay_light_panel_actuator_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.relay_light_panel_actuator_run_btn.setFont(font)
                    self.relay_light_panel_actuator_run_btn.setText("Run")
                    self.relay_light_panel_actuator_run_btn.setFlat(True)
                    self.relay_light_panel_actuator_run_btn.setFont(font)
                    self.relay_light_panel_actuator_run_btn.setStyleSheet("QPushButton{\n"
                                                                          "background-color:rgb(49, 77, 162);\n"
                                                                          "color:rgb(255, 255, 255);\n"
                                                                          "border-radius: 10px;\n"
                                                                          "}"
                                                                          "QPushButton:Pressed{\n"
                                                                          "border: 3px solid;\n"
                                                                          "}"
                                                                          )
                    self.relay_light_panel_actuator_run_btn.setObjectName("relay_light_panel_actuator_run_btn")

                    self.relay_light_panel_actuator_homing_btn = QtWidgets.QPushButton(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_actuator_homing_btn.setGeometry(QtCore.QRect(270, 100, 90, 40))
                    self.relay_light_panel_actuator_homing_btn.setText("Homing")
                    self.relay_light_panel_actuator_homing_btn.setAccessibleName("relay_z_axis homing btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.relay_light_panel_actuator_homing_btn.setFont(font)
                    self.relay_light_panel_actuator_homing_btn.setStyleSheet("QPushButton{\n"
                                                                             "background-color:rgb(49, 77, 162);\n"
                                                                             "color:rgb(255, 255, 255);\n"
                                                                             "border-radius: 10px;\n"
                                                                             "}"
                                                                             "QPushButton:Pressed{\n"
                                                                             "border: 3px solid;\n"
                                                                             "}"
                                                                             )
                    self.relay_light_panel_actuator_homing_btn.setObjectName("relay_light_panel_actuator_homing_btn")

                    self.relay_light_panel_intensity_lbl = QtWidgets.QLabel(self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_intensity_lbl.setGeometry(QtCore.QRect(10, 180, 100, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_light_panel_intensity_lbl.setFont(font)
                    self.relay_light_panel_intensity_lbl.setObjectName("relay_light_panel_intensity_lbl")
                    self.relay_light_panel_intensity_lndt = QtWidgets.QLineEdit(
                        self.relay_light_panel_actuator_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.relay_light_panel_intensity_lndt)
                    self.relay_light_panel_intensity_lndt.setValidator(validator)
                    self.relay_light_panel_intensity_lndt.setGeometry(QtCore.QRect(140, 180, 100, 30))
                    self.relay_light_panel_intensity_lndt.setToolTip("The lux is limited to a range of 0 to 1024")
                    self.relay_light_panel_intensity_lndt.setObjectName("relay_light_panel_intensity_lndt")

                    self.relay_light_panel_intensity_btn = QtWidgets.QPushButton(
                        self.relay_light_panel_actuator_groupbox)
                    self.relay_light_panel_intensity_btn.setGeometry(QtCore.QRect(270, 175, 90, 40))
                    self.relay_light_panel_intensity_btn.setText("Set")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.relay_light_panel_intensity_btn.setFont(font)
                    self.relay_light_panel_intensity_btn.setStyleSheet("QPushButton{\n"
                                                                       "background-color:rgb(49, 77, 162);\n"
                                                                       "color:rgb(255, 255, 255);\n"
                                                                       "border-radius: 10px;\n"
                                                                       "}"
                                                                       "QPushButton:Pressed{\n"
                                                                       "border: 3px solid;\n"
                                                                       "}"
                                                                       )
                    self.relay_light_panel_intensity_btn.setObjectName("relay_light_panel_intensity_btn")

                    self.relay_chart_orientation_lbl = QtWidgets.QLabel(self.relay_light_panel_actuator_groupbox)
                    self.relay_chart_orientation_lbl.setGeometry(QtCore.QRect(10, 230, 100, 30))
                    self.relay_chart_orientation_lbl.setText("Chart orientation")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_chart_orientation_lbl.setFont(font)
                    self.relay_chart_orientation_lbl.setObjectName("relay_chart_orientation_lbl")

                    self.relay_chart_orientation_cmb = combobox(self.relay_light_panel_actuator_groupbox)
                    self.relay_chart_orientation_cmb.setGeometry(QtCore.QRect(140, 230, 100, 30))
                    self.relay_chart_orientation_cmb.addItem("--Select--")
                    self.relay_chart_orientation_cmb.addItem("Horizontal")
                    self.relay_chart_orientation_cmb.addItem("Vertical")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_chart_orientation_cmb.setFont(font)
                    self.relay_chart_orientation_cmb.setObjectName("relay_chart_orientation_cmb")

                    self.img_frmt_lbl = QtWidgets.QLabel(self.relay_light_panel_actuator_groupbox)
                    self.img_frmt_lbl.setGeometry(QtCore.QRect(10, 280, 60, 35))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.img_frmt_lbl.setFont(font)
                    self.img_frmt_lbl.setText("Format type")
                    self.img_frmt_lbl.setObjectName("img_frmt_lbl")
                    self.img_frmt_box = combobox(self.relay_light_panel_actuator_groupbox)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.img_frmt_box.setFont(font)
                    self.img_frmt_box.addItem("Monochrome")
                    self.img_frmt_box.addItem("CN")
                    self.img_frmt_box.addItem("No")
                    self.img_frmt_box.addItem("DB, RG")
                    self.img_frmt_box.addItem("DB, BG")
                    self.img_frmt_box.addItem("DB, GR")
                    self.img_frmt_box.addItem("DB, GB")
                    self.img_frmt_box.setGeometry(QtCore.QRect(140, 280, 100, 30))
                    self.img_frmt_box.setObjectName("img_frmt_box")

                    self.verticalLayout_5.addWidget(self.relay_light_panel_actuator_groupbox)

                    self.relay_offset_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.relay_offset_groupbox.sizePolicy().hasHeightForWidth())
                    self.relay_offset_groupbox.setSizePolicy(sizePolicy)
                    self.relay_offset_groupbox.setMinimumSize(QtCore.QSize(0, 300))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_offset_groupbox.setFont(font)
                    self.relay_offset_groupbox.setStyleSheet("Background-color:RGB(240, 240, 240)")
                    self.relay_offset_groupbox.setObjectName("relay_offset_groupbox")

                    self.relay_after_gluing_focus_lbl = QtWidgets.QLabel(self.relay_offset_groupbox)
                    self.relay_after_gluing_focus_lbl.setGeometry(QtCore.QRect(20, 25, 170, 35))
                    self.relay_after_gluing_focus_lbl.setText("Do you need to \n"
                                                              "check focus after gluing ?")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_after_gluing_focus_lbl.setFont(font)
                    self.relay_after_gluing_focus_lbl.setObjectName("relay_after_gluing_focus_lbl")

                    self.relay_after_gluing_focus_cmb = combobox(self.relay_offset_groupbox)
                    self.relay_after_gluing_focus_cmb.setGeometry(QtCore.QRect(180, 20, 100, 30))
                    self.relay_after_gluing_focus_cmb.addItem("No")
                    self.relay_after_gluing_focus_cmb.addItem("Yes")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_after_gluing_focus_cmb.setFont(font)
                    self.relay_after_gluing_focus_cmb.setObjectName("relay_after_gluing_focus_cmb")

                    self.relay_after_curing_focus_lbl = QtWidgets.QLabel(self.relay_offset_groupbox)
                    self.relay_after_curing_focus_lbl.setGeometry(QtCore.QRect(20, 75, 170, 35))
                    self.relay_after_curing_focus_lbl.setText("Do you need to check\n"
                                                              "focus after curing ?")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_after_curing_focus_lbl.setFont(font)
                    self.relay_after_curing_focus_lbl.setObjectName("relay_after_curing_focus_lbl")

                    self.relay_after_curing_focus_cmb = combobox(self.relay_offset_groupbox)
                    self.relay_after_curing_focus_cmb.setGeometry(QtCore.QRect(180, 70, 100, 30))
                    self.relay_after_curing_focus_cmb.addItem("No")
                    self.relay_after_curing_focus_cmb.addItem("Yes")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_after_curing_focus_cmb.setFont(font)
                    self.relay_after_curing_focus_cmb.setObjectName("relay_after_curing_focus_cmb")

                    self.relay_raw_save_option_lbl = QtWidgets.QLabel(self.relay_offset_groupbox)
                    self.relay_raw_save_option_lbl.setGeometry(QtCore.QRect(20, 125, 110, 35))
                    self.relay_raw_save_option_lbl.setText("Do you need to\n"
                                                           "save raw frame ?")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_raw_save_option_lbl.setFont(font)
                    self.relay_raw_save_option_lbl.setObjectName("relay_raw_save_option_lbl")

                    self.relay_raw_save_option_cmb = combobox(self.relay_offset_groupbox)
                    self.relay_raw_save_option_cmb.setGeometry(QtCore.QRect(180, 120, 100, 30))
                    self.relay_raw_save_option_cmb.addItem("No")
                    self.relay_raw_save_option_cmb.addItem("Yes")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_raw_save_option_cmb.setFont(font)
                    self.relay_raw_save_option_cmb.setObjectName("relay_raw_save_option_cmb")

                    self.relay_offset_lbl = QtWidgets.QLabel(self.relay_offset_groupbox)
                    self.relay_offset_lbl.setGeometry(QtCore.QRect(20, 175, 110, 35))
                    self.relay_offset_lbl.setText("Is there relay lens\n"
                                                  "or not ?")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_offset_lbl.setFont(font)
                    self.relay_offset_lbl.setObjectName("relay_offset_lbl")

                    self.relay_offset_cmb = combobox(self.relay_offset_groupbox)
                    self.relay_offset_cmb.setGeometry(QtCore.QRect(180, 170, 100, 30))
                    self.relay_offset_cmb.addItem("Yes")
                    self.relay_offset_cmb.addItem("No")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_offset_cmb.setFont(font)
                    self.relay_offset_cmb.setObjectName("relay_offset_cmb")

                    self.relay_fixture_offset_lbl = QtWidgets.QLabel(self.relay_offset_groupbox)
                    self.relay_fixture_offset_lbl.setGeometry(QtCore.QRect(20, 225, 110, 35))
                    self.relay_fixture_offset_lbl.setText("Do you need to\n"
                                                          "check offset")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_fixture_offset_lbl.setFont(font)
                    self.relay_fixture_offset_lbl.setObjectName("relay_fixture_offset_lbl")

                    self.relay_fixture_offset_cmb = combobox(self.relay_offset_groupbox)
                    self.relay_fixture_offset_cmb.setGeometry(QtCore.QRect(180, 220, 100, 30))
                    self.relay_fixture_offset_cmb.setEnabled(False)
                    self.relay_fixture_offset_cmb.addItem("No")
                    self.relay_fixture_offset_cmb.addItem("Yes")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_fixture_offset_cmb.setFont(font)
                    self.relay_fixture_offset_cmb.setObjectName("relay_fixture_offset_cmb")

                    self.relay_dx_offset_tolerence_lbl = QtWidgets.QLabel(self.relay_offset_groupbox)
                    self.relay_dx_offset_tolerence_lbl.setGeometry(QtCore.QRect(20, 275, 90, 20))
                    self.relay_dx_offset_tolerence_lbl.setText("Tolerance of Dx: ")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_dx_offset_tolerence_lbl.setFont(font)
                    self.relay_dx_offset_tolerence_lbl.setObjectName("relay_dx_offset_tolerence_lbl")
                    self.relay_dx_offset_tolerence_lndt = QtWidgets.QLineEdit(self.relay_offset_groupbox)
                    self.relay_dx_offset_tolerence_lndt.setGeometry(QtCore.QRect(180, 270, 70, 30))
                    regx = QRegExp(r"^(0?\.[1-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8]"
                                   r"[0-9]\.[0-9][0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9]"
                                   r"[0-9]*|99\.[0-9][0-9]*|[2-8][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9]\.[0-9]"
                                   r"[0-9]*|10[1-9]\.[0-9][0-9]*|100\.[0-9][0-9]*|9[0-8][0-9]\.[0-9]"
                                   r"[0-9]*|99[0-8]\.[0-9][0-9]*|999\.[0-9][0-9]*|[2-2][0-9][0-9][0-9]\.[0-9]"
                                   r"[0-9]*|1[1-9][0-9][0-9]\.[0-9][0-9]*|10[1-9][0-9]\.[0-9][0-9]*|100[1-9]\.[0-9]"
                                   r"[0-9]*|1000\.[0-9][0-9]*|3000\.[0-0][0-9]*)$")
                    relay_dx_offset_tolerence_lndt = QRegExpValidator(regx,
                                                                      self.relay_dx_offset_tolerence_lndt)
                    self.relay_dx_offset_tolerence_lndt.setValidator(relay_dx_offset_tolerence_lndt)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_dx_offset_tolerence_lndt.setFont(font)
                    self.relay_dx_offset_tolerence_lbl.hide()
                    self.relay_dx_offset_tolerence_lndt.hide()
                    self.relay_dx_offset_tolerence_lndt.setObjectName("relay_dx_offset_tolerence_lndt")

                    self.relay_dy_offset_tolerence_lbl = QtWidgets.QLabel(self.relay_offset_groupbox)
                    self.relay_dy_offset_tolerence_lbl.setGeometry(QtCore.QRect(20, 325, 90, 20))
                    self.relay_dy_offset_tolerence_lbl.setText("Tolerance of Dy: ")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_dy_offset_tolerence_lbl.setFont(font)
                    self.relay_dy_offset_tolerence_lbl.setObjectName("relay_dy_offset_tolerence_lbl")
                    self.relay_dy_offset_tolerence_lndt = QtWidgets.QLineEdit(self.relay_offset_groupbox)
                    self.relay_dy_offset_tolerence_lndt.setGeometry(QtCore.QRect(180, 320, 70, 30))
                    regx = QRegExp(r"^(0?\.[1-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8]"
                                   r"[0-9]\.[0-9][0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9]"
                                   r"[0-9]*|99\.[0-9][0-9]*|[2-8][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9]\.[0-9]"
                                   r"[0-9]*|10[1-9]\.[0-9][0-9]*|100\.[0-9][0-9]*|9[0-8][0-9]\.[0-9]"
                                   r"[0-9]*|99[0-8]\.[0-9][0-9]*|999\.[0-9][0-9]*|[2-2][0-9][0-9][0-9]\.[0-9]"
                                   r"[0-9]*|1[1-9][0-9][0-9]\.[0-9][0-9]*|10[1-9][0-9]\.[0-9][0-9]*|100[1-9]\.[0-9]"
                                   r"[0-9]*|1000\.[0-9][0-9]*|3000\.[0-0][0-9]*)$")
                    relay_dy_offset_tolerence_lndt = QRegExpValidator(regx, self.relay_dy_offset_tolerence_lndt)
                    self.relay_dy_offset_tolerence_lndt.setValidator(relay_dy_offset_tolerence_lndt)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_dy_offset_tolerence_lndt.setFont(font)
                    self.relay_dy_offset_tolerence_lbl.hide()
                    self.relay_dy_offset_tolerence_lndt.hide()
                    self.relay_dy_offset_tolerence_lndt.setObjectName("relay_dy_offset_tolerence_lndt")

                    self.relay_lens_offset_check_btn = QtWidgets.QPushButton(self.relay_offset_groupbox)
                    self.relay_lens_offset_check_btn.setText('Offset_check')
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_lens_offset_check_btn.setFont(font)
                    self.relay_lens_offset_check_btn.setGeometry(QtCore.QRect(280, 270, 80, 30))
                    self.relay_lens_offset_check_btn.setStyleSheet("QPushButton{\n"
                                                                   "background-color:rgb(49, 77, 162);\n"
                                                                   "color:rgb(255, 255, 255);\n"
                                                                   "border-radius: 10px;\n"
                                                                   "}"
                                                                   "QPushButton:Pressed{\n"
                                                                   "border: 3px solid;\n"
                                                                   "}"
                                                                   )
                    self.relay_lens_offset_check_btn.setObjectName('relay_lens_offset_check_btn')
                    self.relay_lens_offset_check_btn.hide()

                    self.pixel_in_mm_lbl = QtWidgets.QLabel(self.relay_offset_groupbox)
                    self.pixel_in_mm_lbl.setGeometry(QtCore.QRect(20, 375, 90, 20))
                    self.pixel_in_mm_lbl.setText("No.of Pixels")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.pixel_in_mm_lbl.setFont(font)
                    self.pixel_in_mm_lbl.setObjectName("pixel_in_mm_lbl")
                    self.pixel_in_mm_lndt = QtWidgets.QLineEdit(self.relay_offset_groupbox)
                    self.pixel_in_mm_lndt.setGeometry(QtCore.QRect(180, 370, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.pixel_in_mm_lndt.setFont(font)
                    self.pixel_in_mm_lndt.setToolTip("Here’s what you’re specifying:\n"
                                                     "the pixel difference that occurs when moving 1 mm "
                                                     "in the X or Y actuator.")
                    self.pixel_in_mm_lbl.hide()
                    self.pixel_in_mm_lndt.hide()
                    self.pixel_in_mm_lndt.setObjectName("pixel_in_mm_lndt")
                    self.verticalLayout_5.addWidget(self.relay_offset_groupbox)

                    self.relay_details_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.relay_details_groupbox.sizePolicy().hasHeightForWidth())
                    self.relay_details_groupbox.setSizePolicy(sizePolicy)
                    self.relay_details_groupbox.setMinimumSize(QtCore.QSize(0, 500))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.relay_details_groupbox.setFont(font)
                    self.relay_details_groupbox.setStyleSheet("Background-color:RGB(240, 240, 240)")
                    self.relay_details_groupbox.setObjectName("relay_details_groupbox")

                    self.no_of_ROI_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.no_of_ROI_lbl.setText('No.of ROI')
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.no_of_ROI_lbl.setFont(font)
                    self.no_of_ROI_lbl.setGeometry(QtCore.QRect(10, 20, 100, 35))
                    self.no_of_ROI_lbl.setObjectName('no_of_ROI_lbl')

                    self.no_of_ROI_txtbox = combobox(self.relay_details_groupbox)
                    self.no_of_ROI_txtbox.setGeometry(QtCore.QRect(110, 20, 150, 30))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.no_of_ROI_txtbox.setFont(font)
                    self.no_of_ROI_txtbox.addItem('5')
                    self.no_of_ROI_txtbox.setObjectName('no_of_ROI_txtbox')

                    self.chart_position_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.chart_position_lbl.setGeometry(QtCore.QRect(10, 80, 120, 35))
                    self.chart_position_lbl.setText('Chart Position')
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.chart_position_lbl.setFont(font)
                    self.chart_position_lbl.setObjectName('chart_position_lbl')

                    self.chart_position_box = combobox(self.relay_details_groupbox)
                    self.chart_position_box.setGeometry(QtCore.QRect(110, 80, 150, 35))
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.chart_position_box.setFont(font)
                    self.chart_position_box.addItem('C,TL,TR,BL,BR')
                    self.chart_position_box.setObjectName('chart_position_box')

                    self.azimuth_ang_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.azimuth_ang_lbl.setGeometry(QtCore.QRect(10, 140, 120, 35))
                    self.azimuth_ang_lbl.setText('Azimuth Angle')
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.azimuth_ang_lbl.setFont(font)
                    self.azimuth_ang_lbl.setObjectName('Azimuth_lbl')

                    self.azimuth_ang_txtbox = QtWidgets.QLineEdit(self.relay_details_groupbox)
                    self.azimuth_ang_txtbox.setGeometry(QtCore.QRect(110, 140, 70, 30))
                    regx = QRegExp(r"^(0?\.[1-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8]"
                                   r"[0-9]\.[0-9][0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9]"
                                   r"[0-9]*|99\.[0-9][0-9]*|100\.0[0-9]*)$")
                    azimuth_ang_txtbox = QRegExpValidator(regx, self.azimuth_ang_txtbox)
                    self.azimuth_ang_txtbox.setValidator(azimuth_ang_txtbox)
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.azimuth_ang_txtbox.setFont(font)
                    self.azimuth_ang_txtbox.setObjectName('azimuth_txtbox')

                    self.outer_radius_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.outer_radius_lbl.setGeometry(QtCore.QRect(210, 140, 120, 35))
                    self.outer_radius_lbl.setText('Radius')
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.outer_radius_lbl.setFont(font)
                    self.outer_radius_lbl.setObjectName('outer_radius_lbl')

                    self.outer_radius_txtbox = QtWidgets.QLineEdit(self.relay_details_groupbox)
                    self.outer_radius_txtbox.setGeometry(QtCore.QRect(300, 140, 70, 30))
                    regx = QRegExp(r"^(0?\.[0-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8]"
                                   r"[0-9]\.[0-9][0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9]"
                                   r"[0-9]*|99\.[0-9][0-9]*|[2-8][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9]\.[0-9]"
                                   r"[0-9]*|10[1-9]\.[0-9][0-9]*|100\.[0-9][0-9]*|9[0-8][0-9]\.[0-9]"
                                   r"[0-9]*|99[0-8]\.[0-9][0-9]*|999\.[0-9][0-9]*|[2-3][0-9][0-9][0-9]\.[0-9]"
                                   r"[0-9]*|1[1-9][0-9][0-9]\.[0-9][0-9]*|10[1-9][0-9]\.[0-9][0-9]*|100[1-9]\.[0-9]"
                                   r"[0-9]*|1000\.[0-9][0-9]*|4000\.[0-0][0-9]*)$")
                    outer_radius_txtbox = QRegExpValidator(regx, self.outer_radius_txtbox)
                    self.outer_radius_txtbox.setValidator(outer_radius_txtbox)
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.outer_radius_txtbox.setFont(font)
                    self.outer_radius_txtbox.setObjectName('outer_radius_txtbox')

                    self.width_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.width_lbl.setGeometry(QtCore.QRect(10, 200, 120, 35))
                    self.width_lbl.setText('Width')
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.width_lbl.setFont(font)
                    self.width_lbl.setObjectName('width_lbl')

                    self.width_txtbox = QtWidgets.QLineEdit(self.relay_details_groupbox)
                    self.width_txtbox.setGeometry(QtCore.QRect(110, 200, 70, 30))
                    regx = QRegExp(r"^([2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8][0-9]\.[0-9]"
                                   r"[0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9][0-9]*|99\.[0-9]"
                                   r"[0-9]*|[2-8][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9]\.[0-9][0-9]*|10[1-9]\.[0-9]"
                                   r"[0-9]*|100\.[0-9][0-9]*|9[0-8][0-9]\.[0-9][0-9]*|99[0-8]\.[0-9][0-9]*|999\.[0-9]"
                                   r"[0-9]*|[2-2][0-9][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9][0-9]\.[0-9][0-9]*|10[1-9]"
                                   r"[0-9]\.[0-9][0-9]*|100[1-9]\.[0-9][0-9]*|1000\.[0-9][0-9]*|3000\.[0-0][0-9]*)$")
                    width_txtbox = QRegExpValidator(regx, self.width_txtbox)
                    self.width_txtbox.setValidator(width_txtbox)
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.width_txtbox.setFont(font)
                    self.width_txtbox.setObjectName('width_txtbox')

                    self.height_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.height_lbl.setGeometry(QtCore.QRect(210, 200, 120, 35))
                    self.height_lbl.setText('Height')
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.height_lbl.setFont(font)
                    self.height_lbl.setObjectName('height_lbl')

                    self.height_txtbox = QtWidgets.QLineEdit(self.relay_details_groupbox)
                    self.height_txtbox.setGeometry(QtCore.QRect(300, 200, 70, 30))
                    regx = QRegExp(r"^([2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8][0-9]\.[0-9]"
                                   r"[0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9][0-9]*|99\.[0-9]"
                                   r"[0-9]*|[2-8][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9]\.[0-9][0-9]*|10[1-9]\.[0-9]"
                                   r"[0-9]*|100\.[0-9][0-9]*|9[0-8][0-9]\.[0-9][0-9]*|99[0-8]\.[0-9][0-9]*|999\.[0-9]"
                                   r"[0-9]*|[2-2][0-9][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9][0-9]\.[0-9][0-9]*|10[1-9]"
                                   r"[0-9]\.[0-9][0-9]*|100[1-9]\.[0-9][0-9]*|1000\.[0-9][0-9]*|3000\.[0-0][0-9]*)$")
                    height_txtbox = QRegExpValidator(regx, self.height_txtbox)
                    self.height_txtbox.setValidator(height_txtbox)
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.height_txtbox.setFont(font)
                    self.height_txtbox.setObjectName('height_txtbox')

                    self.relay_black_lvl_value_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.relay_black_lvl_value_lbl.setGeometry(QtCore.QRect(10, 260, 100, 30))
                    self.relay_black_lvl_value_lbl.setText("Black level")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_black_lvl_value_lbl.setFont(font)
                    self.relay_black_lvl_value_lbl.setObjectName("relay_black_lvl_value_lbl")
                    self.relay_black_lvl_value_lndt = QtWidgets.QLineEdit(
                        self.relay_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    relay_black_lvl_value_lndt = QRegExpValidator(regx, self.relay_black_lvl_value_lndt)
                    self.relay_black_lvl_value_lndt.setValidator(relay_black_lvl_value_lndt)
                    self.relay_black_lvl_value_lndt.setGeometry(QtCore.QRect(110, 260, 70, 30))
                    self.relay_black_lvl_value_lndt.setObjectName("relay_black_lvl_value_lndt")

                    self.relay_median_frame_cnt_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.relay_median_frame_cnt_lbl.setGeometry(QtCore.QRect(210, 260, 100, 30))
                    self.relay_median_frame_cnt_lbl.setText("Median frame\ncount")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_median_frame_cnt_lbl.setFont(font)
                    self.relay_median_frame_cnt_lbl.setObjectName("relay_median_frame_cnt_lbl")
                    self.relay_median_frame_cnt_lndt = QtWidgets.QLineEdit(
                        self.relay_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    relay_median_frame_cnt_lndt = QRegExpValidator(regx, self.relay_median_frame_cnt_lndt)
                    self.relay_median_frame_cnt_lndt.setValidator(relay_median_frame_cnt_lndt)
                    self.relay_median_frame_cnt_lndt.setGeometry(QtCore.QRect(300, 260, 70, 30))
                    self.relay_median_frame_cnt_lndt.setObjectName("relay_median_frame_cnt_lndt")

                    self.relay_red_value_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.relay_red_value_lbl.setGeometry(QtCore.QRect(10, 320, 100, 30))
                    self.relay_red_value_lbl.setText("Red value")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_red_value_lbl.setFont(font)
                    self.relay_red_value_lbl.setObjectName("relay_red_value_lbl")
                    self.relay_red_value_lndt = QtWidgets.QLineEdit(
                        self.relay_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    relay_red_value_lndt = QRegExpValidator(regx, self.relay_red_value_lndt)
                    self.relay_red_value_lndt.setValidator(relay_red_value_lndt)
                    self.relay_red_value_lndt.setGeometry(QtCore.QRect(110, 320, 70, 30))
                    self.relay_red_value_lndt.setObjectName("relay_red_value_lndt")

                    self.relay_green_value_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.relay_green_value_lbl.setGeometry(QtCore.QRect(210, 320, 100, 30))
                    self.relay_green_value_lbl.setText("Green value")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_green_value_lbl.setFont(font)
                    self.relay_green_value_lbl.setObjectName("relay_green_value_lbl")
                    self.relay_green_value_lndt = QtWidgets.QLineEdit(
                        self.relay_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    relay_green_value_lndt = QRegExpValidator(regx, self.relay_green_value_lndt)
                    self.relay_green_value_lndt.setValidator(relay_green_value_lndt)
                    self.relay_green_value_lndt.setGeometry(QtCore.QRect(300, 320, 70, 30))
                    self.relay_green_value_lndt.setObjectName("relay_green_value_lndt")

                    self.relay_blue_value_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.relay_blue_value_lbl.setGeometry(QtCore.QRect(10, 370, 100, 30))
                    self.relay_blue_value_lbl.setText("Blue value")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.relay_blue_value_lbl.setFont(font)
                    self.relay_blue_value_lbl.setObjectName("relay_blue_value_lbl")
                    self.relay_blue_value_lndt = QtWidgets.QLineEdit(self.relay_details_groupbox)
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    relay_blue_value_lndt = QRegExpValidator(regx, self.relay_blue_value_lndt)
                    self.relay_blue_value_lndt.setValidator(relay_blue_value_lndt)
                    self.relay_blue_value_lndt.setGeometry(QtCore.QRect(110, 370, 70, 30))
                    self.relay_blue_value_lndt.setObjectName("relay_blue_value_lndt")

                    self.relay_details_save_frame_btn = QtWidgets.QPushButton(self.relay_details_groupbox)
                    self.relay_details_save_frame_btn.setGeometry(QtCore.QRect(210, 370, 100, 30))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_details_save_frame_btn.setFont(font)
                    self.relay_details_save_frame_btn.setText("Save Frame")
                    self.relay_details_save_frame_btn.setStyleSheet("QPushButton{\n"
                                                                    "background-color:rgb(49, 77, 162);\n"
                                                                    "color:rgb(255, 255, 255);\n"
                                                                    "border-radius: 10px;\n"
                                                                    "}"
                                                                    "QPushButton:Pressed{\n"
                                                                    "border: 3px solid;\n"
                                                                    "}"
                                                                    "QPushButton:enabled{\n"
                                                                    "background-color: rgb(49, "
                                                                    "77, 162); }\n"
                                                                    )
                    self.relay_details_save_frame_btn.setObjectName("relay_details_update_btn")

                    self.relay_simulate_btn = QtWidgets.QPushButton(self.relay_details_groupbox)
                    self.relay_simulate_btn.setText('Reference ROI')
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_simulate_btn.setFont(font)
                    self.relay_simulate_btn.setGeometry(QtCore.QRect(30, 450, 80, 30))
                    self.relay_simulate_btn.setStyleSheet("QPushButton{\n"
                                                          "background-color:rgb(49, 77, 162);\n"
                                                          "color:rgb(255, 255, 255);\n"
                                                          "border-radius: 10px;\n"
                                                          "}"
                                                          "QPushButton:Pressed{\n"
                                                          "border: 3px solid;\n"
                                                          "}"
                                                          )
                    self.relay_simulate_btn.setObjectName('relay_simulate_btn')

                    self.relay_update_btn = QtWidgets.QPushButton(self.relay_details_groupbox)
                    self.relay_update_btn.setText('Update')
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_update_btn.setFont(font)
                    self.relay_update_btn.setGeometry(QtCore.QRect(150, 450, 80, 30))
                    self.relay_update_btn.setStyleSheet("QPushButton{\n"
                                                        "background-color:rgb(49, 77, 162);\n"
                                                        "color:rgb(255, 255, 255);\n"
                                                        "border-radius: 10px;\n"
                                                        "}"
                                                        "QPushButton:Pressed{\n"
                                                        "background-color: #1a5276;\n"
                                                        "}"
                                                        )
                    self.relay_update_btn.setObjectName('relay_update_btn')

                    self.relay_chart_check_btn = QtWidgets.QPushButton(self.relay_details_groupbox)
                    self.relay_chart_check_btn.setText('Chart check')
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.relay_chart_check_btn.setFont(font)
                    self.relay_chart_check_btn.setGeometry(QtCore.QRect(270, 450, 80, 30))
                    self.relay_chart_check_btn.setStyleSheet("QPushButton{\n"
                                                             "background-color:rgb(49, 77, 162);\n"
                                                             "color:rgb(255, 255, 255);\n"
                                                             "border-radius: 10px;\n"
                                                             "}"
                                                             "QPushButton:Pressed{\n"
                                                             "border: 3px solid;\n"
                                                             "}"
                                                             )
                    self.relay_chart_check_btn.setObjectName('relay_chart_check_btn')

                    self.inr_radius_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.inr_radius_lbl.setGeometry(QtCore.QRect(10, 380, 120, 35))
                    self.inr_radius_lbl.setText('Inr Radius')
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.inr_radius_lbl.setFont(font)
                    self.inr_radius_lbl.setObjectName('inr_radius_lbl')

                    self.inr_radius_txtbox = QtWidgets.QLineEdit(self.relay_details_groupbox)
                    self.inr_radius_txtbox.setGeometry(QtCore.QRect(110, 380, 150, 30))
                    regx = QRegExp(r"^(0?\.[0-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8]"
                                   r"[0-9]\.[0-9][0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9]"
                                   r"[0-9]*|99\.[0-9][0-9]*|[2-8][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9]\.[0-9]"
                                   r"[0-9]*|10[1-9]\.[0-9][0-9]*|100\.[0-9][0-9]*|9[0-8][0-9]\.[0-9]"
                                   r"[0-9]*|99[0-8]\.[0-9][0-9]*|999\.[0-9][0-9]*|[2-3][0-9][0-9][0-9]\.[0-9]"
                                   r"[0-9]*|1[1-9][0-9][0-9]\.[0-9][0-9]*|10[1-9][0-9]\.[0-9][0-9]*|100[1-9]\.[0-9]"
                                   r"[0-9]*|1000\.[0-9][0-9]*|4000\.[0-0][0-9]*)$")
                    inr_radius_txtbox = QRegExpValidator(regx, self.inr_radius_txtbox)
                    self.inr_radius_txtbox.setValidator(inr_radius_txtbox)
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.inr_radius_txtbox.setFont(font)
                    self.inr_radius_txtbox.setObjectName('inr_radius_txtbox')
                    self.inr_radius_lbl.hide()
                    self.inr_radius_txtbox.hide()

                    self.inr_azimuth_ang_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.inr_azimuth_ang_lbl.setGeometry(QtCore.QRect(10, 440, 120, 35))
                    self.inr_azimuth_ang_lbl.setText('Inr Azimuth Angle')
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.inr_azimuth_ang_lbl.setFont(font)
                    self.inr_azimuth_ang_lbl.setObjectName('inr_Azimuth_lbl')

                    self.inr_azimuth_ang_txtbox = QtWidgets.QLineEdit(self.relay_details_groupbox)
                    self.inr_azimuth_ang_txtbox.setGeometry(QtCore.QRect(110, 440, 150, 30))
                    regx = QRegExp(r"^(0?\.[1-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8]"
                                   r"[0-9]\.[0-9][0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9]"
                                   r"[0-9]*|99\.[0-9][0-9]*|100\.0[0-9]*)$")
                    inr_azimuth_ang_txtbox = QRegExpValidator(regx, self.inr_azimuth_ang_txtbox)
                    self.inr_azimuth_ang_txtbox.setValidator(inr_azimuth_ang_txtbox)
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    self.inr_azimuth_ang_txtbox.setFont(font)
                    self.inr_azimuth_ang_txtbox.setObjectName('inr_azimuth_txtbox')
                    self.inr_azimuth_ang_lbl.hide()
                    self.inr_azimuth_ang_txtbox.hide()

                    self.deep_inr_radius_lbl = QtWidgets.QLabel(self.relay_details_groupbox)
                    self.deep_inr_radius_lbl.setGeometry(QtCore.QRect(10, 500, 120, 35))
                    self.deep_inr_radius_lbl.setText('Deep Inr Radius')
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.deep_inr_radius_lbl.setFont(font)
                    self.deep_inr_radius_lbl.setObjectName('deep_inr_radius_lbl')

                    self.deep_inr_radius_txtbox = QtWidgets.QLineEdit(self.relay_details_groupbox)
                    self.deep_inr_radius_txtbox.setGeometry(QtCore.QRect(110, 500, 150, 30))
                    regx = QRegExp(r"^(0?\.[0-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-8]"
                                   r"[0-9]\.[0-9][0-9]*|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|9[0-8]\.[0-9]"
                                   r"[0-9]*|99\.[0-9][0-9]*|[2-8][0-9][0-9]\.[0-9][0-9]*|1[1-9][0-9]\.[0-9]"
                                   r"[0-9]*|10[1-9]\.[0-9][0-9]*|100\.[0-9][0-9]*|9[0-8][0-9]\.[0-9]"
                                   r"[0-9]*|99[0-8]\.[0-9][0-9]*|999\.[0-9][0-9]*|[2-3][0-9][0-9][0-9]\.[0-9]"
                                   r"[0-9]*|1[1-9][0-9][0-9]\.[0-9][0-9]*|10[1-9][0-9]\.[0-9][0-9]*|100[1-9]\.[0-9]"
                                   r"[0-9]*|1000\.[0-9][0-9]*|4000\.[0-0][0-9]*)$")
                    deep_inr_radius_txtbox = QRegExpValidator(regx, self.deep_inr_radius_txtbox)
                    self.deep_inr_radius_txtbox.setValidator(deep_inr_radius_txtbox)
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.deep_inr_radius_txtbox.setFont(font)
                    self.deep_inr_radius_txtbox.setObjectName('inr_radius_txtbox')
                    self.inr_azimuth_ang_lbl.hide()
                    self.inr_azimuth_ang_txtbox.hide()
                    self.deep_inr_radius_txtbox.hide()
                    self.deep_inr_radius_lbl.hide()
                    self.verticalLayout_5.addWidget(self.relay_details_groupbox)
                    self.relay_scrollarea.setWidget(self.scrollAreaWidgetContents_5)
                    self.stackedWidget.addWidget(self.station_4_layout)

                    self.station_5_layout = QtWidgets.QWidget()
                    self.station_5_layout.setObjectName("station_5_layout")
                    self.gluing_scrollarea = QtWidgets.QScrollArea(self.station_5_layout)
                    self.gluing_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.gluing_scrollarea.setGeometry(QtCore.QRect(0, 0, 420, 900))
                    self.gluing_scrollarea.setWidgetResizable(True)
                    self.gluing_scrollarea.setObjectName("gluing_scrollarea")
                    self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
                    self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 418, 898))
                    self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
                    self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
                    self.verticalLayout_6.setObjectName("verticalLayout_6")

                    self.gluing_enable_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.gluing_enable_groupbox.sizePolicy().hasHeightForWidth())
                    self.gluing_enable_groupbox.setSizePolicy(sizePolicy)
                    self.gluing_enable_groupbox.setMinimumSize(QtCore.QSize(0, 100))
                    self.gluing_enable_groupbox.setStyleSheet("border:0px")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.gluing_enable_groupbox.setFont(font)
                    self.gluing_enable_groupbox.setObjectName("gluing_enable_groupbox")
                    self.gluing_enable_lbl = QLabel(self.gluing_enable_groupbox)
                    self.gluing_enable_lbl.setGeometry(QtCore.QRect(80, 15, 150, 15))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.gluing_enable_lbl.setFont(font)
                    self.gluing_enable_lbl.setText('Station Enable')
                    self.gluing_enable_lbl.setObjectName("gluing_enable_lbl")
                    self.gluing_toggle = Toggle(self.gluing_enable_groupbox)
                    self.gluing_toggle.setChecked(True)
                    self.gluing_toggle.setGeometry(QtCore.QRect(210, 7, 70, 35))
                    self.gluing_toggle.setObjectName("gluing_toggle")
                    self.verticalLayout_6.addWidget(self.gluing_enable_groupbox)

                    self.gluing_cntrl_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.gluing_cntrl_groupbox.sizePolicy().hasHeightForWidth())
                    self.gluing_cntrl_groupbox.setSizePolicy(sizePolicy)
                    self.gluing_cntrl_groupbox.setMinimumSize(QtCore.QSize(0, 220))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_cntrl_groupbox.setFont(font)
                    self.gluing_cntrl_groupbox.setStyleSheet("Background-color:RGB(240, 240, 240)")
                    self.gluing_cntrl_groupbox.setObjectName("gluing_cntrl_groupbox")

                    self.gluing_type_cmb = combobox(self.gluing_cntrl_groupbox)
                    self.gluing_type_cmb.setGeometry(QtCore.QRect(100, 30, 130, 30))
                    self.gluing_type_cmb.addItem("Dry run")
                    self.gluing_type_cmb.addItem("Spot glue")
                    self.gluing_type_cmb.addItem("Continuous glue")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_type_cmb.setFont(font)
                    self.gluing_type_cmb.setObjectName("gluing_type_cmb")
                    self.gluing_type_lbl = QtWidgets.QLabel(self.gluing_cntrl_groupbox)
                    self.gluing_type_lbl.setGeometry(QtCore.QRect(10, 25, 80, 35))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.gluing_type_lbl.sizePolicy().hasHeightForWidth())
                    self.gluing_type_lbl.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_type_lbl.setFont(font)
                    self.gluing_type_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
                    self.gluing_type_lbl.setObjectName("gluing_type_lbl")

                    self.gluing_on_delay_Continuous_lbl = QtWidgets.QLabel(self.gluing_cntrl_groupbox)
                    self.gluing_on_delay_Continuous_lbl.setGeometry(QtCore.QRect(10, 20, 80, 15))
                    self.gluing_on_delay_Continuous_lbl.setText("On delay time")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_on_delay_Continuous_lbl.setFont(font)
                    self.gluing_on_delay_Continuous_lbl.setObjectName("gluing_on_delay_Continuous_lbl")
                    self.gluing_on_delay_Continuous_lndt = QtWidgets.QLineEdit(self.gluing_cntrl_groupbox)
                    self.gluing_on_delay_Continuous_lndt.setGeometry(QtCore.QRect(100, 95, 130, 30))
                    self.gluing_on_delay_Continuous_lndt.setAlignment(Qt.AlignCenter)
                    regx = QRegExp(r"^(0?\.[1-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|10\.0[0-9]*)$")
                    gluing_on_delay_Continuous_lndt = QRegExpValidator(regx, self.gluing_on_delay_Continuous_lndt)
                    self.gluing_on_delay_Continuous_lndt.setValidator(gluing_on_delay_Continuous_lndt)
                    self.gluing_on_delay_Continuous_lndt.setObjectName("gluing_on_delay_Continuous_lndt")

                    self.gluing_off_delay_Continuous_lbl = QtWidgets.QLabel(self.gluing_cntrl_groupbox)
                    self.gluing_off_delay_Continuous_lbl.setGeometry(QtCore.QRect(10, 155, 80, 15))
                    self.gluing_off_delay_Continuous_lbl.setText("Off delay time")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_off_delay_Continuous_lbl.setFont(font)
                    self.gluing_off_delay_Continuous_lbl.setObjectName("gluing_off_delay_Continuous_lbl")
                    self.gluing_off_delay_Continuous_lndt = QtWidgets.QLineEdit(self.gluing_cntrl_groupbox)
                    self.gluing_off_delay_Continuous_lndt.setGeometry(QtCore.QRect(100, 150, 130, 30))
                    self.gluing_off_delay_Continuous_lndt.setAlignment(Qt.AlignCenter)
                    regx = QRegExp(r"^(0?\.[1-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|10\.0[0-9]*)$")
                    gluing_off_delay_Continuous_lndt = QRegExpValidator(regx, self.gluing_off_delay_Continuous_lndt)
                    self.gluing_off_delay_Continuous_lndt.setValidator(gluing_off_delay_Continuous_lndt)
                    self.gluing_off_delay_Continuous_lndt.setObjectName("gluing_off_delay_Continuous_lndt")

                    self.gluing_on_delay_Continuous_lbl.hide()
                    self.gluing_on_delay_Continuous_lndt.hide()
                    self.gluing_off_delay_Continuous_lbl.hide()
                    self.gluing_off_delay_Continuous_lndt.hide()

                    self.gluing_detail_speed_lbl = QtWidgets.QLabel(self.gluing_cntrl_groupbox)
                    self.gluing_detail_speed_lbl.setGeometry(QtCore.QRect(10, 95, 80, 15))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_detail_speed_lbl.setFont(font)
                    self.gluing_detail_speed_lbl.setObjectName("gluing_detail_speed_lbl")
                    self.gluing_detail_speed_lndt = QtWidgets.QLineEdit(self.gluing_cntrl_groupbox)
                    self.gluing_detail_speed_lndt.setGeometry(QtCore.QRect(100, 90, 130, 30))
                    self.gluing_detail_speed_lndt.setAlignment(Qt.AlignCenter)
                    regx = QRegExp(r"^([0-9]|[2-8][0-9]|1[0-9]|9[0-9]|[2-8][0-9][0-9]|1[1-9][0-9]|10[0-9]|9[0-8][ "
                                   r"0-9]|99[0-9]|1000)$")
                    gluing_detail_speed_lndt = QRegExpValidator(regx, self.gluing_detail_speed_lndt)
                    self.gluing_detail_speed_lndt.setValidator(gluing_detail_speed_lndt)
                    self.gluing_detail_speed_lndt.setObjectName("gluing_detail_speed_lndt")

                    self.gluing_detail_diameter_lbl = QtWidgets.QLabel(self.gluing_cntrl_groupbox)
                    self.gluing_detail_diameter_lbl.setGeometry(QtCore.QRect(10, 155, 80, 15))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_detail_diameter_lbl.setFont(font)
                    self.gluing_detail_diameter_lbl.setObjectName("gluing_detail_diameter_lbl")
                    self.gluing_detail_diameter_lndt = QtWidgets.QLineEdit(self.gluing_cntrl_groupbox)
                    self.gluing_detail_diameter_lndt.setGeometry(QtCore.QRect(100, 150, 130, 30))
                    self.gluing_detail_diameter_lndt.setAlignment(Qt.AlignCenter)
                    regx = QRegExp(r"^([2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|[2-2][0-9]\.[0-9][0-9]*"
                                   r"|1[1-9]\.[0-9][0-9]*|10\.[0-9][0-9]*|30\.[0-0][0-9]*)$")
                    gluing_detail_diameter_lndt = QRegExpValidator(regx, self.gluing_detail_diameter_lndt)
                    self.gluing_detail_diameter_lndt.setValidator(gluing_detail_diameter_lndt)
                    self.gluing_detail_diameter_lndt.setObjectName("gluing_detail_diameter_lndt")

                    self.gluing_cntrl_gluing_btn = QtWidgets.QPushButton(self.gluing_cntrl_groupbox)
                    self.gluing_cntrl_gluing_btn.setGeometry(QtCore.QRect(260, 145, 80, 40))
                    self.gluing_cntrl_gluing_btn.setAccessibleName("Gluing apply btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_cntrl_gluing_btn.setFont(font)
                    self.gluing_cntrl_gluing_btn.setStyleSheet("QPushButton{\n"
                                                               "background-color:rgb(49, 77, 162);\n"
                                                               "color:rgb(255, 255, 255);\n"
                                                               "border-radius: 10px;\n"
                                                               "}"
                                                               "QPushButton:Pressed{\n"
                                                               "border: 3px solid;\n"
                                                               "}"
                                                               )
                    self.gluing_cntrl_gluing_btn.setText("Dry run")
                    self.gluing_cntrl_gluing_btn.setIconSize(QtCore.QSize(40, 40))
                    self.gluing_cntrl_gluing_btn.setObjectName("gluing_cntrl_gluing_btn")

                    self.gluing_cntrl_homing_btn = QtWidgets.QPushButton(self.gluing_cntrl_groupbox)
                    self.gluing_cntrl_homing_btn.setGeometry(QtCore.QRect(260, 85, 80, 40))
                    self.gluing_cntrl_homing_btn.setAccessibleName("Gluing init btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_cntrl_homing_btn.setFont(font)
                    self.gluing_cntrl_homing_btn.setStyleSheet("QPushButton{\n"
                                                               "background-color:rgb(49, 77, 162);\n"
                                                               "color:rgb(255, 255, 255);\n"
                                                               "border-radius: 10px;\n"
                                                               "}"
                                                               "QPushButton:Pressed{\n"
                                                               "border: 3px solid;\n"
                                                               "}"
                                                               )
                    self.gluing_cntrl_homing_btn.setText("Homing")
                    self.gluing_cntrl_homing_btn.setIconSize(QtCore.QSize(40, 40))
                    self.gluing_cntrl_homing_btn.setObjectName("gluing_cntrl_homing_btn")

                    self.gluing_dispenser_type_cmb = combobox(self.gluing_cntrl_groupbox)
                    self.gluing_dispenser_type_cmb.setGeometry(QtCore.QRect(135, 520, 140, 30))
                    self.gluing_dispenser_type_cmb.addItem("1st Dispenser")
                    self.gluing_dispenser_type_cmb.addItem("2nd Dispenser")
                    self.gluing_dispenser_type_cmb.addItem("Both Dispenser")
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.gluing_dispenser_type_cmb.setFont(font)
                    self.gluing_dispenser_type_cmb.setObjectName("gluing_dispenser_type_cmb")
                    self.gluing_dispenser_type_lbl = QtWidgets.QLabel(self.gluing_cntrl_groupbox)
                    self.gluing_dispenser_type_lbl.setGeometry(QtCore.QRect(10, 515, 110, 35))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.gluing_dispenser_type_lbl.sizePolicy().hasHeightForWidth())
                    self.gluing_dispenser_type_lbl.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_dispenser_type_lbl.setFont(font)
                    self.gluing_dispenser_type_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
                    self.gluing_dispenser_type_lbl.setObjectName("gluing_dispenser_type_lbl")

                    self.gluing_dispenser_timer_lbl = QtWidgets.QLabel(self.gluing_cntrl_groupbox)
                    self.gluing_dispenser_timer_lbl.setGeometry(QtCore.QRect(10, 580, 75, 15))
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_dispenser_timer_lbl.setFont(font)
                    self.gluing_dispenser_timer_lbl.setObjectName("gluing_dispenser_timer_lbl")
                    self.gluing_dispenser_timer_lndt = QtWidgets.QLineEdit(self.gluing_cntrl_groupbox)
                    self.gluing_dispenser_timer_lndt.setGeometry(QtCore.QRect(130, 575, 140, 30))
                    self.gluing_dispenser_timer_lndt.setAlignment(Qt.AlignCenter)
                    regx = QRegExp(r"^(0?\.[0-9][0-9]*|[2-8]\.[0-9][0-9]*|1\.[0-9][0-9]*|9\.[0-9][0-9]*|10\.0[0-9]*)$")
                    gluing_dispenser_timer_lndt = QRegExpValidator(regx, self.gluing_dispenser_timer_lndt)
                    self.gluing_dispenser_timer_lndt.setValidator(gluing_dispenser_timer_lndt)
                    self.gluing_dispenser_timer_lndt.setObjectName("gluing_dispenser_timer_lndt")

                    self.gluing_dispenser_apply_btn = QtWidgets.QPushButton(self.gluing_cntrl_groupbox)
                    self.gluing_dispenser_apply_btn.setGeometry(QtCore.QRect(280, 572, 90, 35))
                    self.gluing_dispenser_apply_btn.setAccessibleName("gluing_dispenser_apply_btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_dispenser_apply_btn.setFont(font)
                    self.gluing_dispenser_apply_btn.setText("Apply Glue")
                    self.gluing_dispenser_apply_btn.setStyleSheet("QPushButton{\n"
                                                                  "background-color:rgb(49, 77, 162);\n"
                                                                  "color:rgb(255, 255, 255);\n"
                                                                  "border-radius: 10px;\n"
                                                                  "}"
                                                                  "QPushButton:Pressed{\n"
                                                                  "border: 3px solid;\n"
                                                                  "}"
                                                                  )
                    self.gluing_dispenser_apply_btn.setObjectName("gluing_dispenser_apply_btn")

                    self.gluing_dispenser_off_btn = QtWidgets.QPushButton(self.gluing_cntrl_groupbox)
                    self.gluing_dispenser_off_btn.setGeometry(QtCore.QRect(280, 520, 90, 35))
                    self.gluing_dispenser_off_btn.setAccessibleName("gluing_dispenser_off_btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_dispenser_off_btn.setFont(font)
                    self.gluing_dispenser_off_btn.setText("Glue off")
                    self.gluing_dispenser_off_btn.setStyleSheet("QPushButton{\n"
                                                                "background-color:rgb(49, 77, 162);\n"
                                                                "color:rgb(255, 255, 255);\n"
                                                                "border-radius: 10px;\n"
                                                                "}"
                                                                "QPushButton:Pressed{\n"
                                                                "border: 3px solid;\n"
                                                                "}"
                                                                )
                    self.gluing_dispenser_off_btn.setObjectName("gluing_dispenser_off_btn")
                    self.gluing_dispenser_type_lbl.hide()
                    self.gluing_dispenser_type_cmb.hide()
                    self.gluing_dispenser_timer_lbl.hide()
                    self.gluing_dispenser_timer_lndt.hide()
                    self.gluing_dispenser_apply_btn.hide()
                    self.gluing_dispenser_off_btn.hide()
                    self.verticalLayout_6.addWidget(self.gluing_cntrl_groupbox)

                    self.gluing_x_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.gluing_x_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.gluing_x_axis_groupbox.setSizePolicy(sizePolicy)
                    self.gluing_x_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.gluing_x_axis_groupbox.setFont(font)
                    self.gluing_x_axis_groupbox.setObjectName("gluing_x_axis_groupbox")

                    self.gluing_x_axis_mini_lbl = QtWidgets.QLabel(self.gluing_x_axis_groupbox)
                    self.gluing_x_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.gluing_x_axis_mini_lbl.setFont(font)
                    self.gluing_x_axis_mini_lbl.setObjectName("gluing_x_axis_mini_lbl")
                    self.gluing_x_axis_mini_lndt = QtWidgets.QLineEdit(self.gluing_x_axis_groupbox)
                    self.gluing_x_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(\d|[1-9]\d)(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.gluing_x_axis_mini_lndt)
                    self.gluing_x_axis_mini_lndt.setValidator(validator)
                    self.gluing_x_axis_mini_lndt.setObjectName("gluing_x_axis_mini_lndt")

                    self.gluing_x_axis_speed_lbl = QtWidgets.QLabel(self.gluing_x_axis_groupbox)
                    self.gluing_x_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.gluing_x_axis_speed_lbl.setFont(font)
                    self.gluing_x_axis_speed_lbl.setText("Speed")
                    self.gluing_x_axis_speed_lbl.setObjectName("gluing_x_axis_speed_lbl")
                    self.gluing_x_axis_speed_lndt = QtWidgets.QLineEdit(self.gluing_x_axis_groupbox)
                    self.gluing_x_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 5000, self.gluing_x_axis_speed_lndt)
                    self.gluing_x_axis_speed_lndt.setValidator(validator)
                    self.gluing_x_axis_speed_lndt.setToolTip("The X-Actuator speed is limited to a range of 0 to 2000")
                    self.gluing_x_axis_speed_lndt.setObjectName("gluing_x_axis_speed_lndt")

                    self.gluing_x_axis_current_position_lbl = QtWidgets.QLabel(self.gluing_x_axis_groupbox)
                    self.gluing_x_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.gluing_x_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_x_axis_current_position_lbl.setFont(font)
                    self.gluing_x_axis_current_position_lbl.setObjectName("gluing_x_axis_current_position_lbl")
                    self.gluing_x_axis_current_position_value = QtWidgets.QLabel(self.gluing_x_axis_groupbox)
                    self.gluing_x_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.gluing_x_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_x_axis_current_position_value.setFont(font)
                    self.gluing_x_axis_current_position_value.setObjectName("gluing_x_axis_current_position_value")

                    self.gluing_x_axis_run_btn = QtWidgets.QPushButton(self.gluing_x_axis_groupbox)
                    self.gluing_x_axis_run_btn.setAccessibleName('gluing_x_axis_run_btn')
                    self.gluing_x_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_x_axis_run_btn.setFont(font)
                    self.gluing_x_axis_run_btn.setText("Run")
                    self.gluing_x_axis_run_btn.setFlat(True)
                    self.gluing_x_axis_run_btn.setFont(font)
                    self.gluing_x_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                             "background-color:rgb(49, 77, 162);\n"
                                                             "color:rgb(255, 255, 255);\n"
                                                             "border-radius: 10px;\n"
                                                             "}"
                                                             "QPushButton:Pressed{\n"
                                                             "border: 3px solid;\n"
                                                             "}"
                                                             )
                    self.gluing_x_axis_run_btn.setObjectName("gluing_x_axis_run_btn")
                    self.verticalLayout_6.addWidget(self.gluing_x_axis_groupbox)

                    self.gluing_y_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.gluing_y_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.gluing_y_axis_groupbox.setSizePolicy(sizePolicy)
                    self.gluing_y_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.gluing_y_axis_groupbox.setFont(font)
                    self.gluing_y_axis_groupbox.setObjectName("gluing_y_axis_groupbox")

                    self.gluing_y_axis_mini_lbl = QtWidgets.QLabel(self.gluing_y_axis_groupbox)
                    self.gluing_y_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.gluing_y_axis_mini_lbl.setFont(font)
                    self.gluing_y_axis_mini_lbl.setObjectName("gluing_y_axis_mini_lbl")
                    self.gluing_y_axis_mini_lndt = QtWidgets.QLineEdit(self.gluing_y_axis_groupbox)
                    self.gluing_y_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.gluing_y_axis_mini_lndt)
                    self.gluing_y_axis_mini_lndt.setValidator(validator)
                    self.gluing_y_axis_mini_lndt.setObjectName("gluing_y_axis_mini_lndt")

                    self.gluing_y_axis_speed_lbl = QtWidgets.QLabel(self.gluing_y_axis_groupbox)
                    self.gluing_y_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.gluing_y_axis_speed_lbl.setFont(font)
                    self.gluing_y_axis_speed_lbl.setText("Speed")
                    self.gluing_y_axis_speed_lbl.setObjectName("gluing_y_axis_speed_lbl")
                    self.gluing_y_axis_speed_lndt = QtWidgets.QLineEdit(self.gluing_y_axis_groupbox)
                    self.gluing_y_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 15000, self.gluing_y_axis_speed_lndt)
                    self.gluing_y_axis_speed_lndt.setValidator(validator)
                    self.gluing_y_axis_speed_lndt.setToolTip("The Y-Actuator speed is limited to a range of 0 to 15000")
                    self.gluing_y_axis_speed_lndt.setObjectName("gluing_y_axis_speed_lndt")

                    self.gluing_y_axis_current_position_lbl = QtWidgets.QLabel(self.gluing_y_axis_groupbox)
                    self.gluing_y_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.gluing_y_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_y_axis_current_position_lbl.setFont(font)
                    self.gluing_y_axis_current_position_lbl.setObjectName("gluing_y_axis_current_position_lbl")
                    self.gluing_y_axis_current_position_value = QtWidgets.QLabel(self.gluing_y_axis_groupbox)
                    self.gluing_y_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.gluing_y_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_y_axis_current_position_value.setFont(font)
                    self.gluing_y_axis_current_position_value.setObjectName("gluing_y_axis_current_position_value")

                    self.gluing_y_axis_run_btn = QtWidgets.QPushButton(self.gluing_y_axis_groupbox)
                    self.gluing_y_axis_run_btn.setAccessibleName('gluing_y_axis_run_btn')
                    self.gluing_y_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_y_axis_run_btn.setFont(font)
                    self.gluing_y_axis_run_btn.setText("Run")
                    self.gluing_y_axis_run_btn.setFlat(True)
                    self.gluing_y_axis_run_btn.setFont(font)
                    self.gluing_y_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                             "background-color:rgb(49, 77, 162);\n"
                                                             "color:rgb(255, 255, 255);\n"
                                                             "border-radius: 10px;\n"
                                                             "}"
                                                             "QPushButton:Pressed{\n"
                                                             "border: 3px solid;\n"
                                                             "}"
                                                             )
                    self.gluing_y_axis_run_btn.setObjectName("gluing_y_axis_run_btn")
                    self.verticalLayout_6.addWidget(self.gluing_y_axis_groupbox)

                    self.gluing_z_gluing_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.gluing_z_gluing_groupbox.sizePolicy().hasHeightForWidth())
                    self.gluing_z_gluing_groupbox.setSizePolicy(sizePolicy)
                    self.gluing_z_gluing_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.gluing_z_gluing_groupbox.setFont(font)
                    self.gluing_z_gluing_groupbox.setObjectName("gluing_z_gluing_groupbox")

                    self.gluing_z_axis_mini_lbl = QtWidgets.QLabel(self.gluing_z_gluing_groupbox)
                    self.gluing_z_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.gluing_z_axis_mini_lbl.setFont(font)
                    self.gluing_z_axis_mini_lbl.setObjectName("2loading_z_axis_mini_lbl")
                    self.gluing_z_axis_mini_lndt = QtWidgets.QLineEdit(self.gluing_z_gluing_groupbox)
                    self.gluing_z_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.gluing_z_axis_mini_lndt)
                    self.gluing_z_axis_mini_lndt.setValidator(validator)
                    self.gluing_z_axis_mini_lndt.setObjectName("gluing_z_axis_mini_lndt")

                    self.gluing_z_axis_speed_lbl = QtWidgets.QLabel(self.gluing_z_gluing_groupbox)
                    self.gluing_z_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.gluing_z_axis_speed_lbl.setFont(font)
                    self.gluing_z_axis_speed_lbl.setText("Speed")
                    self.gluing_z_axis_speed_lbl.setObjectName("gluing_z_axis_speed_lbl")
                    self.gluing_z_axis_speed_lndt = QtWidgets.QLineEdit(self.gluing_z_gluing_groupbox)
                    self.gluing_z_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 5000, self.gluing_z_axis_speed_lndt)
                    self.gluing_z_axis_speed_lndt.setValidator(validator)
                    self.gluing_z_axis_speed_lndt.setToolTip("The Z-Actuator speed is limited to a range of 0 to 2000")
                    self.gluing_z_axis_speed_lndt.setObjectName("gluing_z_axis_speed_lndt")

                    self.gluing_z_axis_current_position_lbl = QtWidgets.QLabel(self.gluing_z_gluing_groupbox)
                    self.gluing_z_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.gluing_z_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_z_axis_current_position_lbl.setFont(font)
                    self.gluing_z_axis_current_position_lbl.setObjectName("gluing_z_axis_current_position_lbl")
                    self.gluing_z_axis_current_position_value = QtWidgets.QLabel(self.gluing_z_gluing_groupbox)
                    self.gluing_z_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.gluing_z_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_z_axis_current_position_value.setFont(font)
                    self.gluing_z_axis_current_position_value.setObjectName("gluing_z_axis_current_position_value")

                    self.gluing_z_axis_run_btn = QtWidgets.QPushButton(self.gluing_z_gluing_groupbox)
                    self.gluing_z_axis_run_btn.setAccessibleName('gluing_z_axis_run_btn')
                    self.gluing_z_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_z_axis_run_btn.setFont(font)
                    self.gluing_z_axis_run_btn.setText("RUN")
                    self.gluing_z_axis_run_btn.setFlat(True)
                    self.gluing_z_axis_run_btn.setFont(font)
                    self.gluing_z_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                             "background-color:rgb(49, 77, 162);\n"
                                                             "color:rgb(255, 255, 255);\n"
                                                             "border-radius: 10px;\n"
                                                             "}"
                                                             "QPushButton:Pressed{\n"
                                                             "border: 3px solid;\n"
                                                             "}"
                                                             )
                    self.gluing_z_axis_run_btn.setObjectName("gluing_z_axis_run_btn")

                    self.gluing_z_gluing_homing_btn = QtWidgets.QPushButton(self.gluing_z_gluing_groupbox)
                    self.gluing_z_gluing_homing_btn.setGeometry(QtCore.QRect(250, 100, 90, 40))
                    self.gluing_z_gluing_homing_btn.setAccessibleName("gluing z_axis homing btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_z_gluing_homing_btn.setFont(font)
                    self.gluing_z_gluing_homing_btn.setText("Homing")
                    self.gluing_z_gluing_homing_btn.setStyleSheet("QPushButton{\n"
                                                                  "background-color:rgb(49, 77, 162);\n"
                                                                  "color:rgb(255, 255, 255);\n"
                                                                  "border-radius: 10px;\n"
                                                                  "}"
                                                                  "QPushButton:Pressed{\n"
                                                                  "border: 3px solid;\n"
                                                                  "}"
                                                                  )
                    self.gluing_z_gluing_homing_btn.setObjectName("gluing_z_gluing_homing_btn")
                    self.verticalLayout_6.addWidget(self.gluing_z_gluing_groupbox)
                    self.gluing_scrollarea.setWidget(self.scrollAreaWidgetContents_6)

                    self.gluing_teaching_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_6)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.gluing_teaching_groupbox.sizePolicy().hasHeightForWidth())
                    self.gluing_teaching_groupbox.setSizePolicy(sizePolicy)
                    self.gluing_teaching_groupbox.setMinimumSize(QtCore.QSize(0, 460))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.gluing_teaching_groupbox.setFont(font)
                    self.gluing_teaching_groupbox.setObjectName("gluing_teaching_groupbox")

                    self.gluing_teaching_x1_mini_lbl = QtWidgets.QLabel(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x1_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.gluing_teaching_x1_mini_lbl.setFont(font)
                    self.gluing_teaching_x1_mini_lbl.setObjectName("gluing_teaching_x1_mini_lbl")
                    self.gluing_teaching_x1_mini_lndt = QtWidgets.QLineEdit(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x1_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^\d{1,2}(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.gluing_teaching_x1_mini_lndt)
                    self.gluing_teaching_x1_mini_lndt.setValidator(validator)
                    self.gluing_teaching_x1_mini_lndt.setObjectName("gluing_teaching_x1_mini_lndt")

                    self.gluing_teaching_x1_current_position_lbl = QtWidgets.QLabel(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x1_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.gluing_teaching_x1_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_teaching_x1_current_position_lbl.setFont(font)
                    self.gluing_teaching_x1_current_position_lbl.setObjectName(
                        "gluing_teaching_x1_current_position_lbl")
                    self.gluing_teaching_x1_current_position_value = QtWidgets.QLabel(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x1_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.gluing_teaching_x1_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_teaching_x1_current_position_value.setFont(font)
                    self.gluing_teaching_x1_current_position_value.setObjectName(
                        "gluing_teaching_x1_current_position_value")

                    self.gluing_teaching_x1_run_btn = QtWidgets.QPushButton(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x1_run_btn.setAccessibleName('gluing_teaching_x1_run_btn')
                    self.gluing_teaching_x1_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_teaching_x1_run_btn.setFont(font)
                    self.gluing_teaching_x1_run_btn.setText("RUN")
                    self.gluing_teaching_x1_run_btn.setFlat(True)
                    self.gluing_teaching_x1_run_btn.setFont(font)
                    self.gluing_teaching_x1_run_btn.setStyleSheet("QPushButton{\n"
                                                                  "background-color:rgb(49, 77, 162);\n"
                                                                  "color:rgb(255, 255, 255);\n"
                                                                  "border-radius: 10px;\n"
                                                                  "}"
                                                                  "QPushButton:Pressed{\n"
                                                                  "border: 3px solid;\n"
                                                                  "}"
                                                                  )
                    self.gluing_teaching_x1_run_btn.setObjectName("gluing_teaching_x1_run_btn")

                    self.gluing_teaching_x2_mini_lbl = QtWidgets.QLabel(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x2_mini_lbl.setGeometry(QtCore.QRect(10, 170, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.gluing_teaching_x2_mini_lbl.setFont(font)
                    self.gluing_teaching_x2_mini_lbl.setObjectName("gluing_teaching_x2_mini_lbl")
                    self.gluing_teaching_x2_mini_lndt = QtWidgets.QLineEdit(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x2_mini_lndt.setGeometry(QtCore.QRect(10, 190, 70, 30))
                    regx = QRegExp(r'^\d{1,2}(\.\d{1,2})?$')
                    validator = QRegExpValidator(regx, self.gluing_teaching_x2_mini_lndt)
                    self.gluing_teaching_x2_mini_lndt.setValidator(validator)
                    self.gluing_teaching_x2_mini_lndt.setObjectName("gluing_teaching_x2_mini_lndt")

                    self.gluing_teaching_x2_current_position_lbl = QtWidgets.QLabel(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x2_current_position_lbl.setGeometry(QtCore.QRect(200, 200, 150, 15))
                    self.gluing_teaching_x2_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_teaching_x2_current_position_lbl.setFont(font)
                    self.gluing_teaching_x2_current_position_lbl.setObjectName(
                        "gluing_teaching_x2_current_position_lbl")
                    self.gluing_teaching_x2_current_position_value = QtWidgets.QLabel(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x2_current_position_value.setGeometry(QtCore.QRect(320, 200, 50, 15))
                    self.gluing_teaching_x2_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.gluing_teaching_x2_current_position_value.setFont(font)
                    self.gluing_teaching_x2_current_position_value.setObjectName(
                        "gluing_teaching_x2_current_position_value")

                    self.gluing_teaching_x2_run_btn = QtWidgets.QPushButton(self.gluing_teaching_groupbox)
                    self.gluing_teaching_x2_run_btn.setAccessibleName('gluing_teaching_x2_run_btn')
                    self.gluing_teaching_x2_run_btn.setGeometry(QtCore.QRect(30, 240, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_teaching_x2_run_btn.setFont(font)
                    self.gluing_teaching_x2_run_btn.setText("RUN")
                    self.gluing_teaching_x2_run_btn.setFlat(True)
                    self.gluing_teaching_x2_run_btn.setFont(font)
                    self.gluing_teaching_x2_run_btn.setStyleSheet("QPushButton{\n"
                                                                  "background-color:rgb(49, 77, 162);\n"
                                                                  "color:rgb(255, 255, 255);\n"
                                                                  "border-radius: 10px;\n"
                                                                  "}"
                                                                  "QPushButton:Pressed{\n"
                                                                  "border: 3px solid;\n"
                                                                  "}"
                                                                  )
                    self.gluing_teaching_x2_run_btn.setObjectName("gluing_teaching_x2_run_btn")

                    self.gluing_teaching_y_run_btn = QtWidgets.QPushButton(self.gluing_teaching_groupbox)
                    self.gluing_teaching_y_run_btn.setAccessibleName('gluing_teaching_y_run_btn')
                    self.gluing_teaching_y_run_btn.setGeometry(QtCore.QRect(10, 380, 90, 40))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_teaching_y_run_btn.setFont(font)
                    self.gluing_teaching_y_run_btn.setText("Gluing Y")
                    self.gluing_teaching_y_run_btn.setFlat(True)
                    self.gluing_teaching_y_run_btn.setFont(font)
                    self.gluing_teaching_y_run_btn.setStyleSheet("QPushButton{\n"
                                                                 "background-color:rgb(49, 77, 162);\n"
                                                                 "color:rgb(255, 255, 255);\n"
                                                                 "border-radius: 10px;\n"
                                                                 "}"
                                                                 "QPushButton:Pressed{\n"
                                                                 "border: 3px solid;\n"
                                                                 "}"
                                                                 )
                    self.gluing_teaching_y_run_btn.setObjectName("gluing_teaching_y_run_btn")

                    self.gluing_teaching_homing_btn = QtWidgets.QPushButton(self.gluing_teaching_groupbox)
                    self.gluing_teaching_homing_btn.setGeometry(QtCore.QRect(240, 380, 90, 40))
                    self.gluing_teaching_homing_btn.setAccessibleName("gluing_teaching_homing_btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.gluing_teaching_homing_btn.setFont(font)
                    self.gluing_teaching_homing_btn.setText("Homing")
                    self.gluing_teaching_homing_btn.setStyleSheet("QPushButton{\n"
                                                                  "background-color:rgb(49, 77, 162);\n"
                                                                  "color:rgb(255, 255, 255);\n"
                                                                  "border-radius: 10px;\n"
                                                                  "}"
                                                                  "QPushButton:Pressed{\n"
                                                                  "border: 3px solid;\n"
                                                                  "}"
                                                                  )
                    self.gluing_teaching_homing_btn.setObjectName("gluing_teaching_homing_btn")
                    self.verticalLayout_6.addWidget(self.gluing_teaching_groupbox)
                    self.stackedWidget.addWidget(self.station_5_layout)

                    self.station_6_layout = QtWidgets.QWidget()
                    self.station_6_layout.setObjectName("station_6_layout")
                    self.curing_scrollarea = QtWidgets.QScrollArea(self.station_6_layout)
                    self.curing_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.curing_scrollarea.setGeometry(QtCore.QRect(0, 0, 420, 900))
                    self.curing_scrollarea.setWidgetResizable(True)
                    self.curing_scrollarea.setObjectName("curing_scrollarea")
                    self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
                    self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 418, 898))
                    self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
                    self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_7)
                    self.verticalLayout_7.setObjectName("verticalLayout_7")
                    self.curing_enable_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_7)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.curing_enable_groupbox.sizePolicy().hasHeightForWidth())
                    self.curing_enable_groupbox.setSizePolicy(sizePolicy)
                    self.curing_enable_groupbox.setMinimumSize(QtCore.QSize(0, 80))
                    self.curing_enable_groupbox.setStyleSheet("border:0px")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.curing_enable_groupbox.setFont(font)
                    self.curing_enable_groupbox.setObjectName("curing_enable_groupbox")
                    self.curing_enable_lbl = QLabel(self.curing_enable_groupbox)
                    self.curing_enable_lbl.setGeometry(QtCore.QRect(80, 25, 150, 15))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.curing_enable_lbl.setFont(font)
                    self.curing_enable_lbl.setText('Station Enable')
                    self.curing_enable_lbl.setObjectName("curing_enable_lbl")
                    self.curing_toggle = Toggle(self.curing_enable_groupbox)
                    self.curing_toggle.setChecked(True)
                    self.curing_toggle.setGeometry(QtCore.QRect(210, 17, 70, 35))
                    self.verticalLayout_7.addWidget(self.curing_enable_groupbox)

                    self.curing_x_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_7)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.curing_x_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.curing_x_axis_groupbox.setSizePolicy(sizePolicy)
                    self.curing_x_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.curing_x_axis_groupbox.setFont(font)
                    self.curing_x_axis_groupbox.setObjectName("curing_x_axis_groupbox")

                    self.curing_x_axis_mini_lbl = QtWidgets.QLabel(self.curing_x_axis_groupbox)
                    self.curing_x_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.curing_x_axis_mini_lbl.setFont(font)
                    self.curing_x_axis_mini_lbl.setObjectName("curing_x_axis_mini_lbl")
                    self.curing_x_axis_mini_lndt = QtWidgets.QLineEdit(self.curing_x_axis_groupbox)
                    self.curing_x_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.curing_x_axis_mini_lndt)
                    self.curing_x_axis_mini_lndt.setValidator(validator)
                    self.curing_x_axis_mini_lndt.setObjectName("curing_x_axis_mini_lndt")

                    self.curing_x_axis_speed_lbl = QtWidgets.QLabel(self.curing_x_axis_groupbox)
                    self.curing_x_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.curing_x_axis_speed_lbl.setFont(font)
                    self.curing_x_axis_speed_lbl.setText("Speed")
                    self.curing_x_axis_speed_lbl.setObjectName("curing_x_axis_speed_lbl")
                    self.curing_x_axis_speed_lndt = QtWidgets.QLineEdit(self.curing_x_axis_groupbox)
                    self.curing_x_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 5000, self.curing_x_axis_speed_lndt)
                    self.curing_x_axis_speed_lndt.setValidator(validator)
                    self.curing_x_axis_speed_lndt.setToolTip("The X-Actuator speed is limited to a range of 0 to 2000")
                    self.curing_x_axis_speed_lndt.setObjectName("curing_x_axis_speed_lndt")

                    self.curing_x_axis_current_position_lbl = QtWidgets.QLabel(self.curing_x_axis_groupbox)
                    self.curing_x_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.curing_x_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.curing_x_axis_current_position_lbl.setFont(font)
                    self.curing_x_axis_current_position_lbl.setObjectName("curing_x_axis_current_position_lbl")
                    self.curing_x_axis_current_position_value = QtWidgets.QLabel(self.curing_x_axis_groupbox)
                    self.curing_x_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.curing_x_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.curing_x_axis_current_position_value.setFont(font)
                    self.curing_x_axis_current_position_value.setObjectName("curing_x_axis_current_position_value")

                    self.curing_x_axis_run_btn = QtWidgets.QPushButton(self.curing_x_axis_groupbox)
                    self.curing_x_axis_run_btn.setAccessibleName('curing_x_axis_run_btn')
                    self.curing_x_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.curing_x_axis_run_btn.setFont(font)
                    self.curing_x_axis_run_btn.setText("RUN")
                    self.curing_x_axis_run_btn.setFlat(True)
                    self.curing_x_axis_run_btn.setFont(font)
                    self.curing_x_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                             "background-color:rgb(49, 77, 162);\n"
                                                             "color:rgb(255, 255, 255);\n"
                                                             "border-radius: 10px;\n"
                                                             "}"
                                                             "QPushButton:Pressed{\n"
                                                             "border: 3px solid;\n"
                                                             "}"
                                                             )
                    self.curing_x_axis_run_btn.setObjectName("curing_x_axis_run_btn")
                    self.verticalLayout_7.addWidget(self.curing_x_axis_groupbox)

                    self.curing_y_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_7)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.curing_y_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.curing_y_axis_groupbox.setSizePolicy(sizePolicy)
                    self.curing_y_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.curing_y_axis_groupbox.setFont(font)
                    self.curing_y_axis_groupbox.setObjectName("curing_y_axis_groupbox")

                    self.curing_y_axis_mini_lbl = QtWidgets.QLabel(self.curing_y_axis_groupbox)
                    self.curing_y_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.curing_y_axis_mini_lbl.setFont(font)
                    self.curing_y_axis_mini_lbl.setObjectName("curing_y_axis_mini_lbl")
                    self.curing_y_axis_mini_lndt = QtWidgets.QLineEdit(self.curing_y_axis_groupbox)
                    self.curing_y_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.curing_y_axis_mini_lndt)
                    self.curing_y_axis_mini_lndt.setValidator(validator)
                    self.curing_y_axis_mini_lndt.setObjectName("curing_y_axis_mini_lndt")

                    self.curing_y_axis_speed_lbl = QtWidgets.QLabel(self.curing_y_axis_groupbox)
                    self.curing_y_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.curing_y_axis_speed_lbl.setFont(font)
                    self.curing_y_axis_speed_lbl.setText("Speed")
                    self.curing_y_axis_speed_lbl.setObjectName("curing_y_axis_speed_lbl")
                    self.curing_y_axis_speed_lndt = QtWidgets.QLineEdit(self.curing_y_axis_groupbox)
                    self.curing_y_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 15000, self.curing_y_axis_speed_lndt)
                    self.curing_y_axis_speed_lndt.setValidator(validator)
                    self.curing_y_axis_speed_lndt.setToolTip("The Y-Actuator speed is limited to a range of 0 to 15000")
                    self.curing_y_axis_speed_lndt.setObjectName("curing_y_axis_speed_lndt")

                    self.curing_y_axis_current_position_lbl = QtWidgets.QLabel(self.curing_y_axis_groupbox)
                    self.curing_y_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.curing_y_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.curing_y_axis_current_position_lbl.setFont(font)
                    self.curing_y_axis_current_position_lbl.setObjectName("curing_y_axis_current_position_lbl")
                    self.curing_y_axis_current_position_value = QtWidgets.QLabel(self.curing_y_axis_groupbox)
                    self.curing_y_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.curing_y_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.curing_y_axis_current_position_value.setFont(font)
                    self.curing_y_axis_current_position_value.setObjectName("curing_y_axis_current_position_value")

                    self.curing_y_axis_run_btn = QtWidgets.QPushButton(self.curing_y_axis_groupbox)
                    self.curing_y_axis_run_btn.setAccessibleName('curing_y_axis_run_btn')
                    self.curing_y_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.curing_y_axis_run_btn.setFont(font)
                    self.curing_y_axis_run_btn.setText("RUN")
                    self.curing_y_axis_run_btn.setFlat(True)
                    self.curing_y_axis_run_btn.setFont(font)
                    self.curing_y_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                             "background-color:rgb(49, 77, 162);\n"
                                                             "color:rgb(255, 255, 255);\n"
                                                             "border-radius: 10px;\n"
                                                             "}"
                                                             "QPushButton:Pressed{\n"
                                                             "border: 3px solid;\n"
                                                             "}"
                                                             )
                    self.curing_y_axis_run_btn.setObjectName("curing_y_axis_run_btn")
                    self.verticalLayout_7.addWidget(self.curing_y_axis_groupbox)

                    self.curing_z_axis_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_7)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.curing_z_axis_groupbox.sizePolicy().hasHeightForWidth())
                    self.curing_z_axis_groupbox.setSizePolicy(sizePolicy)
                    self.curing_z_axis_groupbox.setMinimumSize(QtCore.QSize(0, 150))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.curing_z_axis_groupbox.setFont(font)
                    self.curing_z_axis_groupbox.setObjectName("curing_z_axis_groupbox")

                    self.curing_z_axis_mini_lbl = QtWidgets.QLabel(self.curing_z_axis_groupbox)
                    self.curing_z_axis_mini_lbl.setGeometry(QtCore.QRect(10, 30, 70, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.curing_z_axis_mini_lbl.setFont(font)
                    self.curing_z_axis_mini_lbl.setObjectName("curing_x_axis_mini_lbl")
                    self.curing_z_axis_mini_lndt = QtWidgets.QLineEdit(self.curing_z_axis_groupbox)
                    self.curing_z_axis_mini_lndt.setGeometry(QtCore.QRect(10, 50, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    validator = QRegExpValidator(regx, self.curing_z_axis_mini_lndt)
                    self.curing_z_axis_mini_lndt.setValidator(validator)
                    self.curing_z_axis_mini_lndt.setObjectName("curing_z_axis_mini_lndt")

                    self.curing_z_axis_speed_lbl = QtWidgets.QLabel(self.curing_z_axis_groupbox)
                    self.curing_z_axis_speed_lbl.setGeometry(QtCore.QRect(110, 30, 50, 15))
                    font = QtGui.QFont()
                    font.setPointSize(8)
                    self.curing_z_axis_speed_lbl.setFont(font)
                    self.curing_z_axis_speed_lbl.setText("Speed")
                    self.curing_z_axis_speed_lbl.setObjectName("curing_z_axis_speed_lbl")
                    self.curing_z_axis_speed_lndt = QtWidgets.QLineEdit(self.curing_z_axis_groupbox)
                    self.curing_z_axis_speed_lndt.setGeometry(QtCore.QRect(110, 50, 70, 30))
                    validator = QIntValidator(0, 5000, self.curing_z_axis_speed_lndt)
                    self.curing_z_axis_speed_lndt.setValidator(validator)
                    self.curing_z_axis_speed_lndt.setToolTip("The Z-Actuator speed is limited to a range of 0 to 2000")
                    self.curing_z_axis_speed_lndt.setObjectName("curing_z_axis_speed_lndt")

                    self.curing_z_axis_current_position_lbl = QtWidgets.QLabel(self.curing_z_axis_groupbox)
                    self.curing_z_axis_current_position_lbl.setGeometry(QtCore.QRect(200, 55, 150, 15))
                    self.curing_z_axis_current_position_lbl.setText("Current Position :")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.curing_z_axis_current_position_lbl.setFont(font)
                    self.curing_z_axis_current_position_lbl.setObjectName("curing_z_axis_current_position_lbl")
                    self.curing_z_axis_current_position_value = QtWidgets.QLabel(self.curing_z_axis_groupbox)
                    self.curing_z_axis_current_position_value.setGeometry(QtCore.QRect(320, 55, 50, 15))
                    self.curing_z_axis_current_position_value.setText("10")
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    self.curing_z_axis_current_position_value.setFont(font)
                    self.curing_z_axis_current_position_value.setObjectName("curing_z_axis_current_position_value")

                    self.curing_z_axis_run_btn = QtWidgets.QPushButton(self.curing_z_axis_groupbox)
                    self.curing_z_axis_run_btn.setAccessibleName('curing_z_axis_run_btn')
                    self.curing_z_axis_run_btn.setGeometry(QtCore.QRect(30, 100, 70, 35))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.curing_z_axis_run_btn.setFont(font)
                    self.curing_z_axis_run_btn.setText("RUN")
                    self.curing_z_axis_run_btn.setFlat(True)
                    self.curing_z_axis_run_btn.setFont(font)
                    self.curing_z_axis_run_btn.setStyleSheet("QPushButton{\n"
                                                             "background-color:rgb(49, 77, 162);\n"
                                                             "color:rgb(255, 255, 255);\n"
                                                             "border-radius: 10px;\n"
                                                             "}"
                                                             "QPushButton:Pressed{\n"
                                                             "border: 3px solid;\n"
                                                             "}"
                                                             )
                    self.curing_z_axis_run_btn.setObjectName("curing_z_axis_run_btn")

                    self.curing_z_axis_homing_btn = QtWidgets.QPushButton(self.curing_z_axis_groupbox)
                    self.curing_z_axis_homing_btn.setGeometry(QtCore.QRect(250, 100, 90, 40))
                    self.curing_z_axis_homing_btn.setAccessibleName("curing z_axis homing btn")
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.curing_z_axis_homing_btn.setFont(font)
                    self.curing_z_axis_homing_btn.setText("Homing")
                    self.curing_z_axis_homing_btn.setStyleSheet("QPushButton{\n"
                                                                "background-color:rgb(49, 77, 162);\n"
                                                                "color:rgb(255, 255, 255);\n"
                                                                "border-radius: 10px;\n"
                                                                "}"
                                                                "QPushButton:Pressed{\n"
                                                                "border: 3px solid;\n"
                                                                "}"
                                                                )
                    self.curing_z_axis_homing_btn.setObjectName("curing_z_axis_homing_btn")
                    self.verticalLayout_7.addWidget(self.curing_z_axis_groupbox)
                    self.curing_scrollarea.setWidget(self.scrollAreaWidgetContents_7)

                    self.curing_details_groupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_7)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.curing_details_groupbox.sizePolicy().hasHeightForWidth())
                    self.curing_details_groupbox.setSizePolicy(sizePolicy)
                    self.curing_details_groupbox.setMinimumSize(QtCore.QSize(0, 180))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.curing_details_groupbox.setFont(font)
                    self.curing_details_groupbox.setObjectName("curing_details_groupbox")

                    self.curing_time_lbl = QtWidgets.QLabel(self.curing_details_groupbox)
                    self.curing_time_lbl.setGeometry(QtCore.QRect(20, 35, 90, 20))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.curing_time_lbl.setFont(font)
                    self.curing_time_lbl.setObjectName("curing_time_lbl")
                    self.curing_time_lndt = QtWidgets.QLineEdit(self.curing_details_groupbox)
                    self.curing_time_lndt.setGeometry(QtCore.QRect(110, 30, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    curing_time_lndt = QRegExpValidator(regx, self.curing_time_lndt)
                    self.curing_time_lndt.setValidator(curing_time_lndt)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.curing_time_lndt.setFont(font)
                    self.curing_time_lndt.setPlaceholderText("")
                    self.curing_time_lndt.setObjectName("curing_time_lndt")

                    self.curing_uv_intensity_lbl = QtWidgets.QLabel(self.curing_details_groupbox)
                    self.curing_uv_intensity_lbl.setGeometry(QtCore.QRect(20, 85, 70, 30))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.curing_uv_intensity_lbl.setFont(font)
                    self.curing_uv_intensity_lbl.setObjectName("curing_uv_intensity_lbl")
                    self.curing_uv_intensity_lndt = QtWidgets.QLineEdit(self.curing_details_groupbox)
                    self.curing_uv_intensity_lndt.setGeometry(QtCore.QRect(110, 85, 70, 30))
                    regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
                    curing_uv_intensity_lndt = QRegExpValidator(regx, self.curing_uv_intensity_lndt)
                    self.curing_uv_intensity_lndt.setValidator(curing_uv_intensity_lndt)
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    self.curing_uv_intensity_lndt.setFont(font)
                    self.curing_uv_intensity_lndt.setPlaceholderText("")
                    self.curing_uv_intensity_lndt.setObjectName("curing_uv_intensity_lndt")

                    self.curing_detail_cure_btn = QtWidgets.QPushButton(self.curing_details_groupbox)
                    self.curing_detail_cure_btn.setGeometry(QtCore.QRect(20, 135, 90, 40))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    font.setWeight(40)
                    self.curing_detail_cure_btn.setFont(font)
                    self.curing_detail_cure_btn.setStyleSheet("QPushButton{\n"
                                                              "background-color:rgb(49, 77, 162);\n"
                                                              "color:rgb(255, 255, 255);\n"
                                                              "border-radius: 10px;\n"
                                                              "}"
                                                              "QPushButton:Pressed{\n"
                                                              "border: 3px solid;\n"
                                                              "}"
                                                              )
                    self.curing_detail_cure_btn.setObjectName("curing_detail_cure_btn")

                    self.curing_door_lbl = QtWidgets.QLabel(self.curing_details_groupbox)
                    self.curing_door_lbl.setGeometry(QtCore.QRect(270, 30, 90, 30))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.curing_door_lbl.setFont(font)
                    self.curing_door_lbl.setObjectName("curing_door_lbl")

                    self.curing_door_out_btn = QtWidgets.QPushButton(self.curing_details_groupbox)
                    self.curing_door_out_btn.setGeometry(QtCore.QRect(250, 75, 50, 50))
                    font = QtGui.QFont()
                    font.setPointSize(28)
                    font.setBold(True)
                    font.setWeight(75)
                    self.curing_door_out_btn.setFont(font)
                    self.curing_door_out_btn.setStyleSheet("QPushButton:hover{"
                                                            "background-color: #000000;}"
                                                            "QPushButton:Pressed{\n"
                                                            "padding-left:5px;\n"
                                                            "padding-top:5px;\n"
                                                           "background-color: #1a5276;\n"
                                                           "}"
                                                            "QPushButton::icon {"
                                                            "padding-right: 1px;}"
                                                            "QPushButton{"
                                                            "border-radius: 25px;}")
                    self.curing_door_out_btn.setText("")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.curing_door_out_btn.setIcon(icon)
                    self.curing_door_out_btn.setIconSize(QtCore.QSize(50, 50))
                    self.curing_door_out_btn.setFlat(True)
                    self.curing_door_out_btn.setObjectName("curing_door_out_btn")

                    self.curing_door_in_btn = QtWidgets.QPushButton(self.curing_details_groupbox)
                    self.curing_door_in_btn.setGeometry(QtCore.QRect(320, 75, 50, 50))
                    font = QtGui.QFont()
                    font.setPointSize(28)
                    font.setBold(True)
                    font.setWeight(75)
                    self.curing_door_in_btn.setFont(font)
                    self.curing_door_in_btn.setStyleSheet("QPushButton:hover{"
                                                            "background-color: #000000;}"
                                                            "QPushButton:Pressed{\n"
                                                            "padding-left:5px;\n"
                                                            "padding-top:5px;\n"
                                                           "background-color: #1a5276;\n"
                                                           "}"
                                                            "QPushButton::icon {"
                                                            "padding-right: 1px;}"
                                                            "QPushButton{"
                                                            "border-radius: 25px;}")
                    self.curing_door_in_btn.setText("")
                    icon1 = QtGui.QIcon()
                    icon1.addPixmap(QtGui.QPixmap(r".\media\up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.curing_door_in_btn.setIcon(icon1)
                    self.curing_door_in_btn.setIconSize(QtCore.QSize(50, 50))
                    self.curing_door_in_btn.setFlat(True)
                    self.curing_door_in_btn.setObjectName("curing_door_in_btn")
                    self.verticalLayout_7.addWidget(self.curing_details_groupbox)
                    self.stackedWidget.addWidget(self.station_6_layout)

                    self.btn_prev = QtWidgets.QPushButton(self.central_widget)
                    self.btn_prev.setGeometry(QtCore.QRect(300, self.window_height - 120, 70, 50))
                    font = QtGui.QFont()
                    font.setPointSize(28)
                    font.setBold(True)
                    font.setWeight(75)
                    self.btn_prev.setFont(font)
                    self.btn_prev.setStyleSheet("border-radius: 25px;")
                    self.btn_prev.setText("")
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(r".\media\prev_page.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
                    self.btn_prev.setIcon(icon)
                    self.btn_prev.setIconSize(QtCore.QSize(50, 50))
                    self.btn_prev.setFlat(True)
                    self.btn_prev.setObjectName("btn_prev")

                    self.btn_next = QtWidgets.QPushButton(self.central_widget)
                    self.btn_next.setGeometry(QtCore.QRect(360, self.window_height - 120, 70, 50))
                    font = QtGui.QFont()
                    font.setPointSize(28)
                    font.setBold(True)
                    font.setWeight(75)
                    self.btn_next.setFont(font)
                    self.btn_next.setStyleSheet("border-radius: 25px;")
                    self.btn_next.setText("")
                    icon1 = QtGui.QIcon()
                    icon1.addPixmap(QtGui.QPixmap(r".\media\nxt_page.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.btn_next.setIcon(icon1)
                    self.btn_next.setIconSize(QtCore.QSize(50, 50))
                    self.btn_next.setFlat(True)
                    self.btn_next.setObjectName("btn_next")

                    self.btn_save = QtWidgets.QPushButton(self.central_widget)
                    self.btn_save.setGeometry(QtCore.QRect(10, self.window_height - 115, 80, 40))
                    font = QtGui.QFont()
                    font.setPointSize(14)
                    self.btn_save.setFont(font)
                    self.btn_save.setStyleSheet("QPushButton{\n"
                                                "background-color:rgb(49, 77, 162);\n"
                                                "color:rgb(255, 255, 255);\n"
                                                "border-radius: 10px;\n"
                                                "}"
                                                "QPushButton:Pressed{\n"
                                                "background-color: #1a5276;\n"
                                                "}"
                                                )
                    self.btn_save.setObjectName("btn_save")

                    self.btn_save_recipe = QtWidgets.QPushButton(self.central_widget)
                    self.btn_save_recipe.setGeometry(QtCore.QRect(190, self.window_height - 115, 110, 40))
                    font = QtGui.QFont()
                    font.setPointSize(14)
                    self.btn_save_recipe.setFont(font)
                    self.btn_save_recipe.setStyleSheet("QPushButton{\n"
                                                       "background-color:rgb(49, 77, 162);\n"
                                                       "color:rgb(255, 255, 255);\n"
                                                       "border-radius: 10px;\n"
                                                       "}"
                                                       "QPushButton:Pressed{\n"
                                                       "background-color: #1a5276;\n"
                                                       "}"
                                                       )
                    self.btn_save_recipe.hide()
                    self.btn_save_recipe.setObjectName("btn_save_recipe")

                    self.btn_cancel = QtWidgets.QPushButton(self.central_widget)
                    self.btn_cancel.setGeometry(QtCore.QRect(100, self.window_height - 115, 80, 40))
                    font = QtGui.QFont()
                    font.setPointSize(14)
                    self.btn_cancel.setFont(font)
                    self.btn_cancel.setStyleSheet("QPushButton{\n"
                                                  "background-color:rgb(49, 77, 162);\n"
                                                  "color:rgb(255, 255, 255);\n"
                                                  "border-radius: 10px;\n"
                                                  "}"
                                                  "QPushButton:Pressed{\n"
                                                  "background-color: #1a5276;\n"
                                                  "}"
                                                  )
                    self.btn_cancel.setObjectName("btn_cancel")

                    self.stackedWidget.setCurrentIndex(0)

                    self.stackedWidget_1 = QtWidgets.QStackedWidget(self.central_widget)
                    self.stackedWidget_1.setGeometry(
                        QtCore.QRect(450, 80, self.window_width - 500, self.window_height - 300))
                    self.stackedWidget_1.setObjectName("stackedWidget_1")

                    self.image_preview_1 = QtWidgets.QLabel()
                    if self.window_height < 1085:
                        self.current_lbl_geomentry = QtCore.QRect(450, 200, (self.window_width - 460),
                                                                  (self.window_height - 350))
                        self.image_preview_1.setGeometry(self.current_lbl_geomentry)

                    elif self.window_height < 1610:
                        self.current_lbl_geomentry = QtCore.QRect(450, 190, (self.window_width - 500),
                                                                  (self.window_height - 340))
                        self.image_preview_1.setGeometry(self.current_lbl_geomentry)

                    elif self.window_height < 2165:
                        self.current_lbl_geomentry = QtCore.QRect(450, 190, (self.window_width - 500),
                                                                  (self.window_height - 360))
                        self.image_preview_1.setGeometry(self.current_lbl_geomentry)

                    self.image_preview_1.setText("")
                    self.image_preview_1.setPixmap(QtGui.QPixmap(r".\media\No-Preview-Available.jpg"))
                    self.image_preview_1.setAlignment(Qt.AlignCenter)
                    self.image_preview_1.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.image_preview_1.setFrameShadow(QtWidgets.QFrame.Plain)
                    self.image_preview_1.setObjectName("image_preview_1")
                    self.stackedWidget_1.addWidget(self.image_preview_1)
                    self.stackedWidget_1.setCurrentIndex(0)

                self.statusbar = QtWidgets.QLabel(self.central_widget)
                self.statusbar.setFont(QtGui.QFont("Times", 10))

                if self.window_height < 1085:
                    self.statusbar.setGeometry(
                        QtCore.QRect(850, (self.window_height - 110), 500, 30))

                elif self.window_height < 1610:
                    self.statusbar.setGeometry(
                        QtCore.QRect(700, (self.window_height - 125), (self.window_width - 510), 30))

                elif self.window_height < 2165:
                    self.statusbar.setGeometry(
                        QtCore.QRect(700, (self.window_height - 140), (self.window_width - 510), 30))

                self.statusbar.setStyleSheet("QLabel {\n"
                                             "color: rgb(0, 0, 255);\n"
                                             "font-size: 20px;\n"
                                             "}")
                self.statusbar.setAlignment(Qt.AlignLeft)
                self.statusbar.setText("")
                self.statusbar.raise_()

                MainWindow.setCentralWidget(self.central_widget)
                if mode == "Auto":
                    self.retranslate_ui(MainWindow)
                else:
                    self.retranslate_ui(MainWindow, mode="recipe_create")

                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at GUI setup ui function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def retranslate_ui(self, MainWindow, mode="Auto"):
        try:
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", f"{self.application_name}_{self.app_version}"))
            if mode == "Auto":
                self.loading_txt.setText(_translate("Auto_mainwindow", "Loading/Unloading"))
                self.h_sensor_txt.setText(_translate("Auto_mainwindow", "Height Sensor"))
                self.relay_txt.setText(_translate("Auto_mainwindow", "Relay"))
                self.collimator_txt.setText(_translate("Auto_mainwindow", "Collimator"))
                self.gluing_txt.setText(_translate("Auto_mainwindow", "Gluing"))
                self.curing_txt.setText(_translate("Auto_mainwindow", "Curing"))
                self.logout_btn.setText(_translate("Auto_mainwindow", "Log Out"))
                self.user_setting.setText(_translate("MainWindow", "Settings"))
            else:
                self.lbl_user_name.setText(_translate("MainWindow", "Name"))
                self.lbl_emp_id.setText(_translate("MainWindow", "Emp ID"))
                self.lnedt_emp_id.setPlaceholderText(_translate("MainWindow", "Enter Emp ID"))
                self.lnedt_name.setPlaceholderText(_translate("MainWindow", "Enter the name"))
                self.lnedt_set_password.setPlaceholderText(_translate("MainWindow", "Enter the password"))
                self.lbl_set_password.setText(_translate("MainWindow", "Set Password"))
                self.lbl_user_permission.setText(_translate("MainWindow", "User permission"))
                self.lbl_privilege.setText(_translate("MainWindow", "Privilege"))
                self.lnedt_set_password_2.setPlaceholderText(_translate("MainWindow", "Confirm the password"))
                self.lbl_set_password_2.setText(_translate("MainWindow", "Confirm Password"))
                self.btn_user_create.setText(_translate("MainWindow", "Create"))
                self.create_fingerprint.setText(_translate("MainWindow", "Create Fingerprint"))
                self.btn_fingerprint_create.setText(_translate("MainWindow", "click here"))
                self.device_details_grpbox.setTitle(_translate("MainWindow", "Device Details"))
                self.path_lbl.setText(_translate("MainWindow", "Save Path"))
                self.path_btn.setText(_translate("MainWindow", "Browse"))
                self.get_device_btn.setText(_translate("MainWindow", "get Device"))
                self.device_name_lbl.setText(_translate("MainWindow", "Device Name"))
                self.resolution_lbl_name.setText(_translate("MainWindow", "Resolution"))
                self.exposure_Lbl_name.setText(_translate("MainWindow", "Exposure"))
                self.product_sr_no_box.setPlaceholderText('Enter the Product Serial.no')
                self.product_name_box.setPlaceholderText('Enter the Product Name')
                self.mod_Serial_No_box.setPlaceholderText('Enter the Mod board Serial.no')
                self.base_Serial_No_box.setPlaceholderText('Enter the Base board Serial.no')

                self.loading_x_axis_groupbox.setTitle(_translate("MainWindow", "X-axis Actuator"))
                self.loading_x_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.loading_y_axis_groupbox.setTitle(_translate("MainWindow", "Y-axis Actuator"))
                self.loading_y_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.loading_slider_groupbox.setTitle(_translate("MainWindow", "Slider"))
                self.loading_slider_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.loading_gripper_groupbox.setTitle(_translate("MainWindow", "Gripper"))
                self.loading_gripper_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.loading_rotation_groupbox.setTitle(_translate("MainWindow", "Rotation"))
                self.loading_rotation_stepvalue_lbl.setText(_translate("MainWindow", "Step Value"))

                self.loading_init_lbl.setText(_translate("MainWindow", "Plc INIT :"))
                self.loading_door_lbl.setText(_translate("MainWindow", "Front Door :"))
                self.front_door_open_lbl.setText(_translate("MainWindow", "Open"))
                self.front_door_close_lbl.setText(_translate("MainWindow", "Close"))
                self.loading_part_load_lbl.setText(_translate("MainWindow", "Part Loading :"))
                self.loading_part_load_open_lbl.setText(_translate("MainWindow", "In"))
                self.loading_part_load_close_lbl.setText(_translate("MainWindow", "Out"))
                self.loading_groupbox.setTitle(_translate("MainWindow", "Loading Station"))

                self.lens_rotator_x_axis_groupbox.setTitle(_translate("MainWindow", "X-axis Actuator"))
                self.lens_rotator_x_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.lens_rotator_y_axis_groupbox.setTitle(_translate("MainWindow", "Y-axis Actuator"))
                self.lens_rotator_y_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.lens_rotator_gripper_groupbox.setTitle(_translate("MainWindow", "Lens Rotator"))
                self.lens_rotator_gripper_stepvalue_lbl.setText(_translate("MainWindow", "Step Value"))
                self.lens_rotator_sensor_groupbox.setTitle(_translate("MainWindow", "Displacement Sensor"))
                self.lens_rotator_sensor_value_lbl.setText(_translate("MainWindow", "Value :"))

                self.collimator_x_axis_groupbox.setTitle(_translate("MainWindow", "X-axis Actuator"))
                self.collimator_x_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.collimator_y_axis_groupbox.setTitle(_translate("MainWindow", "Y-axis Actuator"))
                self.collimator_y_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.collimator_gripper_groupbox.setTitle(_translate("MainWindow", "Lens Rotator"))
                self.collimator_gripper_stepvalue_lbl.setText(_translate("MainWindow", "Step Value"))

                self.Collimator_details_groupbox.setTitle(_translate("MainWindow", "Collimator Parameters"))
                self.Collimator_chart_details_groupbox.setTitle(_translate("MainWindow", "MTF Parameters"))
                self.collimator_chartdistance_lndt.setPlaceholderText(_translate("MainWindow", "in mm"))
                self.collimator_chartdistance_lbl.setText(_translate("MainWindow", "Chart Distance"))
                self.collimator_azimuth_lbl.setText(_translate("MainWindow", "Azimuth Angle"))
                self.collimator_chartintensity_lbl.setText(_translate("MainWindow", "Chart Intensity"))
                self.collimator_tl_chartintensity_lbl.setText(_translate("MainWindow", "TL"))
                self.collimator_tr_chartintensity_lbl.setText(_translate("MainWindow", "TR"))
                self.collimator_bl_chartintensity_lbl.setText(_translate("MainWindow", "BL"))
                self.collimator_br_chartintensity_lbl.setText(_translate("MainWindow", "BR"))
                self.collimator_c_chartintensity_lbl.setText(_translate("MainWindow", "C"))
                self.collimator_chart_detail_update_btn.setText(_translate("MainWindow", "Update"))
                self.collimator_radius_lbl.setText(_translate("MainWindow", "Radius"))
                self.collimator_width_lbl.setText(_translate("MainWindow", "Width"))
                self.collimator_height_lbl.setText(_translate("MainWindow", "Height"))
                self.collimator_details_update_btn.setText(_translate("MainWindow", "Update"))
                self.collimator_details_simulate_btn.setText(_translate("MainWindow", "Reference ROI"))
                self.collimator_details_chart_check_btn.setText(_translate("MainWindow", "Chart check"))
                self.collimator_radius_lndt.setPlaceholderText(_translate("MainWindow", "in pixel"))
                self.collimator_width_lndt.setPlaceholderText(_translate("MainWindow", "in pixel"))
                self.collimator_height_lndt.setPlaceholderText(_translate("MainWindow", "in pixel"))
                self.collimator_height_lndt.setPlaceholderText(_translate("MainWindow", "in pixel"))

                self.relay_x_axis_groupbox.setTitle(_translate("MainWindow", "X-axis Actuator"))
                self.relay_x_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))
                self.relay_y_axis_groupbox.setTitle(_translate("MainWindow", "Y-axis Actuator"))
                self.relay_y_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))
                self.relay_gripper_groupbox.setTitle(_translate("MainWindow", "Lens Rotator"))
                self.relay_gripper_stepvalue_lbl.setText(_translate("MainWindow", "Step Value"))

                self.relay_light_panel_actuator_groupbox.setTitle(_translate("MainWindow", "Light Panel Actuator"))
                self.relay_light_panel_actuator_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.relay_light_panel_intensity_lbl.setText(_translate("MainWindow", "Light Intensity"))
                self.relay_offset_groupbox.setTitle(_translate("MainWindow", "Other Parameters"))
                self.relay_details_groupbox.setTitle(_translate("MainWindow", "MTF Parameters"))

                self.gluing_x_axis_groupbox.setTitle(_translate("MainWindow", "X-axis Actuator"))
                self.gluing_x_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))
                self.gluing_y_axis_groupbox.setTitle(_translate("MainWindow", "Y-axis Actuator"))
                self.gluing_y_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.gluing_z_gluing_groupbox.setTitle(_translate("MainWindow", "Z-Gluing Actuator"))
                self.gluing_z_gluing_homing_btn.setText(_translate("MainWindow", "Homing"))
                self.gluing_z_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))

                self.gluing_cntrl_groupbox.setTitle(_translate("MainWindow", "Gluing Controller"))
                self.gluing_teaching_groupbox.setTitle(_translate("MainWindow", "Gluing Teaching Detail"))
                self.gluing_teaching_x1_mini_lbl.setText(_translate("MainWindow", "X1 position"))
                self.gluing_teaching_x2_mini_lbl.setText(_translate("MainWindow", "X2 position"))

                self.gluing_dispenser_timer_lbl.setText(_translate("MainWindow", "Time"))
                self.gluing_dispenser_type_lbl.setText(_translate("MainWindow", "Dispenser"))
                self.gluing_type_lbl.setText(_translate("MainWindow", "Gluing Type"))
                self.gluing_detail_speed_lbl.setText(_translate("MainWindow", "Speed"))
                self.gluing_detail_diameter_lbl.setText(_translate("MainWindow", "Lens OD"))

                self.curing_x_axis_groupbox.setTitle(_translate("MainWindow", "X-axis Actuator"))
                self.curing_x_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))
                self.curing_y_axis_groupbox.setTitle(_translate("MainWindow", "Y-axis Actuator"))
                self.curing_y_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))
                self.curing_z_axis_groupbox.setTitle(_translate("MainWindow", "Z-Curing Actuator"))
                self.curing_z_axis_mini_lbl.setText(_translate("MainWindow", "Set position"))
                self.curing_details_groupbox.setTitle(_translate("MainWindow", "Curing Details"))
                self.curing_detail_cure_btn.setText(_translate("MainWindow", "Curing"))
                self.curing_time_lbl.setText(_translate("MainWindow", "Curing Time"))
                self.curing_uv_intensity_lbl.setText(_translate("MainWindow", "UV Intensity"))
                self.curing_door_lbl.setText(_translate("MainWindow", "Curing Door"))
                self.user_setting.setText(_translate("MainWindow", "Settings"))
                self.btn_save.setText(_translate("MainWindow", "Save"))
                self.btn_save_recipe.setText(_translate("MainWindow", "Save Recipe"))
                self.btn_cancel.setText(_translate("MainWindow", "Abort"))
                self.get_device_btn.setText(_translate("MainWindow", "Get Device"))

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at GUI retranslate_ui function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))
