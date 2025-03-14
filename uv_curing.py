"""
    This module is used to access the uv controller
"""

import os
import struct
import sys
import time
from logger import logger
from serial.tools import list_ports

from pymodbus.client import ModbusSerialClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException


class UVcuring:
    def __init__(self):
        try:
            self.client = None

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at Initial settings :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def read_values(self):
        try:
            """
                This method is used to read the values of uv controller
                return: str
            """
            res = self.client.read_holding_registers(address=63, count=4, slave=1)
            if not res.isError():
                print(res.registers)
                return "Passed"

            else:
                logger.error("Error in read_holding_registers: {}".format(res))
                return "Movement error occurred"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at read_values :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def write_values(self, brightness, delay):
        try:
            """
                This method is used to write the values of uv controller
                return: str
            """
            if type(brightness) == int and type(delay) == int and (10 <= brightness <= 100) and (1 <= delay <= 999):
                values = [brightness, delay, brightness, delay]

            else:
                logger.error("Incorrect input: brightness {} and delay {}".format(brightness, delay))
                return "Incorrect values"

            write = self.client.write_registers(address=63, values=values, slave=1, count=4)
            if isinstance(write, ModbusIOException):
                logger.error("Error in write_registers: {}".format(write))
                return "Movement error occurred"
            else:
                return "Passed"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at write_values :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))

    def uv_power_on(self):
        try:
            """
                This method is used to turn on uv controller.
                return: str
            """
            write = self.client.write_registers(address=24, values=[1, 0], slave=1, count=2)
            if isinstance(write, ModbusIOException):
                logger.error("Error in write_registers: {}".format(write))
                return "Movement error occurred"

            else:
                res = self.client.read_holding_registers(address=24, count=2, slave=1)
                if not res.isError():
                    print(res.registers)

                else:
                    logger.error("Error in read_holding_registers: {}".format(res))
                    return "Movement error occurred"

                return "Passed"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at uv_power_on :{}|{}|{}|{}".format(exc_type, f_name, exc_tb.tb_lineno, e))
