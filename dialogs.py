"""
This module is responsible for setting up the machine control's entire user interface.
"""

import sys
import os
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from logger import logger
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy


class Toggle_button(QtWidgets.QCheckBox):
    """
    This class is responsible for creating the toggle button for bypass screen.

    """
    def __init__(self, width=60, bgcolor="#777", circle_color="#DDD", active_color="#00BCff",
                 animation_curve=QEasingCurve.OutExpo):
        QtWidgets.QCheckBox.__init__(self)

        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)
        self._bg_color = bgcolor
        self._circle_color = circle_color
        self._active_color = active_color
        self._circle_position = 3
        self.animaton = QPropertyAnimation(self, b"circle_position", self)
        self.animaton.setEasingCurve(animation_curve)
        self.animaton.setDuration(500)
        self.stateChanged.connect(self.start_transition)

    def start_transition(self, value):
        """
            This method is responsible for animate the toggle button.
            value: whenever we change the toggle button
        """
        self.animaton.stop()
        if value:
            self.animaton.setEndValue(self.width() - 26)
        else:
            self.animaton.setEndValue(3)

        self.animaton.start()

    def hitButton(self, pos: QtCore.QPoint):
        """
            This method is responsible to get the rectangle position of toggle button.
        """
        return self.contentsRect().contains(pos)

    @property
    def circle_position(self):
        """
            This method is responsible create the curve of toggle button.
        """
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        """
            This method is responsible create the curve of toggle button.
            pos: position value
        """
        self._circle_position = pos
        self.update()

    def paintEvent(self, e):
        """
            This method is responsible create ui for toggle button.
        """
        p = QPainter(self)

        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(Qt.NoPen)
        rect = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(3, 3, 22, 22)

        else:
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self.width() - 26, 3, 22, 22)

        p.end()


class UiMainWindow_1(object):
    """
        This class is responsible create the mainwindow of this Ui.
    """
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1920, 1080)
        main_window.setFixedSize(1920, 1080)
        main_window.setAutoFillBackground(False)
        main_window.setDocumentMode(False)
        main_window.setWindowTitle("machine control sample")

    def sensor_status_dialog(self, lists, op_list):
        """
            This method is used to design the user interface for input and output operations.
            param lists: datatype in list and input list.
            param op_list: datatype in list and output list.
            return: None
        """
        self.sensor_dialog = QtWidgets.QDialog()
        table_height = (len(lists[0:27]) + 1) * 32
        self.sensor_dialog.setObjectName("sensor_dialog")
        self.sensor_dialog.setStyleSheet("background-color: rgba(196,236,236,255)")
        self.sensor_dialog.resize(1920, 1080)
        self.sensor_dialog.setWindowFlag(Qt.FramelessWindowHint)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sensor_dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.outer_layout = QtWidgets.QVBoxLayout()
        self.outer_layout.setObjectName("outer_layout")
        self.lbl_windowTitle = QtWidgets.QLabel(self.sensor_dialog)
        self.lbl_windowTitle.setGeometry(QtCore.QRect(100, 30, 410, 30))
        self.lbl_windowTitle.setStyleSheet("QLabel {\n"
                                           "color: rgb(0, 0, 0);\n"
                                           "}")
        self.lbl_windowTitle.setText("{}".format("Input Output status"))
        font = QFont("Arial", 16)
        font.setBold(True)
        font.setWeight(QFont.Black)
        self.lbl_windowTitle.setFont(font)
        self.lbl_windowTitle.setAlignment(Qt.AlignCenter)
        self.outer_layout.addWidget(self.lbl_windowTitle)

        self.groupboxes_frame = QtWidgets.QFrame(self.sensor_dialog)
        self.groupboxes_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.groupboxes_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.groupboxes_frame.setObjectName("groupboxes_frame")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupboxes_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.groupbox_h_layout = QtWidgets.QHBoxLayout()
        self.groupbox_h_layout.setSpacing(30)
        self.groupbox_h_layout.setObjectName("groupbox_h_layout")

        self.ip_groupbox = QtWidgets.QGroupBox("Input Status", self.groupboxes_frame)
        font = QFont("Arial", 12)
        font.setBold(True)
        font.setWeight(QFont.Black)
        self.ip_groupbox.setFont(font)
        self.ip_groupbox.setAlignment(Qt.AlignCenter)
        self.ip_groupbox.setStyleSheet("""
                                        QGroupBox {
                                            border: 1px solid #333;
                                            border-radius: 8px;
                                            color: #333;
                                            margin-top: 10px;
                                            text-align: center;
                                        }
                                        QGroupBox::title {
                                            subcontrol-origin: margin;
                                            subcontrol-position: top center; /* Center the title */
                                            padding: 0 10px;
                                        }
                                    """)
        self.ip_groupbox.setObjectName("ip_groupbox")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.ip_groupbox)
        self.horizontalLayout_5.setContentsMargins(10, 15, 10, 10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.input_h_lanputyout = QtWidgets.QHBoxLayout()
        self.input_h_lanputyout.setObjectName("input_h_lanputyout")

        self.sensor_tableWidget_ip_1 = QtWidgets.QTableWidget(self.ip_groupbox)
        self.sensor_tableWidget_ip_1.setObjectName("sensor_tableWidget_ip_1")
        self.sensor_tableWidget_ip_1.setRowCount(len(lists[0:27]) + 1)
        self.sensor_tableWidget_ip_1.setColumnCount(2)
        self.sensor_tableWidget_ip_1.setObjectName("sensor_tableWidget_ip_1")

        self.sensor_tableWidget_ip_1.horizontalHeader().setDefaultSectionSize(200)
        self.sensor_tableWidget_ip_1.verticalHeader().setDefaultSectionSize(32)
        self.sensor_tableWidget_ip_1.setColumnWidth(0, 310)
        self.sensor_tableWidget_ip_1.setColumnWidth(1, 135)

        self.sensor_tableWidget_ip_1.horizontalHeader().setVisible(False)
        self.sensor_tableWidget_ip_1.verticalHeader().setVisible(False)
        self.sensor_tableWidget_ip_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensor_tableWidget_ip_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensor_tableWidget_ip_1.setStyleSheet("border: 1px solid black;")
        self.sensor_tableWidget_ip_1.setEnabled(True)
        self.sensor_tableWidget_ip_1.setShowGrid(True)

        for j in range(2):
            for i in range(len(lists[0:27]) + 1):
                if i == 0:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    font = self.setfontstyle(True)
                    item.setFont(font)
                    self.sensor_tableWidget_ip_1.setItem(i, j, item)
                    self.sensor_tableWidget_ip_1.item(i, j).setBackground(QtGui.QColor(0, 51, 51))

                else:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    font = self.setfontstyle(False)
                    item.setFont(font)
                    self.sensor_tableWidget_ip_1.setItem(i, j, item)

        __sortingEnabled = self.sensor_tableWidget_ip_1.isSortingEnabled()
        self.sensor_tableWidget_ip_1.setSortingEnabled(False)

        for j in range(2):
            for i in range(len(lists[0:27]) + 1):
                if i == 0 and j == 0:
                    item = self.sensor_tableWidget_ip_1.item(i, j)
                    item.setText("Description")
                    item.setForeground(QBrush(QColor(255, 255, 255)))

                elif i == 0 and j == 1:
                    item = self.sensor_tableWidget_ip_1.item(i, j)
                    item.setText("Status")
                    item.setForeground(QBrush(QColor(255, 255, 255)))

                elif j == 0:
                    item = self.sensor_tableWidget_ip_1.item(i, j)
                    item.setText("{}".format(lists[0:27][i - 1]))
                    item.setForeground(QBrush(QColor(0, 0, 0)))

                elif j == 1:
                    item = self.sensor_tableWidget_ip_1.item(i, j)
                    item.setForeground(QBrush(QColor(0, 0, 0)))
                    item.setText("Off")

        self.sensor_tableWidget_ip_1.setSortingEnabled(__sortingEnabled)

        self.input_h_lanputyout.addWidget(self.sensor_tableWidget_ip_1)

        self.sensor_tableWidget_ip_2 = QtWidgets.QTableWidget(self.ip_groupbox)
        self.sensor_tableWidget_ip_2.setObjectName("sensor_tableWidget_ip_2")
        self.sensor_tableWidget_ip_2.setRowCount(len(lists[27:]) + 1)
        self.sensor_tableWidget_ip_2.setColumnCount(2)
        self.sensor_tableWidget_ip_2.setObjectName("sensor_tableWidget_ip_2")
        self.sensor_tableWidget_ip_2.horizontalHeader().setDefaultSectionSize(200)
        self.sensor_tableWidget_ip_2.verticalHeader().setDefaultSectionSize(32)
        self.sensor_tableWidget_ip_2.setColumnWidth(0, 310)
        self.sensor_tableWidget_ip_2.setColumnWidth(1, 150)
        self.sensor_tableWidget_ip_2.horizontalHeader().setVisible(False)
        self.sensor_tableWidget_ip_2.verticalHeader().setVisible(False)
        self.sensor_tableWidget_ip_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensor_tableWidget_ip_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensor_tableWidget_ip_2.setStyleSheet("border: 1px solid black;")
        self.sensor_tableWidget_ip_2.setEnabled(True)
        self.sensor_tableWidget_ip_2.setShowGrid(True)

        for j in range(2):
            for i in range(len(lists[27:]) + 1):
                if i == 0:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    font = self.setfontstyle(True)
                    item.setFont(font)
                    self.sensor_tableWidget_ip_2.setItem(i, j, item)
                    self.sensor_tableWidget_ip_2.item(i, j).setBackground(QtGui.QColor(0, 51, 51))

                else:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    font = self.setfontstyle(False)
                    item.setFont(font)
                    self.sensor_tableWidget_ip_2.setItem(i, j, item)

        __sortingEnabled = self.sensor_tableWidget_ip_2.isSortingEnabled()
        self.sensor_tableWidget_ip_2.setSortingEnabled(False)

        for j in range(2):
            for i in range(len(lists[27:]) + 1):
                if i == 0 and j == 0:
                    item = self.sensor_tableWidget_ip_2.item(i, j)
                    item.setText("Description")
                    item.setForeground(QBrush(QColor(255, 255, 255)))

                elif i == 0 and j == 1:
                    item = self.sensor_tableWidget_ip_2.item(i, j)
                    item.setText("Status")
                    item.setForeground(QBrush(QColor(255, 255, 255)))

                elif j == 0:
                    item = self.sensor_tableWidget_ip_2.item(i, j)
                    item.setText("{}".format(lists[27:][i - 1]))
                    item.setForeground(QBrush(QColor(0, 0, 0)))

                elif j == 1:
                    item = self.sensor_tableWidget_ip_2.item(i, j)
                    item.setForeground(QBrush(QColor(0, 0, 0)))
                    item.setText("Off")
        self.sensor_tableWidget_ip_2.setSortingEnabled(__sortingEnabled)

        self.input_h_lanputyout.addWidget(self.sensor_tableWidget_ip_2)
        self.horizontalLayout_5.addLayout(self.input_h_lanputyout)
        self.groupbox_h_layout.addWidget(self.ip_groupbox)

        self.op_group_box = QtWidgets.QGroupBox("Output Status", self.groupboxes_frame)
        font = QFont("Arial", 12)
        font.setBold(True)
        font.setWeight(QFont.Black)
        self.op_group_box.setFont(font)
        self.op_group_box.setAlignment(Qt.AlignCenter)
        self.op_group_box.setStyleSheet("""
                                        QGroupBox {
                                            border: 1px solid #333;
                                            border-radius: 8px;
                                            color: #333;
                                            margin-top: 10px;
                                            text-align: center;
                                        }
                                        QGroupBox::title {
                                            subcontrol-origin: margin;
                                            subcontrol-position: top center; /* Center the title */
                                            padding: 0 10px;
                                        }
                                    """)
        self.op_group_box.setObjectName("op_group_box")

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.op_group_box)
        self.horizontalLayout_6.setContentsMargins(10, 15, 10, 10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.output_h_layout = QtWidgets.QHBoxLayout()
        self.output_h_layout.setObjectName("output_h_layout")

        self.sensor_tableWidget_op_1 = QtWidgets.QTableWidget(self.op_group_box)
        self.sensor_tableWidget_op_1.setRowCount(len(op_list[0:27]) + 1)
        self.sensor_tableWidget_op_1.setColumnCount(2)
        self.sensor_tableWidget_op_1.setObjectName("sensor_tableWidget_op_1")

        self.sensor_tableWidget_op_1.horizontalHeader().setDefaultSectionSize(200)
        self.sensor_tableWidget_op_1.verticalHeader().setDefaultSectionSize(32)
        self.sensor_tableWidget_op_1.setColumnWidth(0, 310)
        self.sensor_tableWidget_op_1.setColumnWidth(1, 135)
        self.sensor_tableWidget_op_1.horizontalHeader().setVisible(False)
        self.sensor_tableWidget_op_1.verticalHeader().setVisible(False)
        self.sensor_tableWidget_op_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensor_tableWidget_op_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensor_tableWidget_op_1.setStyleSheet("border: 1px solid black;")
        self.sensor_tableWidget_op_1.setEnabled(True)
        self.sensor_tableWidget_op_1.setShowGrid(True)

        for j in range(2):
            for i in range(len(op_list) + 1):
                if i == 0:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    font = self.setfontstyle(True)
                    item.setFont(font)
                    self.sensor_tableWidget_op_1.setItem(i, j, item)
                    self.sensor_tableWidget_op_1.item(i, j).setBackground(QtGui.QColor(0, 51, 51))

                else:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    font = self.setfontstyle(False)
                    item.setFont(font)
                    self.sensor_tableWidget_op_1.setItem(i, j, item)

        __sortingEnabled = self.sensor_tableWidget_op_1.isSortingEnabled()
        self.sensor_tableWidget_op_1.setSortingEnabled(False)

        for j in range(2):
            for i in range(len(op_list[0:27]) + 1):
                if i == 0 and j == 0:
                    item = self.sensor_tableWidget_op_1.item(i, j)
                    item.setText("Description")
                    item.setForeground(QBrush(QColor(255, 255, 255)))

                elif i == 0 and j == 1:
                    item = self.sensor_tableWidget_op_1.item(i, j)
                    item.setText("Status")
                    item.setForeground(QBrush(QColor(255, 255, 255)))

                elif j == 0:
                    item = self.sensor_tableWidget_op_1.item(i, j)
                    item.setText("{}".format(op_list[0:27][i - 1]))
                    item.setForeground(QBrush(QColor(0, 0, 0)))

                elif j == 1:
                    item = self.sensor_tableWidget_op_1.item(i, j)
                    item.setForeground(QBrush(QColor(0, 0, 0)))
                    item.setText("Off")

        self.sensor_tableWidget_op_1.setSortingEnabled(__sortingEnabled)
        self.output_h_layout.addWidget(self.sensor_tableWidget_op_1)

        self.sensor_tableWidget_op_2 = QtWidgets.QTableWidget(self.op_group_box)
        self.sensor_tableWidget_op_2.setRowCount(len(op_list[27:]) + 1)
        self.sensor_tableWidget_op_2.setColumnCount(2)
        self.sensor_tableWidget_op_2.setObjectName("sensor_tableWidget_op_2")

        self.sensor_tableWidget_op_2.horizontalHeader().setDefaultSectionSize(200)
        self.sensor_tableWidget_op_2.verticalHeader().setDefaultSectionSize(32)
        self.sensor_tableWidget_op_2.setColumnWidth(0, 310)
        self.sensor_tableWidget_op_2.setColumnWidth(1, 150)

        self.sensor_tableWidget_op_2.horizontalHeader().setVisible(False)
        self.sensor_tableWidget_op_2.verticalHeader().setVisible(False)
        self.sensor_tableWidget_op_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensor_tableWidget_op_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sensor_tableWidget_op_2.setStyleSheet("border: 1px solid black;")
        self.sensor_tableWidget_op_2.setEnabled(True)
        self.sensor_tableWidget_op_2.setShowGrid(True)

        for j in range(2):
            for i in range(len(op_list[27:]) + 1):
                if i == 0:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    font = self.setfontstyle(True)
                    item.setFont(font)
                    self.sensor_tableWidget_op_2.setItem(i, j, item)
                    self.sensor_tableWidget_op_2.item(i, j).setBackground(QtGui.QColor(0, 51, 51))

                else:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    font = self.setfontstyle(False)
                    item.setFont(font)
                    self.sensor_tableWidget_op_2.setItem(i, j, item)

        __sortingEnabled = self.sensor_tableWidget_op_2.isSortingEnabled()
        self.sensor_tableWidget_op_2.setSortingEnabled(False)

        for j in range(2):
            for i in range(len(op_list[27:]) + 1):
                if i == 0 and j == 0:
                    item = self.sensor_tableWidget_op_2.item(i, j)
                    item.setText("Description")
                    item.setForeground(QBrush(QColor(255, 255, 255)))

                elif i == 0 and j == 1:
                    item = self.sensor_tableWidget_op_2.item(i, j)
                    item.setText("Status")
                    item.setForeground(QBrush(QColor(255, 255, 255)))

                elif j == 0:
                    item = self.sensor_tableWidget_op_2.item(i, j)
                    item.setText("{}".format(op_list[27:][i - 1]))
                    item.setForeground(QBrush(QColor(0, 0, 0)))

                elif j == 1:
                    item = self.sensor_tableWidget_op_2.item(i, j)
                    item.setForeground(QBrush(QColor(0, 0, 0)))
                    item.setText("Off")

        self.sensor_tableWidget_op_2.setSortingEnabled(__sortingEnabled)

        self.output_h_layout.addWidget(self.sensor_tableWidget_op_2)
        self.horizontalLayout_6.addLayout(self.output_h_layout)
        self.groupbox_h_layout.addWidget(self.op_group_box)

        self.horizontalLayout_2.addLayout(self.groupbox_h_layout)
        self.outer_layout.addWidget(self.groupboxes_frame)
        self.verticalLayout_2.addLayout(self.outer_layout)
        self.button_frame = QtWidgets.QFrame(self.sensor_dialog)
        self.button_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.button_frame.setFixedHeight(50)
        self.button_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.button_frame.setObjectName("button_frame")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.button_frame)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setSpacing(100)
        self.button_layout.setObjectName("button_layout")

        self.sensor_status_btn_refresh = QtWidgets.QPushButton(self.button_frame)
        self.sensor_status_btn_refresh.setObjectName("sensor_status_btn_refresh")
        self.sensor_status_btn_refresh.setText("Get Status")
        font = QFont("Arial", 10)
        font.setBold(True)
        font.setWeight(QFont.Black)
        self.sensor_status_btn_refresh.setFont(font)
        self.sensor_status_btn_refresh.setFixedHeight(35)
        self.sensor_status_btn_refresh.setFixedWidth(150)
        self.sensor_status_btn_refresh.setStyleSheet("QPushButton{\n"
                                                     "background-color: rgba(0, 51, 51, 1);\n"
                                                     "color: rgb(255, 255, 255);\n"
                                                     "border-radius:10px;}\n"
                                                     "QPushButton:Pressed{\n"
                                                     "padding-left:5px;\n"
                                                     "padding-top:5px;\n"
                                                     "background-color: #1a5276;\n"
                                                     "}"
                                                     "QPushButton:disabled"
                                                    "{"
                                                    "border-radius: 10px;\n"
                                                    "background-color:#95a5a6;"
                                                    "}"
                                                     )
        self.button_layout.addWidget(self.sensor_status_btn_refresh)

        self.sensor_status_btn_dclose = QtWidgets.QPushButton(self.button_frame)
        self.sensor_status_btn_dclose.setObjectName("sensor_status_btn_dclose")
        self.sensor_status_btn_dclose.setText("Close")
        font = QFont("Arial", 10)
        font.setBold(True)
        font.setWeight(QFont.Black)
        self.sensor_status_btn_dclose.setFont(font)
        self.sensor_status_btn_dclose.setFixedHeight(35)
        self.sensor_status_btn_dclose.setFixedWidth(150)
        self.sensor_status_btn_dclose.setStyleSheet("QPushButton:enabled{\n"
                                                    "background-color:rgb(0, 51, 51);\n"
                                                    "color:rgb(255, 255, 255);\n"
                                                    "border-radius: 10px;\n"
                                                    "}"
                                                    "QPushButton:Pressed{\n"
                                                    "padding-left:5px;\n"
                                                    "padding-top:5px;\n"
                                                    "background-color: #1a5276;\n"
                                                    "}"
                                                    "QPushButton:disabled"
                                                    "{"
                                                    "border-radius: 10px;\n"
                                                    "background-color:#95a5a6;"
                                                    "}"
                                                    )

        self.button_layout.addWidget(self.sensor_status_btn_dclose)
        self.horizontalLayout_8.addLayout(self.button_layout)
        self.verticalLayout_2.addWidget(self.button_frame)

    def port_status_dialog(self, lists):
        try:
            """
            This method is used to design the user interface for port connection.
            param lists: datatype in list and which are ports.
            return: None
            """
            self.port_dialog = QtWidgets.QDialog()
            table_height = (len(lists) + 1) * 32
            self.port_dialog.setObjectName("port_dialog")
            self.port_dialog.setWindowTitle("User Details")
            self.port_dialog.setWindowFlag(Qt.FramelessWindowHint)
            self.port_dialog.setStyleSheet("border-radius: 15px")
            self.port_dialog.resize(600, table_height + 220)
            self.verticalLayout = QtWidgets.QVBoxLayout(self.port_dialog)
            self.verticalLayout.setContentsMargins(10, 10, 10, 10)
            self.verticalLayout.setObjectName("verticalLayout")
            self.ShadowFrame = QtWidgets.QFrame(self.port_dialog)
            self.ShadowFrame.setStyleSheet("QFrame {\n"
                                           "background-color: rgba(196,236,236,255);\n"
                                           "color: rgb(220, 220, 220);\n"
                                           "border-radius: 10px;\n"
                                           "}\n")
            self.ShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.ShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.ShadowFrame.setObjectName("ShadowFrame")

            self.lbl_windowTitle = QtWidgets.QLabel(self.ShadowFrame)
            self.lbl_windowTitle.setGeometry(QtCore.QRect(100, 20, 410, 30))
            self.lbl_windowTitle.setStyleSheet("QLabel {\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "}")
            font = QFont("Arial", 16)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.lbl_windowTitle.setFont(font)
            self.lbl_windowTitle.setText("{}".format("Port Connection Status"))
            self.lbl_windowTitle.setAlignment(Qt.AlignCenter)

            self.port_tableWidget = QtWidgets.QTableWidget(self.port_dialog)
            self.port_tableWidget.setGeometry(QtCore.QRect(50, 100, 500, table_height))
            self.port_tableWidget.setRowCount(len(lists) + 1)
            self.port_tableWidget.setColumnCount(4)
            self.port_tableWidget.setObjectName("port_tableWidget")

            self.port_tableWidget.horizontalHeader().setDefaultSectionSize(200)
            self.port_tableWidget.verticalHeader().setDefaultSectionSize(32)
            self.port_tableWidget.setColumnWidth(0, 100)

            self.port_tableWidget.horizontalHeader().setVisible(False)
            self.port_tableWidget.verticalHeader().setVisible(False)
            self.port_tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.port_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.port_tableWidget.setEnabled(True)
            self.port_tableWidget.setShowGrid(True)

            for j in range(4):
                for i in range(len(lists) + 1):
                    if i == 0:
                        item = QtWidgets.QTableWidgetItem()
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        font = self.setfontstyle(True)
                        item.setFont(font)
                        self.port_tableWidget.setItem(i, j, item)
                        self.port_tableWidget.item(i, j).setBackground(QtGui.QColor(0, 51, 51))

                    else:
                        item = QtWidgets.QTableWidgetItem()
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        font = self.setfontstyle(False)
                        item.setFont(font)
                        self.port_tableWidget.setItem(i, j, item)

            __sortingEnabled = self.port_tableWidget.isSortingEnabled()
            self.port_tableWidget.setSortingEnabled(False)
            for j in range(3):
                for i in range(len(lists) + 1):
                    if i == 0 and j == 0:
                        item = self.port_tableWidget.item(i, j)
                        item.setText("SI. NO.")
                        item.setForeground(QBrush(QColor(255, 255, 255)))

                    elif i == 0 and j == 1:
                        item = self.port_tableWidget.item(i, j)
                        item.setText("Description")
                        item.setForeground(QBrush(QColor(255, 255, 255)))

                    elif i == 0 and j == 2:
                        item = self.port_tableWidget.item(i, j)
                        item.setText("Status")
                        item.setForeground(QBrush(QColor(255, 255, 255)))

                    elif i == 0 and j == 3:
                        item = self.port_tableWidget.item(i, j)
                        item.setText("Port")
                        item.setForeground(QBrush(QColor(255, 255, 255)))

                    elif j == 0:
                        item = self.port_tableWidget.item(i, j)
                        item.setText("{}".format(i))

                    elif j == 1:
                        item = self.port_tableWidget.item(i, j)
                        item.setText("{}".format(lists[i - 1]))

                    elif j == 2:
                        item = self.port_tableWidget.item(i, j)
                        item.setText("Disconnected")

            self.port_tableWidget.setSortingEnabled(__sortingEnabled)

            self.port_btn_refresh = QtWidgets.QPushButton(self.port_dialog)
            self.port_btn_refresh.setGeometry(QtCore.QRect(130, table_height + 140, 150, 40))
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.port_btn_refresh.setFont(font)
            self.port_btn_refresh.setStyleSheet("QPushButton:enabled{\n"
                                                "background-color:rgb(0, 51, 51);\n"
                                                "color:rgb(255, 255, 255);\n"
                                                "border-radius: 10px;\n"
                                                "}"
                                                "QPushButton:Pressed{\n"
                                                "padding-left:5px;\n"
                                                "padding-top:5px;\n"
                                                "background-color: #1a5276;\n"
                                                "}"
                                                "QPushButton:disabled"
                                                "{"
                                                "background-color:#95a5a6;"
                                                "}"
                                                )
            self.port_btn_refresh.setObjectName("port_btn_refresh")
            self.port_btn_refresh.setText("Refresh")
            self.port_btn_refresh.setEnabled(True)

            self.port_btn_dclose = QtWidgets.QPushButton(self.port_dialog)
            self.port_btn_dclose.setGeometry(QtCore.QRect(330, table_height + 140, 150, 40))
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.port_btn_dclose.setFont(font)
            self.port_btn_dclose.setStyleSheet("QPushButton:enabled{\n"
                                                "background-color:rgb(0, 51, 51);\n"
                                                "color:rgb(255, 255, 255);\n"
                                                "border-radius: 10px;\n"
                                                "}"
                                                "QPushButton:Pressed{\n"
                                                "padding-left:5px;\n"
                                                "padding-top:5px;\n"
                                                "background-color: #1a5276;\n"
                                                "}"
                                                "QPushButton:disabled"
                                                "{"
                                                "background-color:#95a5a6;"
                                                "}"
                                                )
            self.port_btn_dclose.setText("Close")
            self.port_btn_dclose.setObjectName("port_btn_dclose")
            self.verticalLayout.addWidget(self.ShadowFrame)
            QtCore.QMetaObject.connectSlotsByName(self.port_dialog)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at port_status dialog : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def machine_sensor_control_dialog(self):
        try:
            """
            This method is used to design the user interface for bypass screen.
            param lists: None
            return: None
            """
            self.machine_sensor_dialog = QtWidgets.QDialog()
            self.machine_sensor_dialog.setObjectName("self.machine_sensor_dialog")
            self.machine_sensor_dialog.setWindowTitle("machine control dialog")
            self.machine_sensor_dialog.setWindowFlag(Qt.FramelessWindowHint)
            self.machine_sensor_dialog.setStyleSheet("border-radius: 15px")
            self.machine_sensor_dialog.resize(500, 850)
            self.verticalLayout = QtWidgets.QVBoxLayout(self.machine_sensor_dialog)
            self.verticalLayout.setContentsMargins(10, 10, 10, 10)
            self.verticalLayout.setObjectName("verticalLayout")
            self.ShadowFrame = QtWidgets.QFrame(self.machine_sensor_dialog)
            self.ShadowFrame.setStyleSheet("QFrame {\n"
                                           "background-color: rgba(196,236,236,255);\n"
                                           "color: rgb(220, 220, 220);\n"
                                           "border-radius: 10px;\n"
                                           "}\n")
            self.ShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.ShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.ShadowFrame.setObjectName("ShadowFrame")

            self.lbl_windowTitle = QtWidgets.QLabel(self.ShadowFrame)
            self.lbl_windowTitle.setGeometry(QtCore.QRect(100, 50, 300, 30))
            self.lbl_windowTitle.setStyleSheet("QLabel {\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "}")
            font = QFont("Arial", 15)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.lbl_windowTitle.setFont(font)
            self.lbl_windowTitle.setText("Sensors Control Access")
            self.lbl_windowTitle.setAlignment(Qt.AlignCenter)

            self.right_door = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.right_door.setGeometry(QtCore.QRect(30, 120, 200, 30))
            self.right_door.setText("Right door sensor")
            self.right_door.setObjectName("right_door")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.right_door.setFont(font)
            self.right_door.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.right_door_toggle = Toggle_button()
            self.right_door_toggle.setGeometry(QtCore.QRect(400, 120, 350, 30))
            self.right_door_toggle.setParent(self.machine_sensor_dialog)

            self.left_door = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.left_door.setGeometry(QtCore.QRect(30, 170, 200, 30))
            self.left_door.setText("Left door sensor")
            self.left_door.setObjectName("left_door")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.left_door.setFont(font)
            self.left_door.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.left_door_toggle = Toggle_button()
            self.left_door_toggle.setGeometry(QtCore.QRect(400, 170, 350, 30))
            self.left_door_toggle.setParent(self.machine_sensor_dialog)

            self.front_door_open = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.front_door_open.setGeometry(QtCore.QRect(30, 220, 200, 30))
            self.front_door_open.setText("Front door open sensor")
            self.front_door_open.setObjectName("front_door_open")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.front_door_open.setFont(font)
            self.front_door_open.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.front_door_open_toggle = Toggle_button()
            self.front_door_open_toggle.setGeometry(QtCore.QRect(400, 220, 350, 30))
            self.front_door_open_toggle.setParent(self.machine_sensor_dialog)

            self.front_door_close = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.front_door_close.setGeometry(QtCore.QRect(30, 270, 200, 30))
            self.front_door_close.setText("Front door close sensor")
            self.front_door_close.setObjectName("front_door_close")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.front_door_close.setFont(font)
            self.front_door_close.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.front_door_close_toggle = Toggle_button()
            self.front_door_close_toggle.setGeometry(QtCore.QRect(400, 270, 350, 30))
            self.front_door_close_toggle.setParent(self.machine_sensor_dialog)

            self.product_present = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.product_present.setGeometry(QtCore.QRect(30, 320, 200, 30))
            self.product_present.setText("Product presence sensor")
            self.product_present.setObjectName("product_present")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.product_present.setFont(font)
            self.product_present.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.product_present_toggle = Toggle_button()
            self.product_present_toggle.setGeometry(QtCore.QRect(400, 320, 350, 30))
            self.product_present_toggle.setParent(self.machine_sensor_dialog)

            self.gd_left_open = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.gd_left_open.setGeometry(QtCore.QRect(30, 370, 300, 30))
            self.gd_left_open.setText("GD left cylinder open sensor")
            self.gd_left_open.setObjectName("gd_left_open")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.gd_left_open.setFont(font)
            self.gd_left_open.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.gd_left_open_toggle = Toggle_button()
            self.gd_left_open_toggle.setGeometry(QtCore.QRect(400, 370, 350, 30))
            self.gd_left_open_toggle.setParent(self.machine_sensor_dialog)

            self.gd_left_close = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.gd_left_close.setGeometry(QtCore.QRect(30, 420, 300, 30))
            self.gd_left_close.setText("GD left cylinder close sensor")
            self.gd_left_close.setObjectName("gd_left_close")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.gd_left_close.setFont(font)
            self.gd_left_close.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.gd_left_close_toggle = Toggle_button()
            self.gd_left_close_toggle.setGeometry(QtCore.QRect(400, 420, 350, 30))
            self.gd_left_close_toggle.setParent(self.machine_sensor_dialog)

            self.gd_right_open = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.gd_right_open.setGeometry(QtCore.QRect(30, 470, 300, 30))
            self.gd_right_open.setText("GD right cylinder open sensor")
            self.gd_right_open.setObjectName("gd_right_open")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.gd_right_open.setFont(font)
            self.gd_right_open.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.gd_right_open_toggle = Toggle_button()
            self.gd_right_open_toggle.setGeometry(QtCore.QRect(400, 470, 350, 30))
            self.gd_right_open_toggle.setParent(self.machine_sensor_dialog)

            self.gd_right_close = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.gd_right_close.setGeometry(QtCore.QRect(30, 520, 300, 30))
            self.gd_right_close.setText("GD right cylinder close sensor")
            self.gd_right_close.setObjectName("gd_right_close")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.gd_right_close.setFont(font)
            self.gd_right_close.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.gd_right_close_toggle = Toggle_button()
            self.gd_right_close_toggle.setGeometry(QtCore.QRect(400, 520, 350, 30))
            self.gd_right_close_toggle.setParent(self.machine_sensor_dialog)

            self.gluing_motor_alarm = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.gluing_motor_alarm.setGeometry(QtCore.QRect(30, 570, 300, 30))
            self.gluing_motor_alarm.setText("Gluing motor alarm")
            self.gluing_motor_alarm.setObjectName("gluing_motor_alarm")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.gluing_motor_alarm.setFont(font)
            self.gluing_motor_alarm.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.gluing_motor_alarm_toggle = Toggle_button()
            self.gluing_motor_alarm_toggle.setGeometry(QtCore.QRect(400, 570, 350, 30))
            self.gluing_motor_alarm_toggle.setParent(self.machine_sensor_dialog)

            self.uv_door_cylinder_open = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.uv_door_cylinder_open.setGeometry(QtCore.QRect(30, 620, 350, 30))
            self.uv_door_cylinder_open.setText("UV light cylinder open sensor")
            self.uv_door_cylinder_open.setObjectName("uv_left_open")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.uv_door_cylinder_open.setFont(font)
            self.uv_door_cylinder_open.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.uv_door_cylinder_open_toggle = Toggle_button()
            self.uv_door_cylinder_open_toggle.setGeometry(QtCore.QRect(400, 620, 350, 30))
            self.uv_door_cylinder_open_toggle.setParent(self.machine_sensor_dialog)

            self.uv_door_cylinder_close = QtWidgets.QLabel(self.machine_sensor_dialog)
            self.uv_door_cylinder_close.setGeometry(QtCore.QRect(30, 670, 350, 30))
            self.uv_door_cylinder_close.setText("UV light cylinder close sensor")
            self.uv_door_cylinder_close.setObjectName("uv_left_close")
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Segoe UI")
            font.setBold(True)
            self.uv_door_cylinder_close.setFont(font)
            self.uv_door_cylinder_close.setStyleSheet("color: rgb(0, 0, 0);\n")

            self.uv_door_cylinder_close_toggle = Toggle_button()
            self.uv_door_cylinder_close_toggle.setGeometry(QtCore.QRect(400, 670, 100, 5))
            self.uv_door_cylinder_close_toggle.setParent(self.machine_sensor_dialog)

            self.machine_sensor_cntrl_btn_update = QtWidgets.QPushButton(self.machine_sensor_dialog)
            self.machine_sensor_cntrl_btn_update.setGeometry(QtCore.QRect(60, 750, 150, 40))
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.machine_sensor_cntrl_btn_update.setFont(font)
            self.machine_sensor_cntrl_btn_update.setStyleSheet("QPushButton:enabled{\n"
                                                                "background-color:rgb(0, 51, 51);\n"
                                                                "color:rgb(255, 255, 255);\n"
                                                                "border-radius: 10px;\n"
                                                                "}"
                                                                "QPushButton:Pressed{\n"
                                                                "padding-left:5px;\n"
                                                                "padding-top:5px;\n"
                                                                "background-color: #1a5276;\n"
                                                                "}"
                                                                "QPushButton:disabled"
                                                                "{"
                                                                "background-color:#95a5a6;"
                                                                "}"
                                                                )
            self.machine_sensor_cntrl_btn_update.setObjectName("machine_sensor_cntrl_btn_update")
            self.machine_sensor_cntrl_btn_update.setText("Update")
            self.machine_sensor_cntrl_btn_update.setEnabled(True)

            self.machine_sensor_cntrl_btn_dclose = QtWidgets.QPushButton(self.machine_sensor_dialog)
            self.machine_sensor_cntrl_btn_dclose.setGeometry(QtCore.QRect(290, 750, 150, 40))
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.machine_sensor_cntrl_btn_dclose.setFont(font)
            self.machine_sensor_cntrl_btn_dclose.setStyleSheet("QPushButton:enabled{\n"
                                                                "background-color:rgb(0, 51, 51);\n"
                                                                "color:rgb(255, 255, 255);\n"
                                                                "border-radius: 10px;\n"
                                                                "}"
                                                                "QPushButton:Pressed{\n"
                                                                "padding-left:5px;\n"
                                                                "padding-top:5px;\n"
                                                                "background-color: #1a5276;\n"
                                                                "}"
                                                                "QPushButton:disabled"
                                                                "{"
                                                                "background-color:#95a5a6;"
                                                                "}"
                                                                )
            self.machine_sensor_cntrl_btn_dclose.setObjectName("machine_sensor_cntrl_btn_update")
            self.machine_sensor_cntrl_btn_dclose.setText("Close")
            self.machine_sensor_cntrl_btn_dclose.setEnabled(True)

            self.verticalLayout.addWidget(self.ShadowFrame)
            QtCore.QMetaObject.connectSlotsByName(self.machine_sensor_dialog)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at machine_sensor_dialog : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def diagnostic_control_dialog(self):
        try:
            """
            This method is used to design the user interface for diagnostic control.
            param lists: None
            return: None
            """
            self.diagnostic_dialog = QtWidgets.QDialog()
            self.diagnostic_dialog.setObjectName("dialog")
            self.diagnostic_dialog.setWindowTitle("User Details")
            self.diagnostic_dialog.setWindowFlag(Qt.FramelessWindowHint)
            self.diagnostic_dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
            self.diagnostic_dialog.resize(1920, 1050)
            font = QtGui.QFont()
            font.setPointSize(10)
            self.diagnostic_dialog.setFont(font)
            self.diagnostic_dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.diagnostic_dialog.setMouseTracking(False)
            self.diagnostic_dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
            self.diagnostic_dialog.setAutoFillBackground(False)

            self.diag_lbl_title = QtWidgets.QLabel(self.diagnostic_dialog)
            self.diag_lbl_title.setGeometry(QtCore.QRect(770, 10, 300, 40))
            self.diag_lbl_title.setStyleSheet("QLabel {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "}")
            font = QFont("Arial", 17)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.diag_lbl_title.setFont(font)
            self.diag_lbl_title.setAlignment(QtCore.Qt.AlignCenter)
            self.diag_lbl_title.setObjectName("diag_lbl_title")

            self.scroll_area_focusing = QtWidgets.QScrollArea(self.diagnostic_dialog)
            self.scroll_area_focusing.setGeometry(QtCore.QRect(955, 560, 945, 450))
            self.scroll_area_focusing.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.scroll_area_focusing.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.scroll_area_focusing.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.scroll_area_focusing.setWidgetResizable(True)
            self.scroll_area_focusing.setObjectName("scroll_area_focusing")
            self.scroll_area_widget_focusing = QtWidgets.QWidget()
            self.scroll_area_widget_focusing.setGeometry(QtCore.QRect(0, 0, 945, 450))
            self.scroll_area_widget_focusing.setObjectName("scroll_area_widget_focusing")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scroll_area_widget_focusing)
            self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
            self.verticalLayout_2.setSpacing(10)
            self.verticalLayout_2.setObjectName("verticalLayout_2")
            self.diag_lbl_focusing = QtWidgets.QLabel(self.scroll_area_widget_focusing)
            self.diag_lbl_focusing.setMinimumSize(QtCore.QSize(0, 40))
            self.diag_lbl_focusing.setMaximumSize(QtCore.QSize(16777215, 40))
            self.diag_lbl_focusing.setStyleSheet("QLabel {\n"
                                                 "color: rgb(0, 0, 0);\n"
                                                 "}")
            self.diag_lbl_focusing.setText("{}".format("Input status"))
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.diag_lbl_focusing.setFont(font)
            self.diag_lbl_focusing.setAlignment(Qt.AlignCenter)
            self.diag_lbl_focusing.setObjectName("diag_lbl_focusing")
            self.verticalLayout_2.addWidget(self.diag_lbl_focusing)

            self.groupbox_light_panel = QtWidgets.QGroupBox(self.scroll_area_widget_focusing)
            self.groupbox_light_panel.setMinimumSize(QtCore.QSize(0, 160))
            self.groupbox_light_panel.setMaximumSize(QtCore.QSize(16777215, 160))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_light_panel.setFont(font)
            self.groupbox_light_panel.setAlignment(Qt.AlignCenter)
            self.groupbox_light_panel.setStyleSheet("""
                                                    QGroupBox {
                                                        border: 1px solid #333;
                                                        border-radius: 8px;
                                                        color: #333;
                                                        margin-top: 10px;
                                                        text-align: center;
                                                    }
                                                    QGroupBox::title {
                                                        subcontrol-origin: margin;
                                                        subcontrol-position: top center;
                                                        padding: 0 10px;
                                                    }
                                                """)
            self.groupbox_light_panel.setObjectName("groupbox_light_panel")

            self.light_panel_up_btn = QtWidgets.QPushButton(self.groupbox_light_panel)
            self.light_panel_up_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.light_panel_up_btn.setStyleSheet("QPushButton:hover{"
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
            self.light_panel_up_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.light_panel_up_btn.setIcon(icon)
            self.light_panel_up_btn.setIconSize(QtCore.QSize(50, 50))
            self.light_panel_up_btn.setObjectName("light_panel_up_btn")

            self.light_panel_down_btn = QtWidgets.QPushButton(self.groupbox_light_panel)
            self.light_panel_down_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.light_panel_down_btn.setStyleSheet("QPushButton:hover{"
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
            self.light_panel_down_btn.setText("")
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(r".\media\up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.light_panel_down_btn.setIcon(icon1)
            self.light_panel_down_btn.setIconSize(QtCore.QSize(50, 50))
            self.light_panel_down_btn.setObjectName("light_panel_down_btn")

            self.light_panel_low_radioButton = QtWidgets.QRadioButton(self.groupbox_light_panel)
            self.light_panel_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.light_panel_low_radioButton.setFont(font)
            self.light_panel_low_radioButton.setText("5mm")
            self.light_panel_low_radioButton.setStyleSheet("border:0px;")
            self.light_panel_min_radioButton = QtWidgets.QRadioButton(self.groupbox_light_panel)
            self.light_panel_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.light_panel_min_radioButton.setFont(font)
            self.light_panel_min_radioButton.setText("25mm")
            self.light_panel_min_radioButton.setStyleSheet("border:0px;")
            self.light_panel_max_radioButton = QtWidgets.QRadioButton(self.groupbox_light_panel)
            self.light_panel_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.light_panel_max_radioButton.setFont(font)
            self.light_panel_max_radioButton.setStyleSheet("border:0px;")
            self.light_panel_max_radioButton.setText("50mm")
            self.light_panel_none_radioButton = QtWidgets.QRadioButton(self.groupbox_light_panel)
            self.light_panel_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.light_panel_none_radioButton.setFont(font)
            self.light_panel_none_radioButton.setText("None")

            self.light_panel_speed_lbl = QtWidgets.QLabel(self.groupbox_light_panel)
            self.light_panel_speed_lbl.setGeometry(QtCore.QRect(310, 90, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.light_panel_speed_lbl.setFont(font)
            self.light_panel_speed_lbl.setStyleSheet("border:0px;")
            self.light_panel_speed_lbl.setObjectName("light_panel_speed_lbl")
            self.light_panel_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_light_panel)
            self.light_panel_speed_lnedt.setGeometry(QtCore.QRect(310, 110, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.light_panel_speed_lnedt)
            self.light_panel_speed_lnedt.setValidator(validator)
            self.light_panel_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.light_panel_speed_lnedt.setObjectName("light_panel_speed_lnedt")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_light_panel)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(470, 95, 65, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Min. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_light_panel)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(470, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_light_panel)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(620, 95, 70, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Max. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_light_panel)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(620, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("2000 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.light_panel_move_position_lbl = QtWidgets.QLabel(self.groupbox_light_panel)
            self.light_panel_move_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.light_panel_move_position_lbl.setFont(font)
            self.light_panel_move_position_lbl.setText("Position")
            self.light_panel_move_position_lbl.setStyleSheet("border:0px;")
            self.light_panel_move_position_lbl.setObjectName("speed_1")
            self.light_panel_move_position_lndt = QtWidgets.QLineEdit(self.groupbox_light_panel)
            self.light_panel_move_position_lndt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            self.light_panel_move_position_lndt.setText("")
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.light_panel_move_position_lndt)
            self.light_panel_move_position_lndt.textChanged.connect(lambda text: self.change(text, "light_panel"))
            self.light_panel_move_position_lndt.setValidator(validator)
            self.light_panel_move_position_lndt.setStyleSheet("border:1px solid gray;")
            self.light_panel_move_position_lndt.setObjectName("light_panel_move_position_lndt")

            self.min_distance_4 = QtWidgets.QLabel(self.groupbox_light_panel)
            self.min_distance_4.setGeometry(QtCore.QRect(620, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_4.setFont(font)
            self.min_distance_4.setStyleSheet("border:0px;")
            self.min_distance_4.setObjectName("min_distance_4")
            self.light_panel_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_light_panel)
            self.light_panel_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.light_panel_min_distance_lnedt)
            self.light_panel_min_distance_lnedt.setValidator(validator)
            self.light_panel_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.light_panel_min_distance_lnedt.setObjectName("light_panel_min_distance_lnedt")

            self.light_panel_act_position_lbl = QtWidgets.QLabel(self.groupbox_light_panel)
            self.light_panel_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.light_panel_act_position_lbl.setFont(font)
            self.light_panel_act_position_lbl.setStyleSheet("border:0px;")
            self.light_panel_act_position_lbl.setObjectName("act_position_4")
            self.light_panel_act_position_value = QtWidgets.QLabel(self.groupbox_light_panel)
            self.light_panel_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.light_panel_act_position_value.setText("20mm")
            self.light_panel_act_position_value.setStyleSheet("border:0px;")
            self.light_panel_act_position_value.setObjectName("light_panel_act_position_lbl")

            self.max_distance_5 = QtWidgets.QLabel(self.groupbox_light_panel)
            self.max_distance_5.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_5.setFont(font)
            self.max_distance_5.setStyleSheet("border:0px;")
            self.max_distance_5.setObjectName("max_distance_5")
            self.light_panel_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_light_panel)
            self.light_panel_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.light_panel_max_distance_lnedt)
            self.light_panel_max_distance_lnedt.setValidator(validator)
            self.light_panel_max_distance_lnedt.setObjectName("light_panel_max_distance_lnedt")
            self.light_panel_max_distance_lnedt.setStyleSheet("border:1px solid gray;")

            self.light_panel_homing_btn = QtWidgets.QPushButton(self.groupbox_light_panel)
            self.light_panel_homing_btn.setGeometry(QtCore.QRect(770, 100, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.light_panel_homing_btn.setFont(font)
            self.light_panel_homing_btn.setText("Homing")
            self.light_panel_homing_btn.setStyleSheet("QPushButton:enabled{\n"
                                                      "background-color:rgb(92, 98, 224);\n"
                                                      "color:rgb(255, 255, 255);\n"
                                                      "border-radius: 10px;\n"
                                                      "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                      "}"
                                                      "QPushButton:Pressed{\n"
                                                      "padding-left:5px;\n"
                                                      "padding-top:5px;\n"
                                                      "background-color: #1a5276;\n"
                                                      "}"
                                                      "QPushButton:disabled"
                                                      "{"
                                                      "background-color:#95a5a6;"
                                                      "}"
                                                      )
            self.light_panel_homing_btn.setIconSize(QtCore.QSize(50, 50))
            self.light_panel_homing_btn.setObjectName("light_panel_homing_btn")
            self.verticalLayout_2.addWidget(self.groupbox_light_panel)

            self.groupbox_light_panel_intensity = QtWidgets.QGroupBox(self.scroll_area_widget_focusing)
            self.groupbox_light_panel_intensity.setMinimumSize(QtCore.QSize(0, 100))
            self.groupbox_light_panel_intensity.setMaximumSize(QtCore.QSize(16777215, 100))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_light_panel_intensity.setFont(font)
            self.groupbox_light_panel_intensity.setStyleSheet("""
                                                    QGroupBox {
                                                        border: 1px solid #333;
                                                        border-radius: 8px;
                                                        color: #333;
                                                        margin-top: 10px;
                                                        text-align: center;
                                                    }
                                                    QGroupBox::title {
                                                        subcontrol-origin: margin;
                                                        subcontrol-position: top center;
                                                        padding: 0 10px;
                                                    }
                                                """)
            self.groupbox_light_panel_intensity.setObjectName("groupbox_light_panel_intensity")

            self.light_panel_intensity_ok_btn = QtWidgets.QPushButton(self.groupbox_light_panel_intensity)
            self.light_panel_intensity_ok_btn.setGeometry(QtCore.QRect(185, 35, 80, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.light_panel_intensity_ok_btn.setFont(font)
            self.light_panel_intensity_ok_btn.setText("Ok")
            self.light_panel_intensity_ok_btn.setStyleSheet("QPushButton:enabled{\n"
                                                 "background-color:rgb(92, 98, 224);\n"
                                                 "color:rgb(255, 255, 255);\n"
                                                 "border-radius: 10px;\n"
                                                 "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                 "}"
                                                 "QPushButton:Pressed{\n"
                                                 "padding-left:5px;\n"
                                                 "padding-top:5px;\n"
                                                 "background-color: #1a5276;\n"
                                                 "}"
                                                 )
            self.light_panel_intensity_ok_btn.setObjectName("light_panel_intensity_ok_btn")
            self.light_panel_intensity_lbl = QtWidgets.QLabel(self.groupbox_light_panel_intensity)
            self.light_panel_intensity_lbl.setGeometry(QtCore.QRect(20, 15, 100, 30))
            self.light_panel_intensity_lbl.setText("Lux Value")
            font = QtGui.QFont()
            font.setPointSize(10)
            self.light_panel_intensity_lbl.setFont(font)
            self.light_panel_intensity_lbl.setStyleSheet("border:0px;")
            self.light_panel_intensity_lbl.setObjectName("light_panel_act_intensity_lbl")
            self.light_panel_intensity_lbl.setStyleSheet("border:0px;")

            self.light_panel_intensity_lnedt = QtWidgets.QLineEdit(self.groupbox_light_panel_intensity)
            self.light_panel_intensity_lnedt.setGeometry(QtCore.QRect(20, 40, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.light_panel_intensity_lnedt)
            self.light_panel_intensity_lnedt.setValidator(validator)
            self.light_panel_intensity_lnedt.setStyleSheet("border:1px solid gray;")
            self.light_panel_intensity_lnedt.setObjectName("light_panel_intensity_lnedt")
            self.verticalLayout_2.addWidget(self.groupbox_light_panel_intensity)

            self.groupbox_light_panel_intensity_dummy = QtWidgets.QGroupBox(self.scroll_area_widget_focusing)
            self.groupbox_light_panel_intensity_dummy.setMinimumSize(QtCore.QSize(0, 100))
            self.groupbox_light_panel_intensity_dummy.setMaximumSize(QtCore.QSize(16777215, 80))
            self.groupbox_light_panel_intensity_dummy.setStyleSheet("border: 0px;")
            self.groupbox_light_panel_intensity_dummy.setObjectName("groupbox_light_panel_intensity")
            self.verticalLayout_2.addWidget(self.groupbox_light_panel_intensity_dummy)

            self.focusing_save_btn = QtWidgets.QPushButton(self.groupbox_light_panel_intensity)
            self.focusing_save_btn.setGeometry(QtCore.QRect(770, 35, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.focusing_save_btn.setFont(font)
            self.focusing_save_btn.setText("Save")
            self.focusing_save_btn.setStyleSheet("QPushButton:enabled{\n"
                                                 "background-color:rgb(92, 98, 224);\n"
                                                 "color:rgb(255, 255, 255);\n"
                                                 "border-radius: 10px;\n"
                                                 "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                 "}"
                                                 "QPushButton:Pressed{\n"
                                                 "padding-left:5px;\n"
                                                 "padding-top:5px;\n"
                                                 "background-color: #1a5276;\n"
                                                 "}"
                                                 )
            self.focusing_save_btn.setObjectName("curing_save_btn")
            self.scroll_area_focusing.setWidget(self.scroll_area_widget_focusing)

            self.scroll_area_curing = QtWidgets.QScrollArea(self.diagnostic_dialog)
            self.scroll_area_curing.setGeometry(QtCore.QRect(10, 560, 945, 450))
            self.scroll_area_curing.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.scroll_area_curing.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.scroll_area_curing.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.scroll_area_curing.setWidgetResizable(True)
            self.scroll_area_curing.setObjectName("scroll_area_curing")
            self.scroll_area_widget_curing = QtWidgets.QWidget()
            self.scroll_area_widget_curing.setGeometry(QtCore.QRect(0, 0, 945, 450))
            self.scroll_area_widget_curing.setObjectName("scroll_area_widget_curing")
            self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scroll_area_widget_curing)
            self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
            self.verticalLayout_3.setSpacing(10)
            self.verticalLayout_3.setObjectName("verticalLayout_3")
            self.diag_lbl_station_4 = QtWidgets.QLabel(self.scroll_area_widget_curing)
            self.diag_lbl_station_4.setMinimumSize(QtCore.QSize(0, 40))
            self.diag_lbl_station_4.setMaximumSize(QtCore.QSize(16777215, 40))
            self.diag_lbl_station_4.setStyleSheet("QLabel {\n"
                                                  "color: rgb(0, 0, 0);\n"
                                                  "}")
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.diag_lbl_station_4.setFont(font)
            self.diag_lbl_station_4.setAlignment(QtCore.Qt.AlignCenter)
            self.diag_lbl_station_4.setObjectName("diag_lbl_station_4")
            self.verticalLayout_3.addWidget(self.diag_lbl_station_4)
            self.groupbox_uv_z_axis = QtWidgets.QGroupBox(self.scroll_area_widget_curing)
            self.groupbox_uv_z_axis.setMinimumSize(QtCore.QSize(0, 160))
            self.groupbox_uv_z_axis.setMaximumSize(QtCore.QSize(16777215, 160))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_uv_z_axis.setFont(font)
            self.groupbox_uv_z_axis.setAlignment(Qt.AlignCenter)
            self.groupbox_uv_z_axis.setStyleSheet("""
                                                    QGroupBox {
                                                        border: 1px solid #333;
                                                        border-radius: 8px;
                                                        color: #333;
                                                        margin-top: 10px;
                                                        text-align: center;
                                                    }
                                                    QGroupBox::title {
                                                        subcontrol-origin: margin;
                                                        subcontrol-position: top center;
                                                        padding: 0 10px;
                                                    }
                                                """)
            self.groupbox_uv_z_axis.setObjectName("groupbox_uv_z_axis")

            self.uv_z_axis_up_btn = QtWidgets.QPushButton(self.groupbox_uv_z_axis)
            self.uv_z_axis_up_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.uv_z_axis_up_btn.setStyleSheet("QPushButton:hover{"
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
            self.uv_z_axis_up_btn.setText("")
            self.uv_z_axis_up_btn.setIcon(icon)
            self.uv_z_axis_up_btn.setIconSize(QtCore.QSize(50, 50))
            self.uv_z_axis_up_btn.setObjectName("uv_z_axis_up_btn")
            self.uv_z_axis_down_btn = QtWidgets.QPushButton(self.groupbox_uv_z_axis)
            self.uv_z_axis_down_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.uv_z_axis_down_btn.setStyleSheet("QPushButton:hover{"
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
            self.uv_z_axis_down_btn.setText("")
            self.uv_z_axis_down_btn.setIcon(icon1)
            self.uv_z_axis_down_btn.setIconSize(QtCore.QSize(50, 50))
            self.uv_z_axis_down_btn.setObjectName("uv_z_axis_down_btn")

            self.uv_z_axis_low_radioButton = QtWidgets.QRadioButton(self.groupbox_uv_z_axis)
            self.uv_z_axis_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_z_axis_low_radioButton.setFont(font)
            self.uv_z_axis_low_radioButton.setText("5mm")
            self.uv_z_axis_min_radioButton = QtWidgets.QRadioButton(self.groupbox_uv_z_axis)
            self.uv_z_axis_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_z_axis_min_radioButton.setFont(font)
            self.uv_z_axis_min_radioButton.setText("10mm")
            self.uv_z_axis_max_radioButton = QtWidgets.QRadioButton(self.groupbox_uv_z_axis)
            self.uv_z_axis_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_z_axis_max_radioButton.setFont(font)
            self.uv_z_axis_max_radioButton.setText("20mm")
            self.uv_z_axis_none_radioButton = QtWidgets.QRadioButton(self.groupbox_uv_z_axis)
            self.uv_z_axis_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_z_axis_none_radioButton.setFont(font)
            self.uv_z_axis_none_radioButton.setText("None")

            self.uv_z_axis_speed_lbl = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.uv_z_axis_speed_lbl.setGeometry(QtCore.QRect(310, 90, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_z_axis_speed_lbl.setFont(font)
            self.uv_z_axis_speed_lbl.setObjectName("uv_z_axis_speed_lbl")
            self.uv_z_axis_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_uv_z_axis)
            self.uv_z_axis_speed_lnedt.setGeometry(QtCore.QRect(310, 110, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.uv_z_axis_speed_lnedt)
            self.uv_z_axis_speed_lnedt.setValidator(validator)
            self.uv_z_axis_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.uv_z_axis_speed_lnedt.setObjectName("uv_z_axis_speed_lnedt")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(470, 95, 65, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Min. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(470, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(620, 95, 70, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Max. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(620, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("2000 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.uv_z_axis_move_position_lbl = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.uv_z_axis_move_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_z_axis_move_position_lbl.setFont(font)
            self.uv_z_axis_move_position_lbl.setText("Position")
            self.uv_z_axis_move_position_lbl.setObjectName("speed_1")
            self.uv_z_axis_move_position_lndt = QtWidgets.QLineEdit(self.groupbox_uv_z_axis)
            self.uv_z_axis_move_position_lndt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            self.uv_z_axis_move_position_lndt.setText("")
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.uv_z_axis_move_position_lndt)
            self.uv_z_axis_move_position_lndt.setValidator(validator)
            self.uv_z_axis_move_position_lndt.textChanged.connect(lambda text: self.change(text, "uv z-axis"))
            self.uv_z_axis_move_position_lndt.setStyleSheet("border:1px solid gray;")
            self.uv_z_axis_move_position_lndt.setObjectName("uv_z_axis_move_position_lndt")

            self.uv_z_axis_act_position_lbl = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.uv_z_axis_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_z_axis_act_position_lbl.setFont(font)
            self.uv_z_axis_act_position_lbl.setObjectName("uv_z_axis_act_position_lbl")
            self.uv_z_axis_act_position_value = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.uv_z_axis_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.uv_z_axis_act_position_value.setText("20mm")
            self.uv_z_axis_act_position_value.setObjectName("uv_z_axis_act_position_value")

            self.min_distance_6 = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.min_distance_6.setGeometry(QtCore.QRect(620, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_6.setFont(font)
            self.min_distance_6.setObjectName("min_distance_6")
            self.uv_z_axis_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_uv_z_axis)
            self.uv_z_axis_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.uv_z_axis_min_distance_lnedt)
            self.uv_z_axis_min_distance_lnedt.setValidator(validator)
            self.uv_z_axis_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.uv_z_axis_min_distance_lnedt.setObjectName("uv_z_axis_min_distance_lnedt")

            self.max_distance_7 = QtWidgets.QLabel(self.groupbox_uv_z_axis)
            self.max_distance_7.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_7.setFont(font)
            self.max_distance_7.setObjectName("max_distance_7")
            self.uv_z_axis_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_uv_z_axis)
            self.uv_z_axis_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.uv_z_axis_max_distance_lnedt)
            self.uv_z_axis_max_distance_lnedt.setValidator(validator)
            self.uv_z_axis_max_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.uv_z_axis_max_distance_lnedt.setObjectName("uv_z_axis_max_distance_lnedt")

            self.uv_z_axis_homing_btn = QtWidgets.QPushButton(self.groupbox_uv_z_axis)
            self.uv_z_axis_homing_btn.setGeometry(QtCore.QRect(770, 100, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.uv_z_axis_homing_btn.setFont(font)
            self.uv_z_axis_homing_btn.setText("Homing")
            self.uv_z_axis_homing_btn.setStyleSheet("QPushButton:enabled{\n"
                                                    "background-color:rgb(92, 98, 224);\n"
                                                    "color:rgb(255, 255, 255);\n"
                                                    "border-radius: 10px;\n"
                                                    "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                    "}"
                                                    "QPushButton:Pressed{\n"
                                                    "padding-left:5px;\n"
                                                    "padding-top:5px;\n"
                                                    "background-color: #1a5276;\n"
                                                    "}"
                                                    "QPushButton:disabled"
                                                    "{"
                                                    "background-color:#95a5a6;"
                                                    "}"
                                                    )
            self.uv_z_axis_homing_btn.setIconSize(QtCore.QSize(50, 50))
            self.uv_z_axis_homing_btn.setObjectName("uv_z_axis_homing_btn")

            self.verticalLayout_3.addWidget(self.groupbox_uv_z_axis)

            self.groupbox_uv_left_cylinder = QtWidgets.QGroupBox(self.scroll_area_widget_curing)
            self.groupbox_uv_left_cylinder.setMinimumSize(QtCore.QSize(0, 100))
            self.groupbox_uv_left_cylinder.setMaximumSize(QtCore.QSize(16777215, 100))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_uv_left_cylinder.setFont(font)
            self.groupbox_uv_left_cylinder.setAlignment(Qt.AlignCenter)
            self.groupbox_uv_left_cylinder.setStyleSheet("""
                                                        QGroupBox {
                                                            border: 1px solid #333;
                                                            border-radius: 8px;
                                                            color: #333;
                                                            margin-top: 10px;
                                                            text-align: center;
                                                        }
                                                        QGroupBox::title {
                                                            subcontrol-origin: margin;
                                                            subcontrol-position: top center;
                                                            padding: 0 10px;
                                                        }
                                                    """)
            self.groupbox_uv_left_cylinder.setObjectName("groupbox_uv_left_cylinder")

            self.act_position_10 = QtWidgets.QLabel(self.groupbox_uv_left_cylinder)
            self.act_position_10.setGeometry(QtCore.QRect(310, 30, 121, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.act_position_10.setFont(font)
            self.act_position_10.setObjectName("act_position_10")

            self.uv_left_cylinder_act_position_lbl = QtWidgets.QLabel(self.groupbox_uv_left_cylinder)
            self.uv_left_cylinder_act_position_lbl.setGeometry(QtCore.QRect(310, 50, 141, 30))
            font = QtGui.QFont()
            font.setPointSize(11)
            self.uv_left_cylinder_act_position_lbl.setFont(font)
            self.uv_left_cylinder_act_position_lbl.setObjectName("uv_left_cylinder_act_position_lbl")
            self.uv_door_cylinder_open_btn = QtWidgets.QPushButton(self.groupbox_uv_left_cylinder)
            self.uv_door_cylinder_open_btn.setGeometry(QtCore.QRect(195, 35, 50, 50))
            self.uv_door_cylinder_open_btn.setStyleSheet("QPushButton:hover{"
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
            self.uv_door_cylinder_open_btn.setText("")
            self.uv_door_cylinder_open_btn.setIcon(icon1)
            self.uv_door_cylinder_open_btn.setIconSize(QtCore.QSize(50, 50))
            self.uv_door_cylinder_open_btn.setObjectName("uv_door_cylinder_open_btn")
            self.uv_door_cylinder_close_btn = QtWidgets.QPushButton(self.groupbox_uv_left_cylinder)
            self.uv_door_cylinder_close_btn.setGeometry(QtCore.QRect(55, 35, 50, 50))
            self.uv_door_cylinder_close_btn.setStyleSheet("QPushButton:hover{"
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
            self.uv_door_cylinder_close_btn.setText("")
            self.uv_door_cylinder_close_btn.setIcon(icon)
            self.uv_door_cylinder_close_btn.setIconSize(QtCore.QSize(50, 50))
            self.uv_door_cylinder_close_btn.setObjectName("uv_door_cylinder_close_btn")
            self.verticalLayout_3.addWidget(self.groupbox_uv_left_cylinder)

            self.groupbox_uv_curing = QtWidgets.QGroupBox(self.scroll_area_widget_curing)
            self.groupbox_uv_curing.setMinimumSize(QtCore.QSize(0, 100))
            self.groupbox_uv_curing.setMaximumSize(QtCore.QSize(16777215, 100))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_uv_curing.setFont(font)
            self.groupbox_uv_curing.setAlignment(Qt.AlignCenter)
            self.groupbox_uv_curing.setStyleSheet("""
                                                QGroupBox {
                                                    border: 1px solid #333;
                                                    border-radius: 8px;
                                                    color: #333;
                                                    margin-top: 10px;
                                                    text-align: center;
                                                }
                                                QGroupBox::title {
                                                    subcontrol-origin: margin;
                                                    subcontrol-position: top center;
                                                    padding: 0 10px;
                                                }
                                            """)
            self.groupbox_uv_curing.setObjectName("groupbox_uv_curing")

            self.uv_curing_time_lbl = QtWidgets.QLabel(self.groupbox_uv_curing)
            self.uv_curing_time_lbl.setGeometry(QtCore.QRect(30, 30, 101, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_curing_time_lbl.setFont(font)
            self.uv_curing_time_lbl.setText("Curing Time")
            self.uv_curing_time_lbl.setObjectName("uv_curing_time_lbl")
            self.uv_curing_time_lndt = QtWidgets.QLineEdit(self.groupbox_uv_curing)
            self.uv_curing_time_lndt.setGeometry(QtCore.QRect(30, 50, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.uv_curing_time_lndt)
            self.uv_curing_time_lndt.setValidator(validator)
            self.uv_curing_time_lndt.setStyleSheet("border:1px solid gray;")
            self.uv_curing_time_lndt.setObjectName("uv_curing_time_lndt")

            self.uv_curing_intensity_lbl = QtWidgets.QLabel(self.groupbox_uv_curing)
            self.uv_curing_intensity_lbl.setGeometry(QtCore.QRect(180, 30, 101, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.uv_curing_intensity_lbl.setFont(font)
            self.uv_curing_intensity_lbl.setText("Curing Intensity")
            self.uv_curing_intensity_lbl.setObjectName("uv_curing_intensity_lbl")
            self.uv_curing_intensity_lndt = QtWidgets.QLineEdit(self.groupbox_uv_curing)
            self.uv_curing_intensity_lndt.setGeometry(QtCore.QRect(180, 50, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.uv_curing_intensity_lndt)
            self.uv_curing_intensity_lndt.setValidator(validator)
            self.uv_curing_intensity_lndt.setStyleSheet("border:1px solid gray;")
            self.uv_curing_intensity_lndt.setObjectName("uv_curing_intensity_lndt")

            self.uv_curing_btn = QtWidgets.QPushButton(self.groupbox_uv_curing)
            self.uv_curing_btn.setGeometry(QtCore.QRect(350, 40, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.uv_curing_btn.setFont(font)
            self.uv_curing_btn.setStyleSheet("QPushButton:enabled{\n"
                                             "background-color:rgb(92, 98, 224);\n"
                                             "color:rgb(255, 255, 255);\n"
                                             "border-radius: 10px;\n"
                                             "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                             "}"
                                             "QPushButton:Pressed{\n"
                                             "padding-left:5px;\n"
                                             "padding-top:5px;\n"
                                             "background-color: #1a5276;\n"
                                             "}"
                                             "QPushButton:disabled"
                                             "{"
                                             "background-color:#95a5a6;"
                                             "}"
                                             )
            self.uv_curing_btn.setIconSize(QtCore.QSize(50, 50))
            self.uv_curing_btn.setObjectName("uv_curing_btn")

            self.curing_save_btn = QtWidgets.QPushButton(self.groupbox_uv_curing)
            self.curing_save_btn.setGeometry(QtCore.QRect(770, 40, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.curing_save_btn.setFont(font)
            self.curing_save_btn.setText("Save")
            self.curing_save_btn.setStyleSheet("QPushButton:enabled{\n"
                                               "background-color:rgb(92, 98, 224);\n"
                                               "color:rgb(255, 255, 255);\n"
                                               "border-radius: 10px;\n"
                                               "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                               "}"
                                               "QPushButton:Pressed{\n"
                                               "padding-left:5px;\n"
                                               "padding-top:5px;\n"
                                               "background-color: #1a5276;\n"
                                               "}"
                                               )
            self.curing_save_btn.setIconSize(QtCore.QSize(50, 50))
            self.curing_save_btn.setObjectName("curing_save_btn")
            self.verticalLayout_3.addWidget(self.groupbox_uv_curing)
            self.scroll_area_curing.setWidget(self.scroll_area_widget_curing)

            self.scroll_area_gluing = QtWidgets.QScrollArea(self.diagnostic_dialog)
            self.scroll_area_gluing.setGeometry(QtCore.QRect(955, 60, 945, 500))
            self.scroll_area_gluing.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_area_gluing.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_area_gluing.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.scroll_area_gluing.setWidgetResizable(True)
            self.scroll_area_gluing.setObjectName("scroll_area_gluing")
            self.scroll_area_widget_gluing = QtWidgets.QWidget()
            self.scroll_area_widget_gluing.setGeometry(QtCore.QRect(0, 0, 945, 500))
            self.scroll_area_widget_gluing.setObjectName("scroll_area_widget_gluing")
            self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scroll_area_widget_gluing)
            self.verticalLayout_4.setObjectName("verticalLayout_4")
            self.diag_lbl_gluing = QtWidgets.QLabel(self.scroll_area_widget_gluing)
            self.diag_lbl_gluing.setMinimumSize(QtCore.QSize(0, 40))
            self.diag_lbl_gluing.setMaximumSize(QtCore.QSize(16777215, 40))
            self.diag_lbl_gluing.setStyleSheet("QLabel {\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "}")
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.diag_lbl_gluing.setFont(font)
            self.diag_lbl_gluing.setAlignment(Qt.AlignCenter)
            self.diag_lbl_gluing.setObjectName("diag_lbl_gluing")
            self.verticalLayout_4.addWidget(self.diag_lbl_gluing)

            self.groupbox_gd_z_axis = QtWidgets.QGroupBox(self.scroll_area_widget_gluing)
            self.groupbox_gd_z_axis.setMinimumSize(QtCore.QSize(0, 150))
            self.groupbox_gd_z_axis.setMaximumSize(QtCore.QSize(16777215, 150))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_gd_z_axis.setFont(font)
            self.groupbox_gd_z_axis.setAlignment(Qt.AlignCenter)
            self.groupbox_gd_z_axis.setStyleSheet("""
                                                    QGroupBox {
                                                        border: 1px solid #333;
                                                        border-radius: 8px;
                                                        color: #333;
                                                        margin-top: 10px;
                                                        text-align: center;
                                                    }
                                                    QGroupBox::title {
                                                        subcontrol-origin: margin;
                                                        subcontrol-position: top center;
                                                        padding: 0 10px;
                                                    }
                                                """)
            self.groupbox_gd_z_axis.setObjectName("groupbox_gd_z_axis")

            self.gd_z_axis_up_btn = QtWidgets.QPushButton(self.groupbox_gd_z_axis)
            self.gd_z_axis_up_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.gd_z_axis_up_btn.setStyleSheet("QPushButton:hover{"
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
            self.gd_z_axis_up_btn.setText("")
            self.gd_z_axis_up_btn.setIcon(icon)
            self.gd_z_axis_up_btn.setIconSize(QtCore.QSize(50, 50))
            self.gd_z_axis_up_btn.setObjectName("gd_z_axis_up_btn")
            self.gd_z_axis_down_btn = QtWidgets.QPushButton(self.groupbox_gd_z_axis)
            self.gd_z_axis_down_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.gd_z_axis_down_btn.setStyleSheet("QPushButton:hover{"
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
            self.gd_z_axis_down_btn.setText("")
            self.gd_z_axis_down_btn.setIcon(icon1)
            self.gd_z_axis_down_btn.setIconSize(QtCore.QSize(50, 50))
            self.gd_z_axis_down_btn.setObjectName("gd_z_axis_down_btn")

            self.gd_z_axis_low_radioButton = QtWidgets.QRadioButton(self.groupbox_gd_z_axis)
            self.gd_z_axis_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gd_z_axis_low_radioButton.setFont(font)
            self.gd_z_axis_low_radioButton.setText("5mm")
            self.gd_z_axis_min_radioButton = QtWidgets.QRadioButton(self.groupbox_gd_z_axis)
            self.gd_z_axis_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gd_z_axis_min_radioButton.setFont(font)
            self.gd_z_axis_min_radioButton.setText("10mm")
            self.gd_z_axis_max_radioButton = QtWidgets.QRadioButton(self.groupbox_gd_z_axis)
            self.gd_z_axis_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gd_z_axis_max_radioButton.setFont(font)
            self.gd_z_axis_max_radioButton.setText("20mm")
            self.gd_z_axis_none_radioButton = QtWidgets.QRadioButton(self.groupbox_gd_z_axis)
            self.gd_z_axis_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gd_z_axis_none_radioButton.setFont(font)
            self.gd_z_axis_none_radioButton.setText("None")

            self.gd_z_axis_speed_lbl = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.gd_z_axis_speed_lbl.setGeometry(QtCore.QRect(310, 90, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gd_z_axis_speed_lbl.setFont(font)
            self.gd_z_axis_speed_lbl.setObjectName("gd_z_axis_speed_lbl")
            self.gd_z_axis_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_gd_z_axis)
            self.gd_z_axis_speed_lnedt.setGeometry(QtCore.QRect(310, 110, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gd_z_axis_speed_lnedt)
            self.gd_z_axis_speed_lnedt.setValidator(validator)
            self.gd_z_axis_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.gd_z_axis_speed_lnedt.setObjectName("gd_z_axis_speed_lnedt")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(470, 95, 65, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Min. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(470, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(620, 95, 70, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Max. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(620, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("2000 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.gd_z_axis_move_position_lbl = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.gd_z_axis_move_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gd_z_axis_move_position_lbl.setFont(font)
            self.gd_z_axis_move_position_lbl.setText("Position")
            self.gd_z_axis_move_position_lbl.setObjectName("speed_1")
            self.gd_z_axis_move_position_lndt = QtWidgets.QLineEdit(self.groupbox_gd_z_axis)
            self.gd_z_axis_move_position_lndt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            self.gd_z_axis_move_position_lndt.setText("")
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gd_z_axis_move_position_lndt)
            self.gd_z_axis_move_position_lndt.setValidator(validator)
            self.gd_z_axis_move_position_lndt.textChanged.connect(lambda text: self.change(text, "gd z-axis"))
            self.gd_z_axis_move_position_lndt.setStyleSheet("border:1px solid gray;")
            self.gd_z_axis_move_position_lndt.setObjectName("gd_z_axis_move_position_lndt")

            self.min_distance_5 = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.min_distance_5.setGeometry(QtCore.QRect(620, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_5.setFont(font)
            self.min_distance_5.setText("Min. distance(mm)")
            self.min_distance_5.setObjectName("min_distance_5")
            self.gd_z_axis_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gd_z_axis)
            self.gd_z_axis_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gd_z_axis_min_distance_lnedt)
            self.gd_z_axis_min_distance_lnedt.setValidator(validator)
            self.gd_z_axis_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gd_z_axis_min_distance_lnedt.setObjectName("gd_z_axis_min_distance_lnedt")

            self.gd_z_axis_act_position_lbl = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.gd_z_axis_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 110, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gd_z_axis_act_position_lbl.setFont(font)
            self.gd_z_axis_act_position_lbl.setText("Actual Position")
            self.gd_z_axis_act_position_lbl.setObjectName("gd_z_axis_act_position_lbl")
            self.gd_z_axis_act_position_value = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.gd_z_axis_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.gd_z_axis_act_position_value.setText("20mm")
            self.gd_z_axis_act_position_value.setObjectName("gd_z_axis_act_position_lbl")

            self.max_distance_6 = QtWidgets.QLabel(self.groupbox_gd_z_axis)
            self.max_distance_6.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_6.setFont(font)
            self.max_distance_6.setText("Max. distance(mm)")
            self.max_distance_6.setObjectName("max_distance_6")
            self.gd_z_axis_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gd_z_axis)
            self.gd_z_axis_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gd_z_axis_max_distance_lnedt)
            self.gd_z_axis_max_distance_lnedt.setValidator(validator)
            self.gd_z_axis_max_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gd_z_axis_max_distance_lnedt.setObjectName("gd_z_axis_max_distance_lnedt")

            self.gd_z_axis_homing_btn = QtWidgets.QPushButton(self.groupbox_gd_z_axis)
            self.gd_z_axis_homing_btn.setGeometry(QtCore.QRect(770, 100, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.gd_z_axis_homing_btn.setFont(font)
            self.gd_z_axis_homing_btn.setText("Homing")
            self.gd_z_axis_homing_btn.setStyleSheet("QPushButton:enabled{\n"
                                                    "background-color:rgb(92, 98, 224);\n"
                                                    "color:rgb(255, 255, 255);\n"
                                                    "border-radius: 10px;\n"
                                                    "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                    "}"
                                                    "QPushButton:Pressed{\n"
                                                    "padding-left:5px;\n"
                                                    "padding-top:5px;\n"
                                                    "background-color: #1a5276;\n"
                                                    "}"
                                                    "QPushButton:disabled"
                                                    "{"
                                                    "background-color:#95a5a6;"
                                                    "}"
                                                    )
            self.gd_z_axis_homing_btn.setIconSize(QtCore.QSize(50, 50))
            self.gd_z_axis_homing_btn.setObjectName("gd_z_axis_homing_btn")

            self.verticalLayout_4.addWidget(self.groupbox_gd_z_axis)

            self.groupbox_gluing_x1 = QtWidgets.QGroupBox(self.scroll_area_widget_gluing)
            self.groupbox_gluing_x1.setMinimumSize(QtCore.QSize(0, 150))
            self.groupbox_gluing_x1.setMaximumSize(QtCore.QSize(16777215, 150))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_gluing_x1.setFont(font)
            self.groupbox_gluing_x1.setAlignment(Qt.AlignCenter)
            self.groupbox_gluing_x1.setStyleSheet("""
                                                    QGroupBox {
                                                        border: 1px solid #333;
                                                        border-radius: 8px;
                                                        color: #333;
                                                        margin-top: 10px;
                                                        text-align: center;
                                                    }
                                                    QGroupBox::title {
                                                        subcontrol-origin: margin;
                                                        subcontrol-position: top center;
                                                        padding: 0 10px;
                                                    }
                                                """)
            self.groupbox_gluing_x1.setObjectName("groupbox_gluing_x1")
            self.gluing_x1_up_btn = QtWidgets.QPushButton(self.groupbox_gluing_x1)
            self.gluing_x1_up_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.gluing_x1_up_btn.setStyleSheet("QPushButton:hover{"
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
            self.gluing_x1_up_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.gluing_x1_up_btn.setIcon(icon)
            self.gluing_x1_up_btn.setIconSize(QtCore.QSize(50, 50))
            self.gluing_x1_up_btn.setObjectName("gluing_x1_up_btn")
            self.gluing_x1_down_btn = QtWidgets.QPushButton(self.groupbox_gluing_x1)
            self.gluing_x1_down_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.gluing_x1_down_btn.setStyleSheet("QPushButton:hover{"
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
            self.gluing_x1_down_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.gluing_x1_down_btn.setIcon(icon)
            self.gluing_x1_down_btn.setIconSize(QtCore.QSize(50, 50))
            self.gluing_x1_down_btn.setObjectName("gluing_x1_down_btn")
            self.gluing_x1_low_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_x1)
            self.gluing_x1_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x1_low_radioButton.setFont(font)
            self.gluing_x1_low_radioButton.setText("0.5mm")
            self.gluing_x1_min_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_x1)
            self.gluing_x1_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x1_min_radioButton.setFont(font)
            self.gluing_x1_min_radioButton.setText("3mm")
            self.gluing_x1_max_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_x1)
            self.gluing_x1_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x1_max_radioButton.setFont(font)
            self.gluing_x1_max_radioButton.setText("5mm")
            self.gluing_x1_none_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_x1)
            self.gluing_x1_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x1_none_radioButton.setFont(font)
            self.gluing_x1_none_radioButton.setText("None")
            self.gluing_x1_speed_lbl = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.gluing_x1_speed_lbl.setGeometry(QtCore.QRect(310, 90, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x1_speed_lbl.setFont(font)
            self.gluing_x1_speed_lbl.setText("Speed")
            self.gluing_x1_speed_lbl.setObjectName("gluing_x1_speed_lbl")
            self.gluing_x1_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_x1)
            self.gluing_x1_speed_lnedt.setGeometry(QtCore.QRect(310, 110, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_x1_speed_lnedt)
            self.gluing_x1_speed_lnedt.setValidator(validator)
            self.gluing_x1_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_x1_speed_lnedt.setObjectName("gluing_x1_speed_lnedt")

            self.gluing_x1_move_position_lbl = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.gluing_x1_move_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x1_move_position_lbl.setFont(font)
            self.gluing_x1_move_position_lbl.setText("Position")
            self.gluing_x1_move_position_lbl.setObjectName("speed_1")
            self.gluing_x1_move_position_lndt = QtWidgets.QLineEdit(self.groupbox_gluing_x1)
            self.gluing_x1_move_position_lndt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            self.gluing_x1_move_position_lndt.setText("")
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_x1_move_position_lndt)
            self.gluing_x1_move_position_lndt.setValidator(validator)
            self.gluing_x1_move_position_lndt.textChanged.connect(lambda text: self.change(text, "gluing x1"))
            self.gluing_x1_move_position_lndt.setStyleSheet("border:1px solid gray;")
            self.gluing_x1_move_position_lndt.setObjectName("gluing_x1_move_position_lndt")

            self.min_distance_2 = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.min_distance_2.setGeometry(QtCore.QRect(620, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_2.setFont(font)
            self.min_distance_2.setText("Min. distance(mm)")
            self.min_distance_2.setObjectName("min_distance_2")
            self.gluing_x1_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_x1)
            self.gluing_x1_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_x1_min_distance_lnedt)
            self.gluing_x1_min_distance_lnedt.setValidator(validator)
            self.gluing_x1_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_x1_min_distance_lnedt.setObjectName("gluing_x1_min_distance_lnedt")

            self.gluing_x1_act_position_lbl = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.gluing_x1_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x1_act_position_lbl.setFont(font)
            self.gluing_x1_act_position_lbl.setText("Actual Position")
            self.gluing_x1_act_position_lbl.setObjectName("gluing_x1_act_position_lbl")
            self.gluing_x1_act_position_value = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.gluing_x1_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.gluing_x1_act_position_value.setText("20mm")
            self.gluing_x1_act_position_value.setObjectName("gluing_x1_act_position_value")

            self.max_distance_3 = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.max_distance_3.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_3.setFont(font)
            self.max_distance_3.setText("Max. distance(mm)")
            self.max_distance_3.setObjectName("max_distance_3")
            self.gluing_x1_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_x1)
            self.gluing_x1_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_x1_max_distance_lnedt)
            self.gluing_x1_max_distance_lnedt.setValidator(validator)
            self.gluing_x1_max_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_x1_max_distance_lnedt.setObjectName("gluing_x1_max_distance_lnedt")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(470, 95, 65, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Min. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(470, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(620, 95, 70, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Max. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_gluing_x1)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(620, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1000 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")
            self.verticalLayout_4.addWidget(self.groupbox_gluing_x1)

            self.groupbox_gluing_x2 = QtWidgets.QGroupBox(self.scroll_area_widget_gluing)
            self.groupbox_gluing_x2.setMinimumSize(QtCore.QSize(0, 150))
            self.groupbox_gluing_x2.setMaximumSize(QtCore.QSize(16777215, 150))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_gluing_x2.setFont(font)
            self.groupbox_gluing_x2.setAlignment(Qt.AlignCenter)
            self.groupbox_gluing_x2.setStyleSheet("""
                                                    QGroupBox {
                                                        border: 1px solid #333;
                                                        border-radius: 8px;
                                                        color: #333;
                                                        margin-top: 10px;
                                                        text-align: center;
                                                    }
                                                    QGroupBox::title {
                                                        subcontrol-origin: margin;
                                                        subcontrol-position: top center;
                                                        padding: 0 10px;
                                                    }
                                                """)
            self.groupbox_gluing_x2.setObjectName("groupbox_gluing_x2")
            self.gluing_x2_up_btn = QtWidgets.QPushButton(self.groupbox_gluing_x2)
            self.gluing_x2_up_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.gluing_x2_up_btn.setStyleSheet("QPushButton:hover{"
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
            self.gluing_x2_up_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.gluing_x2_up_btn.setIcon(icon)
            self.gluing_x2_up_btn.setIconSize(QtCore.QSize(50, 50))
            self.gluing_x2_up_btn.setObjectName("gluing_x2_up_btn")
            self.gluing_x2_down_btn = QtWidgets.QPushButton(self.groupbox_gluing_x2)
            self.gluing_x2_down_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.gluing_x2_down_btn.setStyleSheet("QPushButton:hover{"
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
            self.gluing_x2_down_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.gluing_x2_down_btn.setIcon(icon)
            self.gluing_x2_down_btn.setIconSize(QtCore.QSize(50, 50))
            self.gluing_x2_down_btn.setObjectName("gluing_x2_down_btn")
            self.gluing_x2_low_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_x2)
            self.gluing_x2_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x2_low_radioButton.setFont(font)
            self.gluing_x2_low_radioButton.setText("0.5mm")
            self.gluing_x2_min_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_x2)
            self.gluing_x2_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x2_min_radioButton.setFont(font)
            self.gluing_x2_min_radioButton.setText("3mm")
            self.gluing_x2_max_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_x2)
            self.gluing_x2_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x2_max_radioButton.setFont(font)
            self.gluing_x2_max_radioButton.setText("5mm")
            self.gluing_x2_none_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_x2)
            self.gluing_x2_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x2_none_radioButton.setFont(font)
            self.gluing_x2_none_radioButton.setText("None")
            self.gluing_x2_speed_lbl = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.gluing_x2_speed_lbl.setGeometry(QtCore.QRect(310, 90, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x2_speed_lbl.setFont(font)
            self.gluing_x2_speed_lbl.setText("Speed")
            self.gluing_x2_speed_lbl.setObjectName("gluing_x2_speed_lbl")
            self.gluing_x2_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_x2)
            self.gluing_x2_speed_lnedt.setGeometry(QtCore.QRect(310, 110, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_x2_speed_lnedt)
            self.gluing_x2_speed_lnedt.setValidator(validator)
            self.gluing_x2_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_x2_speed_lnedt.setObjectName("gluing_x2_speed_lnedt")

            self.gluing_x2_move_position_lbl = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.gluing_x2_move_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x2_move_position_lbl.setFont(font)
            self.gluing_x2_move_position_lbl.setText("Position")
            self.gluing_x2_move_position_lbl.setObjectName("speed_1")
            self.gluing_x2_move_position_lndt = QtWidgets.QLineEdit(self.groupbox_gluing_x2)
            self.gluing_x2_move_position_lndt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            self.gluing_x2_move_position_lndt.setText("")
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_x2_move_position_lndt)
            self.gluing_x2_move_position_lndt.setValidator(validator)
            self.gluing_x2_move_position_lndt.setStyleSheet("border:1px solid gray;")
            self.gluing_x2_move_position_lndt.setObjectName("gluing_x2_move_position_lndt")

            self.min_distance_2 = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.min_distance_2.setGeometry(QtCore.QRect(620, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_2.setFont(font)
            self.min_distance_2.setText("Min. distance(mm)")
            self.min_distance_2.setObjectName("min_distance_2")
            self.gluing_x2_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_x2)
            self.gluing_x2_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_x2_min_distance_lnedt)
            self.gluing_x2_min_distance_lnedt.setValidator(validator)
            self.gluing_x2_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_x2_min_distance_lnedt.setObjectName("gluing_x2_min_distance_lnedt")

            self.gluing_x2_act_position_lbl = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.gluing_x2_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_x2_act_position_lbl.setFont(font)
            self.gluing_x2_act_position_lbl.setText("Actual Position")
            self.gluing_x2_act_position_lbl.setObjectName("gluing_x2_act_position_lbl")
            self.gluing_x2_act_position_value = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.gluing_x2_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.gluing_x2_act_position_value.setText("20mm")
            self.gluing_x2_act_position_value.setObjectName("gluing_x2_act_position_value")

            self.max_distance_3 = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.max_distance_3.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_3.setFont(font)
            self.max_distance_3.setText("Max. distance(mm)")
            self.max_distance_3.setObjectName("max_distance_3")
            self.gluing_x2_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_x2)
            self.gluing_x2_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_x2_max_distance_lnedt)
            self.gluing_x2_max_distance_lnedt.setValidator(validator)
            self.gluing_x2_max_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_x2_max_distance_lnedt.setObjectName("gluing_x2_max_distance_lnedt")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(470, 95, 65, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Min. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(470, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(620, 95, 70, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Max. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_gluing_x2)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(620, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1000 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")
            self.verticalLayout_4.addWidget(self.groupbox_gluing_x2)

            self.groupbox_gluing_y = QtWidgets.QGroupBox(self.scroll_area_widget_gluing)
            self.groupbox_gluing_y.setMinimumSize(QtCore.QSize(0, 150))
            self.groupbox_gluing_y.setMaximumSize(QtCore.QSize(16777215, 150))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_gluing_y.setFont(font)
            self.groupbox_gluing_y.setAlignment(Qt.AlignCenter)
            self.groupbox_gluing_y.setStyleSheet("""
                                                                QGroupBox {
                                                                    border: 1px solid #333;
                                                                    border-radius: 8px;
                                                                    color: #333;
                                                                    margin-top: 10px;
                                                                    text-align: center;
                                                                }
                                                                QGroupBox::title {
                                                                    subcontrol-origin: margin;
                                                                    subcontrol-position: top center;
                                                                    padding: 0 10px;
                                                                }
                                                            """)
            self.groupbox_gluing_y.setObjectName("groupbox_gluing_y")
            self.gluing_y_up_btn = QtWidgets.QPushButton(self.groupbox_gluing_y)
            self.gluing_y_up_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.gluing_y_up_btn.setStyleSheet("QPushButton:hover{"
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
            self.gluing_y_up_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.gluing_y_up_btn.setIcon(icon)
            self.gluing_y_up_btn.setIconSize(QtCore.QSize(50, 50))
            self.gluing_y_up_btn.setObjectName("gluing_y_up_btn")
            self.gluing_y_down_btn = QtWidgets.QPushButton(self.groupbox_gluing_y)
            self.gluing_y_down_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.gluing_y_down_btn.setStyleSheet("QPushButton:hover{"
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
            self.gluing_y_down_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.gluing_y_down_btn.setIcon(icon)
            self.gluing_y_down_btn.setIconSize(QtCore.QSize(50, 50))
            self.gluing_y_down_btn.setObjectName("gluing_y_down_btn")
            self.gluing_y_low_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_y)
            self.gluing_y_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_y_low_radioButton.setFont(font)
            self.gluing_y_low_radioButton.setText("0.5mm")
            self.gluing_y_min_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_y)
            self.gluing_y_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_y_min_radioButton.setFont(font)
            self.gluing_y_min_radioButton.setText("3mm")
            self.gluing_y_max_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_y)
            self.gluing_y_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_y_max_radioButton.setFont(font)
            self.gluing_y_max_radioButton.setText("5mm")
            self.gluing_y_none_radioButton = QtWidgets.QRadioButton(self.groupbox_gluing_y)
            self.gluing_y_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_y_none_radioButton.setFont(font)
            self.gluing_y_none_radioButton.setText("None")
            self.gluing_y_speed_lbl = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.gluing_y_speed_lbl.setGeometry(QtCore.QRect(310, 90, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_y_speed_lbl.setFont(font)
            self.gluing_y_speed_lbl.setText("Speed")
            self.gluing_y_speed_lbl.setObjectName("gluing_y_speed_lbl")
            self.gluing_y_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_y)
            self.gluing_y_speed_lnedt.setGeometry(QtCore.QRect(310, 110, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_y_speed_lnedt)
            self.gluing_y_speed_lnedt.setValidator(validator)
            self.gluing_y_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_y_speed_lnedt.setObjectName("gluing_y_speed_lnedt")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(470, 95, 65, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Min. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(470, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(620, 95, 70, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Max. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(620, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1000 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.gluing_y_move_position_lbl = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.gluing_y_move_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_y_move_position_lbl.setFont(font)
            self.gluing_y_move_position_lbl.setText("Position")
            self.gluing_y_move_position_lbl.setObjectName("speed_1")
            self.gluing_y_move_position_lndt = QtWidgets.QLineEdit(self.groupbox_gluing_y)
            self.gluing_y_move_position_lndt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            self.gluing_y_move_position_lndt.setText("")
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_y_move_position_lndt)
            self.gluing_y_move_position_lndt.setValidator(validator)
            self.gluing_y_move_position_lndt.setStyleSheet("border:1px solid gray;")
            self.gluing_y_move_position_lndt.setObjectName("gluing_y_move_position_lndt")

            self.min_distance_2 = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.min_distance_2.setGeometry(QtCore.QRect(620, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_2.setFont(font)
            self.min_distance_2.setText("Min. distance(mm)")
            self.min_distance_2.setObjectName("min_distance_2")
            self.gluing_y_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_y)
            self.gluing_y_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_y_min_distance_lnedt)
            self.gluing_y_min_distance_lnedt.setValidator(validator)
            self.gluing_y_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_y_min_distance_lnedt.setObjectName("gluing_y_min_distance_lnedt")

            self.gluing_y_act_position_lbl = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.gluing_y_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 110, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gluing_y_act_position_lbl.setFont(font)
            self.gluing_y_act_position_lbl.setText("Actual Position")
            self.gluing_y_act_position_lbl.setObjectName("gluing_y_act_position_lbl")
            self.gluing_y_act_position_value = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.gluing_y_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.gluing_y_act_position_value.setText("20mm")
            self.gluing_y_act_position_value.setObjectName("gluing_y_act_position_value")

            self.max_distance_3 = QtWidgets.QLabel(self.groupbox_gluing_y)
            self.max_distance_3.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_3.setFont(font)
            self.max_distance_3.setText("Max. distance(mm)")
            self.max_distance_3.setObjectName("max_distance_3")
            self.gluing_y_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gluing_y)
            self.gluing_y_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_y_max_distance_lnedt)
            self.gluing_y_max_distance_lnedt.setValidator(validator)
            self.gluing_y_max_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_y_max_distance_lnedt.setObjectName("gluing_y_max_distance_lnedt")

            self.gluing_homing_btn = QtWidgets.QPushButton(self.groupbox_gluing_y)
            self.gluing_homing_btn.setGeometry(QtCore.QRect(770, 100, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.gluing_homing_btn.setFont(font)
            self.gluing_homing_btn.setText("Homing")
            self.gluing_homing_btn.setStyleSheet("QPushButton:enabled{\n"
                                                 "background-color:rgb(92, 98, 224);\n"
                                                 "color:rgb(255, 255, 255);\n"
                                                 "border-radius: 10px;\n"
                                                 "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                 "}"
                                                 "QPushButton:Pressed{\n"
                                                 "padding-left:5px;\n"
                                                 "padding-top:5px;\n"
                                                 "background-color: #1a5276;\n"
                                                 "}"
                                                 "QPushButton:disabled"
                                                 "{"
                                                 "background-color:#95a5a6;"
                                                 "}"
                                                 )
            self.gluing_homing_btn.setIconSize(QtCore.QSize(50, 50))
            self.gluing_homing_btn.setObjectName("gluing_homing_btn")
            self.verticalLayout_4.addWidget(self.groupbox_gluing_y)

            self.groupbox_glue_purge = QtWidgets.QGroupBox(self.scroll_area_widget_gluing)
            self.groupbox_glue_purge.setMinimumSize(QtCore.QSize(0, 100))
            self.groupbox_glue_purge.setMaximumSize(QtCore.QSize(16777215, 100))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_glue_purge.setFont(font)
            self.groupbox_glue_purge.setAlignment(Qt.AlignCenter)
            self.groupbox_glue_purge.setStyleSheet("""
                                                    QGroupBox {
                                                        border: 1px solid #333;
                                                        border-radius: 8px;
                                                        color: #333;
                                                        margin-top: 10px;
                                                        text-align: center;
                                                    }
                                                    QGroupBox::title {
                                                        subcontrol-origin: margin;
                                                        subcontrol-position: top center;
                                                        padding: 0 10px;
                                                    }
                                                """)
            self.groupbox_glue_purge.setObjectName("groupbox_glue_purge")

            self.max_distance_3 = QtWidgets.QLabel(self.groupbox_glue_purge)
            self.max_distance_3.setGeometry(QtCore.QRect(20, 20, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_3.setFont(font)
            self.max_distance_3.setText("Purge Time")
            self.max_distance_3.setObjectName("max_distance_3")
            self.gluing_purge_lnedt = QtWidgets.QLineEdit(self.groupbox_glue_purge)
            self.gluing_purge_lnedt.setGeometry(QtCore.QRect(20, 40, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gluing_purge_lnedt)
            self.gluing_purge_lnedt.setValidator(validator)
            self.gluing_purge_lnedt.setStyleSheet("border:1px solid gray;")
            self.gluing_purge_lnedt.setObjectName("gluing_purge_lnedt")

            self.glue_purge_btn = QtWidgets.QPushButton(self.groupbox_glue_purge)
            self.glue_purge_btn.setGeometry(QtCore.QRect(170, 30, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.glue_purge_btn.setFont(font)
            self.glue_purge_btn.setStyleSheet("QPushButton:enabled{\n"
                                              "background-color:rgb(92, 98, 224);\n"
                                              "color:rgb(255, 255, 255);\n"
                                              "border-radius: 10px;\n"
                                              "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                              "}"
                                              "QPushButton:Pressed{\n"
                                              "padding-left:5px;\n"
                                              "padding-top:5px;\n"
                                              "background-color: #1a5276;\n"
                                              "}"
                                              "QPushButton:disabled"
                                              "{"
                                              "background-color:#95a5a6;"
                                              "}"
                                              )
            self.glue_purge_btn.setIconSize(QtCore.QSize(50, 50))
            self.glue_purge_btn.setObjectName("glue_purge_btn")

            self.gluing_save_btn = QtWidgets.QPushButton(self.groupbox_glue_purge)
            self.gluing_save_btn.setGeometry(QtCore.QRect(770, 30, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.gluing_save_btn.setFont(font)
            self.gluing_save_btn.setText("Save")
            self.gluing_save_btn.setStyleSheet("QPushButton:enabled{\n"
                                               "background-color:rgb(92, 98, 224);\n"
                                               "color:rgb(255, 255, 255);\n"
                                               "border-radius: 10px;\n"
                                               "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                               "}"
                                               "QPushButton:Pressed{\n"
                                               "padding-left:5px;\n"
                                               "padding-top:5px;\n"
                                               "background-color: #1a5276;\n"
                                               "}"
                                               )
            self.gluing_save_btn.setIconSize(QtCore.QSize(50, 50))
            self.gluing_save_btn.setObjectName("gluing_save_btn")

            self.verticalLayout_4.addWidget(self.groupbox_glue_purge)
            self.scroll_area_gluing.setWidget(self.scroll_area_widget_gluing)

            self.scroll_area_loading = QtWidgets.QScrollArea(self.diagnostic_dialog)
            self.scroll_area_loading.setGeometry(QtCore.QRect(10, 60, 945, 500))
            self.scroll_area_loading.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_area_loading.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_area_loading.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.scroll_area_loading.setWidgetResizable(True)
            self.scroll_area_loading.setObjectName("scroll_area_loading")
            self.scroll_area_widget_loading = QtWidgets.QWidget()
            self.scroll_area_widget_loading.setGeometry(QtCore.QRect(0, 0, 945, 500))
            self.scroll_area_widget_loading.setObjectName("scroll_area_widget_loading")
            self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scroll_area_widget_loading)
            self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
            self.verticalLayout_5.setSpacing(10)
            self.verticalLayout_5.setObjectName("verticalLayout_5")
            self.diag_lbl_loading = QtWidgets.QLabel(self.scroll_area_widget_loading)
            self.diag_lbl_loading.setMinimumSize(QtCore.QSize(0, 40))
            self.diag_lbl_loading.setMaximumSize(QtCore.QSize(16777215, 40))
            self.diag_lbl_loading.setStyleSheet("QLabel {color: rgb(0, 0, 0);\n}")
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.diag_lbl_loading.setFont(font)
            self.diag_lbl_loading.setAlignment(Qt.AlignCenter)
            self.diag_lbl_loading.setObjectName("diag_lbl_loading")
            self.verticalLayout_5.addWidget(self.diag_lbl_loading)

            self.groupbox_gripper = QtWidgets.QGroupBox(self.scroll_area_widget_loading)
            self.groupbox_gripper.setMinimumSize(QtCore.QSize(0, 150))
            self.groupbox_gripper.setMaximumSize(QtCore.QSize(16777215, 150))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_gripper.setFont(font)
            self.groupbox_gripper.setAlignment(Qt.AlignCenter)
            self.groupbox_gripper.setStyleSheet("""
                                                                QGroupBox {
                                                                    border: 1px solid #333;
                                                                    border-radius: 8px;
                                                                    color: #333;
                                                                    margin-top: 10px;
                                                                    text-align: center;
                                                                }
                                                                QGroupBox::title {
                                                                    subcontrol-origin: margin;
                                                                    subcontrol-position: top center; /* Center the title */
                                                                    padding: 0 10px;
                                                                }
                                                            """)
            self.groupbox_gripper.setObjectName("groupbox_gripper")

            self.gripper_open_btn = QtWidgets.QPushButton(self.groupbox_gripper)
            self.gripper_open_btn.setGeometry(QtCore.QRect(30, 30, 100, 50))
            self.gripper_open_btn.setStyleSheet("QPushButton:Pressed{\n"
                                                "padding-left:2px;\n"
                                                "padding-top:2px;\n"
                                                "}"
                                                "QPushButton::icon {"
                                                "padding-right: 1px;}"
                                                "QPushButton{"
                                                "border-radius: 15px;}")
            self.gripper_open_btn.setText("")
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap(r".\media\open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.gripper_open_btn.setIcon(icon4)
            self.gripper_open_btn.setIconSize(QtCore.QSize(100, 40))
            self.gripper_open_btn.setObjectName("gripper_open_btn")

            self.gripper_close_btn = QtWidgets.QPushButton(self.groupbox_gripper)
            self.gripper_close_btn.setGeometry(QtCore.QRect(170, 30, 100, 50))
            self.gripper_close_btn.setStyleSheet("QPushButton:Pressed{\n"
                                                 "padding-left:2px;\n"
                                                 "padding-top:2px;\n"
                                                 "}"
                                                 "QPushButton::icon {"
                                                 "padding-right: 5px;}"
                                                 "QPushButton{"
                                                 "border-radius: 15px;}")
            self.gripper_close_btn.setText("")
            icon5 = QtGui.QIcon()
            icon5.addPixmap(QtGui.QPixmap(r".\media\close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.gripper_close_btn.setIcon(icon5)
            self.gripper_close_btn.setIconSize(QtCore.QSize(100, 40))
            self.gripper_close_btn.setObjectName("gripper_close_btn")

            self.gripper_low_radioButton = QtWidgets.QRadioButton(self.groupbox_gripper)
            self.gripper_low_radioButton.setGeometry(QtCore.QRect(10, 100, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gripper_low_radioButton.setFont(font)
            self.gripper_low_radioButton.setText("0.5mm")
            self.gripper_min_radioButton = QtWidgets.QRadioButton(self.groupbox_gripper)
            self.gripper_min_radioButton.setGeometry(QtCore.QRect(80, 100, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gripper_min_radioButton.setFont(font)
            self.gripper_min_radioButton.setText("3mm")
            self.gripper_max_radioButton = QtWidgets.QRadioButton(self.groupbox_gripper)
            self.gripper_max_radioButton.setGeometry(QtCore.QRect(160, 100, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gripper_max_radioButton.setFont(font)
            self.gripper_max_radioButton.setText("5mm")
            self.gripper_none_radioButton = QtWidgets.QRadioButton(self.groupbox_gripper)
            self.gripper_none_radioButton.setGeometry(QtCore.QRect(240, 100, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gripper_none_radioButton.setFont(font)
            self.gripper_none_radioButton.setText("None")
            self.gripper_position_lbl = QtWidgets.QLabel(self.groupbox_gripper)
            self.gripper_position_lbl.setGeometry(QtCore.QRect(310, 20, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gripper_position_lbl.setFont(font)
            self.gripper_position_lbl.setObjectName("gripper_position_lbl")
            self.gripper_position_lnedt = QtWidgets.QLineEdit(self.groupbox_gripper)
            self.gripper_position_lnedt.setGeometry(QtCore.QRect(310, 40, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gripper_position_lnedt)
            self.gripper_position_lnedt.setValidator(validator)
            self.gripper_position_lnedt.setStyleSheet("border:1px solid gray;")
            self.gripper_position_lnedt.setText("")
            self.gripper_position_lnedt.textChanged.connect(lambda text: self.change(text, "gripper"))
            self.gripper_position_lnedt.setObjectName("gripper_position_lnedt")
            self.max_distance_1 = QtWidgets.QLabel(self.groupbox_gripper)
            self.max_distance_1.setGeometry(QtCore.QRect(770, 20, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_1.setFont(font)
            self.max_distance_1.setObjectName("max_distance_1")
            self.gripper_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gripper)
            self.gripper_max_distance_lnedt.setGeometry(QtCore.QRect(770, 40, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gripper_max_distance_lnedt)
            self.gripper_max_distance_lnedt.setValidator(validator)
            self.gripper_max_distance_lnedt.setStyleSheet("border: 1px solid gray;")
            self.gripper_max_distance_lnedt.setObjectName("gripper_max_distance_lnedt")
            self.min_distance_1 = QtWidgets.QLabel(self.groupbox_gripper)
            self.min_distance_1.setGeometry(QtCore.QRect(620, 20, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_1.setFont(font)
            self.min_distance_1.setObjectName("min_distance_1")
            self.gripper_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_gripper)
            self.gripper_min_distance_lnedt.setGeometry(QtCore.QRect(620, 40, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.gripper_min_distance_lnedt)
            self.gripper_min_distance_lnedt.setValidator(validator)
            self.gripper_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.gripper_min_distance_lnedt.setObjectName("gripper_min_distance_lnedt")
            self.gripper_act_position_lbl = QtWidgets.QLabel(self.groupbox_gripper)
            self.gripper_act_position_lbl.setGeometry(QtCore.QRect(470, 20, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.gripper_act_position_lbl.setFont(font)
            self.gripper_act_position_lbl.setObjectName("gripper_act_position_lbl")
            self.gripper_act_position_value = QtWidgets.QLabel(self.groupbox_gripper)
            self.gripper_act_position_value.setGeometry(QtCore.QRect(470, 40, 75, 30))
            self.gripper_act_position_value.setText("20mm")
            self.gripper_act_position_value.setObjectName("gripper_act_position_value")

            self.gripper_homing_btn = QtWidgets.QPushButton(self.groupbox_gripper)
            self.gripper_homing_btn.setGeometry(QtCore.QRect(770, 100, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.gripper_homing_btn.setFont(font)
            self.gripper_homing_btn.setText("Plc init")
            self.gripper_homing_btn.setStyleSheet("QPushButton:enabled{\n"
                                                  "background-color:rgb(92, 98, 224);\n"
                                                  "color:rgb(255, 255, 255);\n"
                                                  "border-radius: 10px;\n"
                                                  "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                  "}"
                                                  "QPushButton:Pressed{\n"
                                                  "padding-left:5px;\n"
                                                  "padding-top:5px;\n"
                                                  "background-color: #1a5276;\n"
                                                  "}"
                                                  "QPushButton:disabled"
                                                  "{"
                                                  "background-color:#95a5a6;"
                                                  "}"
                                                  )
            self.gripper_homing_btn.setIconSize(QtCore.QSize(50, 50))
            self.gripper_homing_btn.setObjectName("gripper_homing_btn")
            self.verticalLayout_5.addWidget(self.groupbox_gripper)

            self.groupbox_slider = QtWidgets.QGroupBox(self.scroll_area_widget_loading)
            self.groupbox_slider.setMinimumSize(QtCore.QSize(0, 150))
            self.groupbox_slider.setMaximumSize(QtCore.QSize(16777215, 150))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_slider.setFont(font)
            self.groupbox_slider.setAlignment(Qt.AlignCenter)
            self.groupbox_slider.setStyleSheet("""
                                                QGroupBox {
                                                    border: 1px solid #333;
                                                    border-radius: 8px;
                                                    color: #333;
                                                    margin-top: 10px;
                                                    text-align: center;
                                                }
                                                QGroupBox::title {
                                                    subcontrol-origin: margin;
                                                    subcontrol-position: top center; /* Center the title */
                                                    padding: 0 10px;
                                                }
                                            """)
            self.groupbox_slider.setMaximumSize(QtCore.QSize(16777215, 130))

            self.groupbox_slider.setObjectName("groupbox_slider")
            self.slider_up_btn = QtWidgets.QPushButton(self.groupbox_slider)
            self.slider_up_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.slider_up_btn.setStyleSheet("QPushButton:hover{"
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
            self.slider_up_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.slider_up_btn.setIcon(icon)
            self.slider_up_btn.setIcon(icon)
            self.slider_up_btn.setIconSize(QtCore.QSize(50, 50))
            self.slider_up_btn.setObjectName("slider_up_btn")
            self.slider_down_btn = QtWidgets.QPushButton(self.groupbox_slider)
            self.slider_down_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.slider_down_btn.setStyleSheet("QPushButton:hover{"
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
            self.slider_down_btn.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(r".\media\down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.slider_down_btn.setIcon(icon)
            self.slider_down_btn.setIconSize(QtCore.QSize(50, 50))
            self.slider_down_btn.setObjectName("slider_down_btn")
            self.slider_low_radioButton = QtWidgets.QRadioButton(self.groupbox_slider)
            self.slider_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.slider_low_radioButton.setFont(font)
            self.slider_low_radioButton.setText("0.5mm")
            self.slider_min_radioButton = QtWidgets.QRadioButton(self.groupbox_slider)
            self.slider_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.slider_min_radioButton.setFont(font)
            self.slider_min_radioButton.setText("3mm")
            self.slider_max_radioButton = QtWidgets.QRadioButton(self.groupbox_slider)
            self.slider_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.slider_max_radioButton.setFont(font)
            self.slider_max_radioButton.setText("5mm")
            self.slider_none_radioButton = QtWidgets.QRadioButton(self.groupbox_slider)
            self.slider_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.slider_none_radioButton.setFont(font)
            self.slider_none_radioButton.setText("None")
            self.slider_position_lbl = QtWidgets.QLabel(self.groupbox_slider)
            self.slider_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.slider_position_lbl.setFont(font)
            self.slider_position_lbl.setObjectName("slider_position_lbl")
            self.slider_position_lnedt = QtWidgets.QLineEdit(self.groupbox_slider)
            self.slider_position_lnedt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.slider_position_lnedt)
            self.slider_position_lnedt.setValidator(validator)
            self.slider_position_lnedt.textChanged.connect(lambda text: self.change(text, "slider"))
            self.slider_position_lnedt.setStyleSheet("border:1px solid gray;")
            self.slider_position_lnedt.setObjectName("slider_position_lnedt")

            self.min_distance_2 = QtWidgets.QLabel(self.groupbox_slider)
            self.min_distance_2.setGeometry(QtCore.QRect(620, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_2.setFont(font)
            self.min_distance_2.setObjectName("min_distance_2")
            self.slider_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_slider)
            self.slider_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.slider_min_distance_lnedt)
            self.slider_min_distance_lnedt.setValidator(validator)
            self.slider_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.slider_min_distance_lnedt.setObjectName("slider_min_distance_lnedt")

            self.slider_act_position_lbl = QtWidgets.QLabel(self.groupbox_slider)
            self.slider_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.slider_act_position_lbl.setFont(font)
            self.slider_act_position_lbl.setObjectName("slider_act_position_lbl")
            self.slider_act_position_value = QtWidgets.QLabel(self.groupbox_slider)
            self.slider_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.slider_act_position_value.setText("20mm")
            self.slider_act_position_value.setObjectName("slider_act_position_value")

            self.max_distance_3 = QtWidgets.QLabel(self.groupbox_slider)
            self.max_distance_3.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_3.setFont(font)
            self.max_distance_3.setObjectName("max_distance_3")
            self.slider_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_slider)
            self.slider_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.slider_max_distance_lnedt)
            self.slider_max_distance_lnedt.setValidator(validator)
            self.slider_max_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.slider_max_distance_lnedt.setObjectName("slider_max_distance_lnedt")

            self.slider_homing_btn = QtWidgets.QPushButton(self.groupbox_slider)
            self.slider_homing_btn.setGeometry(QtCore.QRect(770, 100, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.slider_homing_btn.setFont(font)
            self.slider_homing_btn.setText("Plc init")
            self.slider_homing_btn.setStyleSheet("QPushButton:enabled{\n"
                                                 "background-color:rgb(92, 98, 224);\n"
                                                 "color:rgb(255, 255, 255);\n"
                                                 "border-radius: 10px;\n"
                                                 "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                 "}"
                                                 "QPushButton:Pressed{\n"
                                                 "padding-left:5px;\n"
                                                 "padding-top:5px;\n"
                                                 "background-color: #1a5276;\n"
                                                 "}"
                                                 "QPushButton:disabled"
                                                 "{"
                                                 "background-color:#95a5a6;"
                                                 "}"
                                                 )
            self.slider_homing_btn.setIconSize(QtCore.QSize(50, 50))
            self.slider_homing_btn.setObjectName("slider_homing_btn")
            self.verticalLayout_5.addWidget(self.groupbox_slider)

            self.groupbox_y_axis = QtWidgets.QGroupBox(self.scroll_area_widget_loading)
            self.groupbox_y_axis.setMinimumSize(QtCore.QSize(0, 160))
            self.groupbox_y_axis.setMaximumSize(QtCore.QSize(16777215, 160))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_y_axis.setFont(font)
            self.groupbox_y_axis.setAlignment(Qt.AlignCenter)
            self.groupbox_y_axis.setStyleSheet("""
                                                QGroupBox {
                                                    border: 1px solid #333;
                                                    border-radius: 8px;
                                                    color: #333;
                                                    margin-top: 10px;
                                                    text-align: center;
                                                }
                                                QGroupBox::title {
                                                    subcontrol-origin: margin;
                                                    subcontrol-position: top center; /* Center the title */
                                                    padding: 0 10px;
                                                }
                                            """)
            self.groupbox_y_axis.setMaximumSize(QtCore.QSize(16777215, 130))
            self.groupbox_y_axis.setObjectName("groupbox_y_axis")
            self.y_axis_forward_btn = QtWidgets.QPushButton(self.groupbox_y_axis)
            self.y_axis_forward_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.y_axis_forward_btn.setStyleSheet("QPushButton:hover{"
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
            self.y_axis_forward_btn.setText("")
            icon6 = QtGui.QIcon()
            icon6.addPixmap(QtGui.QPixmap(r".\media\up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.y_axis_forward_btn.setIcon(icon6)
            self.y_axis_forward_btn.setIconSize(QtCore.QSize(50, 50))
            self.y_axis_forward_btn.setObjectName("y_axis_forward_btn")
            self.y_axis_reverse_btn = QtWidgets.QPushButton(self.groupbox_y_axis)
            self.y_axis_reverse_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.y_axis_reverse_btn.setStyleSheet("QPushButton:hover{"
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
            self.y_axis_reverse_btn.setText("")
            icon7 = QtGui.QIcon()
            icon7.addPixmap(QtGui.QPixmap(r".\media\down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.y_axis_reverse_btn.setIcon(icon7)
            self.y_axis_reverse_btn.setIconSize(QtCore.QSize(50, 50))
            self.y_axis_reverse_btn.setObjectName("y_axis_reverse_btn")
            self.y_axis_low_radioButton = QtWidgets.QRadioButton(self.groupbox_y_axis)
            self.y_axis_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_low_radioButton.setFont(font)
            self.y_axis_low_radioButton.setText("5mm")
            self.y_axis_min_radioButton = QtWidgets.QRadioButton(self.groupbox_y_axis)
            self.y_axis_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_min_radioButton.setFont(font)
            self.y_axis_min_radioButton.setText("25mm")
            self.y_axis_max_radioButton = QtWidgets.QRadioButton(self.groupbox_y_axis)
            self.y_axis_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_max_radioButton.setFont(font)
            self.y_axis_max_radioButton.setText("50mm")
            self.y_axis_none_radioButton = QtWidgets.QRadioButton(self.groupbox_y_axis)
            self.y_axis_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_none_radioButton.setFont(font)
            self.y_axis_none_radioButton.setText("None")
            self.y_axis_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_y_axis)
            self.y_axis_speed_lnedt.setGeometry(QtCore.QRect(310, 110, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.y_axis_speed_lnedt)
            self.y_axis_speed_lnedt.setValidator(validator)
            self.y_axis_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.y_axis_speed_lnedt.setObjectName("y_axis_speed_lnedt")

            self.y_axis_speed_lbl = QtWidgets.QLabel(self.groupbox_y_axis)
            self.y_axis_speed_lbl.setGeometry(QtCore.QRect(310, 90, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_speed_lbl.setFont(font)
            self.y_axis_speed_lbl.setText("Speed")
            self.y_axis_speed_lbl.setObjectName("y_axis_speed_lbl")

            self.y_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_y_axis)
            self.y_axis_speed_range_lbl.setGeometry(QtCore.QRect(470, 95, 65, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_speed_range_lbl.setFont(font)
            self.y_axis_speed_range_lbl.setText("Min. Speed")
            self.y_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.y_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_y_axis)
            self.y_axis_speed_range_value.setGeometry(QtCore.QRect(470, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_speed_range_value.setFont(font)
            self.y_axis_speed_range_value.setText("1 rpm")
            self.y_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.y_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_y_axis)
            self.y_axis_speed_range_lbl.setGeometry(QtCore.QRect(620, 95, 70, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_speed_range_lbl.setFont(font)
            self.y_axis_speed_range_lbl.setText("Max. Speed")
            self.y_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.y_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_y_axis)
            self.y_axis_speed_range_value.setGeometry(QtCore.QRect(620, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_speed_range_value.setFont(font)
            self.y_axis_speed_range_value.setText("15000 rpm")
            self.y_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.y_axis_move_position_lbl = QtWidgets.QLabel(self.groupbox_y_axis)
            self.y_axis_move_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_move_position_lbl.setFont(font)
            self.y_axis_move_position_lbl.setText("Position")
            self.y_axis_move_position_lbl.setObjectName("speed_1")
            self.y_axis_move_position_lndt = QtWidgets.QLineEdit(self.groupbox_y_axis)
            self.y_axis_move_position_lndt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            self.y_axis_move_position_lndt.setText("")
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.y_axis_move_position_lndt)
            self.y_axis_move_position_lndt.setValidator(validator)
            self.y_axis_move_position_lndt.textChanged.connect(lambda text: self.change(text, "y-axis"))
            self.y_axis_move_position_lndt.setStyleSheet("border:1px solid gray;")
            self.y_axis_move_position_lndt.setObjectName("y_axis_move_position_lndt")

            self.min_distance_3 = QtWidgets.QLabel(self.groupbox_y_axis)
            self.min_distance_3.setGeometry(QtCore.QRect(620, 30, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_3.setFont(font)
            self.min_distance_3.setText("Min. distance(mm)")
            self.min_distance_3.setObjectName("min_distance_3")
            self.y_axis_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_y_axis)
            self.y_axis_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.y_axis_min_distance_lnedt)
            self.y_axis_min_distance_lnedt.setValidator(validator)
            self.y_axis_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.y_axis_min_distance_lnedt.setObjectName("y_axis_min_distance_lnedt")

            self.y_axis_act_position_lbl = QtWidgets.QLabel(self.groupbox_y_axis)
            self.y_axis_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.y_axis_act_position_lbl.setFont(font)
            self.y_axis_act_position_lbl.setText("Actual position")
            self.y_axis_act_position_lbl.setObjectName("y_axis_act_position_lbl")
            self.y_axis_act_position_value = QtWidgets.QLabel(self.groupbox_y_axis)
            self.y_axis_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.y_axis_act_position_value.setText("20mm")
            self.y_axis_act_position_value.setObjectName("y_axis_act_position_lbl")

            self.max_distance_4 = QtWidgets.QLabel(self.groupbox_y_axis)
            self.max_distance_4.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_4.setFont(font)
            self.max_distance_4.setText("Max. distance(mm)")
            self.max_distance_4.setObjectName("max_distance_4")
            self.y_axis_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_y_axis)
            self.y_axis_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.y_axis_max_distance_lnedt)
            self.y_axis_max_distance_lnedt.setValidator(validator)
            self.y_axis_max_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.y_axis_max_distance_lnedt.setObjectName("y_axis_max_distance_lnedt")

            self.y_axis_homing_btn = QtWidgets.QPushButton(self.groupbox_y_axis)
            self.y_axis_homing_btn.setGeometry(QtCore.QRect(770, 100, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.y_axis_homing_btn.setFont(font)
            self.y_axis_homing_btn.setText("Homing")
            self.y_axis_homing_btn.setStyleSheet("QPushButton:enabled{\n"
                                                 "background-color:rgb(92, 98, 224);\n"
                                                 "color:rgb(255, 255, 255);\n"
                                                 "border-radius: 10px;\n"
                                                 "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                 "}"
                                                 "QPushButton:Pressed{\n"
                                                 "padding-left:5px;\n"
                                                 "padding-top:5px;\n"
                                                 "background-color: #1a5276;\n"
                                                 "}"
                                                 "QPushButton:disabled"
                                                 "{"
                                                 "background-color:#95a5a6;"
                                                 "}"
                                                 )
            self.y_axis_homing_btn.setIconSize(QtCore.QSize(50, 50))
            self.y_axis_homing_btn.setObjectName("y_axis_homing_btn")
            self.verticalLayout_5.addWidget(self.groupbox_y_axis)

            self.groupbox_x_axis_dummy = QtWidgets.QGroupBox(self.scroll_area_widget_loading)
            self.groupbox_x_axis_dummy.setMinimumSize(QtCore.QSize(0, 10))
            self.groupbox_x_axis_dummy.setMaximumSize(QtCore.QSize(16777215, 10))
            self.groupbox_x_axis_dummy.setStyleSheet("border: 0px;")
            self.verticalLayout_5.addWidget(self.groupbox_x_axis_dummy)

            self.groupbox_x_axis = QtWidgets.QGroupBox(self.scroll_area_widget_loading)
            self.groupbox_x_axis.setMinimumSize(QtCore.QSize(0, 160))
            self.groupbox_x_axis.setMaximumSize(QtCore.QSize(16777215, 160))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_x_axis.setFont(font)
            self.groupbox_x_axis.setAlignment(Qt.AlignCenter)
            self.groupbox_x_axis.setStyleSheet("""
                                                QGroupBox {
                                                    border: 1px solid #333;
                                                    border-radius: 8px;
                                                    color: #333;
                                                    margin-top: 10px;
                                                    text-align: center;
                                                }
                                                QGroupBox::title {
                                                    subcontrol-origin: margin;
                                                    subcontrol-position: top center; /* Center the title */
                                                    padding: 0 10px;
                                                }
                                            """)
            self.groupbox_x_axis.setObjectName("groupbox_x_axis")
            self.x_axis_forward_btn = QtWidgets.QPushButton(self.groupbox_x_axis)
            self.x_axis_forward_btn.setGeometry(QtCore.QRect(55, 40, 50, 50))
            self.x_axis_forward_btn.setStyleSheet("QPushButton:hover{"
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
            self.x_axis_forward_btn.setText("")
            icon6 = QtGui.QIcon()
            icon6.addPixmap(QtGui.QPixmap(r".\media\up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.x_axis_forward_btn.setIcon(icon6)
            self.x_axis_forward_btn.setIconSize(QtCore.QSize(50, 50))
            self.x_axis_forward_btn.setObjectName("x_axis_forward_btn")
            self.x_axis_reverse_btn = QtWidgets.QPushButton(self.groupbox_x_axis)
            self.x_axis_reverse_btn.setGeometry(QtCore.QRect(195, 40, 50, 50))
            self.x_axis_reverse_btn.setStyleSheet("QPushButton:hover{"
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
            self.x_axis_reverse_btn.setText("")
            icon7 = QtGui.QIcon()
            icon7.addPixmap(QtGui.QPixmap(r".\media\down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.x_axis_reverse_btn.setIcon(icon7)
            self.x_axis_reverse_btn.setIconSize(QtCore.QSize(50, 50))
            self.x_axis_reverse_btn.setObjectName("x_axis_reverse_btn")
            self.x_axis_low_radioButton = QtWidgets.QRadioButton(self.groupbox_x_axis)
            self.x_axis_low_radioButton.setGeometry(QtCore.QRect(10, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_low_radioButton.setFont(font)
            self.x_axis_low_radioButton.setText("0.5mm")
            self.x_axis_low_radioButton.setObjectName("x_axis_low_radioButton")
            self.x_axis_min_radioButton = QtWidgets.QRadioButton(self.groupbox_x_axis)
            self.x_axis_min_radioButton.setGeometry(QtCore.QRect(80, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_min_radioButton.setFont(font)
            self.x_axis_min_radioButton.setText("3mm")
            self.x_axis_min_radioButton.setObjectName("x_axis_min_radioButton")
            self.x_axis_max_radioButton = QtWidgets.QRadioButton(self.groupbox_x_axis)
            self.x_axis_max_radioButton.setGeometry(QtCore.QRect(160, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_max_radioButton.setFont(font)
            self.x_axis_max_radioButton.setText("5mm")
            self.x_axis_max_radioButton.setObjectName("x_axis_max_radioButton")
            self.x_axis_none_radioButton = QtWidgets.QRadioButton(self.groupbox_x_axis)
            self.x_axis_none_radioButton.setGeometry(QtCore.QRect(240, 120, 100, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_none_radioButton.setFont(font)
            self.x_axis_none_radioButton.setText("None")
            self.x_axis_none_radioButton.setObjectName("x_axis_none_radioButton")

            self.x_axis_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_x_axis)
            self.x_axis_speed_lnedt.setGeometry(QtCore.QRect(310, 110, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.x_axis_speed_lnedt)
            self.x_axis_speed_lnedt.setValidator(validator)
            self.x_axis_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.x_axis_speed_lnedt.setObjectName("x_axis_speed_lnedt")
            self.x_axis_speed_lbl = QtWidgets.QLabel(self.groupbox_x_axis)
            self.x_axis_speed_lbl.setGeometry(QtCore.QRect(310, 90, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_lbl.setFont(font)
            self.x_axis_speed_lbl.setObjectName("x_axis_speed_lbl")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_x_axis)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(470, 95, 65, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Min. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_x_axis)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(470, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("1 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.x_axis_speed_range_lbl = QtWidgets.QLabel(self.groupbox_x_axis)
            self.x_axis_speed_range_lbl.setGeometry(QtCore.QRect(620, 95, 70, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_lbl.setFont(font)
            self.x_axis_speed_range_lbl.setText("Max. Speed")
            self.x_axis_speed_range_lbl.setObjectName("x_axis_speed_range_lbl")

            self.x_axis_speed_range_value = QtWidgets.QLabel(self.groupbox_x_axis)
            self.x_axis_speed_range_value.setGeometry(QtCore.QRect(620, 115, 65, 30))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_speed_range_value.setFont(font)
            self.x_axis_speed_range_value.setText("2000 rpm")
            self.x_axis_speed_range_value.setObjectName("x_axis_speed_range_value")

            self.x_axis_move_position_lbl = QtWidgets.QLabel(self.groupbox_x_axis)
            self.x_axis_move_position_lbl.setGeometry(QtCore.QRect(310, 30, 55, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_move_position_lbl.setFont(font)
            self.x_axis_move_position_lbl.setText("Position")
            self.x_axis_move_position_lbl.setObjectName("speed_1")
            self.x_axis_move_position_lndt = QtWidgets.QLineEdit(self.groupbox_x_axis)
            self.x_axis_move_position_lndt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            self.x_axis_move_position_lndt.setText("")
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.x_axis_move_position_lndt)
            self.x_axis_move_position_lndt.setValidator(validator)
            self.x_axis_move_position_lndt.textChanged.connect(lambda text: self.change(text, "x-axis"))
            self.x_axis_move_position_lndt.setStyleSheet("border:1px solid gray;")
            self.x_axis_move_position_lndt.setObjectName("x_axis_move_position_lndt")

            self.min_distance_3 = QtWidgets.QLabel(self.groupbox_x_axis)
            self.min_distance_3.setGeometry(QtCore.QRect(620, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.min_distance_3.setFont(font)
            self.min_distance_3.setText("Min. distance(mm)")
            self.min_distance_3.setObjectName("min_distance_3")
            self.x_axis_min_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_x_axis)
            self.x_axis_min_distance_lnedt.setGeometry(QtCore.QRect(620, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.x_axis_min_distance_lnedt)
            self.x_axis_min_distance_lnedt.setValidator(validator)
            self.x_axis_min_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.x_axis_min_distance_lnedt.setObjectName("x_axis_min_distance_lnedt")

            self.x_axis_act_position_lbl = QtWidgets.QLabel(self.groupbox_x_axis)
            self.x_axis_act_position_lbl.setGeometry(QtCore.QRect(470, 30, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.x_axis_act_position_lbl.setFont(font)
            self.x_axis_act_position_lbl.setObjectName("x_axis_act_position_lbl")
            self.x_axis_act_position_value = QtWidgets.QLabel(self.groupbox_x_axis)
            self.x_axis_act_position_value.setGeometry(QtCore.QRect(470, 50, 75, 30))
            self.x_axis_act_position_value.setText("20mm")
            self.x_axis_act_position_value.setObjectName("x_axis_act_position_value")

            self.max_distance_4 = QtWidgets.QLabel(self.groupbox_x_axis)
            self.max_distance_4.setGeometry(QtCore.QRect(770, 30, 120, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.max_distance_4.setFont(font)
            self.max_distance_4.setText("Max. distance(mm)")
            self.max_distance_4.setObjectName("max_distance_4")

            self.x_axis_max_distance_lnedt = QtWidgets.QLineEdit(self.groupbox_x_axis)
            self.x_axis_max_distance_lnedt.setGeometry(QtCore.QRect(770, 50, 110, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.x_axis_max_distance_lnedt)
            self.x_axis_max_distance_lnedt.setValidator(validator)
            self.x_axis_max_distance_lnedt.setStyleSheet("border:1px solid gray;")
            self.x_axis_max_distance_lnedt.setObjectName("x_axis_max_distance_lnedt")

            self.x_axis_homing_btn = QtWidgets.QPushButton(self.groupbox_x_axis)
            self.x_axis_homing_btn.setGeometry(QtCore.QRect(770, 100, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.x_axis_homing_btn.setFont(font)
            self.x_axis_homing_btn.setText("Homing")
            self.x_axis_homing_btn.setStyleSheet("QPushButton:enabled{\n"
                                                 "background-color:rgb(92, 98, 224);\n"
                                                 "color:rgb(255, 255, 255);\n"
                                                 "border-radius: 10px;\n"
                                                 "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                 "}"
                                                 "QPushButton:Pressed{\n"
                                                 "padding-left:5px;\n"
                                                 "padding-top:5px;\n"
                                                 "background-color: #1a5276;\n"
                                                 "}"
                                                 "QPushButton:disabled"
                                                 "{"
                                                 "background-color:#95a5a6;"
                                                 "}"
                                                 )
            self.x_axis_homing_btn.setIconSize(QtCore.QSize(50, 50))
            self.x_axis_homing_btn.setObjectName("x_axis_homing_btn")
            self.verticalLayout_5.addWidget(self.groupbox_x_axis)

            self.groupbox_front_door = QtWidgets.QGroupBox(self.scroll_area_widget_loading)
            self.groupbox_front_door.setMinimumSize(QtCore.QSize(0, 100))
            self.groupbox_front_door.setMaximumSize(QtCore.QSize(16777215, 100))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_front_door.setFont(font)
            self.groupbox_front_door.setAlignment(Qt.AlignCenter)
            self.groupbox_front_door.setStyleSheet("""
                                                                    QGroupBox {
                                                                        border: 1px solid #333;
                                                                        border-radius: 8px;
                                                                        color: #333;
                                                                        margin-top: 10px;
                                                                        text-align: center;
                                                                    }
                                                                    QGroupBox::title {
                                                                        subcontrol-origin: margin;
                                                                        subcontrol-position: top center;
                                                                        padding: 0 10px;
                                                                    }
                                                                """)
            self.groupbox_front_door.setObjectName("groupbox_front_door")

            self.act_position_20 = QtWidgets.QLabel(self.groupbox_front_door)
            self.act_position_20.setGeometry(QtCore.QRect(310, 30, 121, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.act_position_20.setFont(font)
            self.act_position_20.setObjectName("act_position_20")

            self.front_door_act_position_lbl = QtWidgets.QLabel(self.groupbox_front_door)
            self.front_door_act_position_lbl.setGeometry(QtCore.QRect(310, 50, 141, 30))
            font = QtGui.QFont()
            font.setPointSize(11)
            self.front_door_act_position_lbl.setFont(font)
            self.front_door_act_position_lbl.setObjectName("front_door_act_position_lbl")

            self.front_door_close_btn = QtWidgets.QPushButton(self.groupbox_front_door)
            self.front_door_close_btn.setGeometry(QtCore.QRect(30, 35, 100, 50))
            self.front_door_close_btn.setStyleSheet("QPushButton:Pressed{\n"
                                                "padding-left:2px;\n"
                                                "padding-top:2px;\n"
                                                "}"
                                                "QPushButton::icon {"
                                                "padding-right: 1px;}"
                                                "QPushButton{"
                                                "border-radius: 15px;}")
            self.front_door_close_btn.setText("")
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap(r".\media\close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.front_door_close_btn.setIcon(icon4)
            self.front_door_close_btn.setIconSize(QtCore.QSize(100, 40))
            self.front_door_close_btn.setObjectName("front_door_close_btn")

            self.front_door_open_btn = QtWidgets.QPushButton(self.groupbox_front_door)
            self.front_door_open_btn.setGeometry(QtCore.QRect(175, 35, 100, 50))
            self.front_door_open_btn.setStyleSheet("QPushButton:Pressed{\n"
                                                "padding-left:2px;\n"
                                                "padding-top:2px;\n"
                                                "}"
                                                "QPushButton::icon {"
                                                "padding-right: 1px;}"
                                                "QPushButton{"
                                                "border-radius: 15px;}")
            self.front_door_open_btn.setText("")
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap(r".\media\open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.front_door_open_btn.setIcon(icon4)
            self.front_door_open_btn.setIconSize(QtCore.QSize(100, 40))
            self.front_door_open_btn.setObjectName("front_door_open_btn")
            self.verticalLayout_5.addWidget(self.groupbox_front_door)

            self.groupbox_roller = QtWidgets.QGroupBox(self.scroll_area_widget_loading)
            self.groupbox_roller.setMinimumSize(QtCore.QSize(0, 100))
            self.groupbox_roller.setMaximumSize(QtCore.QSize(16777215, 100))
            font = QFont("Arial", 10)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.groupbox_roller.setFont(font)
            self.groupbox_roller.setAlignment(Qt.AlignCenter)
            self.groupbox_roller.setStyleSheet("""
                                                QGroupBox {
                                                    border: 1px solid #333;
                                                    border-radius: 8px;
                                                    color: #333;
                                                    margin-top: 10px;
                                                    text-align: center;
                                                }
                                                QGroupBox::title {
                                                    subcontrol-origin: margin;
                                                    subcontrol-position: top center; /* Center the title */
                                                    padding: 0 10px;
                                                }
                                            """)
            self.groupbox_roller.setObjectName("groupbox_roller")

            self.roller_clock_btn = QtWidgets.QPushButton(self.groupbox_roller)
            self.roller_clock_btn.setGeometry(QtCore.QRect(55, 30, 50, 50))
            self.roller_clock_btn.setStyleSheet("QPushButton:hover{"
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
            self.roller_clock_btn.setText("")
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap(r".\media\clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.roller_clock_btn.setIcon(icon8)
            self.roller_clock_btn.setIconSize(QtCore.QSize(50, 50))
            self.roller_clock_btn.setObjectName("roller_clock_btn")
            self.roller_anticlock_btn = QtWidgets.QPushButton(self.groupbox_roller)
            self.roller_anticlock_btn.setGeometry(QtCore.QRect(195, 30, 50, 50))
            self.roller_anticlock_btn.setStyleSheet("QPushButton:hover{"
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
            self.roller_anticlock_btn.setText("")
            icon9 = QtGui.QIcon()
            icon9.addPixmap(QtGui.QPixmap(r".\media\anti-clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.roller_anticlock_btn.setIcon(icon9)
            self.roller_anticlock_btn.setIconSize(QtCore.QSize(50, 50))
            self.roller_anticlock_btn.setObjectName("roller_anticlock_btn")
            self.roller_speed_lnedt = QtWidgets.QLineEdit(self.groupbox_roller)
            self.roller_speed_lnedt.setGeometry(QtCore.QRect(310, 50, 100, 30))
            regx = QRegExp(r'^(?:[0-9]{1,4}(?:\.[0-9]{1,2})?|9999(?:\.00?)?)$')
            validator = QRegExpValidator(regx, self.roller_speed_lnedt)
            self.roller_speed_lnedt.setValidator(validator)
            self.roller_speed_lnedt.setStyleSheet("border:1px solid gray;")
            self.roller_speed_lnedt.setObjectName("roller_speed_lnedt")
            self.speed_7 = QtWidgets.QLabel(self.groupbox_roller)
            self.speed_7.setGeometry(QtCore.QRect(310, 30, 80, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.speed_7.setFont(font)
            self.speed_7.setObjectName("speed_7")

            self.loading_save_btn = QtWidgets.QPushButton(self.groupbox_roller)
            self.loading_save_btn.setGeometry(QtCore.QRect(770, 40, 100, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.loading_save_btn.setFont(font)
            self.loading_save_btn.setText("Save")
            self.loading_save_btn.setStyleSheet("QPushButton:enabled{\n"
                                                "background-color:rgb(92, 98, 224);\n"
                                                "color:rgb(255, 255, 255);\n"
                                                "border-radius: 10px;\n"
                                                "font: 75 14pt \"MS Shell Dlg 2\";\n"
                                                "}"
                                                "QPushButton:Pressed{\n"
                                                "padding-left:5px;\n"
                                                "padding-top:5px;\n"
                                                "background-color: #1a5276;\n"
                                                "}"
                                                )
            self.loading_save_btn.setIconSize(QtCore.QSize(50, 50))
            self.loading_save_btn.setObjectName("loading_save_btn")
            self.verticalLayout_5.addWidget(self.groupbox_roller)
            self.scroll_area_loading.setWidget(self.scroll_area_widget_loading)

            self.diagnostics_btn_dclose = QtWidgets.QPushButton(self.diagnostic_dialog)
            self.diagnostics_btn_dclose.setGeometry(QtCore.QRect(1860, 10, 40, 40))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.diagnostics_btn_dclose.setFont(font)
            self.diagnostics_btn_dclose.setStyleSheet("QPushButton:Pressed{\n"
                                                      "padding-left:5px;\n"
                                                      "padding-top:5px;\n"
                                                      "}"
                                                      "QPushButton::icon {"
                                                      "padding-right: 1px;}"
                                                      "QPushButton{"
                                                      "border-radius: 25px;}")
            self.diagnostics_btn_dclose.setText("")
            icon10 = QtGui.QIcon()
            icon10.addPixmap(QtGui.QPixmap(r".\media\window_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.diagnostics_btn_dclose.setIcon(icon10)
            self.diagnostics_btn_dclose.setIconSize(QtCore.QSize(40, 40))
            self.diagnostics_btn_dclose.setObjectName("diagnostics_btn_dclose")

            self.diagnostic_page_statusbar = QtWidgets.QLabel(self.diagnostic_dialog)
            self.diagnostic_page_statusbar.setGeometry(QtCore.QRect(1100, 1005, 800, 30))
            font = QFont("Arial", 12)
            font.setBold(True)
            font.setWeight(QFont.Black)
            self.diagnostic_page_statusbar.setFont(font)
            self.diagnostic_page_statusbar.setText("Diagnostic page launched")
            self.diagnostic_page_statusbar.setAlignment(Qt.AlignCenter)
            self.diagnostic_page_statusbar.setObjectName("x_axis_act_position_lbl")

            self.diagnostic_retranslateUi(self.diagnostic_dialog)
            QtCore.QMetaObject.connectSlotsByName(self.diagnostic_dialog)


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at diagnostic_dialog : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def change(self, text, lndt):
        if lndt == "x-axis":
            self.x_axis_none_radioButton.setChecked(True)
        elif lndt == "y-axis":
            self.y_axis_none_radioButton.setChecked(True)
        elif lndt == "slider":
            self.slider_none_radioButton.setChecked(True)
        elif lndt == "gripper":
            self.gripper_none_radioButton.setChecked(True)
        elif lndt == "light_panel":
            self.light_panel_none_radioButton.setChecked(True)
        elif lndt == "uv z-axis":
            self.uv_z_axis_none_radioButton.setChecked(True)
        elif lndt == "gd z-axis":
            self.gd_z_axis_none_radioButton.setChecked(True)
        elif lndt == "gluing x1":
            self.gluing_x1_none_radioButton.setChecked(True)
        elif lndt == "gluing x2":
            self.gluing_x2_none_radioButton.setChecked(True)
        elif lndt == "gluing y":
            self.gluing_y_none_radioButton.setChecked(True)

    def diagnostic_retranslateUi(self, diagnostic_control):
        _translate = QtCore.QCoreApplication.translate
        diagnostic_control.setWindowTitle(_translate("diagnostic_control", "Dialog"))
        self.diag_lbl_title.setText(_translate("diagnostic_control", "Diagnostic control"))
        self.diag_lbl_focusing.setText(_translate("diagnostic_control", "Focusing station"))
        self.groupbox_light_panel.setTitle(_translate("diagnostic_control", "Light panel movement"))
        self.light_panel_speed_lbl.setText(_translate("diagnostic_control", "Speed"))
        self.light_panel_act_position_lbl.setText(_translate("diagnostic_control", "Actual position"))
        self.min_distance_4.setText(_translate("diagnostic_control", "Min. distance(mm)"))
        self.max_distance_5.setText(_translate("diagnostic_control", "Max. distance(mm)"))
        self.groupbox_light_panel_intensity.setTitle(_translate("diagnostic_control", "Light panel intensity"))
        self.light_panel_intensity_ok_btn.setText(_translate("diagnostic_control", "OK"))
        self.diag_lbl_station_4.setText(_translate("diagnostic_control", "Curing station"))
        self.groupbox_uv_z_axis.setTitle(_translate("diagnostic_control", "Z-axis Curing actuator"))
        self.uv_z_axis_speed_lbl.setText(_translate("diagnostic_control", "Speed"))
        self.uv_z_axis_act_position_lbl.setText(_translate("diagnostic_control", "Actual position"))
        self.min_distance_6.setText(_translate("diagnostic_control", "Min. distance(mm)"))
        self.max_distance_7.setText(_translate("diagnostic_control", "Max. distance(mm)"))
        self.groupbox_uv_left_cylinder.setTitle(_translate("diagnostic_control", "UV door and cylinder"))
        self.act_position_10.setText(_translate("diagnostic_control", "Actual position"))
        self.act_position_20.setText(_translate("diagnostic_control", "Actual position"))
        self.uv_left_cylinder_act_position_lbl.setText(_translate("diagnostic_control", "None"))
        self.front_door_act_position_lbl.setText(_translate("diagnostic_control", "None"))
        self.groupbox_uv_curing.setTitle(_translate("diagnostic_control", "UV curing"))
        self.uv_curing_btn.setText(_translate("diagnostic_control", "Curing"))
        self.diag_lbl_gluing.setText(_translate("diagnostic_control", "Gluing station"))
        self.groupbox_gd_z_axis.setTitle(_translate("diagnostic_control", "Z-axis Gluing actuator"))
        self.gd_z_axis_speed_lbl.setText(_translate("diagnostic_control", "Speed"))
        self.gd_z_axis_act_position_lbl.setText(_translate("diagnostic_control", "Actual position"))
        self.min_distance_5.setText(_translate("diagnostic_control", "Min. distance(mm)"))
        self.max_distance_6.setText(_translate("diagnostic_control", "Max. distance(mm)"))
        self.groupbox_gluing_x1.setTitle(_translate("diagnostic_control", "Gluing X1 actuator"))
        self.groupbox_gluing_x2.setTitle(_translate("diagnostic_control", "Gluing X2 actuator"))
        self.groupbox_gluing_y.setTitle(_translate("diagnostic_control", "Gluing Y actuator"))
        self.groupbox_glue_purge.setTitle(_translate("diagnostic_control", "Glue purge"))
        self.glue_purge_btn.setText(_translate("diagnostic_control", "Purge"))
        self.diag_lbl_loading.setText(_translate("diagnostic_control", "Loading & Unloading station"))
        self.groupbox_gripper.setTitle(_translate("diagnostic_control", "Gripper"))
        self.gripper_position_lbl.setText(_translate("diagnostic_control", "Position"))
        self.max_distance_1.setText(_translate("diagnostic_control", "Max. distance(mm)"))
        self.min_distance_1.setText(_translate("diagnostic_control", "Min. distance(mm)"))
        self.gripper_act_position_lbl.setText(_translate("diagnostic_control", "Actual position"))
        self.groupbox_slider.setTitle(_translate("diagnostic_control", "Slider"))
        self.slider_position_lbl.setText(_translate("diagnostic_control", "Position"))
        self.slider_act_position_lbl.setText(_translate("diagnostic_control", "Actual position"))
        self.min_distance_2.setText(_translate("diagnostic_control", "Min. distance(mm)"))
        self.max_distance_3.setText(_translate("diagnostic_control", "Max. distance(mm)"))
        self.groupbox_y_axis.setTitle(_translate("diagnostic_control", "Y-axis actuator"))
        self.groupbox_x_axis.setTitle(_translate("diagnostic_control", "X-axis actuator"))
        self.groupbox_front_door.setTitle(_translate("diagnostic_control", "Front door"))
        self.x_axis_speed_lbl.setText(_translate("diagnostic_control", "Speed"))
        self.x_axis_act_position_lbl.setText(_translate("diagnostic_control", "Actual position"))
        self.min_distance_3.setText(_translate("diagnostic_control", "Min. distance(mm)"))
        self.max_distance_4.setText(_translate("diagnostic_control", "Max. distance(mm)"))
        self.groupbox_roller.setTitle(_translate("diagnostic_control", "Lens Rotation"))
        self.speed_7.setText(_translate("diagnostic_control", "Step value"))

    def setfontstyle(self, bool_value=False):
        """
        This method is used to set the font and its size.
        param lists: bool
        return: font type
        """
        font = QtGui.QFont()
        font.setBold(bool_value)
        font.setWeight(75)
        font.setPointSize(12)
        return font


class Machine_control_Window(QtWidgets.QMainWindow, UiMainWindow_1):
    def __init__(self, parent=None):
        try:
            super(Machine_control_Window, self).__init__(parent)
            self.setupUi(self)
            self.port_list = ["PLC controller", "PLC controller 2", "Actuators", "UV curing system", "Collimator",
                              "Light controller"]
            self.port_status_dialog(self.port_list)

            self.i_o_monitor = ["Start button left", "Start button right", "Reset button", "Emergency Switch-1,2",
                                "Curtain sensor", "Air pressure sensor", "Left door sensor", "Right door sensor",
                                "GD X-Axis 1 Home Sensor", "GD X-Axis 1 Override sensor", "GD Y-Axis Home Sensor",
                                "GD Y-Axis Override sensor", "GD X-Axis 2 Home Sensor", "GD X-Axis 2 Override sensor",
                                "GD X-Axis 1 Alarm", "GD Y-Axis Alarm", "GD X-Axis 2 Alarm", "Relay lens Holder",
                                "Front Door Open sensor", "Front Door Close sensor", "Product Present",
                                "Product loading Cyl In", "Product loading Cyl Out", "Spare1",
                                "UV Door Open Sensor", "UV Door Close Sensor", "UV light Right Out Sensor",
                                "UV light Right Close Sensor", "UV light Left Out Sensor",
                                "UV light Left Close Sensor", "Glue Cartridge 1 Empty Sensor",
                                "Glue Cartridge 2 Empty Sensor", "Control Panel Door Sensor", "EMS",
                                "Spare2", "Spare3", "Spare4", "Spare5", "Spare6", "Spare7"
                                ]

            self.o_p_list = ["Lens Rotator Motor", "Lens Rotator Motor Direction",
                             "GD X Axis 1 Motor", "GD X Axis 1 Motor Direction",
                             "GD Y Axis Motor", "GD Y Axis Motor Direction",
                             "GD X Axis 2 Motor", "GD X Axis 2 Motor Direction", "Spare1",
                             "Spare2", "Spare3", "Spare4", "Lens Rotator Motor Enable",
                             "GD X Axis 1 Motor Enable", "GD X Axis 2 Motor Enable",
                             "GD Y Axis Motor Enable", "Glue Dispenser unit 1",
                             "Glue Dispenser unit 2", "Spare5", "Spare6",
                             "Front Door Open Solenoid", "Front Door Close Solenoid",
                             "Product Loading Out Solenoid", "Product Loading In Solenoid",
                             "Spare7", "UV Door Open Solenoid", "UV Door Close Solenoid",
                             "UV Close Solenoid", "UV Out Solenoid", "Tower-lamp Red",
                             "Tower-lamp Green", "Tower-lamp Yellow", "Tower-lamp Buzzer",
                             "Spare8", "Spare9", "Spare10"]

            self.sensor_status_dialog(self.i_o_monitor, self.o_p_list)
            self.diagnostic_control_dialog()
            self.machine_sensor_control_dialog()

        except Exception as e:
            print(e)


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     screen_count = app.screens()
#     screen_res = {}
#     for i, screen_names in enumerate(screen_count):
#         resolution = screen_count[i].size()
#         height = resolution.height()
#         width = resolution.width()
#         screen_res[i] = [width, height]
#     ui = Machine_control_Window()
#     sys.exit(app.exec_())
