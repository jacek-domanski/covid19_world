
from setup import logger_setup
logger = logger_setup(__name__)

class Covid19_World:
    def __init__(self):
        logger.info('Initialization...')

        logger.info('Initialized!')

    def download_data_file(self, day):
        pass

    def run(self):
        pass

if __name__ == '__main__':
    covid = Covid19_World()
    covid.run()