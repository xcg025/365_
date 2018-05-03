import logging
import logging.config
import json

class Logging(object):
    # print('-----------------------')
    logging.config.fileConfig('logging.config')
    logger = logging.getLogger('bet365')

    @classmethod
    def debug(cls, text):
        # print('debug start-----')
        cls.logger.debug(text)

    @classmethod
    def info(cls, text):
        # print('info start-----')
        cls.logger.info(text)

    @classmethod
    def warning(cls, text):
        # print('warning start-----')
        cls.logger.warning(text)



if __name__ == '__main__':
    info = {'key':123, 'key2':234, 'key3':['123', '456']}
    Logging.info(u'赢了且更新数据库, {}'.format(info))
    # Logging.debug('This is debug message')
    # Logging.info('This is info message')
    # Logging.warning('This is warning message')
    # log = Logging()
    # log.debug('This is debug message')
    # log.info('This is info message')
    # log.warning('This is warning message')
