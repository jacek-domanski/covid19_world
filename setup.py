import logging


def logger_setup(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    # path = config['log_directory']
    # name = 'log_' + strftime('%Y.%m.%d_%H.%M.%S') + '.txt'
    # file_name = path + name
    # file_handler = logging.FileHandler(file_name)
    LOG_FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler.setFormatter(LOG_FORMATTER)
    # file_handler.setFormatter(LOG_FORMATTER)
    logger.addHandler(console_handler)
    # logger.addHandler(file_handler)

    logger.info('Logger configured')
    return logger