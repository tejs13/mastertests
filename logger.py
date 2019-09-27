import os
import logging
from logging.handlers import RotatingFileHandler


def init_logging(log_name='logger', log_directory='logs'):

    logger_formatter = '[%(asctime)s] -- %(levelname)s - %(filename)s -- %(funcName)s - ' \
                       'Line no - %(lineno)d -- %(message)s\n'

    def prepare_log_directory():

        try:
            base_logs_path = log_directory
            if not os.path.exists(base_logs_path):
                os.mkdir(base_logs_path)

            logs_file_path = os.path.join(base_logs_path, log_name)

            print("Log Path : %s" % str(logs_file_path))

            if not os.path.exists(logs_file_path):
                print("Making directory : %s" % str(logs_file_path))
                os.mkdir(logs_file_path)

            if not os.path.exists(os.path.join(logs_file_path, 'Error')):
                os.mkdir(os.path.join(logs_file_path, 'Error'))

            if not os.path.exists(os.path.join(logs_file_path, 'Debug')):
                os.mkdir(os.path.join(logs_file_path, 'Debug'))

            if not os.path.exists(os.path.join(logs_file_path, 'Info')):
                os.mkdir(os.path.join(logs_file_path, 'Info'))

            if not os.path.exists(os.path.join(logs_file_path, 'Warning')):
                os.mkdir(os.path.join(logs_file_path, 'Warning'))

            return logs_file_path

        except Exception as e:
            print(e)

    logs_path = prepare_log_directory()

    log = logging.getLogger(log_name)
    log_formatter = logging.Formatter(logger_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)

    # Create Debug log file
    debug_log_file_name = os.path.join(os.path.join(logs_path, 'Debug'), (log_name + '.debug'))
    file_handler_debug = RotatingFileHandler(debug_log_file_name, mode='a', maxBytes=200 * 1024 * 1024,
                                             backupCount=20, encoding=None, delay=0)
    file_handler_debug.setFormatter(log_formatter)
    file_handler_debug.setLevel(logging.DEBUG)
    log.addHandler(file_handler_debug)
    file_handler_debug.addFilter(MyFilter(logging.DEBUG))

    # Create Info log file
    info_log_file_name = os.path.join(os.path.join(logs_path, 'Info'), (log_name + '.info'))
    file_handler_info = RotatingFileHandler(info_log_file_name, mode='a', maxBytes=200 * 1024 * 1024,
                                            backupCount=20, encoding=None, delay=0)
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)
    file_handler_info.addFilter(MyFilter(logging.INFO))

    # Create Warning log file
    warning_log_file_name = os.path.join(os.path.join(logs_path, 'Warning'), (log_name + '.warn'))
    file_handler_warnig = RotatingFileHandler(warning_log_file_name, mode='a', maxBytes=200 * 1024 * 1024,
                                              backupCount=20, encoding=None, delay=0)
    file_handler_warnig.setFormatter(log_formatter)
    file_handler_warnig.setLevel(logging.WARNING)
    log.addHandler(file_handler_warnig)
    file_handler_warnig.addFilter(MyFilter(logging.WARNING))

    # Create Error log file
    error_log_file_name = os.path.join(os.path.join(logs_path, 'Error'), (log_name + '.error'))
    file_handler_error = RotatingFileHandler(error_log_file_name, mode='a', maxBytes=200 * 1024 * 1024,
                                             backupCount=20, encoding=None, delay=0)
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)
    file_handler_error.addFilter(MyFilter(logging.ERROR))

    log.setLevel(logging.INFO)

    return log


class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno <= self.__level
