#coding=utf8

import sys
import json
import logging
import logging.handlers as handlers
import TexasPub

#此文件主要用来做配置，就不另写配置xml/ini等

#DB配置
DB_HOST = "10.2.1.74"
DB_PORT = 3306
DB_USER = "mdzpk_rw"
DB_PASS = "aPr5FBhVJ8Km23BAFk7g"
DB_DATABASE = "mdzpkweb"

#redis配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_SESSION_DB = 1

#游戏服务器配置
GAME_HOST = "42.62.40.186"
GAME_PORT = 8888

#日志服务器配置
LOG_SVR_HOST = '127.0.0.1'
LOG_SVR_PORT = 20001

#JSS服务配置
JSS_HOST = "117.121.18.42:8000"
JSS_BUYVIP_URL = "/jss/mbuserbuyvip?userId=%s&viptype=%d"
JSS_ADDSCORE_URL = "/jss/mbuseraddscore?userId=%s&type=%d&score=%d"

#DBService服务
DBSERVER_HOST = "202.106.182.117"
DBSERVER_PORT = 6000

#渠道配置
CHANNEL_DEMO = "demo"

PROMPT_INFO = "{\"title\":\"提示信息\", \"prompt\":\"系统正在维护，请您稍候登录\", \"btn\":\"退出\", \"action\":\"exit\"}"

#定义平台ID
PLATFORMID_MACHINEID	= 0
PLATFORMID_TENCENTWEIBO	= 1
PLATFORMID_TEST			= 10
PLATFORMID_DEMO			= 11

#支付宝通知URL
ALIPAY_NOTIFY_URL = ""

#360支付平台URL通知
ICHANNEL360_NOTIFY_URL = ""

#爱贝通知URL
IAPPPAY_NOTIFY_URL = ""

#游戏服务器的一些配置，web从那边读取
SERVER_CONF_FILE = "/etc/aow/server.conf"
#动态更新的配置文件位置
UPDATE_CONF_JSONFILE = "./dyncfg.json"
#分享结果网址
SHARE_RESULT_ICON = "http://aow.winwp.cn/static/logo.png"
SHARE_RESULT_URL = "http://fusion.qq.com/cgi-bin/qzapps/unified_jump?appid=10348188&from=mqq&actionFlag=0&params=pname%3Dcom.aow.aow%26versioncode%3D17%26actionflag%3D0%26channelid%3D"
SHARE_RESULT_TITLE = "【微信推荐】《全民争霸》"

g_dictGameSvr = {}
g_dictConnectSvr = {}
#加载游戏服务器配置，主要是解析出各个游戏服务器地址
def LoadServerConf():
    global g_dictGameSvr
    global g_dictConnectSvr

    try:
        print("read server conf:" + SERVER_CONF_FILE)
        file = open(SERVER_CONF_FILE, "r")
        strServerConf = file.read()
        file.close()

        dictConf = json.loads(strServerConf)
        g_dictGameSvr = dictConf["game_svr"]
        g_dictConnectSvr = dictConf["connect_svr"]

        return True
    except Exception, e:
        print("LoadServerConf exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
        return False

#用户名分配算法
def GetUserIndex(strUserID):
    nLen = len(strUserID)
    nIndex = (ord(strUserID[nLen-1]) << 24) | (ord(strUserID[nLen-2]) << 16) | (ord(strUserID[nLen-3]) << 8) | (ord(strUserID[nLen-4]))
    return nIndex

#根据用户ID确定其在哪台游戏服务器
def GetGameServerFromUserID(strUserID):
    global g_dictGameSvr

    if len(g_dictGameSvr) == 0:
        return None
    nIndex = GetUserIndex(strUserID) % len(g_dictGameSvr)
    dictSvr = g_dictGameSvr[nIndex]["mgmt"]
    print("user:" + strUserID + ",host:" + dictSvr["host"] + ",port:" + str(dictSvr["port"]))
    return (dictSvr["host"], dictSvr["port"])

#根据用户ID确定其在哪台连接服务器
def GetConnectServerFromUserID(strUserID):
    global g_dictConnectSvr

    if len(g_dictConnectSvr) == 0:
        return None
    dictSvr = g_dictConnectSvr[0]["mgmt"]
    return (dictSvr["host"], dictSvr["port"])

g_strUptCfg = ""
#加载需要更新的json文件
def LoadUpdateConf():
    global g_strUptCfg
    try:
        print("read update conf:" + UPDATE_CONF_JSONFILE)
        file = open(UPDATE_CONF_JSONFILE, "r")
        g_strUptCfg = file.read()
        file.close()

        return True
    except Exception, e:
        print("LoadUpdateConf exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
        return False

#根据版本和用户本地时间取更新配置文件
def GetUpdateConfigJson(nTimeCfg, nVer):
    global g_strUptCfg
    if len(g_strUptCfg) == 0:
        return "{\"code\":-1}"

    return g_strUptCfg

#取得日志处理器
def GetSocketLogger(name):
    return getSocketLogger(name, logging.DEBUG, host = LOG_SVR_HOST, port = LOG_SVR_PORT, memoryCapacity = 0)

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

DEVICE_TYPE_UNKNOW = 0
DEVICE_TYPE_ANDROID  = 1
DEVICE_TYPE_IPHONE  = 2
DEVICE_TYPE_IPAD  = 3
DEVICE_TYPE_PC  = 4
#分渠道更新，指定不同更新URL
def GetUpdateUrl(strChannel, nDeviceType):
    if nDeviceType == DEVICE_TYPE_IPHONE or nDeviceType == DEVICE_TYPE_IPAD:
        strUrl = "itms-apps://itunes.apple.com/cn/app/de-zhou-ke/id633399763?mt=8"
    else:
        strUrl = "http://pw.lianzhong.com/Mobile/Download.html"
    UPDATE_INFO_FMT = "{\"prompt\":\"2.2.0版更新内容：\n1、全新的保险玩法；\n2、创新的任务活动模式；\n3、优化游戏进程。\", \"url\":\"%s\"}"
#    UPDATE_INFO_FMT = "{\"prompt\":\"2.0.2版更新内容：\n1、解决游戏中崩溃问题；\n2、大幅优化性能。\n别等了，赶快更新吧！\", \"url\":\"%s\"}"
    return UPDATE_INFO_FMT % (strUrl)

#import时先加载一些配置
# LoadServerConf()
LoadUpdateConf()

if __name__ == "__main__":
    print(GetUserIndex("s074798b778141cf53fd9e386a5a8a36"))
    # GetSocketLogger("detail")
    # pairSvr = GetGameServerFromUserID("")
    # if pairSvr != None:
    #     print(pairSvr[0])
    #     print(pairSvr[1])
