"""
This module is responsible for connect and access the old collimator.

"""
import ctypes
import time
from logger import logger
import os
import sys


class Collimator:
    def __init__(self):
        try:
            # import the DLL files
            self.color_type = None
            self.position_c = None
            self.distance_c = None
            self.product_type = None
            self.pwm_value = None
            self.pb_enabled = None
            self.pus_error_code = None
            self.pos_status = None
            self.electric_collimator = ctypes.cdll.LoadLibrary("{}\\{}".format(os.getcwd(), "electricCollimator_C.dll"))

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at collimator class init function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                        exc_tb.tb_lineno, e))

    def error_return(self, collimator):
        try:
            """
            param collimator: datatype in an integer which is the collimator no.
            return: result
            """
            self.pus_error_code = ctypes.c_int(15)
            if self.electric_collimator.GetErrorCode(collimator, ctypes.byref(self.pus_error_code)):
                # 0: normal, 1: Motor not enabled, 2: The motor is still moving, 3: Follow error alarm,
                # 4: Follow error fault,
                # 5: Driver current is slightly high, 6: Drive overheating, 7: Operation not permitted,
                # 8: Serial number error, 9: Power element failure, 10: Control mode conflict, 11: Servo mode error
                error = self.pus_error_code.value
                if self.electric_collimator.ClearError(collimator):
                    logger.info("Error cleared for collimator no. {}".format(collimator))
                else:
                    logger.info("Error is not cleared for collimator no. {}".format(collimator))
                if error == 0:
                    return 'Success'
                elif error == 1:
                    return 'Motor not enabled'
                elif error == 2:
                    return 'The motor is still moving'
                elif error == 3:
                    return 'Follow error alarm'
                elif error == 4:
                    return 'Follow error fault'
                elif error == 5:
                    return 'Driver current is slightly high'
                elif error == 6:
                    return 'Drive overheating'
                elif error == 7:
                    return 'Operation not permitted'
                elif error == 8:
                    return 'Serial number error'
                elif error == 9:
                    return 'Power element failure'
                elif error == 10:
                    return 'Control mode conflict'
                elif error == 11:
                    return 'Servo mode error'
                else:
                    return 'Unknown error found'
            else:
                return 'Unable to fetch the error code.'

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at collimator error_return function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                          exc_tb.tb_lineno, e))

    def connect_device(self, port_name=None, collimator_list=None):
        try:
            """
            param port_name: datatype in str and port no.
            param collimator_list: datatype in list which are the collimator no.
            return: result
            """
            if port_name:
                if type(collimator_list) == list and collimator_list:
                    for x in collimator_list:
                        if self.electric_collimator.ManualConnect2(port_name, 19200, x):
                            logger.info('Collimator no. {} is connected'.format(x))
                            time.sleep(0.25)
                        else:
                            logger.error('Collimator no. {} is not connected'.format(x))
                            return 'Collimator no. {} is not connected: {}'.format(x, self.error_return(x))
                    return 'Passed'
                else:
                    return "Invalid collimator_list"
            else:
                if type(collimator_list) == list and collimator_list:
                    for x in collimator_list:
                        if self.electric_collimator.AutoConnect2(19200, x):
                            logger.info('Collimator no. {} is connected'.format(x))
                            time.sleep(0.25)
                        else:
                            logger.error('Collimator no. {} is not connected'.format(x))
                            return 'Collimator no. {} is not connected{}'.format(x, self.error_return(x))
                    return 'Passed'

                else:
                    logger.error("Invalid collimator list")
                    return "Invalid collimator_list"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at collimator connect_device function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                            exc_tb.tb_lineno, e))

    def enable_device(self, collimator_list=None):
        try:
            """
            param collimator_list: datatype in list which are the collimator no.
            return: result
            """
            if type(collimator_list) == list and collimator_list:
                for x in collimator_list:
                    if self.electric_collimator.Enable(x, bool(1)):
                        self.pb_enabled = ctypes.c_bool(False)
                        self.electric_collimator.IsEnabled(x, ctypes.byref(self.pb_enabled))
                        if self.pb_enabled.value:
                            logger.info('Collimator no. {} is enabled'.format(x))
                        else:
                            logger.error('Collimator no. {} is not enabled'.format(x))
                            return 'Collimator no. {} is not enabled'.format(x)
                    else:
                        logger.error('Collimator no. {} is not enabled'.format(x))
                        return 'Collimator no. {} is not enabled'.format(x)
                return 'Passed'
            else:
                logger.error("Invalid collimator_list")
                return "Invalid collimator_list"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at collimator enable_device function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                           exc_tb.tb_lineno, e))

    def disable_device(self, collimator_list=None):
        try:
            """
            param collimator_list: datatype in list which are the collimator no.
            return: result
            """
            if type(collimator_list) == list and collimator_list:
                for x in collimator_list:
                    if self.electric_collimator.Enable(x, bool(0)):
                        self.pb_enabled = ctypes.c_bool(True)
                        self.electric_collimator.IsEnabled(x, ctypes.byref(self.pb_enabled))
                        if not self.pb_enabled.value:
                            logger.info('Collimator no. {} is disabled'.format(x))
                        else:
                            logger.error('Collimator no. {} is not disabled'.format(x))
                            return 'Collimator no. {} is not disabled'.format(x)
                    else:
                        logger.error('Collimator no. {} is not disabled'.format(x))
                        return 'Collimator no. {} is not disabled'.format(x)
                return 'Passed'
            else:
                logger.error("Invalid collimator list")
                return "Invalid collimator_list"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at collimator disable_device function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                            exc_tb.tb_lineno, e))

    def change_collimator_distance(self, distances=0, collimator_list=None):
        try:
            """
            param distances: datatype in an integer and value in  mm.
            param collimator_list: datatype in list which are the collimator no.
            return: result
            """
            if type(distances) == int and 500 <= distances <= 1000000000:
                self.product_type = ctypes.c_wchar_p("")
                self.distance_c = ctypes.c_float(distances)
                if type(collimator_list) == list and collimator_list:
                    for x in collimator_list:
                        if self.electric_collimator.GetProductType(x, self.product_type):
                            if self.electric_collimator.MoveAbsByFun(x, self.distance_c, self.product_type, 0):
                                logger.info("The chart in collimator no. {} is "
                                            "trying to reach the distance {}".format(x, distances))
                            else:
                                logger.error('MoveAbsByFun function failed; collimator no. {} at the position ' \
                                             '{}: {}'.format(x, distances, self.error_return(x)))
                                return 'MoveAbsByFun function failed; collimator no. {} at the position ' \
                                       '{}: {}'.format(x, distances, self.error_return(x))
                        else:
                            logger.error("Failed to get the product type for collimator no. {}".format(x))
                            return "Failed to get the product type for collimator no. {}".format(x)
                    time.sleep(1)
                    for x in collimator_list:
                        if self.electric_collimator.GetProductType(x, self.product_type):
                            self.position_c = ctypes.c_float(0.0)
                            if self.electric_collimator.GetActPos2(x, ctypes.byref(self.position_c), self.product_type,
                                                                   0):
                                if self.position_c.value != distances / 1000:
                                    return 'The chart in collimator no. {} is failed to reach the position ' \
                                           '{}: {}|{}'.format(x, distances, self.error_return(x), self.position_c.value)
                            else:
                                logger.error('GetActPos2 function failed; collimator no. {} at the position ' \
                                             '{}: {}'.format(x, distances, self.error_return(x)))
                                return 'GetActPos2 function failed; collimator no. {} at the position ' \
                                       '{}: {}'.format(x, distances, self.error_return(x))
                        else:
                            logger.error("Failed to get the product type for collimator no. {}".format(x))
                            return "Failed to get the product type for collimator no. {}".format(x)
                    return 'Passed'
                else:
                    logger.error("Invalid collimator_list")
                    return "Invalid collimator_list"
            else:
                logger.error('Distances is incorrect')
                return 'Distances is incorrect'

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at collimator change_collimator_distance function : {}|{}|{}|{}".format(
                exc_type, func_name, exc_tb.tb_lineno, e))

    def change_collimator_light(self, light=None, collimator_list=None, light_type='Visible'):
        """
        param light: datatype in an integer from 0 to 255.
        param collimator_list: datatype in list which are the collimator no.
        return: result
        collimator position as old collimator no: 1:BL, 2:TL, 3:TR, 4:BR, 5:C (For Info)
        """
        if light is None:
            light = [0, 0, 0, 0, 0]

        if light_type == 'Visible':
            self.color_type = ctypes.c_char(b"w")
        elif light_type == "IR850":
            self.color_type = ctypes.c_char(b"i")
        elif light_type == "IR940":
            self.color_type = ctypes.c_char(b"9")
        else:
            return "Invalid light type of collimator"

        if type(light) == list and type(collimator_list) == list:
            for x, y in zip(collimator_list, light):
                if 0 <= y <= 255 and type(y) == int:
                    self.product_type = ctypes.c_wchar_p("")
                    self.pwm_value = ctypes.c_ushort(y)
                    if type(collimator_list) == list and collimator_list:
                        if self.electric_collimator.GetProductType(x, self.product_type):
                            if not self.electric_collimator.SetLedPwm(x, self.color_type,
                                                                      self.pwm_value, self.product_type):
                                return 'The chart in collimator no. {} is failed to change the light ' \
                                       '{}: {}|{}'.format(x, light, self.error_return(x), self.pwm_value.value)
                            time.sleep(0.25)
                        else:
                            return "Failed to get the product type for collimator no. {}".format(x)
                    else:
                        return "Invalid collimator_list"
                else:
                    return 'Light value is incorrect'

            return 'Passed'

        else:
            return "Invalid collimator_list"

    def reset_collimator(self, collimator_list=None):
        """
        param collimator_list: datatype in list which are the collimator no.
        return: result
        """
        if type(collimator_list) == list and collimator_list:
            enable_device_return = self.enable_device(collimator_list)
            if enable_device_return == "Passed":
                # Turn off the light
                light_return = self.change_collimator_light(collimator_list=collimator_list)
                if light_return == "Passed":
                    for x in collimator_list:
                        if not self.electric_collimator.SoftLanding(x, ctypes.c_ushort(10), 1, ctypes.c_ushort(800), 0):
                            logger.error("Failed to softlanding the collimator no. {}".format(x))
                            return "Failed to softlanding the collimator no. {}".format(x)
                    time.sleep(2)
                    for x in collimator_list:
                        self.pos_status = ctypes.c_bool(False)
                        n_timeout = 0
                        while n_timeout < 80:  # Timeout for limit seeking in negative direction: 8 seconds
                            self.electric_collimator.IsInPosition(x, ctypes.byref(self.pos_status))
                            if self.pos_status.value:
                                break
                            time.sleep(0.1)
                            n_timeout += 1
                        else:
                            logger.error("SoftLanding timeout for collimator no. {}: {}".format(x, self.error_return(x)))
                            return "SoftLanding timeout for collimator no. {}: {}".format(x, self.error_return(x))

                    for x in collimator_list:
                        if not self.electric_collimator.FindIndex(x, ctypes.c_ushort(10), ctypes.c_ushort(100), 0, 0):
                            logger.error("Failed to find_index of the collimator no. {}".format(x))
                            return "Failed to find_index of the collimator no. {}".format(x)
                    time.sleep(2)
                    for x in collimator_list:
                        self.pos_status = ctypes.c_bool(False)
                        n_timeout = 0
                        while n_timeout < 50:  # Timeout for limit seeking in negative direction: 8 seconds
                            self.electric_collimator.IsInPosition(x, ctypes.byref(self.pos_status))
                            if self.pos_status.value:
                                # reset the motor
                                # self.electric_collimator.SetVel(x, 50)
                                # self.electric_collimator.SetAcc(x, 10)
                                break
                            time.sleep(0.1)
                            n_timeout += 1
                        else:
                            logger.error("FindIndex timeout for collimator no. {}: {}".format(x, self.error_return(x)))
                            return "FindIndex timeout for collimator no. {}: {}".format(x, self.error_return(x))
                    return 'Passed'
                else:
                    logger.error("The light is turned off: {}".format(light_return))
                    return "The light is turned off: {}".format(light_return)
            else:
                logger.error("Enable issue: {}".format(enable_device_return))
                return "Enable issue: {}".format(enable_device_return)
        else:
            logger.error("Invalid collimator_list")
            return "Invalid collimator_list"

    def __del__(self):
        self.electric_collimator = None
        self.color_type = None
        self.position_c = None
        self.distance_c = None
        self.product_type = None
        self.pwm_value = None
        self.pb_enabled = None
        self.pus_error_code = None
        self.pos_status = None
