"""
This module is used to access of all plc controller
"""

import serial
import time
import os
import sys
import re
from logger import logger
from machine_logger import machine_logger


class PLCControl:
    def __init__(self):
        try:
            self.plc_indicate_about = None
            self.serial_port = ''
            self.serial_port_2 = ''
            self.port_name = ''
            self.serial_port_1 = ''
            self.port_name_1 = ''
            self.port_name_2 = ''
            self.input_status = {"Start Left": False, "Start Right": False, "Reset": False, "EMO": False,
                                 "Curtain": False, "Air Pressure": False, "Left Door": False, "Right Door": False,
                                 "GD X-Axis 1 Home Sensor": False, "GD X-Axis 1 Override sensor": False,
                                 "GD Y-Axis Home Sensor": False, "GD Y-Axis Override sensor": False,
                                 "GD X-Axis 2 Home Sensor": False, "GD X-Axis 2 Override sensor": False,
                                 "GD X-Axis 1 Alarm": False, "GD Y-Axis Alarm": False, "GD X-Axis 2 Alarm": False,
                                 "Relay lens Holder": False, "Front Door Open sensor": False,
                                 "Front Door Close sensor": False, "Product Present": False,
                                 "Product loading Cyl In": False, "Product loading Cyl Out": False, "Spare1": False,
                                 "UV Protection Door Open Sensor": False, "UV Protection Door Close Sensor": False,
                                 "UV light Right Out Sensor": False, "UV light Right Close Sensor": False,
                                 "UV light Left Out Sensor": False, "UV light Left Close Sensor": False,
                                 "Glue Cartridge 1 Empty Sensor": False, "Glue Cartridge 2 Empty Sensor": False,
                                 "Control Panel Door Sensor": False, "EMS": False, "Spare2": False, "Spare3": False,
                                 "Spare4": False, "Spare5": False, "Spare6": False, "Spare7": False}

            self.output_status = {"Lens Rotator Motor": False, "Lens Rotator Motor Direction": False,
                                  "GD X Axis 1 Motor": False, "GD X Axis 1 Motor Direction": False,
                                  "GD Y Axis Motor": False, "GD Y Axis Motor Direction": False,
                                  "GD X Axis 2 Motor": False, "GD X Axis 2 Motor Direction": False, "Spare1": False,
                                  "Spare2": False, "Spare3": False, "Spare4": False, "Lens Rotator Motor Enable": False,
                                  "GD X Axis 1 Motor Enable": False, "GD X Axis 2 Motor Enable": False,
                                  "GD Y Axis Motor Enable": False, "Glue Dispenser unit 1": False,
                                  "Glue Dispenser unit 2": False, "Spare5": False, "Spare6": False,
                                  "Front Door Open Solenoid": False, "Front Door Close Solenoid": False,
                                  "Product Loading Out Solenoid": False, "Product Loading In Solenoid": False,
                                  "Spare7": False, "UV Door Open Solenoid": False, "UV Door Close Solenoid": False,
                                  "UV Close Solenoid": False, "UV Out Solenoid": False, "Tower-lamp Red": False,
                                  "Tower-lamp Green": False, "Tower-lamp Yellow": False, "Tower-lamp Buzzer": False,
                                  "Spare8": False, "Spare9": False, "Spare10": False}


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at Initial settings :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def is_port_open(self, port):
        """
            This method is used to check if the connected port is open or not
            param port: port number
            return: str
        """
        if port == "Port 1":
            port = self.serial_port
        else:
            port = self.serial_port_2

        if not port.isOpen():
            try:
                port.open()
                port.flushInput()
                port.flushOutput()
                return "Connected"

            except Exception as e:
                logger.error("PLC is not connected.: {}".format(e))
                return "Connection Failed"
        else:
            return "Connected"

    def plc_initialize(self, port_number="Port 1"):
        try:
            """
                This method is used to initialize the plc(Slider and Gripper)
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("INT:\r\n".encode())
            logger.info("PLC input: INT:\r\n")

            t_end = time.time() + 7
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while plc initializing {}".format(status))
                    return "Emergency button pressed"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while plc initializing {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while plc initializing {}".format(status))
                    return "Earth leakage is low"

                if 'K:INT\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:AER\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while plc initializing {}".format(status))
                    return "Actuator error in Slider or Gripper"

                if 'E:LSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Left side door open while plc initializing {}".format(status))
                    return "Left side door is opened"

                if 'E:RSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Right side door open while plc initializing {}".format(status))
                    return "Right side door is opened"

                if 'E:INT\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Init failed while plc initializing {}".format(status))
                    return "Init failed while plc initializing."

            else:
                logger.info('Status from the Device: {}'.format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at plc_initialize function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                exc_tb.tb_lineno, e))
            return "Connection Failed"

    def slider(self, slider, port_number="Port 2"):
        try:
            """
                This method is used to move the slider
                param port_number: port number as str
                param slider: slider value
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            if "".join(list(str(slider).split("."))).isdigit():
                if len(str(int(slider))) <= 3:
                    x = float(slider) * 100
                    slid = (5 - len(str(int(x)))) * '0' + str(int(x))
                else:
                    logger.error("Incorrect slider input")
                    return "Incorrect slider input"
            else:
                logger.error("Incorrect slider input")
                return "Incorrect slider input"

            status = ""
            port.write("S{}:\r\n".format(str(slid)).encode())
            logger.info("PLC input: S{}:\r\n".format(str(slid)))

            t_end = time.time() + 7
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'K:STA\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while slider moving {}".format(status))
                    return "Emergency button pressed"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while slider moving {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while slider moving {}".format(status))
                    return "Earth leakage is low"

                if 'E:AER\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while slider moving {}".format(status))
                    return "Actuator error in Slider or Gripper"

                if 'E:STA\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while slider moving {}".format(status))
                    return "Error occurred while slider moving."


            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while slider moving {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at slider function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                        exc_tb.tb_lineno, e))
            return "Connection Failed"

    def gripper(self, gripper, port_number="Port 1"):
        try:
            """
                This method is used to move the gripper
                param port_number: port number as str
                param gripper: gripper value
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            if "".join(list(str(gripper).split("."))).isdigit():
                if len(str(int(gripper))) <= 3:
                    x = float(gripper) * 100
                    grip = (5 - len(str(int(x)))) * '0' + str(int(x))
                else:
                    logger.error("Incorrect gripper input")
                    return "Incorrect gripper input"
            else:
                logger.error("Incorrect gripper input")
                return "Incorrect gripper input"

            status = ""
            port.write("G{}:\r\n".format(str(grip)).encode())
            logger.info("PLC input: G{}:\r\n".format(str(grip)))

            t_end = time.time() + 7
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while gripper moving {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while gripper moving {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while gripper moving {}".format(status))
                    return "Earth leakage is low"

                if 'K:GRP\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:GRP\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while gripper moving {}".format(status))
                    return "Error occurred while gripper moving."

                if 'E:AER\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while gripper moving {}".format(status))
                    return "Actuator error in Slider or Gripper"

            else:
                logger.info('Status from the Device: {}'.format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at gripper function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                         exc_tb.tb_lineno, e))
            return "Connection Failed"

    def lens_rotate(self, degree, direction, port_number="Port 1"):
        try:
            """
                This method is used to rotate the lens
                param port_number: port number as str
                param degree: number of degree to rotate
                param direction: which direction to rotate
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            if str(degree).replace(".", "", 1).isdigit() and 1406.24 >= degree > 0:
                x = int((25600 * float(degree)) / 360)
                deg = (5 - len(str(x))) * '0' + str(x)
                logger.info("Input degree: {} in {} direction".format(degree, direction))
                if direction == 'clockwise':
                    port.write("C{}:\r\n".format(deg).encode())
                    logger.info("PLC len rotation command: {}".format("C{}:\r\n".format(deg)))

                elif direction == 'anticlockwise':
                    port.write("A{}:\r\n".format(deg).encode())
                    logger.info("PLC len rotation command: {}".format("A{}:\r\n".format(deg)))
                else:
                    logger.error("Incorrect direction input")
                    return "Incorrect direction input"
            else:
                logger.error("Incorrect degree input: {}".format(degree))
                return "Incorrect degree input"

            status = ""
            t_end = time.time() + 15
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while lens rotate {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while lens rotate {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while lens rotate {}".format(status))
                    return "Earth leakage is low"

                if 'E:LSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Left side door opened while lens rotate {}".format(status))
                    return "Left side door is opened"

                if 'E:RSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Right side door opened while lens rotate {}".format(status))
                    return "Right side door is opened"

                if 'K:LRD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"
            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while lens rotate {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at lens rotation function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                               exc_tb.tb_lineno, e))
            return "Connection Failed"

    def front_door_open(self, port_number="Port 2"):
        try:
            """
                This method is used to open the front door
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("FDO:\r\n".encode())
            logger.info("PLC input: FDO:\r\n")

            t_end = time.time() + 8
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure low while front door open {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while front door open {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while front door open {}".format(status))
                    return "Earth leakage is low"

                if 'E:LSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Left side door opened while front door open {}".format(status))
                    return "Left side door is opened"

                if 'E:RSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Right side door opened while front door open {}".format(status))
                    return "Right side door is opened"

                if 'K:FDO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:CTS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Curtain door interrupt while front door open {}".format(status))
                    return "Error in Curtain sensor"

                if 'E:FDO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while front door open {}".format(status))
                    return "Error in front door open"

            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while front door open {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at front_door_open function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                 exc_tb.tb_lineno, e))
            return "Connection Failed"

    def front_door_close(self, port_number="Port 2"):
        try:
            """
                This method is used to close the front door
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("FDC:\r\n".encode())
            logger.info("PLC input: FDC:\r\n")

            t_end = time.time() + 8
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure low while front door close {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while front door close {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while front door close {}".format(status))
                    return "Earth leakage is low"

                if 'E:LSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Left side door opened while front door close {}".format(status))
                    return "Left side door is opened"

                if 'E:RSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Right side door opened while front door close {}".format(status))
                    return "Right side door is opened"

                if 'K:FDC\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:CTS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Curtain door interrupt while front door close {}".format(status))
                    return "Error in Curtain sensor"

                if 'E:FDC\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while front door close {}".format(status))
                    return "Error in front door open"

            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while front door close {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at front_door_close function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                  exc_tb.tb_lineno, e))
            return "Connection Failed"

    def module_loading_out(self, port_number="Port 1"):
        try:
            """
                This method is used to get out the part-loading
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("PLO:\r\n".encode())
            logger.info("PLC input: PLO:\r\n")

            t_end = time.time() + 7
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while module out {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while module out {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while module out {}".format(status))
                    return "Earth leakage is low"

                if 'E:LSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Left side door opened while module out {}".format(status))
                    return "Left side door is opened"

                if 'E:RSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Right side door opened while module out {}".format(status))
                    return "Right side door is opened"

                if 'K:PLO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:PLO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while module out {}".format(status))
                    return "Error in module loading out-position"

            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while module out {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at module_loading_out function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                    exc_tb.tb_lineno, e))
            return "Connection Failed"

    def module_loading_in(self, port_number="Port 1"):
        try:
            """
                This method is used to get in the part-loading
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("PLI:\r\n".encode())
            logger.info("PLC input: PLI:\r\n")

            t_end = time.time() + 7
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while module in {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while module in {}".format(status))
                    return "Earth leakage is low"

                if 'E:LSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Left side door opened while module out {}".format(status))
                    return "Left side door is opened"

                if 'E:RSD\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Right side door opened while module out {}".format(status))
                    return "Right side door is opened"

                if 'K:PLI\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:PLI\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while module in {}".format(status))
                    return "Error in module loading out-position"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while module in {}".format(status))
                    return "Air Pressure is low"

            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while module in {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at module_loading_in function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                   exc_tb.tb_lineno, e))
            return "Connection Failed"

    def tower_light_control(self, light, port_number="Port 1"):
        try:
            """
                This method is used to turn on light color
                param port_number: port number as str
                param light: which light color to turn on
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            if light == "Green":
                port.write("TLG:\r\n".encode())
                logger.info("PLC input: TLG:\r\n")

                t_end = time.time() + 3
                while time.time() < t_end:
                    status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if 'K:TLG\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        return "Passed"

                    if 'E:AIR\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Air pressure is low while tower light set {}".format(status))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Emergency pressed while tower light set {}".format(status))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Earth leakage is low while tower light set {}".format(status))
                        return "Earth leakage is low"

                else:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while tower light set {}".format(status))
                    return "PLC didn't return anything"

            elif light == "Yellow":
                port.write("TLY:\r\n".encode())
                logger.info("PLC input: TLY:\r\n")

                t_end = time.time() + 3
                while time.time() < t_end:
                    status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if 'K:TLY\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        return "Passed"

                    if 'E:AIR\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Air pressure is low while tower light set {}".format(status))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Emergency pressed while tower light set {}".format(status))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Earth leakage is low while tower light set {}".format(status))
                        return "Earth leakage is low"

                else:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while tower light set {}".format(status))
                    return "PLC didn't return anything"

            elif light == "Red":
                port.write("TLR:\r\n".encode())
                logger.info("PLC input: TLR:\r\n")

                t_end = time.time() + 3
                while time.time() < t_end:
                    status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if 'K:TLR\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        return "Passed"

                    if 'E:AIR\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Air pressure is low while tower light set {}".format(status))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Emergency pressed while tower light set {}".format(status))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Earth leakage is low while tower light set {}".format(status))
                        return "Earth leakage is low"

                else:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while tower light set {}".format(status))
                    return "PLC didn't return anything"

            elif light == "Red with Buzzer":
                port.write("TLE:\r\n".encode())
                logger.info("PLC input: TLE:\r\n")

                t_end = time.time() + 3
                while time.time() < t_end:
                    status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if 'K:TLE\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        return "Passed"

                    if 'E:AIR\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Air pressure is low while tower light set {}".format(status))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Emergency pressed while tower light set {}".format(status))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Earth leakage is low while tower light set {}".format(status))
                        return "Earth leakage is low"

                else:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while tower light set {}".format(status))
                    return "PLC didn't return anything"

            elif light == "Yellow blink":
                port.write("TLT:\r\n".encode())
                logger.info("PLC input: TLT:\r\n")

                t_end = time.time() + 3
                while time.time() < t_end:
                    status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if 'K:TLT\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        return "Passed"

                    if 'E:AIR\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Air pressure is low while tower light set {}".format(status))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Emergency pressed while tower light set {}".format(status))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Earth leakage is low while tower light set {}".format(status))
                        return "Earth leakage is low"

                else:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while tower light set {}".format(status))
                    return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at tower_light_control function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                     exc_tb.tb_lineno, e))
            return "Connection Failed"

    def gluing_init(self, port_number="Port 1"):
        try:
            """
                This method is used to initialize the gluing actuators
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("HMF:\r\n".encode())
            logger.info("PLC input: HMF:\r\n")

            t_end = time.time() + 50
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'K:HMF\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:HMF\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue motor initialization {}".format(status))
                    return "Error in glue motor initialization"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while gluing init {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while gluing init {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while gluing init {}".format(status))
                    return "Earth leakage is low"

            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while gluing init {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at gluing_init function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                             exc_tb.tb_lineno, e))
            return "Connection Failed"

    def apply_glue(self, speed=500, diameter=12, glue_type='Dry run', on_delay=None, off_delay=None,
                   port_number="Port 1"):
        try:
            """
                This method is used to apply gluing
                param port_number: port number as str
                param speed: At what speed should the arc occur?
                param diameter: lens diameter
                param glue_type: what type of glue apply (Dry run or Continuous glue)
                param on_delay: Pause the glue purge after the arc starts.
                param off_delay: Pause the glue purge before the arc ends.
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            if glue_type == "Dry run":
                command = "RUN9"

            elif glue_type == "Continuous glue":
                command = "RUN0"

                if on_delay is not None:
                    if type(on_delay) == float or type(on_delay) == int:
                        on_delay_value = float(on_delay) * 1000
                        on_delay_value_sec = int(on_delay_value)
                        status = ''
                        port.write("n{}:\r\n".format(str(on_delay_value_sec)).encode())
                        logger.info("PLC input: n{}:\r\n".format(str(on_delay_value_sec)))

                        t_end = time.time() + 15
                        while time.time() < t_end:
                            status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                            if "n:{}".format(str(on_delay_value_sec)) in status:
                                logger.info('Status from the Device: {}'.format(status))
                                break

                            if 'E:AIR\r\n' in status:
                                logger.info('Status from the Device: {}'.format(status))
                                machine_logger.error("Air pressure is low while gluing init {}".format(status))
                                return "Air Pressure is low"

                            if 'E:EMO\r\n' in status:
                                logger.info('Status from the Device: {}'.format(status))
                                machine_logger.error("Emergency pressed while gluing init {}".format(status))
                                return "Emergency button pressed"

                            if 'E:EMS\r\n' in status:
                                logger.info('Status from the Device: {}'.format(status))
                                machine_logger.error("Earth leakage is low while gluing init {}".format(status))
                                return "Earth leakage is low"
                        else:
                            logger.info('Failed to get acknowledge from on_delay: {}'.format(status))
                            return 'Failed to get acknowledge from on_delay'

                else:
                    logger.info("on_delay is None")

                if off_delay is not None:
                    if type(off_delay) == float or type(off_delay) == int:
                        off_delay_value = float(off_delay) * 1000
                        off_delay_value_sec = int(off_delay_value)

                        status = ''
                        port.write("f{}:\r\n".format(str(off_delay_value_sec)).encode())
                        logger.info("PLC input: f{}:\r\n".format(str(off_delay_value_sec)))

                        t_end = time.time() + 15
                        while time.time() < t_end:
                            status += port.read(port.inWaiting()).decode('utf-8', 'ignore')
                            if "f:{}".format(str(off_delay_value_sec)) in status:
                                logger.info('Status from the Device: {}'.format(status))
                                break
                            if 'E:AIR\r\n' in status:
                                logger.info('Status from the Device: {}'.format(status))
                                machine_logger.error("Air pressure is low while gluing init {}".format(status))
                                return "Air Pressure is low"

                            if 'E:EMO\r\n' in status:
                                logger.info('Status from the Device: {}'.format(status))
                                machine_logger.error("Emergency pressed while gluing init {}".format(status))
                                return "Emergency button pressed"

                            if 'E:EMS\r\n' in status:
                                logger.info('Status from the Device: {}'.format(status))
                                machine_logger.error("Earth leakage is low while gluing init {}".format(status))
                                return "Earth leakage is low"
                        else:
                            logger.info('Failed to get acknowledge from off_delay: {}'.format(status))
                            return 'Failed to get acknowledge from off_delay'
                else:
                    logger.info("off_delay is None")

            else:
                logger.error("Incorrect glue type: {}".format(glue_type))
                return "Incorrect glue type"

            if "".join(list(str(diameter).split("."))).isdigit():
                if 1 <= len("".join(list(str(diameter).split(".")))) <= 3:
                    x = float(diameter) * 10
                    diameter = (3 - len(str(int(x)))) * '0' + str(int(x))
                else:
                    logger.error("Incorrect glue diameter input")
                    return "Incorrect glue diameter input"
            else:
                logger.error("Incorrect glue diameter input")
                return "Incorrect glue diameter input"

            if "".join(list(str(speed).split("."))).isdigit():
                if 1 <= speed <= 1000:
                    speed = (4 - len(str(int(speed)))) * '0' + str(int(speed))
                    port.write("r{}:\r\n".format(str(speed)).encode())
                    logger.info("PLC input: r{}:\r\n".format(str(speed)))

                    t_end = time.time() + 15
                    while time.time() < t_end:
                        status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                        if "r:{}".format(str(speed)) in status:
                            logger.info('Status from the Device: {}'.format(status))
                            break
                    else:
                        logger.info('Failed to get acknowledge: {}'.format(status))

                else:
                    logger.error("Incorrect glue speed input")
                    return "Incorrect glue speed input"
            else:
                logger.error("Incorrect glue speed input")
                return "Incorrect glue speed input"

            time.sleep(0.15)
            port.write("{}{}:\r\n".format(str(command), str(diameter)).encode())
            logger.info("PLC input: {}{}:\r\n".format(str(command), str(diameter)))
            status = ""
            t_end = time.time() + 45
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'K:RUN\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while gluing apply {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while gluing apply {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while gluing apply {}".format(status))
                    return "Earth leakage is low"

                elif 'E:X1A\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense X-Axis 1 alarm {}".format(status))
                    return "Error in glue dispense X-Axis 1 alarm"

                elif 'E:X1H\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense X-Axis 1 home {}".format(status))
                    return "Error in glue dispense X-Axis 1 home"

                elif 'E:X1O\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense X-Axis 1 override {}".format(status))
                    return "Error in glue dispense X-Axis 1 override"

                elif 'E:X2A\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense X-Axis 2 alarm {}".format(status))
                    return "Error in glue dispense X-Axis 2 alarm"

                elif 'E:X2H\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense X-Axis 2 home {}".format(status))
                    return "Error in glue dispense X-Axis 2 home"

                elif 'E:X2O\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense X-Axis 2 override {}".format(status))
                    return "Error in glue dispense X-Axis 2 override"

                elif 'E:Y1A\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense Y-Axis 1 alarm {}".format(status))
                    return "Error in glue dispense Y-Axis 1 alarm"

                elif 'E:Y1H\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense Y-Axis 1 home {}".format(status))
                    return "Error in glue dispense Y-Axis 1 home"

                elif 'E:Y1O\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue dispense Y-Axis 1 override {}".format(status))
                    return "Error in glue dispense Y-Axis 1 override"

                elif 'E:GE1\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue cartridge 1 empty {}".format(status))
                    return "Error in glue cartridge 1 empty"

                elif 'E:GE2\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue cartridge 2 empty {}".format(status))
                    return "Error in glue cartridge 2 empty"

            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while gluing apply {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at apply_glue function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                            exc_tb.tb_lineno, e))
            return "Connection Failed"

    def write_glue_speed(self, speed=500, port_number="Port 1"):
        try:
            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""

            if "".join(list(str(speed).split("."))).isdigit():
                if 1 <= speed <= 1000:
                    speed = (4 - len(str(int(speed)))) * '0' + str(int(speed))
                    port.write("r{}:\r\n".format(str(speed)).encode())
                    logger.info("PLC input: r{}:\r\n".format(str(speed)))

                    t_end = time.time() + 2
                    while time.time() < t_end:
                        status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                        if "r:{}".format(str(speed)) in status:
                            logger.info('Status from the Device: {}'.format(status))
                            return "Passed"
                    else:
                        logger.info('Failed to get acknowledge: {}'.format(status))

                else:
                    logger.error("Incorrect glue speed input")
                    return "Incorrect glue speed input"
            else:
                logger.error("Incorrect glue speed input")
                return "Incorrect glue speed input"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at write_glue_speed function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                            exc_tb.tb_lineno, e))
            return "Connection Failed"

    def glue_reverse_paralel(self, port_number="Port 1", reverse_x1_x2=5):
        try:
            """
                This method is used to reverse the glue parallely.
                param port_number: port number as str
                param reverse_x1_x2: reverse position
                return: str
            """
            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            if reverse_x1_x2 is not None:
                if "".join(list(str(reverse_x1_x2).split("."))).isdigit():
                    if 1 <= len("".join(list(str(reverse_x1_x2).split(".")))) <= 3:
                        x = float(reverse_x1_x2) * 10
                        y_value = (3 - len(str(int(x)))) * '0' + str(int(x))
                    else:
                        logger.error("Incorrect glue y_value input")
                        return "Incorrect glue y_value input"
                else:
                    logger.error("Incorrect glue reverse_x1_x2 input")
                    return "Incorrect glue reverse_x1_x2 input"

                status_2 = ''
                port.write("xx{}:\r\n".format(str(y_value)).encode())
                logger.info("PLC input: xx{}:\r\n".format(str(y_value)))

                t_end = time.time() + 10
                while time.time() < t_end:
                    status_2 += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if "x1:{}".format(str(y_value)) in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        return "Passed"

                    if "x2:{}".format(str(y_value)) in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        return "Passed"

                    if 'E:AIR\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Air pressure is low while gluing y moving {}".format(status_2))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Emergency pressed while gluing y moving {}".format(status_2))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Earth leakage is low while gluing y moving {}".format(status_2))
                        return "Earth leakage is low"

                else:
                    logger.info('Failed to get acknowledge from xx: {}'.format(status_2))
                    machine_logger.error("Error occurred while gluing xx moving {}".format(status_2))
                    return "PLC didn't return anything"
            else:
                logger.info("xx value is None")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at apply_glue function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                            exc_tb.tb_lineno, e))

    def glue_manual_move_recipe(self, port_number="Port 1", x2_manual=None, x1_manual=None, y_manual=None):
        try:
            """
                This method is used to move the gluing actuators.
                param port_number: port number as str
                param x1_manual: position to move
                param x2_manual: position to move
                param y_manual: position to move
                return: str
            """
            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            if y_manual is not None:
                if "".join(list(str(y_manual).split("."))).isdigit():
                    if 1 <= len("".join(list(str(y_manual).split(".")))) <= 3:
                        x = float(y_manual) * 10
                        y_value = (3 - len(str(int(x)))) * '0' + str(int(x))
                    else:
                        logger.error("Incorrect glue y_value input")
                        return "Incorrect glue y_value input"
                else:
                    logger.error("Incorrect glue y_manual input")
                    return "Incorrect glue y_manual input"

                status_2 = ''
                port.write("y0{}:\r\n".format(str(y_value)).encode())
                logger.info("PLC input: y0{}:\r\n".format(str(y_value)))

                t_end = time.time() + 7
                while time.time() < t_end:
                    status_2 += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if "y0:{}".format(str(y_value)) in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        return "Passed"

                    if 'E:AIR\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Air pressure is low while gluing y moving {}".format(status_2))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Emergency pressed while gluing y moving {}".format(status_2))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Earth leakage is low while gluing y moving {}".format(status_2))
                        return "Earth leakage is low"

                else:
                    logger.info('Failed to get acknowledge from y0: {}'.format(status_2))
                    machine_logger.error("Error occurred while gluing y moving {}".format(status_2))
                    return "PLC didn't return anything"
            else:
                logger.info("Y value is None")

            if x1_manual is not None:
                if "".join(list(str(x1_manual).split("."))).isdigit():
                    if 1 <= len("".join(list(str(x1_manual).split(".")))) <= 3:
                        x = float(x1_manual) * 10
                        x1_value = (3 - len(str(int(x)))) * '0' + str(int(x))
                    else:
                        logger.error("Incorrect glue x1_value input")
                        return "Incorrect glue x1_value input"
                else:
                    logger.error("Incorrect glue x1_value input")
                    return "Incorrect glue x1_value input"

                status = ""
                port.write("x1{}:\r\n".format(str(x1_value)).encode())
                logger.info("PLC input: x1{}:\r\n".format(str(x1_value)))

                t_end = time.time() + 7
                while time.time() < t_end:
                    status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if "x1:{}".format(str(x1_value)) in status:
                        logger.info('Status from the Device: {}'.format(status))
                        return "Passed"

                    if 'E:AIR\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Air pressure is low while gluing X1 moving {}".format(status))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Emergency pressed while gluing X1 moving {}".format(status))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Earth leakage is low while gluing X1 moving {}".format(status))
                        return "Earth leakage is low"
                else:
                    logger.info('Failed to get acknowledge from x1: {}'.format(status))
                    machine_logger.error("Error occurred while gluing X1 moving {}".format(status))
                    return 'Failed to get acknowledge from'
            else:
                logger.info("X1 value is None")

            if x2_manual is not None:
                if "".join(list(str(x2_manual).split("."))).isdigit():
                    if 1 <= len("".join(list(str(x2_manual).split(".")))) <= 3:
                        x = float(x2_manual) * 10
                        x2_value = (3 - len(str(int(x)))) * '0' + str(int(x))
                    else:
                        logger.error("Incorrect glue x2_value input")
                        return "Incorrect glue x2_manual input"
                else:
                    logger.error("Incorrect glue x2_manual input")
                    return "Incorrect glue x2_manual input"

                status_1 = ""
                port.write("x2{}:\r\n".format(str(x2_value)).encode())
                logger.info("PLC input: x2{}:\r\n".format(str(x2_value)))

                t_end = time.time() + 7
                while time.time() < t_end:
                    status_1 += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if "x2:{}".format(str(x2_value)) in status_1:
                        logger.info('Status from the Device: {}'.format(status_1))
                        return "Passed"

                    if 'E:AIR\r\n' in status_1:
                        logger.info('Status from the Device: {}'.format(status_1))
                        machine_logger.error("Air pressure is low while gluing X2 moving {}".format(status_1))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status_1:
                        logger.info('Status from the Device: {}'.format(status_1))
                        machine_logger.error("Emergency pressed while gluing X2 moving {}".format(status_1))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status_1:
                        logger.info('Status from the Device: {}'.format(status_1))
                        machine_logger.error("Earth leakage is low while gluing X2 moving {}".format(status_1))
                        return "Earth leakage is low"
                else:
                    logger.info('Failed to get acknowledge from x2: {}'.format(status_1))
                    machine_logger.error("Error occurred while gluing X2 moving {}".format(status_1))
                    return "PLC didn't return anything"

            else:
                logger.info("X2 value is None")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at glue_move_manual function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                  exc_tb.tb_lineno, e))
            return "Connection Failed"

    def write_values_glue_offset(self, port_number="Port 1", c1_manual=None, c2_manual=None, c_manual=20):
        try:
            """
                This method is used to write the x1 and x2 values where the two needles meet.
                param port_number: port number as str
                param c1_manual: The x1 position value where the two needles meet.
                param c2_manual: The x2 position value where the two needles meet.
                param c_manual: The y position value where the two needles meet. 20 is the default value
                return: str
            """
            c1_manual_result = ""
            c2_manual_result = ""
            c_manual_result = ""

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            if c1_manual is not None:
                if "".join(list(str(c1_manual).split("."))).isdigit():
                    if 1 <= len("".join(list(str(c1_manual).split(".")))) <= 3:
                        x = float(c1_manual) * 10
                        c1_value = (3 - len(str(int(x)))) * '0' + str(int(x))
                    else:
                        logger.error("Incorrect glue x1_value input")
                        return "Incorrect glue x1_value input"
                else:
                    logger.error("Incorrect glue x1_value input")
                    return "Incorrect glue x1_value input"

                status = ""
                port.write("c1{}:\r\n".format(str(c1_value)).encode())
                logger.info("PLC input: c1{}:\r\n".format(str(c1_value)))

                t_end = time.time() + 7
                while time.time() < t_end:
                    status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if "c1:{}".format(str(c1_value)) in status:
                        logger.info('Status from the Device: {}'.format(status))
                        c1_manual_result = "Done"
                        break

                    if 'E:AIR\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Air pressure is low while gluing C1 offset writing {}".format(status))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Emergency pressed while gluing C1 Offset writing {}".format(status))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status:
                        logger.info('Status from the Device: {}'.format(status))
                        machine_logger.error("Earth leakage is low while gluing C1 offset writing {}".format(status))
                        return "Earth leakage is low"
                else:
                    logger.info('Failed to get acknowledge from c1: {}'.format(status))
                    machine_logger.error("Error occurred while gluing C1 offset writing {}".format(status))
                    return 'Failed to get acknowledge from C1'
            else:
                logger.info("c1_manual is None")

            if c2_manual is not None:
                if "".join(list(str(c2_manual).split("."))).isdigit():
                    if 1 <= len("".join(list(str(c2_manual).split(".")))) <= 3:
                        x = float(c2_manual) * 10
                        c2_value = (3 - len(str(int(x)))) * '0' + str(int(x))
                    else:
                        logger.error("Incorrect glue x2_value input")
                        return "Incorrect glue x2_manual input"
                else:
                    logger.error("Incorrect glue x2_manual input")
                    return "Incorrect glue x2_manual input"

                status_1 = ""
                port.write("c2{}:\r\n".format(str(c2_value)).encode())
                logger.info("PLC input: c2{}:\r\n".format(str(c2_value)))

                t_end = time.time() + 7
                while time.time() < t_end:
                    status_1 += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if "c2:{}".format(str(c2_value)) in status_1:
                        logger.info('Status from the Device: {}'.format(status_1))
                        c2_manual_result = "Done"
                        break

                    if 'E:AIR\r\n' in status_1:
                        logger.info('Status from the Device: {}'.format(status_1))
                        machine_logger.error("Air pressure is low while gluing C2 offset writing {}".format(status_1))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status_1:
                        logger.info('Status from the Device: {}'.format(status_1))
                        machine_logger.error("Emergency pressed while gluing C2 Offset writing {}".format(status_1))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status_1:
                        logger.info('Status from the Device: {}'.format(status_1))
                        machine_logger.error("Earth leakage is low while gluing C2 offset writing {}".format(status_1))
                        return "Earth leakage is low"
                else:
                    logger.info('Failed to get acknowledge from C2: {}'.format(status_1))
                    machine_logger.error("Error occurred while gluing C2 offset writing {}".format(status_1))
                    return 'Failed to get acknowledge from C2'
            else:
                logger.info("c2_manual is None")

            if c_manual is not None:
                if "".join(list(str(c_manual).split("."))).isdigit():
                    if 1 <= len("".join(list(str(c_manual).split(".")))) <= 3:
                        x = float(c_manual) * 10
                        c_value = (3 - len(str(int(x)))) * '0' + str(int(x))
                    else:
                        logger.error("Incorrect glue y_value input")
                        return "Incorrect glue y_value input"
                else:
                    logger.error("Incorrect glue y_manual input")
                    return "Incorrect glue y_manual input"

                status_2 = ''
                port.write("c0{}:\r\n".format(str(c_value)).encode())
                logger.info("PLC input: c0{}:\r\n".format(str(c_value)))

                t_end = time.time() + 7
                while time.time() < t_end:
                    status_2 += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                    if "c0:{}".format(str(c_value)) in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        c_manual_result = "Done"
                        break

                    if 'E:AIR\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Air pressure is low while gluing C0 offset writing {}".format(status_2))
                        return "Air Pressure is low"

                    if 'E:EMO\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Emergency pressed while gluing C0 offset writing {}".format(status_2))
                        return "Emergency button pressed"

                    if 'E:EMS\r\n' in status_2:
                        logger.info('Status from the Device: {}'.format(status_2))
                        machine_logger.error("Earth leakage is low while gluing C0 offset writing {}".format(status_2))
                        return "Earth leakage is low"
                else:
                    logger.info('Failed to get acknowledge from C2: {}'.format(status_2))
                    machine_logger.error("Error occurred while gluing C0 offset writing {}".format(status_2))
                    return 'Failed to get acknowledge from C0'
            else:
                logger.info("c0_manual is None")

            if c1_manual_result == "Done" and c2_manual_result == "Done" and c_manual_result == "Done":
                return "Passed"
            else:
                logger.info("Failed to write in center offset")
                return "Failed to write in center offset"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at center_glue_move_manual function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                         exc_tb.tb_lineno, e))
            return "Connection Failed"

    def glue_dispenser_timer(self, port_number="Port 1", dispenser_type="Both", timer=0, x1_value=40.0):
        try:
            """
                This method is used to purge the glue.
                param port_number: port number as str
                param dispenser_type: which needle to purge
                param timer: how many seconds to glue purge  
                param x1_value: values to return from plc once glue is purged.
                return: str
            """
            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            if dispenser_type == "Both":
                command = "D0"
            elif dispenser_type == "First":
                command = "D1"
            elif dispenser_type == "Second":
                command = "D2"

            if timer == 0:
                timer_value_sec = 0000

            elif type(timer) == float or type(timer) == int:
                timer_value_sec = timer * 1000
                timer_value_sec = str(int(timer_value_sec)).zfill(4)

            else:
                logger.error("Incorrect glue_timer input")
                return "Incorrect glue_timer input"

            status = ''
            port.write("{}{}:\r\n".format(command, str(timer_value_sec)).encode())
            logger.info("PLC input: {}{}:\r\n".format(command, str(timer_value_sec)))

            t_end = time.time() + 15
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if "x1:{}".format(str(x1_value)) in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if "D:{}{}".format(command[1], str(timer_value_sec)) in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure is low while spot glue apply {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while spot glue apply {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while spot glue apply {}".format(status))
                    return "Earth leakage is low"

                if 'E:GE1\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue cartridge 1 empty {}".format(status))
                    return "Error in glue cartridge 1 empty"

                if 'E:GE2\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in glue cartridge 2 empty {}".format(status))
                    return "Error in glue cartridge 2 empty"
            else:
                logger.info('Failed to get acknowledge {}'.format(status))
                machine_logger.error("Error occurred while spot glue apply {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at glue_dispenser_timer function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                                      exc_tb.tb_lineno, e))
            return "Connection Failed"

    def uv_door_open(self, port_number="Port 2"):
        try:
            """
                This method is used to open the uv door and cylinder.
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("UDO:\r\n".encode())
            logger.info("PLC input: UDO:\r\n")

            t_end = time.time() + 10
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'K:UDO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:UDO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while uv door open {}".format(status))
                    return "Error in UV door open"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure low while uv door open {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while uv door open {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while uv door open {}".format(status))
                    return "Earth leakage is low"
            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while uv door open {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at uv_door_open function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                              exc_tb.tb_lineno, e))
            return "Connection Failed"

    def uv_door_close(self, port_number="Port 1"):
        try:
            """
                This method is used to close the uv door and cylinder.
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("UDC:\r\n".encode())
            logger.info("PLC input: UDC:\r\n")
            t_end = time.time() + 10
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'K:UDC\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:UDC\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error occurred while uv door close {}".format(status))
                    return "Error in UV door open"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure low while uv door close {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while uv door close {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while uv door close {}".format(status))
                    return "Earth leakage is low"
            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while uv door close {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at uv_door_close function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                               exc_tb.tb_lineno, e))
            return "Connection Failed"

    def uv_light_out(self, port_number="Port 1"):
        try:
            """
                This method is used to out the uv cylinder.
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("UVO:\r\n".encode())
            logger.info("PLC input: UVO:\r\n")

            t_end = time.time() + 10
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'K:UVO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:URO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in uv move-out the right light {}".format(status))
                    return "Error in move-out the right light"

                if 'E:ULO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in uv move-out the left light {}".format(status))
                    return "Error in move-out the left light"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure low while uv light out {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while uv light out {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while uv light out {}".format(status))
                    return "Earth leakage is low"

            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while uv light out {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at uv_light_out function :{}|{}|{}|{}".format(exc_type, f_name,
                                                                              exc_tb.tb_lineno, e))
            return "Connection Failed"

    def uv_light_in(self, port_number="Port 1"):
        try:
            """
                This method is used to get in the uv cylinder.
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("UVC:\r\n".encode())
            logger.info("PLC input: UVC:\r\n")

            t_end = time.time() + 10
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', 'ignore')

                if 'K:UVC\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    return "Passed"

                if 'E:URC\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in uv move-in the right light {}".format(status))
                    return "Error in move-out the right light"

                if 'E:ULC\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Error in uv move-in the left light {}".format(status))
                    return "Error in move-out the left light"

                if 'E:AIR\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Air pressure low while uv light in {}".format(status))
                    return "Air Pressure is low"

                if 'E:EMO\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Emergency pressed while uv light in {}".format(status))
                    return "Emergency button pressed"

                if 'E:EMS\r\n' in status:
                    logger.info('Status from the Device: {}'.format(status))
                    machine_logger.error("Earth leakage is low while uv light in {}".format(status))
                    return "Earth leakage is low"

            else:
                logger.info('Status from the Device: {}'.format(status))
                machine_logger.error("Error occurred while uv light in {}".format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at uv_light_in function :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def check_input_status(self, port_number="Port 2"):
        try:
            """
                This method is used to get the ip status.
                param port_number: port number as str
                return: str
            """
            if port_number == "Port 1":
                port_1 = self.serial_port
            else:
                port_1 = self.serial_port_2

            for x in range(1):
                status = ""
                port_1.write("IPP:\r\n".encode())
                t_end = time.time() + 3
                logger.info("PLC input: IPP:\r\n")
                while time.time() < t_end:
                    status += port_1.read(port_1.inWaiting()).decode("unicode_escape")
                    result = re.split(r'[\n\r]+', status)
                    for x in result:
                        if x.startswith("I:"):
                            string = ""
                            for x in x[6:1:-1]:
                                string += bin(int(ord(x)))[2:].zfill(8)
                            input_values = string[::-1]
                            logger.info('Input status: length {} and values {}'.format(len(input_values), input_values))

                            if len(list(self.input_status.keys())) == len(input_values):
                                for x, y in zip(list(self.input_status.keys()), input_values):
                                    if int(y):
                                        self.input_status[x] = True
                                    else:
                                        self.input_status[x] = False
                                return "Status updated"

                            else:
                                return "Incorrect values"
                else:
                    logger.info("No status from plc")
                    return
            else:
                logger.info("After 3 iteration there is no response from plc")
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at input_status function :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def check_output_status(self, port_number="Port 1"):
        try:
            """
                This method is used to get the op status.
                param port_number: port number as str
                return: str
            """

            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            status = ""
            port.write("OPP:\r\n".encode())
            logger.info("PLC input: OPP:\r\n")
            t_end = time.time() + 3
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode('utf-8', "unicode_escape")
                if status.find("O:") != -1:
                    logger.info('Status from the Device: {}'.format(status))
                    string = ""
                    for x in status[6:1:-1]:
                        string += bin(int(ord(x)))[2:].zfill(8)

                    input_values = string[::-1]
                    logger.info('Output status: length {} and values {}'.format(len(input_values), input_values))
                    if len(list(self.input_status.keys())) == len(input_values):
                        for x, y in zip(list(self.output_status.keys()), input_values):
                            if int(y):
                                self.output_status[x] = True
                            else:
                                self.output_status[x] = False
                        return "Status updated"
                    else:
                        return "Incorrect values"
            else:
                logger.info('Status from the Device: {}'.format(status))
                return "PLC didn't return anything"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at output_status function :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def light_panel_lux(self, value=None):
        try:
            """
                This method is used to set the relay light panel lux.
                param value: intensity of lux value
                return: str
            """
            if not self.serial_port_1.isOpen():
                try:
                    logger.info("serial port is not opened: {}.".format(self.port_name_1))
                    self.serial_port_1.open()
                    self.serial_port_1.flushInput()
                    self.serial_port_1.flushOutput()
                    logger.info("serial port is opened")

                except Exception as e:
                    logger.error("Light panel is not connected.: {}".format(e))
                    return "Connection Failed"

            if type(value) == int and 0 <= value <= 1024:
                self.serial_port_1.write("{}".format(value).encode())
                logger.info("PLC input: {}\r\n".format(value))
                time.sleep(0.05)
                self.serial_port_1.write("{}".format("brt").encode())
                logger.info("PLC input: brt".format(value))
                time.sleep(0.05)
                status = ""
                t_end = time.time() + 10
                while time.time() < t_end:
                    status += self.serial_port_1.read(self.serial_port_1.inWaiting()).decode('utf-8', 'ignore')

                    if '{}'.format(value) in status:
                        logger.info('Status from the Device: {}'.format(status))
                        return "Passed"

                else:
                    logger.info('Status from the Device: {}'.format(status))
                    return "PLC didn't return anything"

            else:
                return "Invalid lux value"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at light_panel_lux function :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"

    def read_current_values_plc(self, text="Slider", port_number="Port 1"):
        try:
            """
                This method is used to get the current value of plc.
                param port_number: port number as str
                param text: The current value of which PLC should be retrieved
                return: str
            """
            if port_number == "Port 1":
                port = self.serial_port
            else:
                port = self.serial_port_2

            command = {"Slider": "Z1P:", "Gripper": "Z2P:", "Gluing_x1": "X1P:", "Gluing_x2": "X2P:",
                       "Gluing_y": "Y0P:"}

            status = ""
            port.write("{}\r\n".format(command[text]).encode())
            logger.info("PLC input: {}\r\n".format(command[text]))
            t_end = time.time() + 3
            add_string = []
            while time.time() < t_end:
                status += port.read(port.inWaiting()).decode("unicode_escape")
                for x in status.split("\r\n"):
                    if command[text][:-2] in x:
                        logger.info('Status from the Device: {}'.format(x))
                        for i in x:
                            add_string.append(str(ord(i)))
                        string_join = "".join(add_string[3:7])
                        logger.info(f"{text} current value is {string_join[0:2]}.{string_join[2:]}")
                        return f"{string_join[0:2]}.{string_join[2:]}"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at read_current_values_plc function :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
            return "Connection Failed"
