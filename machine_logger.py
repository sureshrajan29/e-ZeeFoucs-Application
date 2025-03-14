"""
This module is used log the errors of plc and actuators
"""

import logging
import os
from custom_roatating import EnhancedRotatingFileHandler
from datetime import datetime

try:
    now = datetime.now()
    curdate = now.strftime("%Y%m%d")
    machine_error_log_filename = "Machine_error_Logs_{}.log".format(curdate)
    is_logCreated = False

    # Logging Setup
    base_dir = os.getenv('LOCALAPPDATA').replace("\\", "/")
    if "Lens_Tuning_Automation" not in os.listdir(base_dir):
        os.mkdir("{}/Lens_Tuning_Automation".format(base_dir))
    if "Machine error Logs" not in os.listdir("{}/Lens_Tuning_Automation/".format(base_dir)):
        os.mkdir("{}/Lens_Tuning_Automation/Machine error Logs".format(base_dir))
    is_logCreated = True
    updated_base_dir_machine_logger = "{}/Lens_Tuning_Automation/Machine error Logs/{}".format(base_dir,
                                                                                               machine_error_log_filename)

    machine_logger = logging.getLogger(__name__)
    machine_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(message)s')
    rotating_file_handler_machine_error = EnhancedRotatingFileHandler(filename=updated_base_dir_machine_logger,
                                                                      mode='a',
                                                                      maxBytes=100 * 1025 * 1025, backupCount=12,
                                                                      when='midnight', interval=1)

    rotating_file_handler_machine_error.setFormatter(formatter)
    machine_logger.addHandler(rotating_file_handler_machine_error)

except Exception as e:
    raise Exception("Error while creating logger: {}".format(e))
