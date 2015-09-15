#coding:utf8
#author:TooNTonG 2011-11-07

from SocketServer import ThreadingTCPServer, StreamRequestHandler
import logging.config
import logging.handlers as lhandlers
import os
import struct
import cPickle

LOG_BIND_PORT = 20001

class LogRequestHandler(StreamRequestHandler):
    def handle(self):
        while 1:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            # 使用SocketHandler发送过来的数据包，要使用解包成为LogRecord
            # 看SocketHandler文档
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return cPickle.loads(data)

    def handleLogRecord(self, record):
        logger = logging.getLogger(record.name)
        logger.handle(record)
        # print(record)

def startLogSvr(bindAddress, requestHandler):
    svr = ThreadingTCPServer(bindAddress, requestHandler)
    svr.serve_forever()

def addHandler(name, handler):
    logger = logging.getLogger(name)
    logger.addHandler(handler)

    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(fmt)

    logger.setLevel(logging.NOTSET)

def memoryWapper(handler, capacity):
    hdlr = lhandlers.MemoryHandler(capacity, target = handler)
    hdlr.setFormatter(handler.formatter)
    return hdlr

def main():
    path, dirname = os.path, os.path.dirname
    pth = dirname((path.realpath(__file__)))
#    filename = path.join(dirname(pth), 'log', 'logging.log')
    filename = path.join(pth, 'log', 'logging.log')
#    logging.config.fileConfig(pth + r'/logging.conf')
    logging.config.fileConfig(pth + r"/webpy-texas.conf")

    # 最终写到文件中
    # hdlr = lhandlers.RotatingFileHandler(filename,
    #                               maxBytes = 1024,
    #                               backupCount = 3)

    # # 还可以一个memoryhandler，达到一定数据或是有ERROR级别再flush到硬盘
    # hdlr = memoryWapper(hdlr, 1024)

    # addHandler('core', hdlr)

    print 'OK: logerserver running...'
    startLogSvr(('0.0.0.0', LOG_BIND_PORT), LogRequestHandler)


if __name__ == "__main__":
    main()
