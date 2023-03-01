from os import path
import logging.config


class Logger:
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.conf')
    logging.config.fileConfig(fname=log_file_path)
    logger = logging.getLogger("root")