"""
This module is used to access the actuators.
"""

import os
import struct
import sys
import time
from logger import logger
from machine_logger import machine_logger
from serial.tools import list_ports
from pymodbus.client import ModbusSerialClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException


class ModbusControl:
    def __init__(self):
        # 1 : slave id
        # 985.145848 : Pulse
        self.pulse_per_mm = {1: 985.145848, 2: 25600, 3: 800, 4: 800, 5: 800}  #
        try:
            self.timer_stop = None
            self.client = None

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at Initial settings :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def read_modbus_holding_registers(self, address, count, unit):
        try:
            res = self.client.read_holding_registers(address=address, count=count, slave=unit)
            if not res.isError():
                return res.registers
            else:
                return res

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at read_modbus_holding_registers :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def write_modbus_registers(self, address, value, unit, count=1):
        if count == 1:
            write = self.client.write_register(address=address, value=value, slave=unit)
        elif count == 2:
            write = self.client.write_registers(address=address, values=value, slave=unit, count=2)
        else:
            return "Incorrect count."

        if isinstance(write, ModbusIOException):
            return write
        else:
            return True

    def read_modbus_input_registers(self, address, count, unit, client):
        res = self.client_1.read_input_registers(address=address, counts=count, slave=unit)
        if not res.isError():
            return res.registers
        else:
            return res

    def height_sensor_value(self):
        try:
            """
              This method is used to get the height sensor value.
              param lists: None
              return: None
            """
            res = self.client.read_input_registers(address=109, counts=2, slave=6)
            if not res.isError():
                if res.registers[0] == 0:
                    res = self.client.read_input_registers(address=101, counts=2, slave=6)
                    if not res.isError():
                        return res.registers[0]
                    else:
                        logger.error('Can not able to read the height input register: {}'.format(res))
                        return "Error"

                else:
                    logger.error('Error while reading the laser height value: {}'.format(res.registers[0]))
                    return "Error"
            else:
                logger.error('Can not able to read the height input register: {}'.format(res))
                return "Error"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at height_sensor_value :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    @staticmethod
    def struct_32_to_16(value):
        """
          This method is used to convert 32bit into 16bit.
          param lists: value is bit type
          return: value as list
        """
        result = struct.unpack(">HH", struct.pack(">l", value))
        return [result[1], result[0]]

    @staticmethod
    def struct_16_to_32(values):
        if len(values) == 2:
            return struct.unpack(">l", struct.pack(">HH", values[1], values[0]))[0]
        else:
            return "Incorrect values."

    def read_status(self):
        try:
            while True:
                if not self.client.connect():
                    logger.error('Cannot connect to the Modbus Server')
                    break
                slave_id = [1, 2, 3, 4, 5, 6]
                for x in slave_id:
                    self.alarm_display(x)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at read_status :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def actuator_homing(self, slave_id):
        try:
            if not self.client.connect():
                logger.error('Cannot connect to the Modbus Server')
                return "Connection Failed"
            if slave_id == 1:
                logger.info("The slave id {} is move to homing".format(slave_id))
            elif slave_id == 2:
                logger.info("The slave id {} is move to homing".format(slave_id))
            elif slave_id == 3:
                logger.info("The slave id {} is move to homing".format(slave_id))
            elif slave_id == 4:
                logger.info("The slave id {} is move to homing".format(slave_id))
            elif slave_id == 5:
                logger.info("The slave id {} is move to homing".format(slave_id))
            else:
                logger.info("Incorrect ID given: {}".format(slave_id))
                return "Incorrect ID"

            # trigger homing position command
            trigger_position = 2
            trigger_position = self.struct_32_to_16(trigger_position)
            write = self.client.write_registers(address=1294, values=trigger_position, slave=slave_id, count=2)
            if isinstance(write, ModbusIOException):
                logger.error("Error in write_registers: {}".format(write))
                return "Movement error occurred"
            else:
                while True:
                    res = self.client.read_holding_registers(address=18, count=2, slave=slave_id)
                    if not res.isError():
                        current_position = self.struct_16_to_32(res.registers)
                        time.sleep(1)
                        res = self.client.read_holding_registers(address=18, count=2, slave=slave_id)
                        if not res.isError():
                            current_position_1 = self.struct_16_to_32(res.registers)
                            if current_position_1 == current_position:
                                logger.info("The slave id {} is moved to homing position.".format(slave_id))
                                return_value = self.actuator_movement(slave_id=slave_id, distance=5)
                                if return_value == "Passed":
                                    return "Passed"
                                else:
                                    logger.debug("Error in movement:{}".format(return_value))
                                    alarm_check = self.alarm_display(slave_id=slave_id)
                                    if alarm_check != "Passed":
                                        machine_logger.error("Error in actuator while homing {}".format(alarm_check))
                                    return "Movement error occurred"
                        else:
                            logger.error("Error in read_holding_registers: {}".format(res))
                            return "Movement error occurred"

                    else:
                        logger.error("Error in read_holding_registers: {}".format(res))
                        return "Movement error occurred"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at actuator_homing :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def alarm_display(self, slave_id):
        try:
            if not self.client.connect():
                logger.error('Cannot connect to the Modbus Server')
                return "Connection Failed"

            if slave_id == 1:
                pass
                # print("1")
                # logger.info("The slave id {} alarm".format(slave_id))
            elif slave_id == 2:
                pass
                # logger.info("The slave id {} alarm".format(slave_id))
            elif slave_id == 3:
                pass
                # logger.info("The slave id {} alarm".format(slave_id))
            elif slave_id == 4:
                pass
                # logger.info("The slave id {} alarm".format(slave_id))
            elif slave_id == 5:
                pass
                # logger.info("The slave id {} alarm".format(slave_id))
            else:
                logger.info("Incorrect ID given: {}".format(slave_id))
                return "Incorrect ID"

            res = self.client.read_holding_registers(address=2, count=2, slave=slave_id)
            if not res.isError():
                if hex(self.struct_16_to_32(res.registers))[2:] == "13":
                    machine_logger.error(f"Emergency pressed while slave id {slave_id} is moving")
                    return "Emergency pressed"

                elif hex(self.struct_16_to_32(res.registers))[2:] == "14":
                    machine_logger.error(f"The slave id {slave_id} is Home sensor detected")
                    return "Home sensor detected"

                elif hex(self.struct_16_to_32(res.registers))[2:] == "15":
                    machine_logger.error(f"The slave id {slave_id} is Overload sensor detected")
                    return "Overload sensor detected"

                elif hex(self.struct_16_to_32(res.registers))[2:] == "30":
                    machine_logger.error("The slave id {} is Motor crash".format(slave_id))
                    return "Motor crash"
                else:
                    if hex(self.struct_16_to_32(res.registers))[2:] != "0":
                        machine_logger.error("Alarm status: {}".format(hex(self.struct_16_to_32(res.registers))[2:]))
                        logger.error("Alarm status: {}".format(hex(self.struct_16_to_32(res.registers))[2:]))
                        return "Alarm occurred"

                    else:
                        return "Passed"
            else:
                logger.error("Error in read_holding_registers: {}".format(res))
                return "Alarm read error occurred"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at alarm_display :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def read_actuator_current_position(self, slave_id):
        try:
            res = self.client.read_holding_registers(address=18, count=2, slave=slave_id)
            if not res.isError():
                current_position = self.struct_16_to_32(res.registers)
                current_position = round(current_position / self.pulse_per_mm[slave_id], 2)
                # print(current_position, type(current_position), "current position")
                logger.info(f"The slave id {slave_id} current position is {current_position}")
                return current_position

            return "Unable to read actuator"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at read_actuator_current_position :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def actuator_movement(self, slave_id, distance, speed=2000):
        try:
            if not self.client.connect():
                logger.error('Cannot connect to the Modbus Server')
                return "Connection Failed"

            if slave_id == 1:
                logger.info("The slave id {} is move to {} mm".format(slave_id, distance))
                distance_value = int(distance * self.pulse_per_mm[slave_id])
                # Speed Control(RPM)
                speed_value = speed  # 1000 speed is 100 mm/min  #15000

            elif slave_id == 2:
                logger.info("The slave id {} is move to {} mm".format(slave_id, distance))
                distance_value = int(distance * self.pulse_per_mm[slave_id])
                # print("distance_value", distance_value)
                # Speed Control(RPM)
                speed_value = speed  # 1000 speed is 100 mm/min  #2000

            elif slave_id == 3:
                logger.info("The slave id {} is move to {} mm".format(slave_id, distance))
                distance_value = int(distance * self.pulse_per_mm[slave_id])
                # print("distance_value", distance_value)
                # Speed Control(RPM)
                speed_value = speed  # 1000 speed is 100 mm/min  #2000

            elif slave_id == 4:
                logger.info("The slave id {} is move to {} mm".format(slave_id, distance))
                distance_value = int(distance * self.pulse_per_mm[slave_id])
                # print("distance_value", distance_value)
                # Speed Control(RPM)
                speed_value = speed  # 1000 speed is 100 mm/min  #2000

            elif slave_id == 5:
                logger.info("The slave id {} is move to {} mm".format(slave_id, distance))
                distance_value = int(distance * self.pulse_per_mm[slave_id])
                # Speed Control(RPM)
                speed_value = speed  # 1000 speed is 100 mm/min  #2000

            else:
                logger.info("Incorrect ID given: {}".format(slave_id))
                return "Incorrect ID"

            # Path 1 for position
            distance_values = self.struct_32_to_16(distance_value)
            # print("distance_values", distance_values)
            write = self.client.write_registers(address=1542, values=distance_values, slave=slave_id, count=2)
            if isinstance(write, ModbusIOException):
                logger.error("Error in write_registers: {}".format(write))
                return "Movement error occurred"

            res = self.client.read_holding_registers(address=1542, count=2, slave=slave_id)
            if not res.isError():
                if distance_value == self.struct_16_to_32(res.registers):
                    speed_values = self.struct_32_to_16(speed_value)
                    write = self.client.write_registers(address=1400, values=speed_values, slave=slave_id, count=2)
                    if isinstance(write, ModbusIOException):
                        logger.error("Error in write_registers: {}".format(write))
                        return "Movement error occurred"

                    # trigger position command
                    trigger_position = 1
                    trigger_position = self.struct_32_to_16(trigger_position)
                    write = self.client.write_registers(address=1294, values=trigger_position, slave=slave_id, count=2)
                    if isinstance(write, ModbusIOException):
                        logger.error("Error in write_registers: {}".format(write))
                        return "Movement error occurred"

                    while True:
                        res = self.client.read_holding_registers(address=18, count=2, slave=slave_id)
                        if not res.isError():
                            alarm_check = self.alarm_display(slave_id=slave_id)
                            if alarm_check != "Passed":
                                machine_logger.error("Error in actuator movement {}".format(alarm_check))
                                return "Movement error occurred"

                            current_position = self.struct_16_to_32(res.registers)
                            if distance_value == current_position:
                                logger.info("The slave id {} is moved to {} mm".format(slave_id, distance))
                                return "Passed"

                            # time.sleep(1)
                            res = self.client.read_holding_registers(address=18, count=2, slave=slave_id)
                            if not res.isError():
                                alarm_check = self.alarm_display(slave_id=slave_id)
                                if alarm_check != "Passed":
                                    machine_logger.error("Error in actuator movement {}".format(alarm_check))
                                    return "Movement error occurred"

                                current_position_1 = self.struct_16_to_32(res.registers)
                                if current_position_1 == current_position:
                                    if distance_value - 5 <= current_position_1 <= distance_value + 5:
                                        logger.info("The slave id {} is moved to {} mm".format(slave_id, distance))
                                        return "Passed"
                                    else:
                                        logger.error("Unable to move the actuator")
                                        logger.error("Actuator current position {} requested position {}".format(
                                            current_position / self.pulse_per_mm[slave_id], distance))
                                        alarm_check = self.alarm_display(slave_id=slave_id)
                                        if alarm_check != "Passed":
                                            machine_logger.error("Error in actuator movement {}".format(alarm_check))
                                            return "Movement error occurred"
                                        return "Movement error occurred"
                            else:
                                logger.error("Error in read_holding_registers: {}".format(res))
                                return "Movement error occurred"

                        else:
                            logger.error("Error in read_holding_registers: {}".format(res))
                            return "Movement error occurred"

                else:
                    logger.error("Error in read_holding_registers: {}".format(res))
                    return "Movement error occurred"
            else:
                logger.error("Error in read_holding_registers: {}".format(res))
                return "Movement error occurred"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at actuator_movement :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))


# modbus = ModbusControl()
# modbus.read_actuator_current_position(slave_id=2)
# print(modbus.actuator_homing(5))
# print(modbus.height_sensor_value())
# print(modbus.actuator_movement(5, 15))
# print(modbus.alarm_display(5))
# res = modbus.client.read_holding_registers(address=18, count=2, slave=1)
# if not res.isError():
#     # if distance_value == modbus.struct_16_to_32(res.registers):
#         # logger.info("The slave id {} is moved to {} mm".format(slave_id, distance))
#     print(modbus.struct_16_to_32(res.registers))
# else:
#     # logger.error("Error in: {}".format(res))
#     print("Movement error occurred")

# res = modbus.client.read_holding_registers(address=1542, counts=[2, 0], unit=2)
# if not res.isError():
#     print(res.registers)
# else:
#     print(res)
#
# if modbus.client.connect():  # Trying for connect to Modbus Server/Slave
#     '''Reading from a holding register with the below content.'''
#     print("connected")
#     # print(modbus.read_modbus_input_registers(address=101, count=1, unit=1)) # for height sensor
#     # res = client.read_input_registers(address=101, count=1, unit=1)
#     values = modbus.read_modbus_holding_registers(address=1542, count=2, unit=1)
#     # res = client.read_holding_registers(address=1542, count=2, unit=1)
#     print(modbus.struct_16_to_32(values), values)
#     #     '''Reading from a discrete register with the below content.'''
#     #     # res = client.read_discrete_inputs(address=1, count=1, unit=1)
#
#     # if not res.isError():
#     #     print(res.registers)
#     # else:
#     #     print(res)
#     # Path 1 for position
#     unit = 1
#     value = 300
#     values = modbus.struct_32_to_16(value)
#     print(modbus.write_modbus_registers(address=1542, value=values, unit=unit, count=2))
#     # write = client.write_registers(address=1542, values=value, unit=unit,
#     # count=2)
#     # Speed Control(RPM)
#     value = 1000  # speed is 100 mm/min
#     values = modbus.struct_32_to_16(value)
#     print(modbus.write_modbus_registers(address=1400, value=values, unit=unit, count=2))
#     # speed = client.write_registers(address=1400, values=[1000, 0], unit=unit, count=2)
#     # write = client.write_register(address=1034, value=value, unit=unit)
#
#     # print(write)
#     # if isinstance(write, ModbusIOException):
#     #     print(write)
#     # time.sleep(2)
#     # trigger position command
#     value = 1
#     values = modbus.struct_32_to_16(value)
#     print(modbus.write_modbus_registers(address=1294, value=values, unit=unit, count=2))
#     # trigger = client.write_registers(address=1294, values=[1, 0], unit=unit, count=2)
#     read_values = modbus.read_modbus_holding_registers(address=1542, count=2, unit=1)
#     print(modbus.struct_16_to_32(read_values), read_values)
#
#     # trigger Homing position command
#     value = 2
#     values = modbus.struct_32_to_16(value)
#     print(modbus.write_modbus_registers(address=1294, value=values, unit=unit, count=2))
#     # trigger = client.write_registers(address=1294, values=[1, 0], unit=unit, count=2)
#     read_values = modbus.read_modbus_holding_registers(address=1542, count=2, unit=1)
#     print(modbus.struct_16_to_32(read_values), read_values)
#
#
# else:
#     print('Cannot connect to the Modbus Server/Slave')
