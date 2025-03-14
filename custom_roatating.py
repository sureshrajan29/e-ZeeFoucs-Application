from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import time


class EnhancedRotatingFileHandler(TimedRotatingFileHandler, RotatingFileHandler):
    """
        A custom logging handler that combines the features of both TimedRotatingFileHandler
        and RotatingFileHandler.

        - Provides time-based log rotation (e.g., hourly or daily rollovers).
        - Supports size-based rotation to maintain log file size limits.
        """
    try:        
        def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None,
                     delay=0, when='h', interval=1, utc=False):
            TimedRotatingFileHandler.__init__(
                self, filename=filename, when=when, interval=interval,
                backupCount=backupCount, encoding=encoding, delay=delay, utc=utc)

            RotatingFileHandler.__init__(self, filename=filename, mode=mode, maxBytes=maxBytes,
                                                          backupCount=backupCount, encoding=encoding, delay=delay)

        def computeRollover(self, current_time):
            return TimedRotatingFileHandler.computeRollover(self, current_time)

        def doRollover(self):
            # get from logging.handlers.TimedRotatingFileHandler.doRollover()
            current_time = int(time.time())
            dst_now = time.localtime(current_time)[-1]
            new_rollover_at = self.computeRollover(current_time)

            while new_rollover_at <= current_time:
                new_rollover_at = new_rollover_at + self.interval

            # If DST changes and midnight or weekly rollover, adjust for this.
            if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
                dst_at_rollover = time.localtime(new_rollover_at)[-1]
                if dst_now != dst_at_rollover:
                    if not dst_now:  # DST kicks in before next rollover, so we need to deduct an hour
                        addend = -3600
                    else:  # DST bows out before next rollover, so we need to add an hour
                        addend = 3600
                    new_rollover_at += addend
            self.rolloverAt = new_rollover_at

            return RotatingFileHandler.doRollover(self)

        def shouldRollover(self, record):
            return TimedRotatingFileHandler.shouldRollover(self, record) or RotatingFileHandler.shouldRollover(self, record)

    except Exception as e:
        raise Exception("Error in EnhancedRotatingFileHandler logger file: {}".format(e))
