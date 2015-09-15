#coding:utf8
#author: TooNTonG 2012-11-07

import logging
import logging.handlers as handlers

APP_NAME = 'app1'
LOG_SVR_HOST = '127.0.0.1'
LOG_SVR_PORT = 20001

# 此logger name必需与服务端中有相应的logger处理handler
# 如果服务端logging.getLogger()返回空，会使用root处理
LOGGER_NAME = 'detail'

def getSocketLogger(name, level, host, port, memoryCapacity):
    target = handlers.SocketHandler(host, port)
    if memoryCapacity > 0:

        hdlr = handlers.MemoryHandler(memoryCapacity,
                                       logging.ERROR, # 此参数是指遇到此级别时，马上flush
                                       target)
    else:
        hdlr = target

    hdlr.setLevel(level)
    logger = logging.getLogger(name)
    logger.addHandler(hdlr)
    logger.setLevel(level)
    return logger

def main():
    logger = getSocketLogger(LOGGER_NAME,
                             logging.DEBUG, # 如果使用NOTSET，相当warning
                             host = LOG_SVR_HOST,
                             port = LOG_SVR_PORT,
                             memoryCapacity = 0)

    for i in range(10):
        logger.info('run %s main' % APP_NAME)
        logger.debug('thisis the debug log by %s' % APP_NAME)
        logger.warning('thisis the warning log by %s' % APP_NAME)
        logger.error('thisis the error log by %s' % APP_NAME)
        logger.critical('thisis the critical log by %s' % APP_NAME)

    print 'end main'

if '__main__' == __name__:
    main()
