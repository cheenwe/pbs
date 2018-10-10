import sys
import logging

sys.path.append('..')

from util.log_handler import LogHandler

# noinspection PyPep8Naming
def testLogHandler():
    """
    test function LogHandler  in Util/LogHandler
    :return:
    """
    log = LogHandler('test')
    log.error('this is a log from test')

    log.resetName(name='test1')
    log.warning('this is a log from test1')

    log.resetName(name='test2')
    log.info('this is a log from test2')



if __name__ == '__main__':
    testLogHandler()
