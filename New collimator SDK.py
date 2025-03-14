"""
This module is used to connect new collimator and its functionalities
"""

import time
import ctypes
from logger import logger
import sys
import os


class New_collimator:
    def __init__(self):
        self.productType = ctypes.c_char_p(b'PL120STS')
        self.read_actual_distance_m = ctypes.c_float(-1)
        self.read_actual_distance_mm = ctypes.c_float(-1)
        self.collimator_dll = ctypes.cdll.LoadLibrary(r"D:\lens-focusing-automation-master-Source\MTF "
                                                      r"PROJECT\e-ZeeFocus-automation3.2.2\New collimator "
                                                      r"dll's\electricCollimator_C.dll")

    def collimator_homing(self, collimator_list=None):
        try:
            """
              This method is used to initialize the collimator.
              param lists: None
              return: None
            """
            if type(collimator_list) == list and collimator_list:
                for x in collimator_list:
                    ret = self.collimator_dll.MX_Homing(x)
                    if not ret:
                        return f"Failed to homing collimator no.{x}"
                    time.sleep(0.5)
                    logger.info(f"Collimator {x} homing is completed")
                return "Passed"
            logger.error("Invalid collimator_list")
            return "Invalid collimator_list"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(
                "Error at collimator_homing function : {}|{}|{}|{}".format(exc_type, func_name, exc_tb.tb_lineno, e))

    def connect_device(self, collimator_list=None):
        try:
            """
            connect Collimator
            param collimator_list: addresses of collimator's
            return:0 or 1
            """
            if type(collimator_list) == list and collimator_list:
                for x in collimator_list:
                    if x not in ["1", "2", "3", "4", "5"]:  # The addresses of connect multiple collimator's
                        logger.error(f"Input collimator address error {collimator_list}")
                        return

                    var = self.collimator_dll.MX_AutoConnect(int(x))
                    if not var:
                        logger.error(f"Error to connect collimator no.{x}")
                        return "Error to connect collimator"

                    logger.info(f"Collimator no.{x} is connected")
                    time.sleep(0.5)

                for i in collimator_list:
                    if i not in ["1", "2", "3", "4", "5"]:  # The addresses of connect multiple collimator's
                        logger.error(f"Input collimator address error {collimator_list}")
                        return

                    ret = self.collimator_dll.GetProductType(int(i), self.productType)
                    if not ret:
                        logger.error(f"Error to connect collimator no.{i}")
                        return "Failed to connect collimator"
                    time.sleep(0.5)
                return "Passed"
            logger.error("Invalid collimator_list")
            return "Invalid collimator_list"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at connect_device function : {}|{}|{}|{}".format(exc_type, func_name, exc_tb.tb_lineno,
                                                                                 e))

    def change_lux_and_color_temp(self, collimator_list=None, cct=6500, lux=None):
        try:
            """
                This method is used to change lux and color temperature
                param collimator_list: addresses of collimator's
                param cct: color temperature
                param lux: lux value as list
                return: str
            """
            if lux is None:
                lux = [40, 40, 40, 40, 40]

            if type(lux) == list and type(cct) == int:
                for i, j in zip(collimator_list, lux):
                    lux_value = ctypes.c_float(j)
                    color_temp = ctypes.c_int(cct)
                    duv = ctypes.c_float(0.0)
                    pointer_value = ctypes.pointer(duv)

                    if i not in ["1", "2", "3", "4", "5"]:  # The addresses of connect multiple collimator's
                        logger.error("Input collimator address error: address list:'1','2','3','4','5'")
                        return

                    ret = self.collimator_dll.MX_SetLedEx(int(i), color_temp, lux_value, pointer_value)
                    if not ret:
                        logger.error(f"Error to set lux and color temperature in collimator no.{i}")
                        return "Failed to set lux and color temperature"
                    else:
                        logger.error(f"Lux value and color temperature is set in collimator no.{i}")
                    time.sleep(0.25)

                return "Passed"

            else:
                if type(cct) != int:
                    return "Invalid type of color temperature value"
                return "Invalid type of lux value"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at change_lux_and_color_temp function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                            exc_tb.tb_lineno, e))

    def collimator_lights_off(self, collimator_list=None):
        try:
            """
                This method is used to change lux and color temperature
                param collimator_list: addresses of collimator's
                return: str
            """
            for i in collimator_list:
                if i not in ["1", "2", "3", "4", "5"]:
                    logger.error("Input collimator address error: address list:'1','2','3','4','5'")
                    return

                ret = self.collimator_dll.MX_CloseLedEx(int(i))
                if not ret:
                    logger.error(f"Error to turn off light in collimator no.{i}")
                    return "Failed to turn off collimator light"
                time.sleep(0.2)
            return "Passed"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at collimator_lights_off function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                        exc_tb.tb_lineno, e))

    def change_ir(self, collimator_list=None, ir_mode="850", ir_level=0, wd_fov="150 & 06"):
        try:
            """
                This method is used to set the ir mode, ir value and working distance & fov
                param collimator_list: addresses of collimator's
                param ir_mode: 850 or 940
                param ir_level: value of ir
                param wd_fov: type of working distance and fov
                return: str
            """
            if type(collimator_list) == list:
                if type(ir_mode) == str:
                    if wd_fov == "150 & 06":
                        wd_fov = ctypes.c_char_p(b'PL120STS_15006')
                    elif wd_fov == "80 & 15":
                        wd_fov = ctypes.c_char_p(b'PL120STS_8015')
                    elif wd_fov == "100 & 12":
                        wd_fov = ctypes.c_char_p(b'PL120STS_10012')
                    elif wd_fov == "120 & 07":
                        wd_fov = ctypes.c_char_p(b'PL120STS_12007')
                    elif wd_fov == "120 & 09":
                        wd_fov = ctypes.c_char_p(b'PL120STS_12009')

                    if type(ir_level) == int and 1 < ir_level < 1023:
                        if ir_mode == "850":
                            ir_850 = ctypes.c_char(b"8")  # b"w" for visible light
                        elif ir_mode == "940":
                            ir_940 = ctypes.c_char(b"9")

                        for i in collimator_list:
                            if i not in ["1", "2", "3", "4", "5"]:
                                logger.error("Invalid collimator list")
                                return "Invalid collimator list"

                            if ir_mode == "850":  # Infrared: 850 wave band
                                ret = self.collimator_dll.SetLedPwm(int(i), ir_850, ctypes.c_ushort(ir_level),
                                                                    wd_fov)
                                if not ret:
                                    logger.error(f"Error to set ir in collimator no.{i}")
                                    return "Failed to set ir"

                            elif ir_mode == "940":  # Infrared: 940 wave band
                                ret = self.collimator_dll.SetLedPwm(int(i), ir_940, ctypes.c_ushort(ir_level),
                                                                    wd_fov)
                                if not ret:
                                    logger.error(f"Error to set ir in collimator no.{i}")
                                    return "Failed to set ir"
                            else:
                                logger.error("Infrared mode input error")
                                return "Infrared mode input error"

                            time.sleep(0.25)

                        return "Passed"

                    return "Invalid ir level value"

                return "Invalid type of ir mode"

            return "Invalid type collimator list"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at collimator_lights_off function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                                        exc_tb.tb_lineno, e))

    def change_distance_with_wd_fov(self, collimator_list=None, distance=0.5, light_type=0, wd_fov="150 & 06"):
        """
            This method is used to change the distance
            param collimator_list: addresses of collimator's
            param distance: set the distance value
            param light_type: light type 0 = Visible light, light type 1 = Infrared850, light type 2 = Infrared940
            param wd_fov: type of working distance and fov
            return: str
        """
        try:
            if 0.3 <= distance <= 1000000:
                distance = float(distance)
                distance = distance * 1000
                distance_value = ctypes.c_float(distance)

                if wd_fov == "150 & 06":
                    wd_fov = ctypes.c_char_p(b'PL120STS_15006')
                elif wd_fov == "80 & 15":
                    wd_fov = ctypes.c_char_p(b'PL120STS_8015')
                elif wd_fov == "100 & 12":
                    wd_fov = ctypes.c_char_p(b'PL120STS_10012')
                elif wd_fov == "120 & 07":
                    wd_fov = ctypes.c_char_p(b'PL120STS_12007')
                elif wd_fov == "120 & 09":
                    wd_fov = ctypes.c_char_p(b'PL120STS_12009')

                for i in collimator_list:
                    if i not in ["1", "2", "3", "4", "5"]:
                        logger.error("Input collimator address error: address list:'1','2','3','4','5'")
                        return
                    ret = self.collimator_dll.MoveAbsByFun(int(i), distance_value, wd_fov, light_type)
                    if not ret:
                        logger.error(f"Error to set distance in collimator no.{i}")
                        return "Failed to set distance"
                    time.sleep(0.2)

                time.sleep(3)
                return "Passed"

            else:
                return "Invalid distance"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at change_d function : {}|{}|{}|{}".format(exc_type, func_name, exc_tb.tb_lineno, e))

    # def sep_set_distance(self, collimator_list=None, distance=None, light_type=0, wd_fov="150 & 96"):
    #     """
    #         This method is used to change the distance
    #         param collimator_list: addresses of collimator's
    #         param distance: set the distance value
    #         param light_type: light type 0 = Visible light, light type 1 = Infrared850, light type 2 = Infrared940
    #         param wd_fov: type of working distance and fov
    #         return: str
    #     """
    #     if wd_fov == "150 & 06":
    #         wd_fov = ctypes.c_char_p(b'PL120STS_15006')
    #     elif wd_fov == "80 & 15":
    #         wd_fov = ctypes.c_char_p(b'PL120STS_8015')
    #     elif wd_fov == "100 & 12":
    #         wd_fov = ctypes.c_char_p(b'PL120STS_10012')
    #     elif wd_fov == "120 & 07":
    #         wd_fov = ctypes.c_char_p(b'PL120STS_12007')
    #     elif wd_fov == "120 & 09":
    #         wd_fov = ctypes.c_char_p(b'PL120STS_12009')
    #
    #     for i, d in zip(collimator_list, distance):
    #         if 0.3 <= d <= 1000000:
    #             d = d * 1000
    #             d = ctypes.c_float(d)
    #             if i not in ["1", "2", "3", "4", "5"]:
    #                 logger.error("Input collimator address error: address list:'1','2','3','4','5'")
    #                 return
    #
    #             """The third parameter of the MoveAbsByFun function is the working distance and field of view
    #             angle of the currently installed collimator."""
    #
    #             logger.error("Simulated object distance setting" + str(i),
    #                   self.collimator_dll.MoveAbsByFun(int(i), d, wd_fov, light_type))
    #             time.sleep(0.25)
    #         else:
    #             logger.error("Simulated object distance of PL120STS: 300mm <= distance <= 1000000000mm:")

        # time.sleep(5)

    def get_simulation_distance(self, collimator_list=None, light_type=0, wd_fov="150 & 06"):
        """Get simulation object distance(unit: m)"""
        """
            This method is used to get the setting distance
            param collimator_list: addresses of collimator's
            param light_type: light type 0 = Visible light, light type 1 = Infrared850, light type 2 = Infrared940
            param wd_fov: type of working distance and fov
            return: str
        """
        if wd_fov == "150 & 06":
            wd_fov = ctypes.c_char_p(b'PL120STS_15006')
        elif wd_fov == "80 & 15":
            wd_fov = ctypes.c_char_p(b'PL120STS_8015')
        elif wd_fov == "100 & 12":
            wd_fov = ctypes.c_char_p(b'PL120STS_10012')
        elif wd_fov == "120 & 07":
            wd_fov = ctypes.c_char_p(b'PL120STS_12007')
        elif wd_fov == "120 & 09":
            wd_fov = ctypes.c_char_p(b'PL120STS_12009')
        ret = []
        for i in collimator_list:
            if i not in ["1", "2", "3", "4", "5"]:
                logger.info("Input collimator address error: address list:'1','2','3','4','5'")
                return
            pos2 = ctypes.c_float(-1)
            logger.info("GetSimulationPos",
                        self.collimator_dll.GetActPos2(int(i), ctypes.byref(pos2), wd_fov, light_type))
            logger.info("Get simulation object distance" + str(i), pos2.value)
            ret.append(pos2.value)  # round(,0)
            time.sleep(0.2)
        return ret

    def disconnect(self):
        try:
            time.sleep(0.2)
            ret = self.collimator_dll.MX_Disconnect()
            if not ret:
                logger.error("Failed to disconnect collimator")
                return "Failed to disconnect collimator"

            return "Passed"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            func_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at change_d function : {}|{}|{}|{}".format(exc_type, func_name,
                                                                           exc_tb.tb_lineno, e))

    def reset(self, collimator_list=None):
        for i in collimator_list:
            if i not in ["1", "2", "3", "4", "5"]:
                print("Input collimator address error: address list:'1','2','3','4','5'")
                return
            ret = self.collimator_dll.MX_Homing(int(i))
            if not ret:
                logger.error("Error to reset collimator")
                return "Error to reset collimator"
            time.sleep(0.2)
        time.sleep(2)
        return "Passed"

    def GetStatus(self, collimator_list=None):
        ret_list = []
        for i in collimator_list:
            if i not in ["1", "2", "3", "4", "5"]:
                print("Input collimator address error: address list:'1','2','3','4','5'")
                return
            status = ctypes.c_ushort(0)
            ret = self.collimator_dll.GetStatus(int(i), ctypes.byref(status), self.productType)
            ret_list.append(str(bin(status.value)[2:]))
            logger.info("GetStatus Result", str(bin(status.value)[2:]))
            logger.info("GetStatus:", ret_list)
            time.sleep(0.2)
        return ret_list


# def error_return(collimator):
#     """
#     param collimator: datatype in an integer which is the collimator no.
#     return: result
#     """
#     pus_error_code = ctypes.c_int(15)
#     if self.collimator_dll.GetErrorCode(collimator, ctypes.byref(pus_error_code)):
#         # 0: normal, 1: Motor not enabled, 2: The motor is still moving, 3: Follow error alarm,
#         # 4: Follow error fault,
#         # 5: Driver current is slightly high, 6: Drive overheating, 7: Operation not permitted,
#         # 8: Serial number error, 9: Power element failure, 10: Control mode conflict, 11: Servo mode error
#         error = pus_error_code.value
#         if self.electric_collimator.ClearError(collimator):
#             print("Error cleared for collimator no. {}".format(collimator))
#         else:
#             print("Error is not cleared for collimator no. {}".format(collimator))
#         if error == 0:
#             return 'Success'
#         elif error == 1:
#             return 'Motor not enabled'
#         elif error == 2:
#             return 'The motor is still moving'
#         elif error == 3:
#             return 'Follow error alarm'
#         elif error == 4:
#             return 'Follow error fault'
#         elif error == 5:
#             return 'Driver current is slightly high'
#         elif error == 6:
#             return 'Drive overheating'
#         elif error == 7:
#             return 'Operation not permitted'
#         elif error == 8:
#             return 'Serial number error'
#         elif error == 9:
#             return 'Power element failure'
#         elif error == 10:
#             return 'Control mode conflict'
#         elif error == 11:
#             return 'Servo mode error'
#         else:
#             return 'Unknown error found'
#     else:
#         return 'Unable to fetch the error code.'


# if __name__ == '__main__':
#     connect(["1", "2", "3", "4", "5"])
#     time.sleep(1)
    # sep_set_lux_cct(['5'], 5000, 20)
    # reset(["1", "2", "3", "4", "5"])
    # time.sleep(1)
    # close_led(["1", "2", "3", "4", "5"])
    # set_distance(["1", "2", "3", "4", "5"], 2, 0)  # connected collimators simulate a 1-meter object distance under
    # visible light sources

    # time.sleep(1)
    # set_ir(["1", "2", "3", "4", "5"], "940", 1000) #open 1000 level infrared 850 light source
    # time.sleep(1)
    # close_led(["1", "2", "3", "4", "5"])  # turn off light source of all colliator
    # time.sleep(2)
    # set_lux_cct(["1", "2", "3", "4", "5"], 6500, 4.2)
    #             5.0)  # Calling the unified visible light color temperature and illuminance function
    # PL120STS WorkDistance & FOV = ["8015", "10012", "12009", "12007", "15006"] This Demo selects 8015:Test = c_char_p(b'PL120STS_8015')
    #
    # time.sleep(1)
    # GetStatus(["1"])#If it is necessary to determine whether the simulated distance of the Collimator is complete, it can be determined by the value of Bit 0. If Bit 0 is equal to 0, the collimator completes the simulated distance work.
    # get_real_distance(["1","2","3","4","5"])
    # get_simulation_distance(["1", "2", "3", "4", "5"], 0)
    # time.sleep(1)
    # disconnect()

# obj = New_collimator()
# print(obj.connect_device(["1", "2", "3", "4", "5"]))
# time.sleep(1)
# print(obj.change_ir(collimator_list=["1", "2", "3", "4", "5"], ir_mode="850", ir_level=200))
# print(obj.change_lux_and_color_temp(["1"], cct=7000, lux=5))
# time.sleep(0.5)
# print(obj.change_lux_and_color_temp(["2"], cct=7000, lux=5))
# time.sleep(0.5)
# print(obj.change_lux_and_color_temp(["3"], cct=7000, lux=5))
# time.sleep(0.5)
# print(obj.change_lux_and_color_temp(["4"], cct=7000, lux=5))
# time.sleep(0.5)
# print(obj.change_lux_and_color_temp(["5"], cct=7000, lux=5))
# time.sleep(1)
# print(obj.change_distance_with_wd_fov(["1", "2", "3", "4", "5"], distance=2))
# time.sleep(1)
# obj.get_simulation_distance(["1", "2", "3", "4", "5"])
# obj.collimator_homing()