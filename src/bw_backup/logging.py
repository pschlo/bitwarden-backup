import logging
import sys


def setup(root_loglevel: int = logging.INFO, others_loglevel: int = logging.WARNING):
    # set log level for loggers of other packages
    loggers = {logging.getLogger(name) for name in logging.root.manager.loggerDict}
    for logger in loggers:
        logger.setLevel(others_loglevel)
    _setup_root_logger(root_loglevel)


def _setup_root_logger(loglevel: int):
    logger = logging.getLogger()
    logger.setLevel(loglevel)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s', '%H:%M:%S')

    # configure stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logging.addLevelName(logging.DEBUG, 'DBUG')
    logging.addLevelName(logging.INFO, 'INFO')
    logging.addLevelName(logging.WARNING, 'WARN')
    logging.addLevelName(logging.ERROR, ' ERR')
    logging.addLevelName(logging.CRITICAL, 'CRIT')

    # log uncaught errors
    # see https://stackoverflow.com/a/16993115
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            logger.info('Keyboard interrupt')
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
