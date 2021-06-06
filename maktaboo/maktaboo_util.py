import colorlog
import logging


def get_basic_logger(logger_name, shell_logger_level=logging.INFO):
    """Get a basic logger.

    Args:
      logger_name: the name of the logger.
      shell_logger_level controls the message level that gets displayed in standard output.
    """
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            '%(log_color)s%(name)s:%(levelname)s - %(message)s'))
    handler.setLevel(shell_logger_level)
    logger = colorlog.getLogger(logger_name)
    logger.addHandler(handler)
    return logger
