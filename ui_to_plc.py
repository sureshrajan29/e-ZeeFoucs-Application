"""
This module manages the connection of all ports and operation of actuators.
"""
from PyQt5.QtCore import Qt

from logger import logger
import modbus
import plc_control
import uv_curing
from serial.tools import list_ports
import serial
import collimator_SDK
import sys
import time
import os
from threading import Thread
import pandas as pd


class Communication:
    def __init__(self):
        self.uv_light_done = False
        self.uv_door_done = False
        self.gluing_init_done = False
        self.glue_cure_done = False
        self.relay_y_axis_done = False
        self.plc_init_done = False
        self.part_load_done = False
        self.front_door_done = False
        self.x_homing = None
        self.y_homing = None
        self.station_4 = None
        self.station_5 = None
        self.station_6 = None
        self.modbus_class = modbus.ModbusControl()
        self.plc_control_class = plc_control.PLCControl()
        self.uv_control_class = uv_curing.UVcuring()
        self.collimator_class = collimator_SDK.Collimator()

    def connect_collimator(self, collimator_list=None, port=None):
        try:
            """
                This method is used to connect the collimator.
                param collimator_list: Which collimator numbers need to be connected
                param port: port number
                return: str
            """
            if type(collimator_list) == list and collimator_list:
                for x in collimator_list:
                    if x not in [1, 2, 3, 4, 5]:
                        logger.debug("Incorrect collimator list: {}".format(collimator_list))
                        return "Incorrect collimator list"
            else:
                logger.debug("Incorrect collimator list: {}".format(collimator_list))
                return "Incorrect collimator list"

            if collimator_list == [1, 2, 3, 4, 5]:
                connect_return = self.collimator_class.connect_device(collimator_list=collimator_list, port_name=port)
                if connect_return == "Passed":
                    logger.info("All collimator are connected.")
                    reset_collimator_return = self.collimator_class.reset_collimator(
                        collimator_list=collimator_list)
                    if reset_collimator_return == "Passed":
                        logger.info("All collimator are reset.")

                    else:
                        logger.debug("Reset error: {}".format(reset_collimator_return))
                    return "Connected"
                else:
                    logger.debug("Connection error: {}".format(connect_return))
                    return "Connection Failed"
            else:
                connect_return = self.collimator_class.connect_device(collimator_list=collimator_list, port_name=port)
                if connect_return == "Passed":
                    logger.info("List of collimator [{}]  are connected.".format(collimator_list))
                    enable_return = self.collimator_class.enable_device(collimator_list=collimator_list)
                    if enable_return == 'Passed':
                        logger.info("List of collimator [{}]  are enabled.".format(collimator_list))
                        reset_collimator_return = self.collimator_class.reset_collimator(
                            collimator_list=collimator_list)
                        if reset_collimator_return == "Passed":
                            logger.info("List of collimator [{}]  are reset.".format(collimator_list))

                        else:
                            logger.debug("Reset error: {}".format(reset_collimator_return))

                        return "Connected"
                    else:
                        logger.debug("Enable error: {}".format(enable_return))
                        return "Enable Failed"
                else:
                    logger.debug("Connection error: {}".format(connect_return))
                    return "Connection Failed"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at connect_collimator:{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def connect_modbus(self, port_name=None):
        try:
            """
                This method is used to connect the modbus controller.
                param port_name: port number
                return: str
            """
            if port_name is None:
                try:
                    if self.modbus_class.client.connect():
                        logger.info("Modbus server for all actuators is connected.")
                        return "Connected"
                except Exception as e:
                    logger.error("light panel port is not connected.: {}".format(e))
                    return "Port name is None"

            if self.modbus_class.client is not None:
                if self.modbus_class.client.connect():
                    logger.info("Modbus server for all actuators is connected.")
                    return "Connected"

            if type(port_name) == str and 4 <= len(port_name) <= 5 and port_name[:3] == "COM":
                port = list(list_ports.comports())
                for p in port:
                    if port_name == p.device:
                        self.modbus_class.client = modbus.ModbusClient(method='rtu', port=port_name, baudrate=38400,
                                                                       parity='N', stopbits=2, bytesize=8)
                        if self.modbus_class.client.connect():
                            logger.info("Modbus server for all actuators is connected.")
                            return "Connected"
                        else:
                            logger.error('Cannot connect to the Modbus Server')
                            return "Connection Failed"

                else:
                    return "Given modbus port name is not found"
            else:
                return "Incorrect Port name"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at connect_modbus:{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def connect_uv(self, port_name=None):
        try:
            """
                This method is used to connect the uv controller.
                param port_name: port number
                return: str
            """
            if port_name is None:
                try:
                    if self.uv_control_class.client.connect():
                        logger.info("Modbus server for UV is connected.")
                        return "Connected"
                except Exception as e:
                    logger.error("UV port is not connected.: {}".format(e))
                    return "Port name is None"

            if self.uv_control_class.client is not None:
                if self.uv_control_class.client.connect():
                    logger.info("Modbus server for UV is connected.")
                    return "Connected"

            if type(port_name) == str and 4 <= len(port_name) <= 5 and port_name[:3] == "COM":
                port = list(list_ports.comports())
                for p in port:
                    if port_name == p.device:
                        self.uv_control_class.client = uv_curing.ModbusClient(method='rtu', port=port_name,
                                                                              baudrate=9600, parity='N',
                                                                              stopbits=1, bytesize=8)
                        if self.uv_control_class.client.connect():
                            logger.info("Modbus server for UV is connected.")
                            return "Connected"
                        else:
                            logger.error('Cannot connect to the Modbus Server')
                            return "Connection Failed"

                else:
                    return "Given UV port name is not found"
            else:
                return "Incorrect Port name"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at connect_uv:{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def connect_plc_2(self, port_name=None):
        try:
            """
                This method is used to connect the second plc controller.
                param port_name: port number
                return: str
            """
            if port_name is None:
                try:
                    status = self.plc_control_class.is_port_open()
                    if status == "Connected":
                        logger.info("PLC is connected.")
                        return "Connected"
                    else:
                        return "Port name is None"
                except Exception as e:
                    logger.error("PLC port is not connected.: {}".format(e))
                    return "Port name is None"
            self.plc_control_class.serial_port_2 = None
            if type(port_name) == str and 4 <= len(port_name) <= 5 and port_name[:3] == "COM":
                port = list(list_ports.comports())
                for p in port:
                    if port_name == p.device:
                        self.plc_control_class.port_name = port_name
                        self.plc_control_class.serial_port_2 = serial.Serial(port=port_name, baudrate=115200,
                                                                             parity=serial.PARITY_NONE,
                                                                             stopbits=serial.STOPBITS_TWO,
                                                                             bytesize=serial.EIGHTBITS)
                        status = self.plc_control_class.is_port_open("Port 2")
                        return status
                else:
                    return "Given PLC port name is not found"
            else:
                return "Incorrect Port name"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at connect_plc 2:{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def connect_plc(self, port_name=None):
        try:
            """
                This method is used to connect the plc controller.
                param port_name: port number
                return: str
            """
            if port_name is None:
                try:
                    status = self.plc_control_class.is_port_open()
                    if status == "Connected":
                        logger.info("PLC is connected.")
                        return "Connected"
                    else:
                        return "Port name is None"
                except Exception as e:
                    logger.error("PLC port is not connected.: {}".format(e))
                    return "Port name is None"
            self.plc_control_class.serial_port = None
            if type(port_name) == str and 4 <= len(port_name) <= 5 and port_name[:3] == "COM":
                port = list(list_ports.comports())
                for p in port:
                    if port_name == p.device:
                        self.plc_control_class.port_name = port_name
                        self.plc_control_class.serial_port = serial.Serial(port=port_name, baudrate=115200,
                                                                           parity=serial.PARITY_NONE,
                                                                           stopbits=serial.STOPBITS_TWO,
                                                                           bytesize=serial.EIGHTBITS)
                        status = self.plc_control_class.is_port_open("Port 1")
                        return status
                else:
                    return "Given PLC port name is not found"
            else:
                return "Incorrect Port name"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at connect_plc:{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def connect_light_panel(self, port_name=None):
        try:
            """
                This method is used to connect the light panel controller.
                param port_name: port number
                return: str
            """
            if port_name is None:
                try:
                    if not self.plc_control_class.serial_port_1.isOpen():
                        try:
                            self.plc_control_class.serial_port_1.open()
                            time.sleep(0.5)
                            self.plc_control_class.serial_port_1.flushInput()
                            self.plc_control_class.serial_port_1.flushOutput()
                            return "Connected"
                        except Exception as e:
                            logger.error("light panel port is not connected.: {}".format(e))
                            return "Port name is None"
                    else:
                        return "Connected"
                except Exception as e:
                    logger.error("light panel port is not connected.: {}".format(e))
                    return "Port name is None"

            self.plc_control_class.serial_port_1 = None
            if type(port_name) == str and 4 <= len(port_name) <= 5 and port_name[:3] == "COM":
                port = list(list_ports.comports())
                for p in port:
                    if port_name == p.device:
                        self.plc_control_class.port_name_1 = port_name
                        self.plc_control_class.serial_port_1 = serial.Serial(port=port_name, baudrate=9600,
                                                                             parity=serial.PARITY_NONE,
                                                                             stopbits=serial.STOPBITS_ONE,
                                                                             bytesize=serial.EIGHTBITS)
                        try:
                            if not self.plc_control_class.serial_port_1.isOpen():
                                try:
                                    self.plc_control_class.serial_port_1.open()
                                    time.sleep(0.5)
                                    self.plc_control_class.serial_port_1.flushInput()
                                    self.plc_control_class.serial_port_1.flushOutput()
                                    return "Connected"
                                except Exception as e:
                                    logger.error("light panel port is not connected.: {}".format(e))
                                    return "Connection Failed"
                            else:
                                return "Connected"

                        except Exception as e:
                            logger.error("light panel port is not connected.: {}".format(e))
                            return "Connection Failed"
                else:
                    return "Given light panel port name is not found"
            else:
                return "Incorrect Port name"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at connect_light_panel:{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def y_homing_stage(self, class_name=None, home_position=None):
        try:
            """
                This method is used to initialize the y-actuator.
                param class_name: checkbox name in dialog box
                param home_position: After completing the homing, at which position should it stop
                return: str
            """
            return_value = self.modbus_class.alarm_display(1)
            if return_value == "Alarm read error occurred":
                self.y_homing = "Alarm read error occurred"
            elif return_value == "Emergency is pressed":
                self.y_homing = "Emergency is pressed"
            elif return_value == "Overload sensor detected":
                self.y_homing = "Overload sensor detected"
            elif return_value == "Motor crash":
                self.y_homing = "Motor crash"
            elif return_value == "Alarm occurred":
                self.y_homing = "Alarm occurred"
            else:
                if home_position is None:
                    status = self.modbus_class.actuator_homing(1)
                    if status == "Passed":
                        if class_name is not None:
                            class_name.y_axis_homing.setCheckState(Qt.Checked)
                            self.y_homing = "Passed"
                        else:
                            self.y_homing = "Passed"
                    else:
                        self.y_homing = self.modbus_class.alarm_display(slave_id=1)
                else:
                    status = self.modbus_class.actuator_movement(slave_id=1, distance=home_position)
                    if status == "Passed":
                        if class_name is not None:
                            class_name.y_axis_homing.setCheckState(Qt.Checked)
                            self.y_homing = "Passed"
                        else:
                            self.y_homing = "Passed"
                    else:
                        self.y_homing = self.modbus_class.alarm_display(slave_id=1)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at y_homing_stage function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))
            return None

    def x_homing_stage(self, class_name=None, home_position=None):
        try:
            """
                This method is used to initialize the x-actuator.
                param class_name: checkbox name in dialog box
                param home_position: After completing the homing, at which position should it stop
                return: str
            """
            return_value = self.modbus_class.alarm_display(5)
            if return_value == "Alarm read error occurred":
                self.x_homing = "Alarm read error occurred"
            elif return_value == "Emergency is pressed":
                self.x_homing = "Emergency is pressed"
            elif return_value == "Overload sensor detected":
                self.x_homing = "Overload sensor detected"
            elif return_value == "Motor crash":
                self.x_homing = "Motor crash"
            elif return_value == "Alarm occurred":
                self.x_homing = "Alarm occurred"
            else:
                if home_position is None:
                    status = self.modbus_class.actuator_homing(5)
                    if status == "Passed":
                        time.sleep(0.25)
                        status = self.modbus_class.actuator_movement(5, 10)
                        if status == "Passed":
                            if class_name is not None:
                                class_name.x_axis_homing.setCheckState(Qt.Checked)
                                self.x_homing = "Passed"

                            else:
                                self.x_homing = "Passed"
                        else:
                            self.x_homing = self.modbus_class.alarm_display(slave_id=5)
                    else:
                        self.x_homing = self.modbus_class.alarm_display(slave_id=5)
                else:
                    status = self.modbus_class.actuator_movement(slave_id=5, distance=home_position)
                    if status == "Passed":
                        if status == "Passed":
                            if class_name is not None:
                                class_name.x_axis_homing.setCheckState(Qt.Checked)
                                self.x_homing = "Passed"
                        else:
                            self.x_homing = self.modbus_class.alarm_display(slave_id=5)
                    else:
                        self.x_homing = self.modbus_class.alarm_display(slave_id=5)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at x_homing_stage function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))
            return None

    def station_6_homing(self, class_name=None, home_position=None):
        try:
            """
                This method is used to initialize the curing z-actuator.
                param class_name: checkbox name in dialog box
                param home_position: After completing the homing, at which position should it stop
                return: str
            """
            return_value = self.modbus_class.alarm_display(4)
            if return_value == "Alarm read error occurred":
                self.station_6 = "Alarm read error occurred"
            elif return_value == "Emergency is pressed":
                self.station_6 = "Emergency is pressed"
            elif return_value == "Overload sensor detected":
                self.station_6 = "Overload sensor detected"
            elif return_value == "Motor crash":
                self.station_6 = "Motor crash"
            elif return_value == "Alarm occurred":
                self.station_6 = "Alarm occurred"
            else:
                if home_position is None:
                    status = self.modbus_class.actuator_homing(4)
                    if status == "Passed":
                        if class_name is not None:
                            class_name.z_curing_homing.setCheckState(Qt.Checked)
                            self.station_6 = "Passed"
                        else:
                            self.station_6 = "Passed"
                    else:
                        self.station_6 = self.modbus_class.alarm_display(slave_id=4)

                else:
                    status = self.modbus_class.actuator_movement(slave_id=4, distance=home_position)
                    if status == "Passed":
                        if class_name is not None:
                            class_name.z_curing_homing.setCheckState(Qt.Checked)
                            self.station_6 = "Passed"
                        else:
                            self.station_6 = "Passed"
                    else:
                        self.station_6 = self.modbus_class.alarm_display(slave_id=4)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at station_6_homing function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))
            self.station_6 = None

    def station_5_homing(self, class_name=None, home_position=None):
        try:
            """
                This method is used to initialize the gluing z-actuator.
                param class_name: checkbox name in dialog box
                param home_position: After completing the homing, at which position should it stop
                return: str
            """
            return_value = self.modbus_class.alarm_display(3)
            if return_value == "Alarm read error occurred":
                self.station_5 = "Alarm read error occurred"
            elif return_value == "Emergency is pressed":
                self.station_5 = "Emergency is pressed"
            elif return_value == "Overload sensor detected":
                self.station_5 = "Overload sensor detected"
            elif return_value == "Motor crash":
                self.station_5 = "Motor crash"
            elif return_value == "Alarm occurred":
                self.station_5 = "Alarm occurred"
            else:
                if home_position is None:
                    status = self.modbus_class.actuator_homing(3)
                    if status == "Passed":
                        if class_name is not None:
                            class_name.z_gluing_homing.setCheckState(Qt.Checked)
                            self.station_5 = "Passed"
                        else:
                            self.station_5 = "Passed"
                    else:
                        self.station_5 = self.modbus_class.alarm_display(slave_id=3)
                else:
                    status = self.modbus_class.actuator_movement(slave_id=3, distance=home_position)
                    if status == "Passed":
                        if class_name is not None:
                            class_name.z_gluing_homing.setCheckState(Qt.Checked)
                            self.station_5 = "Passed"
                        else:
                            self.station_5 = "Passed"
                    else:
                        self.station_5 = self.modbus_class.alarm_display(slave_id=3)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at station_5_homing function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))
            self.station_5 = None

    def station_4_homing(self, class_name=None, home_position=None):
        try:
            """
                This method is used to initialize the relay z-actuator.
                param class_name: checkbox name in dialog box
                param home_position: After completing the homing, at which position should it stop
                return: str
            """
            return_value = self.modbus_class.alarm_display(2)
            if return_value == "Alarm read error occurred":
                self.station_4 = "Alarm read error occurred"
            elif return_value == "Emergency is pressed":
                self.station_4 = "Emergency is pressed"
            elif return_value == "Overload sensor detected":
                self.station_4 = "Overload sensor detected"
            elif return_value == "Motor crash":
                self.station_4 = "Motor crash"
            elif return_value == "Alarm occurred":
                self.station_4 = "Alarm occurred"
            else:
                if home_position is None:
                    status = self.modbus_class.actuator_homing(2)
                    if status == "Passed":
                        if class_name is not None:
                            class_name.z_relay_homing.setCheckState(Qt.Checked)
                            self.station_4 = "Passed"
                        else:
                            self.station_4 = "Passed"
                    else:
                        self.station_4 = self.modbus_class.alarm_display(slave_id=2)
                else:
                    status = self.modbus_class.actuator_movement(slave_id=2, distance=home_position)
                    if status == "Passed":
                        if class_name is not None:
                            class_name.z_relay_homing.setCheckState(Qt.Checked)
                            self.station_4 = "Passed"
                        else:
                            self.station_4 = "Passed"
                    else:
                        self.station_4 = self.modbus_class.alarm_display(slave_id=2)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at station_4_homing function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))
            self.station_4 = None

    def verify_input_status(self, port="Port 2"):
        try:
            """
                This method is used to verify the ip status.
                param port: port number
                return: str
            """
            count = 0
            while count < 3:
                status = self.plc_control_class.check_input_status(port)
                count += 1
                if status == "Status updated":
                    value = self.plc_control_class.input_status
                    if value["EMO"]:
                        return "Emergency pressed"
                    elif not value["Air Pressure"]:
                        return "Air Pressure is low"
                    elif not value["Left Door"]:
                        return "Left side door is opened"
                    elif not value["Right Door"]:
                        return "Right side door is opened"
                    elif not value["EMS"]:
                        return "Earth leakage"
                    else:
                        return "Done"
                else:
                    time.sleep(1)
            else:
                return "Unable to read input status"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at verify_input_status function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                      exc_tb.tb_lineno, e))
            return "Not Done"

    def parallel_homing_old(self, class_name=None, homing_position=None):
        try:
            """
                This method is used to homing all actuators and plc.
                param class_name: checkbox name in dialog box
                param home_position: After completing the homing, at which position should it stop
                return: str
            """
            status = ""
            self.uv_light_done = True
            if status == "Passed" or self.uv_light_done:
                if not self.uv_door_done:
                    status = self.plc_control_class.uv_door_open()
                    if status == "Passed":
                        time.sleep(0.5)
                        self.uv_door_done = True
                    else:
                        time.sleep(0.5)
                        ip_status = self.plc_control_class.check_input_status()
                        if ip_status == "Status updated":
                            value = self.plc_control_class.input_status

                            if value["EMO"]:
                                logger.error("Emergency is pressed")
                                return ["Emergency is pressed"]

                            if not value["Air Pressure"]:
                                logger.error("Air Pressure is low")
                                return ["Air pressure is low"]

                            if value["EMS"]:
                                logger.error("Earth leakage")
                                return ["Earth leakage"]

                            if not value["UV Protection Door Open Sensor"]:
                                logger.error("Error in UV Protection Door Open Sensor {}".format(ip_status))
                                return ["Error in UV Protection Door Open Sensor"]

                            if not value["Left Door"]:
                                logger.error("Left side door opened error")
                                return ["Left side door is opened"]

                            if not value["Right Door"]:
                                logger.error("Right Door is opened")
                                return ["Right side door is opened"]

                            if value["GD X-Axis 1 Alarm"]:
                                logger.error("Error in GD X-Axis 1 Alarm {}".format(ip_status))
                                return ["Error in GD X-Axis 1 Alarm"]

                            if value["GD Y-Axis Alarm"]:
                                logger.error("Error in GD Y-Axis Alarm {}".format(ip_status))
                                return ["Error in GD Y-Axis Alarm"]

                            if value["GD X-Axis 2 Alarm"]:
                                logger.error("Error in GD X-Axis 2 Alarm {}".format(ip_status))
                                return ["Error in GD X-Axis 2 Alarm"]
                        else:
                            logger.error("Error in input status function {}".format(ip_status))
                            return ["Error in read input status"]

                if status == "Passed" or self.uv_door_done:
                    time.sleep(0.15)
                    ip_check = self.verify_input_status()
                    if ip_check != "Done":
                        return [ip_check]
                    time.sleep(0.15)
                    if not self.gluing_init_done:
                        class_name.gluing_homing.setCheckState(Qt.PartiallyChecked)
                        time.sleep(0.25)
                        status = self.plc_control_class.gluing_init()
                        if status != "Passed":
                            ip_status = self.plc_control_class.check_input_status()
                            if ip_status == "Status updated":
                                value = self.plc_control_class.input_status
                                if value["EMO"]:
                                    logger.error("Emergency is pressed")
                                    return ["Emergency is pressed"]

                                if not value["Air Pressure"]:
                                    logger.error("Air Pressure is low")
                                    return ["Air pressure is low"]

                                if value["EMS"]:
                                    logger.error("Earth leakage")
                                    return ["Earth leakage"]

                                if not value["Left Door"]:
                                    logger.error("Left side door opened error")
                                    return ["Left side door is opened"]

                                if not value["Right Door"]:
                                    logger.error("Right Door is opened")
                                    return ["Right side door is opened"]

                                if value["GD X-Axis 1 Alarm"]:
                                    logger.error("Error in GD X-Axis 1 Alarm {}".format(ip_status))
                                    return ["Error in GD X-Axis 1 Alarm"]

                                if value["GD Y-Axis Alarm"]:
                                    logger.error("Error in GD Y-Axis Alarm {}".format(ip_status))
                                    return ["Error in GD Y-Axis Alarm"]

                                if value["GD X-Axis 2 Alarm"]:
                                    logger.error("Error in GD X-Axis 2 Alarm {}".format(ip_status))
                                    return ["Error in GD X-Axis 2 Alarm"]

                            else:
                                logger.error("Error in input ip_status function {}".format(ip_status))
                                return ["Error in read input status"]
                        else:
                            self.gluing_init_done = True
                            time.sleep(0.15)

                    if status == "Passed" or self.gluing_init_done:
                        ip_check = self.verify_input_status()
                        if ip_check != "Done":
                            return [ip_check]
                        time.sleep(0.15)
                        self.gluing_init_done = True
                        if not self.glue_cure_done:
                            class_name.gluing_homing.setCheckState(Qt.Checked)
                            time.sleep(0.25)
                            class_name.z_gluing_homing.setCheckState(Qt.PartiallyChecked)
                            time.sleep(0.25)
                            class_name.z_curing_homing.setCheckState(Qt.PartiallyChecked)
                            time.sleep(0.25)
                            if homing_position is None:
                                thread_1 = Thread(target=self.station_6_homing,
                                                  args=(class_name,))
                                thread_2 = Thread(target=self.station_5_homing,
                                                  args=(class_name,))
                                thread_1.start()
                                thread_2.start()
                                thread_1.join()
                                thread_2.join()

                            else:
                                thread_1 = Thread(target=self.station_6_homing,
                                                  args=(class_name, homing_position))
                                thread_2 = Thread(target=self.station_5_homing,
                                                  args=(class_name, homing_position))
                                thread_1.start()
                                thread_2.start()
                                thread_1.join()
                                thread_2.join()

                            if self.station_5 == "Passed" and self.station_6 == "Passed":
                                status = "Passed"

                            else:
                                station_5, station_6 = self.station_5, self.station_6
                                if station_6 != "Passed":
                                    return [station_6, "Error in Curing z-axis"]

                                if station_5 != "Passed":
                                    return [station_5, "Error in Gluing z-axis"]

                        if status == "Passed" or self.glue_cure_done:
                            self.glue_cure_done = True
                            ip_check = self.verify_input_status()
                            if ip_check != "Done":
                                return [ip_check]
                            time.sleep(0.25)
                            if not self.relay_y_axis_done:
                                class_name.z_relay_homing.setCheckState(Qt.PartiallyChecked)
                                class_name.y_axis_homing.setCheckState(Qt.PartiallyChecked)
                                class_name.x_axis_homing.setCheckState(Qt.PartiallyChecked)
                                if homing_position is None:
                                    thread_3 = Thread(target=self.station_4_homing,
                                                      args=(class_name,))
                                    thread_4 = Thread(target=self.y_homing_stage,
                                                      args=(class_name,))
                                    thread_5 = Thread(target=self.x_homing_stage,
                                                      args=(class_name,))
                                    thread_3.start()
                                    thread_4.start()
                                    thread_5.start()
                                    print("Relay & y started all")
                                    thread_3.join()
                                    thread_4.join()
                                    thread_5.join()
                                else:
                                    thread_3 = Thread(target=self.station_4_homing,
                                                      args=(class_name, homing_position))
                                    thread_4 = Thread(target=self.y_homing_stage,
                                                      args=(class_name, homing_position))
                                    thread_5 = Thread(target=self.x_homing_stage,
                                                      args=(class_name, homing_position))
                                    thread_3.start()
                                    thread_4.start()
                                    thread_5.start()
                                    print("Relay & y started all")
                                    thread_3.join()
                                    thread_4.join()
                                    thread_5.join()

                                if (self.station_4 == "Passed" and self.y_homing == "Passed" and
                                        self.x_homing == "Passed"):
                                    status = "Passed"

                                else:
                                    station_4, y_status = self.station_4, self.y_homing
                                    if station_4 != "Passed":
                                        return [station_4, "Error in relay z-axis"]
                                    if y_status != "Passed":
                                        return [y_status, "Error in y-axis"]

                            if status == "Passed" or self.relay_y_axis_done:
                                self.relay_y_axis_done = True
                                ip_check = self.verify_input_status()
                                if ip_check != "Done":
                                    return [ip_check]
                                if status == "Passed" or self.relay_y_axis_done:
                                    if not self.plc_init_done:
                                        time.sleep(0.15)
                                        class_name.plc_initialize_homing.setCheckState(Qt.PartiallyChecked)
                                        status = self.plc_control_class.plc_initialize()
                                        if status == "Passed":
                                            time.sleep(0.25)
                                            class_name.plc_initialize_homing.setCheckState(Qt.Checked)
                                        else:
                                            logger.error("Error in plc initialize {}".format(status))
                                            return ["Error in plc initialize"]

                                    if status == "Passed" or self.plc_init_done:
                                        self.plc_init_done = True
                                        if not self.front_door_done:
                                            time.sleep(0.5)
                                            class_name.front_door_homing.setCheckState(Qt.PartiallyChecked)
                                            status = self.plc_control_class.front_door_open()
                                            if status == "Passed":
                                                class_name.front_door_homing.setCheckState(Qt.Checked)
                                                time.sleep(0.5)
                                                self.front_door_done = True
                                                self.uv_light_done = False
                                                self.uv_door_done = False
                                                self.gluing_init_done = False
                                                self.glue_cure_done = False
                                                self.relay_y_axis_done = False
                                                self.x_axis_done = False
                                                self.plc_init_done = False
                                                self.part_load_done = False
                                                self.front_door_done = False
                                                return ["Passed"]
                                            else:
                                                ip_status = self.plc_control_class.check_input_status()
                                                if ip_status == "Status updated":
                                                    value = self.plc_control_class.input_status
                                                    if not value["Front Door Open sensor"]:
                                                        logger.error(
                                                            "Error in front door open sensor {}".format(ip_status))
                                                        return ["Error in front door open sensor"]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at parallel_homing function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def height_adjustment(self, height_value):
        try:
            """
                This method is used to adjust the lens height.
                param height_value: height value of focusing lens
                return: str
            """
            if len(str(height_value)) <= 5 and type(height_value) == int:
                i = 0
                j = 0
                values = []
                while i < 3 and j < 3:
                    list_value = []
                    for x in range(10):
                        value = self.modbus_class.height_sensor_value()
                        if value != "Error":
                            list_value.append(value)
                    if len(list_value) == 0:
                        i += 1
                    else:
                        value = (sum(list_value) // len(list_value))
                        values.append(value)
                        if abs(values[-1] - height_value) > 50:
                            if (values[-1] - height_value) > 0:
                                direction = "clockwise"
                            else:
                                direction = "anticlockwise"

                            if len(values) > 1 and abs(values[-1] - values[-2]) < 30:
                                logger.error("Lens rotation is too minimal")
                                j += 1

                            else:
                                j = 0

                            if abs(values[-1] - height_value) > 3000:
                                return "Height value difference is more than 3 mm"

                            elif abs(values[-1] - height_value) > 2500:
                                degree = 400

                            elif abs(values[-1] - height_value) > 2000:
                                degree = 300

                            elif abs(values[-1] - height_value) > 1500:
                                degree = 250

                            elif abs(values[-1] - height_value) > 1000:
                                degree = 200

                            elif abs(values[-1] - height_value) > 500:
                                degree = 150

                            elif abs(values[-1] - height_value) > 200:
                                degree = 100

                            elif abs(values[-1] - height_value) > 100:
                                degree = 70

                            elif abs(values[-1] - height_value) > 50:
                                degree = 50

                            else:
                                degree = 30

                            plc_status = ''
                            plc_status = self.plc_control_class.lens_rotate(degree=degree, direction=direction)
                            time.sleep(1)
                            if plc_status == "Connection Failed":
                                logger.error("Unable to access the Port")
                                return plc_status

                            elif plc_status == "Incorrect direction input":
                                logger.error("Incorrect direction input.")
                                return plc_status

                            elif plc_status == "Incorrect degree input":
                                logger.error("Incorrect degree input.")
                                return plc_status

                            elif plc_status == "Lens rotation Failed":
                                logger.error("Lens rotation Failed.")
                                return plc_status

                            elif plc_status == "Passed":
                                i = 0

                            else:
                                return plc_status
                        else:
                            break

                if i >= 3:
                    logger.error("Continuously we get three times error")
                    return "Error in Height adjustment"

                elif j >= 3:
                    logger.error("Lens is not rotating properly")
                    return "Lens rotation Failed"

                else:
                    return "Passed"

            else:
                return "Incorrect value"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at height_adjustment function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def tower_light_thread(self, port, color):
        try:
            """
                This method is used to turn on the tower light color.
                param port: port number
                param color: which color to turn on
                return: str
            """
            tower_light_status = self.plc_control_class.tower_light_control(port_number=port, light=color)
            if tower_light_status == "Passed":
                self.towerlight_status = "Passed"
            else:
                self.towerlight_status = tower_light_status

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at front door open close function : {}|{}|{}|{}".format(exc_type, func_name, exc_tb.tb_lineno,
                                                                               e))

    def y_parallel(self, position):
        try:
            """
                This method is used to move y-actuator.
                param position: position value
                return: str
            """
            status = self.modbus_class.actuator_movement(slave_id=1, distance=position, speed=15000)
            if status == "Passed":
                self.y_moved = "Passed"
            else:
                self.y_moved = status

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at station_4_homing function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def x_parallel(self, position):
        try:
            """
                This method is used to move x-actuator.
                param position: position value
                return: str
            """
            status = self.modbus_class.actuator_movement(slave_id=5, distance=position)
            if status == "Passed":
                self.x_moved = "Passed"
            else:
                self.x_moved = status

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at station_4_homing function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))
            self.station_4 = None
