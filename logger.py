"""
This module is used to log all actions of application.
"""
import logging
import os
from custom_roatating import EnhancedRotatingFileHandler
from datetime import datetime

try:
    now = datetime.now()
    curdate = now.strftime("%Y%m%d")
    log_filename = "Logs_{}.log".format(curdate)
    is_logCreated = False

    # Logging Setup
    base_dir = os.getenv('LOCALAPPDATA').replace("\\", "/")
    if "Lens_Tuning_Automation" not in os.listdir(base_dir):
        os.mkdir("{}/Lens_Tuning_Automation".format(base_dir))
    if "Logs" not in os.listdir("{}/Lens_Tuning_Automation/".format(base_dir)):
        os.mkdir("{}/Lens_Tuning_Automation/Logs".format(base_dir))
    is_logCreated = True
    updated_base_dir = "{}/Lens_Tuning_Automation/Logs/{}".format(base_dir, log_filename)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(message)s')
    rotating_file_handler = EnhancedRotatingFileHandler(
        filename=updated_base_dir, mode='a',
        maxBytes=100 * 1025 * 1025, backupCount=12, when='midnight', interval=1)
    rotating_file_handler.setFormatter(formatter)
    logger.addHandler(rotating_file_handler)

except Exception as e:
    raise Exception("Error while creating logger: {}".format(e))
