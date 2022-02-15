import logging
def log():
    logger = logging.getLogger()
    return logger

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    log().info('info')
