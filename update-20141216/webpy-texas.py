#coding=utf8

import web
import os
import json
import sys
import urllib
import StringIO
import struct
import binascii
import time
import random
import traceback
import logging
import logging.config
import gzip
import base64
import md5
import redis
import TexasPub
import TexasConfig
import httplib
from xml.etree import ElementTree
import re
import rediswebpy
import time

import hashlib

from TexasSyncSocket import TexasSyncSocket

#定义常量
SESSION_TIMEOUT = 12*60*60              #session有效时长
COOKIE_NAME = "texas_session_id"			#cookie名，会设置到客户端cookie文件中
MIN_PASSWORD_LEN = 1                    #密码最小长度

#定义商品类型
SKU_TYPE_COIN  = "coin"
SKU_TYPE_VIP      = "vip"

#定义ID类型
PLATFORMID_MACHINEID = 0
PLATFORMID_TEST = 10

#定义商店类型
SHOP_OURGAME    = "ourgame"
SHOP_ALIPAY         = "alipay"
SHOP_GOOGLEPLAY     = "ggplay"
SHOP_IAPPPAY		= "iappay"
SHOP_IOSPPAY        = "iospay"
SHOP_CHNNEL_360_PAY        = "channel_360"

#通用错误
E_NOLOGINNED = -101
ES_NOLOGINNED = "no loginned"
E_EXCEPTION = -102
ES_EXCEPTION = "internal exception"
E_BADURL = -103
ES_BADURL = "bad url"
E_DATANOTFOUND = -104
ES_DATANOTFOUND = "data not found"
E_INVALIDCHAR = -105
ES_INVALIDCHAR = "invalid char"
E_NOTSUPPORT = 106
ES_NOTSUPPORT = "not support"

#设置日志文件
strLogPath = os.path.join(TexasPub.GetModulePath(), "log")
if not os.path.exists(strLogPath):
    os.mkdir(strLogPath)
    os.chmod(strLogPath, 0777)

g_strCrashPath = os.path.join(strLogPath, 'crash')
if not os.path.exists(g_strCrashPath):
    os.mkdir(g_strCrashPath)
    os.chmod(g_strCrashPath, 0777)

g_strRlogPath = os.path.join(strLogPath, 'rlog')
if not os.path.exists(g_strRlogPath):
    os.mkdir(g_strRlogPath)
    os.chmod(g_strRlogPath, 0777)

#本地直接写文件日志可能会丢数据，不想丢数据就用下面的SocketLogger
logging.config.fileConfig("webpy-texas.conf")
g_log = logging.getLogger("common")
g_logE = logging.getLogger("exception")
g_logD = logging.getLogger("detail")
# g_log = TexasConfig.GetSocketLogger("common")
# g_logE = TexasConfig.GetSocketLogger("exception")
# g_logD = TexasConfig.GetSocketLogger("detail")

#设置字符集
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    g_log.critical("setdefaultencoding to utf-8")

#读动态配置数据，在登录时返回
g_strDyncJson = ""
try:
    file = open("./dyncfg.json", "r")
    g_strDyncJson = file.read()
    file.close()
except Exception, e:
    g_log.info("Can't find dyncfg.json.")
if len(g_strDyncJson) > 0:
    g_log.info("dyncfg.json\n" + g_strDyncJson)

#如果配置为localhost需要在hosts中进行域名解析，否则无法连接
g_log.critical("DB host:"+TexasConfig.DB_HOST+",port:"+str(TexasConfig.DB_PORT)+",user:"+TexasConfig.DB_USER+",pass:"+TexasConfig.DB_PASS+",database:"+TexasConfig.DB_DATABASE)
if TexasConfig.DB_ENABLE:
    g_db = web.database(dbn='mysql', host=TexasConfig.DB_HOST, port=TexasConfig.DB_PORT, user=TexasConfig.DB_USER, pw=TexasConfig.DB_PASS, db=TexasConfig.DB_DATABASE)
# g_log.critical("REDIS host:"+AowConfig.REDIS_HOST+",port:"+str(AowConfig.REDIS_PORT)+",db:"+str(AowConfig.REDIS_DB))
# g_r = redis.Redis(host=AowConfig.REDIS_HOST, port=AowConfig.REDIS_PORT, db=AowConfig.REDIS_DB)

urls = (
    '/report/crash_native', 'Report_Crash_native',
    '/report/crash_acra', 'Report_Crash_arca',
    '/report/rlog', 'report_rlog',
    '/reset', 'reset',
    '/debug/info', 'debug_info',
    '/test', 'test',
    '/capture', 'capture',
    '/favicon.ico', 'favicon',
    '/iospay/purchase','iospay_purchase',
    '/verandcfg', 'verandcfg',
    '/purchase/skus', 'purchase_skus',
    '/purchase/payload', 'purchase_payload',
    '/purchase/confirm', 'purchase_confirm',
    '/ourgame/notify', 'channel_ourgame_notify',
    '/chat/whiteusers', 'chat_whiteusers',
    '/shareresult', 'shareresult',
    '/check', 'check',
    '/(.*)', 'redirect'
)

app = web.application(urls, globals())
if web.config.get('_session') is None:
    g_log.info("web.config.get('_session') is None")
	
    #设置session参数
    web.config.session_parameters['timeout'] = SESSION_TIMEOUT
    web.config.session_parameters['cookie_domain'] = None
    web.config.session_parameters['ignore_expiry'] = True
    web.config.session_parameters['ignore_change_ip'] = True
    web.config.session_parameters['cookie_name'] = COOKIE_NAME
    #web.config.session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
    #web.config.session_parameters['expired_message'] = 'Session expired'
	
    #初始化session
    # sessionStore = rediswebpy.RedisStore(AowConfig.REDIS_HOST, AowConfig.REDIS_PORT, AowConfig.REDIS_SESSION_DB)
    # session = web.session.Session(app, sessionStore, initializer={'count':0, 'login':0, 'privilege':1, 'aid':'', 'pid':0, 'uid':'', 'lang':TexasPub.LANG_CN, 'channel':'', 'token': '','nickname':''})
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count':0, 'login':0, 'privilege':1, 'aid':'', 'pid':0, 'uid':'', 'lang':TexasPub.LANG_CN, 'channel':'', 'token': '','nickname':''})
    web.config._session = session
else:
    g_log.info("web.config.get('_session') ok")
    session = web.config._session

#返回错误字符串JSON格式
def ErrResult(nErr, strMsg):
    print("error code:"+str(nErr)+",msg:"+strMsg)
    return json.dumps({"code":nErr,"reason":strMsg}, ensure_ascii=False)
#正确的
def OKResult():
    return json.dumps({"code":0}, ensure_ascii=False)

#显示原始请求数据
class capture:
    def GET(self):
        print(web.input)
        d = dict(web.input())
        return str(type(web.input()))
	
    def POST(self):
        print(web.input)
        return web.input()

#重置，删除session，此方法没有使用，仅用于调试
class reset:
    def GET(self):
        session.aid = ''
        session.pid = 0
        session.uid = ''
        session.login = 0
        session.privilege = 1
        session.count   = 0
        session.channel = ''
        session.kill()
        return "Login out"

#调试目的，返回一些用户信息
class debug_info:
    def GET(self):
        return printinfo()

#调试函数，返回一些信息
def printinfo():
    strInfo = "account_id:"+session.aid+",platform_id:"+str(session.pid)+",user_id:"+session.uid+",login:"+str(session.login)+",privilege:"+str(session.privilege)+",count:"+str(session.count)+",channel:"+session.channel
    print(strInfo)
    return strInfo

#此方法没有用，只是浏览器测试时会调用favicon取网站图标
class favicon:
    def GET(self):
        web.ctx.status='404 not found'

#访问未定义链接
class redirect:
    def GET(self, path):
        g_log.debug("invalid url:"+path+",ip:"+web.ctx.ip)
        return ErrResult(E_BADURL, ES_BADURL)

#gzip压缩数据，内部已设置HTTP头等
def GZip(strData):
    web.webapi.header('Content-Encoding', 'gzip')
    zbuf = StringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9)
    zfile.write(strData)
    zfile.close()
    data = zbuf.getvalue()
    web.webapi.header('Content-Length',str(len(data)))
    web.webapi.header('Vary','Accept-Encoding', unique=True)
    return data

#native crash report
class Report_Crash_native:
    def POST(self):
        try:
            data = web.input()
            tm = time.localtime()
            strTime = "native_%04d%02d%02d%02d%02d%02d-%s" % (tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,tm.tm_min,tm.tm_sec, web.ctx.ip)
            strFile = os.path.join(g_strCrashPath, (strTime+".txt"))
            file = open(strFile, 'w')
            file.write("web.ctx.ip="+web.ctx.ip+"\n")
            for k in data:
                strLine = k + "=" + data[k] + "\n"
                file.write(strLine)
            file.close()
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

#arca捕获的崩溃报告
class Report_Crash_arca:
    def POST(self):
        try:
            data = web.input()
            tm = time.localtime()
            strTime = "arca_%04d%02d%02d%02d%02d%02d-%s" % (tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,tm.tm_min,tm.tm_sec, web.ctx.ip)
            strFile = os.path.join(g_strCrashPath, (strTime+".txt"))
            file = open(strFile, 'w')
            file.write("web.ctx.ip="+web.ctx.ip+"\n")
            for k in data:
                strLine = k + "=" + data[k] + "\n"
                file.write(strLine)
            file.close()
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

class report_rlog:
    def POST(self):
        try:
            data = web.input()
	    strUid = 'unknown'
	    if 'uid' in data:
	        strUid = data['uid']
		    
            tm = time.localtime()
            strTime = "%04d%02d%02d%02d%02d%02d" % (tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,tm.tm_min,tm.tm_sec)
            strIp = "%s" % (web.ctx.ip)
            strFile = os.path.join(g_strRlogPath, (strUid+".txt"))
            file = open(strFile, 'a')
            file.write("t["+strTime+"] ip["+web.ctx.ip+"] ")

            strLine = '\n'
            if 'data' in data:
                strLine = urllib.unquote(data['data'])

            file.write(strLine)
            file.close()
            return OKResult()
            
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

class ggreg:
    def POST(self):
        try:
            data = web.input(did="", regid="");
            device_id = data.did
            gcm_id = data.regid
            if len(gcm_id) == 0 or len(device_id) == 0:
                g_log.error(self.__class__.__name__ + "," + str(session.aid) + "," + ES_GOOGLEREG_PARAM)
                return ErrResult(E_GOOGLEREG_PARAM, ES_GOOGLEREG_PARAM)

            myvar = dict(did=device_id, gid=gcm_id)
            res = g_db.query('replace tb_d_usergcmid set device_id=$did, gcm_id=$gid', myvar);
            return OKResult()
 
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

#登录错误值和错误字符串
E_LOGIN_PARAM_USER      = 1
E_LOGIN_PARAM_PASSWD    = 2
E_LOGIN_NORECORD    = 3
E_LOGIN_MULTIRECORDS = 4
E_LOGIN_PASSWORD  = 5
E_LOGIN_STATUS      = 6
E_LOGIN_MEMCACHED   = 7
E_LOGIN_NONACTIVEUSERID = 8
E_LOGIN_VERSION_UPDATE = 11
E_LOGIN_VERSION_FORBIDDEN = 12
E_LOGIN_PROMPT = 13
E_LOGIN_PROMPT_FORBIDDEN = 14
ES_LOGIN_PARAM_USER      = "user is none"
ES_LOGIN_PARAM_PASSWD    = "password too short"
ES_LOGIN_NORECORD    = "no record"
ES_LOGIN_MULTIRECORDS = "multi records"
ES_LOGIN_PASSWORD  = "password is not correct"
ES_LOGIN_STATUS      = "status abnormal"
ES_LOGIN_MEMCACHED   = "can't save data to memcache"
ES_LOGIN_NONACTIVEUSERID = "non active userid"
ES_LOGIN_VERSION_UPDATE = "version update"
ES_LOGIN_VERSION_FORBIDDEN = "version forbidden"
#-- POST /login
#req：user_id(email), password
#ack：json: code(0表示成功), msg(错误信息), session_key(32个hex字符， 16字节)
class login:
    def GET(self):
        if Loginned():
            g_log.info(self.__class__.__name__ + ",not loginned. ip:"+web.ctx.ip)
            return "Login Double"
        else:
            render = create_render(1)
            return "%s" % (render.login())

    def POST(self):
        try:
            #取得请求数据，并进行基本判断
            data = web.input(aid="",pwd="",pid=0,sid=0,did="",passtype=PASSTYPE_MD5,autoregister=1,model="",package="",jver="1.0",channel="")
            strAccountID = data.aid
            strPassword = data.pwd
            nPlatformID = int(data.pid)
            nSourceID = int(data.sid)
            strDeviceID = data.did
            strNick = data.model
            strVersion = data.jver
            if len(strVersion) > 0:
                nVersion = TexasPub.Version2Int(strVersion)
            else:
                nVersion = 0
            strChannel = data.channel
            if nPlatformID == AowConfig.PLATFORMID_MACHINEID and strChannel == AowConfig.CHANNEL_DEMO:
                nPlatformID = AowConfig.PLATFORMID_DEMO#此处需要换平台ID，因为表中帐号和平台ID为联合主键
            g_logD.info(self.__class__.__name__ + "," + str(session.aid) + ",account:" + strAccountID + ",platformid:" + str(nPlatformID) + ",sourceid:" + str(nSourceID) + ",device:" + strDeviceID + ",model:" + strNick + ",ver:" + strVersion + ",channel:" + strChannel)
            
            #先判断版本
            #"info"指定为1.07(包括)以前版本，只是更新url
            #"prompt"指定为1.07以后版本，可以配置提示文字和更新url等
            nCode = 0
            strPrompt = ""
            strPromptJson = ""
            #如果是强制升级版本，直接返回出错，不继续下面的流程
            if nVersion < VPub.Version2Int("1.18") or (nVersion >= 0x133 and nVersion <= 0x134):
                jsonInfo = AowConfig.GetUpdateUrl(strChannel)
                strInfo = json.dumps({"code":E_LOGIN_VERSION_FORBIDDEN, "info":AowConfig.URL_UPDATE, "promptjson":jsonInfo}, ensure_ascii=False)
                return strInfo
            # 非强制升级版本要继续下面的流程
            # if nVersion < VPub.Version2Int("1.0"):
            # 	nCode = E_LOGIN_VERSION_UPDATE
            # 	strPrompt = AowConfig.URL_UPDATE
			
            # 强制提示并禁止继续登录
            # nCode = E_LOGIN_PROMPT_FORBIDDEN
            # strInfo = json.dumps({"code":E_LOGIN_PROMPT_FORBIDDEN, "promptjson":AowConfig.PROMPT_INFO}, ensure_ascii=False)
            #    return strInfo
            # 提示并可继续登录
            # nCode = E_LOGIN_PROMPT
            # strPromptJson = AowConfig.PROMPT_INFO
            #再判断输入合法性
            if len(strAccountID) == 0:
                g_log.info(self.__class__.__name__ + "," + str(session.aid) + "," + ES_LOGIN_PARAM_USER)
                return ErrResult(E_LOGIN_PARAM_USER, ES_LOGIN_PARAM_USER)
            if len(strPassword) < MIN_PASSWORD_LEN:
                g_log.info(self.__class__.__name__ + "," + str(session.aid) + "," + ES_LOGIN_PARAM_PASSWD)
                return ErrResult(E_LOGIN_PARAM_PASSWD, ES_LOGIN_PARAM_PASSWD)
			
            nNewbie = 0
            #先查表，判断用户存不存在
            myvar = dict(aid=strAccountID, pid=nPlatformID)
            results = g_db.select('tb_d_account', myvar, where="account_id=$aid and platform_id=$pid", what="secrete, user_id, device_id")                
            if len(results) == 0:
                if int(data.autoregister) == 1:#and nPlatformID == PLATFORMID_MACHINEID
                    #帐号不存在，再判断是否有此机器用户，如果有则进行绑定，如果没有则建立机器用户并绑定
                    strMd5Pass = VPub.EncodePassword(strAccountID, strPassword)

                    myvar2 = dict(did=strDeviceID)
                    results2 = g_db.select('tb_d_account', myvar2, where="account_id=$did and platform_id=0", what="user_id")
                    if len(results2) > 0:#设备ID对应的帐号已存在，直接绑定此帐号
                        row2 = results2[0]
                        strUserID = row2.user_id
                        #注册用户，插入用户数据
                        g_db.insert('tb_d_account', account_id=strAccountID, platform_id=nPlatformID, secrete=strMd5Pass, source_id=nSourceID, user_id=strUserID, device_id=strDeviceID, register_time=web.SQLLiteral("NOW()"), register_ip=web.ctx.ip, last_login_time=web.SQLLiteral("NOW()"), last_login_ip=web.ctx.ip, register_ver=strVersion, register_channel=strChannel, register_model=strNick)
                        g_logD.info(self.__class__.__name__ + "," + str(session.aid) + ",auto bind account:" + strAccountID + ",userid:" + strUserID + ",platformid:" + str(nPlatformID) + ",deviceid:" + strDeviceID)
                    else:
                        #从redis里取游戏中用户ID
                        if strChannel == AowConfig.CHANNEL_DEMO:
                            strUserID = g_r.lpop(KEY_NONACTIVE_FOR_DEMO)
                        else:
                            strUserID = g_r.lpop(KEY_NONACTIVE)
                        if strUserID is None:
                            g_log.error(self.__class__.__name__ + "," + str(session.aid) + "," + ES_REGISTER_NONACTIVEUSERID)
                            return ErrResult(E_LOGIN_NONACTIVEUSERID, ES_LOGIN_NONACTIVEUSERID)
    					
                        #注册用户，插入用户数据，同时插入设备对应的帐号
                        g_db.insert('tb_d_account', account_id=strAccountID, platform_id=nPlatformID, secrete=strMd5Pass, source_id=nSourceID, user_id=strUserID, device_id=strDeviceID, register_time=web.SQLLiteral("NOW()"), register_ip=web.ctx.ip, last_login_time=web.SQLLiteral("NOW()"), last_login_ip=web.ctx.ip, register_ver=strVersion, register_channel=strChannel, register_model=strNick)
                        if strAccountID != strDeviceID or nPlatformID != 0:#本身是设备ID的帐号不需要再次插入
                            strMd5PassDevice = VPub.EncodePassword(strDeviceID, strDeviceID)
                            g_db.insert('tb_d_account', account_id=strDeviceID, platform_id=0, secrete=strMd5PassDevice, source_id=nSourceID, user_id=strUserID, device_id=strDeviceID, register_time=web.SQLLiteral("NOW()"), register_ip=web.ctx.ip, last_login_time=web.SQLLiteral("NOW()"), last_login_ip=web.ctx.ip, register_ver=strVersion, register_channel=strChannel, register_model=strNick)
    				    
                        #更新数据库中用户状态为新手状态，并加上新手护盾时间
                        if len(strNick) < 2:
                            strNick = strUserID[:6]
                        myvar = dict(userid=strUserID)
    #                    g_db.update('tb_d_user', vars=myvar, where="user_id=$userid and status=0", status=GUID_STATUS_NEWBIE)#此行不设置新手护盾和昵称
    #                    g_db.update('tb_d_user', vars=myvar, where="user_id=$userid and status=0", status=GUID_STATUS_NEWBIE, name=strNick)#此行不设置新手护盾
                        g_db.update('tb_d_user', vars=myvar, where="user_id=$userid and status=0", status=GUID_STATUS_NEWBIE, name=strNick, shield_expire=web.SQLLiteral("date_add(now(), interval 24 hour)"))
                        #置新手标志，数据表中的新手标志会由游戏服务在新手完成后置为正常
                        if strChannel != AowConfig.CHANNEL_DEMO:#demo帐户有城池不置新手标志
                            nNewbie = 1

                        g_logD.info(self.__class__.__name__ + "," + str(session.aid) + ",auto register account:" + strAccountID + ",userid:" + strUserID + ",platformid:" + str(nPlatformID) + ",deviceid:" + strDeviceID)
                        if 2 == nPlatformID:
                            newbieAward = dict(timestamp=int(time.time()), text="输入新人礼包激活码，宝石，资源快到碗里来！")
			    userPromoKey = 'avail_promo:{}'.format(strUserID)
                            newbiePromoId = '00'
                            newbieAwardStr = json.dumps(newbieAward)
                            g_r.hset(userPromoKey, newbiePromoId, newbieAwardStr)

                    #继续走登录的流程吧
                    myvar = dict(aid=strAccountID, pid=nPlatformID)
                    results = g_db.select('tb_d_account', myvar, where="account_id=$aid and platform_id=$pid", what="secrete, user_id, device_id")
                else:
                    return ErrResult(E_LOGIN_NORECORD, ES_LOGIN_NORECORD)
            elif len(results) > 1:
                return ErrResult(E_LOGIN_MULTIRECORDS, ES_LOGIN_MULTIRECORDS)
			
            row = results[0]
            strUserID = row.user_id
            nPassType = int(data.passtype)
            #进行密码比较
            if nPassType == PASSTYPE_MD5:#已经对用户和密码进行和数据库中同样的加密，则直接比对
                if data.pwd != row.secrete:
                    return ErrResult(E_LOGIN_PASSWORD, ES_LOGIN_PASSWORD)
            else:
                strMd5Pass = VPub.EncodePassword(strAccountID, strPassword)
                if strMd5Pass != row.secrete:
                    return ErrResult(E_LOGIN_PASSWORD, ES_LOGIN_PASSWORD)

            #生成邀请码，如果此人尚无邀请码。
            myvar = dict(uid = strUserID)
            refcode_res = g_db.select('tb_d_refcode', myvar, where='user_id=$uid', what='ref_code');
            if len(refcode_res) == 0:
                g_db.insert('tb_d_refcode', ref_code=0, user_id=strUserID, referer='');
 
            #md5加密生成sessionkey，这个seesionkey每次登录都会不同，保存到redis中，客户端将之传到游戏服务器，游戏服务器通过redis比对，确认用户
            strInfo = time.asctime()+web.ctx.ip+strAccountID
            m = md5.new()
            m.update(strInfo)
            strSession = m.hexdigest().upper()

            #更新session到redis中
            jsonSession = json.dumps({"sessionKey":strSession, "loginTime":time.time(), "serverid":0})
            g_r.hset(KEY_USERSESSION, strUserID, jsonSession)

            #更新登录时间和IP到表
            myvar = dict(aid=strAccountID, pid=nPlatformID)
            g_db.update('tb_d_account', vars=myvar, where="account_id=$aid", last_login_ip=web.ctx.ip, last_login_time=web.SQLLiteral("NOW()"))

            strInfo = json.dumps({"code":nCode,"session_key":strSession,"aid":strAccountID,"pid":nPlatformID,"uid":strUserID,"gamehost":AowConfig.GAME_HOST,"gameport":AowConfig.GAME_PORT,"newbie":nNewbie,"info":strPrompt,"dyncfg":g_strDyncJson,"promptjson":strPromptJson}, ensure_ascii=False)

            #登录成功设置session值
            session.aid	= strAccountID
            session.pid	= nPlatformID
            session.uid = row.user_id
            session.login   = 1
            session.count   = session.count + 1
            session.channel = strChannel
            g_logD.info(self.__class__.__name__ + "," + str(session.aid) + ",userid:" + strUserID + ",platformid:" + str(nPlatformID) + ",sourceid:" + str(nSourceID) + ",device:" + strDeviceID + ",nick:" + strNick + ",ver:" + strVersion + ",channel:" + strChannel + ",info:" + strInfo)
            return strInfo
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

E_PURCHASE_DBSERVICE = 1
E_PURCHASE_SAMETRADENO = 2
E_PURCHASE_UNKNOWNDATA = 3
class iospay_purchase:
    def POST(self):
        try:
            i = web.input(user="", role="", payresult="")
            strUserID = i.user
            strRoleName = i.role
            strResult = base64.decodestring(i.payresult)
            g_logD.info("user:" + strUserID + ",role:" + strRoleName + ",result:"+strResult)
            receipt = i.payresult;#需要用base64数据

            #验证苹果服务器
            jsonStr = json.dumps({"receipt-data": receipt})
            #connect = httplib.HTTPSConnection("buy.itunes.apple.com")
            # sandbox
            connect = httplib.HTTPSConnection("sandbox.itunes.apple.com")
            headers = {"Content-type": "application/json"}
            connect.request("POST", "/verifyReceipt", jsonStr)
            result = connect.getresponse()
            data = result.read()
            connect.close()
            decodedJson = json.loads(data)
            g_logD.info("response result:" + data)
            status = decodedJson[u'status']
            if status != 0:
                g_logD.info("trade status is " + str(status))
                return ErrResult(E_INVALIDCHAR, ES_INVALIDCHAR)
            g_logD.info("https to apple.com success!")

            strTransactionID = decodedJson[u'receipt'][u'original_transaction_id']
            g_logD.info("transaction_id:" + strTransactionID)
            strProductID = decodedJson[u'receipt'][u'product_id']
            g_logD.info("product_id:" + strProductID)

            strSku = strProductID
            strTradeNo = strTransactionID
            strTradeUser = strUserID
            nTradeVip = 0

            #调用存储过程进行各种判断，如签名是否已使用过，是否已完成的交易等
            myvar = dict(tradeno=strTradeNo, userid=strTradeUser, sku=strSku, result=strResult, viplevel=nTradeVip)
            ret = g_db.query("call pd_w_purchase(@result, @msg, $tradeno, $userid, $sku, $result, $viplevel, @chipspurchased, @chipsnow, @skutype)", vars=myvar)
            results = g_db.query("select @result, @msg, @chipspurchased, @chipsnow, @skutype")
            if len(results) == 0:
                 g_log.error(self.__class__.__name__ + ",procedure purchase no result. user:"+strTradeUser+",sku:"+strSku+",tradeno:"+strTradeNo+",original"+strResult)
                 return ErrResult(E_DATANOTFOUND, ES_DATANOTFOUND)
            dictResult = dict(results[0])
            nRet = dictResult['@result']
            strMsg = dictResult['@msg']
            llChipsPurchased = dictResult['@chipspurchased']
            llChipsNow = dictResult['@chipsnow']
            strSkuType = dictResult["@skutype"]
            if nRet != 0 or llChipsPurchased is None or llChipsNow is None:
                 g_log.error(self.__class__.__name__ + ",procedure purchase return:"+str(nRet)+",reason:" + strMsg + ",user:"+strTradeUser+",sku:"+strSku+",tradeno:"+strTradeNo+",original"+strResult)
                 if nRet == 2:#同样的定单号，则这笔交易已处理过，直接返回成功，让客户端IAP完成此笔交易（这种情况可能是在充值web没有返回前断开，导致交易没有调用finish完成）
                    strInfo = json.dumps({"code":0,"id":strUserID,"tradeno":strTradeNo,"purchased":llChipsPurchased,"now":llChipsNow}, ensure_ascii=False)
                    g_logD.info(self.__class__.__name__ + "," + str(session.aid) + "," + strInfo)
                    return strInfo
                 else:
                    return ErrResult(nRet, strMsg)

            #加积分
            if strSkuType == SKU_TYPE_COIN:#只有礼包才需要这边加积分
                nScore = DB_ScoreOfSku(strSku)
                if CMD_AddScore(strRoleName, 1, nScore) == False:#购买加积分类型是1
                    g_log.error(self.__class__.__name__ + ",add score fail! Role:" + strRoleName + ",score:" + str(nScore))

            #到此已经增加充值记录，需要根据不同商品去各个服务器给用户加数据
            if strSkuType == SKU_TYPE_COIN:#加万能豆，用的是用户名
                if CMD_AddPowerGameCoin(strTradeUser, llChipsPurchased) == False:
                     g_log.error(self.__class__.__name__ + ",add powergamecoin fail! User:" + strTradeUser + ",coin:" + str(llChipsPurchased))

                     strInfo = json.dumps({"code":E_PURCHASE_DBSERVICE,"id":strUserID,"tradeno":strTradeNo,"purchased":0,"now":0}, ensure_ascii=False)
                     g_logD.info(self.__class__.__name__ + "," + str(session.aid) + "," + strInfo)
                     return strInfo
            elif strSkuType == SKU_TYPE_VIP:#加会员资格，用的是角色名
                nVipType = GetVipType(strTradeSku)
                if 0 == nVipType:
                     g_log.error(self.__class__.__name__ + ",can't find vip type! Role:" + strRoleName + ",sku:" + strTradeSku)

                     strInfo = json.dumps({"code":E_PURCHASE_DBSERVICE,"id":strUserID,"tradeno":strTradeNo,"purchased":0,"now":0}, ensure_ascii=False)
                     g_logD.info(self.__class__.__name__ + "," + str(session.aid) + "," + strInfo)
                     return strInfo
                if CMD_AddVip(strRoleName, nVipType) == False:
                     g_log.error(self.__class__.__name__ + ",add vip fail! Role:" + strRoleName + ",viptype:" + str(nVipType))

                     strInfo = json.dumps({"code":E_PURCHASE_DBSERVICE,"id":strUserID,"tradeno":strTradeNo,"purchased":0,"now":0}, ensure_ascii=False)
                     g_logD.info(self.__class__.__name__ + "," + str(session.aid) + "," + strInfo)
                     return strInfo
            else:
                 g_log.error(self.__class__.__name__ + "unknown sku type:" + strSkuType)

                 strInfo = json.dumps({"code":E_PURCHASE_UNKNOWNDATA,"id":strUserID,"tradeno":strTradeNo,"purchased":0,"now":0}, ensure_ascii=False)
                 g_logD.info(self.__class__.__name__ + "," + str(session.aid) + "," + strInfo)
                 return strInfo

            #更新定单状态
            DB_UpdatePurchaseResult(strTradeNo, 1)
            
            strInfo = json.dumps({"code":0,"id":strUserID,"tradeno":strTradeNo,"purchased":llChipsPurchased,"now":llChipsNow}, ensure_ascii=False)
            g_logD.info(self.__class__.__name__ + "," + str(session.aid) + "," + strInfo)

            return strInfo
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

E_VERSION_UPDATE = 11
E_VERSION_FORBIDDEN = 12
E_VERSION_PROMPT = 13
E_VERSION_PROMPT_FORBIDDEN = 14
class verandcfg:
    def POST(self):
        try:
            d = web.data()
            data = web.input(gzip="0", cfgtime="", channel="", ver="", devicetype="")
            if data.gzip.isdigit() and int(data.gzip) > 0:
                bZip = True
            else:
                bZip = False
            if data.devicetype.isdigit():
                nDeviceType = int(data.devicetype)
            print(dict(data))

            strVersion = data.ver
            if len(strVersion) > 0:
                nVersion = TexasPub.Version2Int(strVersion)
            else:
                nVersion = 0
            strChannel = data.channel

            strTime = data.cfgtime
            if len(strTime) > 0:
                nCfgTime = int(strTime)
            else:
                nCfgTime = 0

            #写连接session信息
            session.channel = data.channel
            session.aid = ""

            #先得生成需要的json文件，以下版本限制可能仍是要继续使用而不是禁止
            strJson = TexasConfig.GetUpdateConfigJson(nCfgTime, nVersion)

            #先判断版本
            #"prompt"可以配置提示文字和更新url等
            nCode = 0
            strPromptJson = ""
            # 如果是强制升级版本，直接返回出错，不继续下面的流程
            # if nVersion < TexasPub.Version2Int("2.2.0"):
            #     dictConf = json.loads(strJson)
            #     dictConf["code"] = E_VERSION_FORBIDDEN
            #     dictConf["promptjson"] = TexasConfig.GetUpdateUrl(strChannel, nDeviceType)
            #     strJson = json.dumps(dictConf, ensure_ascii=False)

            # 非强制升级版本要继续下面的流程
            # if nVersion < TexasPub.Version2Int("3.0"):
            #     dictConf = json.loads(strJson)
            #     dictConf["code"] = E_VERSION_UPDATE
            #     dictConf["promptjson"] = TexasConfig.GetUpdateUrl(strChannel, nDeviceType)
            #     strJson = json.dumps(dictConf, ensure_ascii=False)
            
            # 强制提示并禁止继续登录
            # dictConf = json.loads(strJson)
            # dictConf["code"] = E_VERSION_PROMPT_FORBIDDEN
            # dictConf["promptjson"] = TexasConfig.PROMPT_INFO
            # strJson = json.dumps(dictConf, ensure_ascii=False)

            # 提示并可继续登录
            # dictConf = json.loads(strJson)
            # dictConf["code"] = E_VERSION_PROMPT
            # dictConf["promptjson"] = TexasConfig.PROMPT_INFO
            # strJson = json.dumps(dictConf, ensure_ascii=False)

            print(strJson)
            if bZip:
                return GZip(strJson)
            else:
                return strJson

        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

class purchase_skus:
    def GET(self):
        try:
            i = web.input(gzip="0", userid="", viplevel="0")
            # if not Loginned():
            #     g_log.info(self.__class__.__name__ + ",not loginned. ip:"+web.ctx.ip)
            #     return ErrResult(E_NOLOGINNED, ES_NOLOGINNED)
            if i.gzip.isdigit() and int(i.gzip) > 0:
                bZip = True
            else:
                bZip = False
            strUserID = i.userid
            #用户是否VIP，web这边没有VIP信息，由客户端传上来
            nVipLevel = int(i.viplevel)
            print("uid:"+strUserID+",level:"+str(nVipLevel))

            #将用户ID存入session，现在没有登录，在此存入并不安全，只用在日志等    
            session.aid = i.userid

            if not TexasConfig.DB_ENABLE:#没有数据库时返回空数据
                dictInfo = {"code":0, "charged":0, "skus":[]}
                strInfo = json.dumps(dictInfo, ensure_ascii=False)
                if bZip:
                    return GZip(strInfo)
                else:
                    return strInfo

            #查找用户是否首充
            bFirstCharge = IsFirstCharge(session.uid)
            nCharged = 1
            if bFirstCharge:
                nCharged = 0

            strChannel = session.channel
            if not HaveSkusOfChannel(strChannel):#此渠道没有单独配置商品数据，使用缺省商品数据
                strChannel = "default"

            #从数据库中读取商品信息，生成列表
            listSkus = []
            myvar = dict(viplevel=nVipLevel, channel=strChannel)
            if nVipLevel > 0:#需要查VIP表
                results = g_db.query("select a.Sku,a.DispOrder,a.Icon,a.Image,a.PriceInfo,a.Price,a.Title,a.Name,a.Type,a.Addition,a.Descript,a.AmountInfo,a.Amount,a.FirstAddition,a.FirstAmount, a.Addition2, a.Visible, b.VipName,b.VipAddition,b.VipAmount,b.VipTime,b.VipAddition2 from tb_w_skus a, tb_w_skus_for_vip b where a.sku=b.sku and a.Enable=1 and b.VipLevel=$viplevel and a.sku in (select sku from tb_w_skus_of_channel where channel=$channel) order by a.Price;", vars=myvar)
            else:
                results = g_db.query("select a.Sku,a.DispOrder,a.Icon,a.Image,a.PriceInfo,a.Price,a.Title,a.Name,a.Type,a.Addition,a.Descript,a.AmountInfo,a.Amount,a.FirstAddition,a.FirstAmount, a.Addition2, a.Visible from tb_w_skus a where a.Enable=1 and a.sku in (select sku from tb_w_skus_of_channel where channel=$channel) order by a.Price;", vars=myvar)
            for r in results:
                print(r)
                strName = r.Name
                nVipTime = 0
                strAddition2 = r.Addition2
                if bFirstCharge:
                    strAddition = r.FirstAddition
                    nAmount = r.FirstAmount
                else:
                    if nVipLevel > 0:#VIP用户需要取一些VIP的数据
                        strAddition = r.VipAddition
                        nAmount = r.VipAmount
                        strName = r.VipName
                    else:
                        strAddition = r.Addition
                        nAmount = r.Amount

                if not DB_IsExceedLimitToday(r.Sku):
                    listSkus.append({"sku":r.Sku,"order":r.DispOrder,"icon":r.Icon,"image":r.Image,"price":r.PriceInfo,"title":r.Title,"name":strName,"type":r.Type,"desc":r.Descript,"addition":strAddition,"amountinfo":r.AmountInfo,"amount":nAmount,"viptime":nVipTime,"addition2":strAddition2,"visible":r.Visible})
            
            dictInfo = {"code":0, "charged":nCharged, "skus":listSkus}
            strInfo = json.dumps(dictInfo, ensure_ascii=False)
            if bZip:
                return GZip(strInfo)
            else:
                return strInfo
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

E_PAYLOAD_INVALIDSHOP       = 1
ES_PAYLOAD_INVALIDSHOP      = "invalid shop"
E_EXCEEDLIMIT  = 2
ES_EXCEEDLIMIT = "exceed limit"
#购买请求一个payload字符串
class purchase_payload:
    def POST(self):
        try:
            # if not Loginned():
            #     g_log.info(self.__class__.__name__ + ",not loginned. ip:"+web.ctx.ip)
            #     return ErrResult(E_NOLOGINNED, ES_NOLOGINNED)
            
            strChannel = "official"

            i = web.input(shop="",userid="",sku="",machineid="",mobile="",userdata="")
            g_logD.info(self.__class__.__name__ + "," + str(session.aid)+",shop:"+i.shop+",userid:"+i.userid+",sku:"+i.sku+",mid:"+i.machineid+",mobile:"+i.mobile)
            if i.shop == SHOP_OURGAME:
                #先查询商品信息
                myvar = dict(sku=i.sku)
                results = g_db.select('tb_w_skus', myvar, where="Sku=$sku", what="Price,Name,FirstName,Descript")
                if len(results) == 0:
                    return ErrResult(E_DATANOTFOUND, ES_DATANOTFOUND)
                
                row = results[0]

                if DB_IsExceedLimitToday(i.sku):#超过当天购买限制
                    return ErrResult(E_EXCEEDLIMIT, ES_EXCEEDLIMIT)

                strPrice = "%.02f" % row.Price
                if IsFirstCharge(i.userid):
                    strSubject = row.FirstName
                else:
                    strSubject = row.Name
                strPayload = strChannel + "-" + str(i.userid) + "-" + str(int(time.time())) + "-" + i.sku + "-" + i.userdata
                print("Payload:"+strPayload)
                strInfo = json.dumps({"code":0,"shop":i.shop,"payload":strPayload,"sku":i.sku}, ensure_ascii=False)
                g_logD.info(self.__class__.__name__ + "," + str(session.aid) + "," + strInfo)
                return strInfo
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

#确认交易
class purchase_confirm:
    def POST(self):
        try:
            i = web.input(tradeno="")
            strTradeNo = i.tradeno
            print("purchase_confirm:" + strTradeNo)

            #从数据库中查询定单是否已完成
            myvar = dict(tradeno=strTradeNo)
            results = g_db.select('tb_w_purchase', myvar, where="trade_no=$tradeno", what="UserID, sku, amount")
            if len(results) == 0:
                return ErrResult(E_DATANOTFOUND, ES_DATANOTFOUND)

            row = results[0]
            strUserID = row.UserID
            nPurchased = row.amount
            strInfo = json.dumps({"code":0,"id":strUserID,"tradeno":strTradeNo,"purchased":nPurchased}, ensure_ascii=False)
            g_logD.info(self.__class__.__name__ + "," + str(session.aid) + "," + strInfo)
            return strInfo
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

#联众移动中心的SDK通知
# transactionDataData
# {
#     "trade_no":"131028095149706053541029",
#     "uid":"34560079",
#     "product_id":"z4fwHlnlAkMdxxxx",
#     "fee":2,
#     "coins":20,
#     "result":0,
#     "terminal":"UMPAYD",
#     "item_id":"mashang.jinbi.2", //产品ID
#     "productType":0, //商品类型
#     "productTypeChildren":"1", //商品子类型
#     "channel":"thran",//渠道
#     "version":"1.0.0"//客户端版本
# }
class channel_ourgame_notify:
    def GET(self):
        g_logD.info(self.__class__.__name__ + ", web.ctx.ip="+web.ctx.ip)
        strJson = "{\"transactionData\": {\"trade_no\":\"official-zhidong001-1404963750-LZDZPK.01-0\",\"uid\":\"志东001\",\"product_id\":\"lzdzpk\",\"fee\":1,\"gameId\":\"25011\",\"coins\":5000,\"result\":0,\"terminal\":\"ALIPAY\",\"item_id\":\"LZDZPK.01\",\"productType\":0,\"productTypeChildren\":\"1\",\"channel\":\"thran\",\"version\":\"2.0\"}, \"sign\": \"9750103E26C3A297B2343BD8172D2A1D\"}"
        print(strJson)
        d = json.loads(strJson)
        print(d)
        strData = json.dumps(d["transactionData"], ensure_ascii=False)
        d["transactionData"] = strData
        return self.ProcessNotify(d, strJson)

    def POST(self):
        g_logD.info(self.__class__.__name__ + ", web.ctx.ip="+web.ctx.ip)
        dInput = dict(web.input())
        print(dInput)
        strResult = json.dumps(dInput,  ensure_ascii=False)
        g_logD.info(self.__class__.__name__ + ",original data:" + strResult)
        # print(strResult)
        return self.ProcessNotify(dInput, strResult)            

    def ProcessNotify(self, dictRes, strResult):
        try:
            if dictRes.has_key("thranPay"):#不处理定单数据
                return self.Result(0)

            #解析用户ID，SKU等
            if not dictRes.has_key("transactionData"):
                return self.Result(2)
            strData = dictRes["transactionData"]
            d = json.loads(strData)
            nResult = d["result"]
            strRoleName= d["uid"]#此处是角色名
            strTradeNo = d["trade_no"]
            strItemID = d["item_id"]
            g_logD.info(self.__class__.__name__ + ",result:" + str(nResult) + ",role:" + strRoleName + ",trade_no:" + strTradeNo + ",item_id:" + strItemID)
            print("result:" + str(nResult) + ",role:" + strRoleName + ",trade_no:" + strTradeNo + ",item_id:" + strItemID)

            listTrade = strTradeNo.split("-")
            if len(listTrade) < 5:
                return self.Result(3)
            print(listTrade)
            strTradeChannel = listTrade[0]
            strTradeUser = listTrade[1]
            strTradeSku = listTrade[3]
            nTradeVip = int(listTrade[4])
            strSku = strTradeSku

            #调用存储过程进行各种判断，如签名是否已使用过，是否已完成的交易等
            myvar = dict(tradeno=strTradeNo, userid=strTradeUser, sku=strSku, result=strResult, viplevel=nTradeVip)
            ret = g_db.query("call pd_w_purchase(@result, @msg, $tradeno, $userid, $sku, $result, $viplevel, @chipspurchased, @chipsnow, @skutype)", vars=myvar)
            results = g_db.query("select @result, @msg, @chipspurchased, @chipsnow, @skutype")
            if len(results) == 0:
                 g_log.error(self.__class__.__name__ + ",procedure purchase no result. user:"+strTradeUser+",sku:"+strSku+",tradeno:"+strTradeNo+",original"+strResult)
                 return self.Result(4)
            dictResult = dict(results[0])
            nRet = dictResult['@result']
            strMsg = dictResult['@msg']
            llChipsPurchased = dictResult['@chipspurchased']
            llChipsNow = dictResult['@chipsnow']
            strSkuType = dictResult["@skutype"]
            if nRet != 0 or llChipsPurchased is None or llChipsNow is None:
                 g_log.error(self.__class__.__name__ + ",procedure purchase return:"+str(nRet)+",reason:" + strMsg + ",user:"+strTradeUser+",sku:"+strSku+",tradeno:"+strTradeNo+",original"+strResult)
                 return self.Result(5)

            #到此已经增加充值记录，需要根据不同商品去各个服务器给用户加数据
            if strSkuType == SKU_TYPE_COIN:#加万能豆，用的是用户名
                if CMD_AddPowerGameCoin(strTradeUser, llChipsPurchased) == False:
                     g_log.error(self.__class__.__name__ + ",add powergamecoin fail! User:" + strTradeUser + ",coin:" + str(llChipsPurchased))
                     # return self.Result(6)
                     return self.Result(0)#只要记录已加入到这边库中，就返回成功
            elif strSkuType == SKU_TYPE_VIP:#加会员资格，用的是角色名
                nVipType = GetVipType(strTradeSku)
                if 0 == nVipType:
                     g_log.error(self.__class__.__name__ + ",can't find vip type! Role:" + strRoleName + ",sku:" + strTradeSku)
                     # return self.Result(7)
                     return self.Result(0)#只要记录已加入到这边库中，就返回成功
                if CMD_AddVip(strRoleName, nVipType) == False:
                     g_log.error(self.__class__.__name__ + ",add vip fail! Role:" + strRoleName + ",viptype:" + str(nVipType))
                     # return self.Result(8)
                     return self.Result(0)#只要记录已加入到这边库中，就返回成功
            else:
                # return self.Result(9)
                 return self.Result(0)#只要记录已加入到这边库中，就返回成功

            #加积分
            if strSkuType == SKU_TYPE_COIN:#只有礼包才需要这边加积分
                nScore = DB_ScoreOfSku(strSku)
                if CMD_AddScore(strRoleName, 1, nScore) == False:#购买加积分类型是1
                    g_log.error(self.__class__.__name__ + ",add score fail! Role:" + strRoleName + ",score:" + str(nScore))

            #更新定单状态
            DB_UpdatePurchaseResult(strTradeNo, 1)
            #正确返回{"result":0}
            return self.Result(0)
        except Exception, e:
            g_logE.error(self.__class__.__name__  + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + fp.getvalue())
            return self.Result(-1)

    def Result(self, nResult):
        strJson = json.dumps({"result":nResult})
        g_logD.info(self.__class__.__name__ + ",result:" + strJson)
        return strJson

#根据SKU取得游戏服务需要的VIP类型
def GetVipType(strSku):
    if strSku == "LZDZPKHY.01" or strSku == "LZDZPKHY.TEST.01":
        return 1
    elif strSku == "LZDZPKHY.02":
        return 2
    elif strSku == "LZDZPKHY.03":
        return 3
    elif strSku == "LZDZPKHY.04":
        return 4
    else:
        return 0

#白名单用户
class chat_whiteusers:
    def GET(self):
       web.seeother("/static/chat/whiteusers.json")

class test:
    def GET(self):
        d = dict(web.input())
        if CMD_AddVip(d["uid"], 1) == True:
            return "ok"
        else:
            return "fail"
        # data = web.input(uid="")
        # dtVip = VipLevel(data.uid)
        # if dtVip.has_key("seconds"):
        #     return "level:" + str(dtVip["level"]) + ",seconds:" + str(dtVip["seconds"])
        # else:
        #     return "level:" + str(dtVip["level"])

class redirect_test:
    def GET(self):
        i = web.input()
        dictData = dict(i)
        postData = urllib.urlencode(dictData);
        req = urllib2.Request("http://aow.winwp.cn/capture", postData);
        # in most case, for do POST request, the content-type, is application/x-www-form-urlencoded
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
        resp = urllib2.urlopen(req);
        return "ok"

#是否已经登录
def Loginned():
    if session.login == 1:
        return True
    else:
        return False

#建立模板对象
def create_render(privilege):
    if privilege == 0:
        render = web.template.render('templates/admin')
    else:
        render = web.template.render('templates/user')
	
    return render

#gzip压缩数据，内部已设置HTTP头等
def GZip(strData):
    web.webapi.header('Content-Encoding', 'gzip') 
    zbuf = StringIO.StringIO() 
    zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9) 
    zfile.write(strData) 
    zfile.close() 
    data = zbuf.getvalue()
    web.webapi.header('Content-Length',str(len(data))) 
    web.webapi.header('Vary','Accept-Encoding', unique=True)
    return data

#查找用户是否首充
def IsFirstCharge(strUserID):
    if not TexasConfig.DB_ENABLE:
        return False
    myvar = dict(userid=strUserID, skutype="coin")
    results = g_db.select('tb_w_purchase', myvar, where="UserID=$userid and skutype=$skutype", what="sku")
    if len(results) == 0:
        return True
    else:
        return False

#是否渠道有单独配置的商品数据
def HaveSkusOfChannel(strChannel):
    if not TexasConfig.DB_ENABLE:
        return False
    myvar = dict(channel=strChannel)
    results = g_db.select('tb_w_skus_of_channel', myvar, where="Channel=$channel", what="sku")
    if len(results) == 0:
        return False
    else:
        return True

if __name__ == "__main__":
	app.run()
else:
	application = app.wsgifunc()

#加会员资格
def CMD_AddVip(strUserID, nVipType):
    bRet = False
    strEncodedUserID = urlencodestr(strUserID)#此处要求用UTF8
    print(strEncodedUserID)
    strUrl = TexasConfig.JSS_BUYVIP_URL % (strEncodedUserID, nVipType)
    print(strUrl)
    g_logD.info("CMD_AddVip user:" + strUserID + ",vip type:" + str(nVipType) + " ...")

    connect = None
    try:
        connect = httplib.HTTPConnection(TexasConfig.JSS_HOST)
        headers={"Content-Type":"text/html;charset=utf8"}  
        connect.request("GET", strUrl, headers=headers)
        result = connect.getresponse()
        nStatus = result.status
        if nStatus != 200:
            g_logE.error("http status:" + str(nStatus) + ",reason:" + result.reason)
            return False
        data = result.read()
        print(data)
        g_logD.info(data)

        dictResult = json.loads(data)
        if dictResult["state"] == "1":
            bRet = True
    except Exception, e:
        g_logE.error("http exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
        return False
    finally:
        if connect:
            connect.close()

    g_logD.info("CMD_AddVip user:" + strUserID + ",vip type:" + str(nVipType) + " OK")
    return bRet

#加积分
def CMD_AddScore(strUserID, nType, nScore):
    bRet = False
    strEncodedUserID = urlencodestr(strUserID)#此处要求用UTF8
    print(strEncodedUserID)
    strUrl = TexasConfig.JSS_ADDSCORE_URL % (strEncodedUserID, nType, nScore)#1是购买礼包加积分 4是分享加积分
    print(strUrl)
    g_logD.info("CMD_AddScore user:" + strUserID + ",score:" + str(nScore) + " ...")

    connect = None
    try:
        connect = httplib.HTTPConnection(TexasConfig.JSS_HOST)
        headers={"Content-Type":"text/html;charset=utf8"}  
        connect.request("GET", strUrl, headers=headers)
        result = connect.getresponse()
        nStatus = result.status
        if nStatus != 200:
            g_logE.error("http status:" + str(nStatus) + ",reason:" + result.reason)
            return False
        data = result.read()
        print(data)
        g_logD.info(data)

        dictResult = json.loads(data)
        if dictResult["state"] == "1":
            bRet = True
    except Exception, e:
        g_logE.error("http exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
        return False
    finally:
        if connect:
            connect.close()

    g_logD.info("CMD_AddScore user:" + strUserID + ",score:" + str(nScore) + " OK")
    return bRet

#urlencode字符串
def urlencodestr(val):
    if isinstance(val, unicode):
        return urllib.quote_plus(str(val))
    return urllib.quote_plus(val)
    # reprStr = repr(str).replace(r'\x', '%')
    # return reprStr[1:-1]

#加万能豆
def CMD_AddPowerGameCoin(strUserName, nCoin):
    g_logD.info("CMD_AddPowerGameCoin user:" + strUserName + ",coin:" + str(nCoin) + " ...")
    s = TexasSyncSocket()
    if s.Connect(TexasConfig.DBSERVER_HOST, TexasConfig.DBSERVER_PORT) == False:
        return False
    ret = s.PowerGameCoinChange(strUserName, nCoin)
    print(ret)
    s.Close()

    if ret[0] != 0:
        return False
    g_logD.info("CMD_AddPowerGameCoin user:" + strUserName + ",coin:" + str(nCoin) + " OK")
    return True

#更新购买结果
def DB_UpdatePurchaseResult(strTradeNo, nResult):
    myvar = dict(tradeno=strTradeNo)
    ret = g_db.update('tb_w_purchase', vars=myvar, where="trade_no=$tradeno", result=nResult)
    if ret == 1:
        return True
    else:
        return False

#取得购买商品奖励积分
def DB_ScoreOfSku(strSku):
    if not TexasConfig.DB_ENABLE:
        return 0
    myvar = dict(sku=strSku)
    results = g_db.select('tb_w_score_of_sku', myvar, where="Sku=$sku", what="Score")
    if len(results) == 0:
        return 0
    row = results[0]
    return row.Score

#是否已购买超限
def DB_IsExceedLimitToday(strSku):
    if not TexasConfig.DB_ENABLE:
        return False
    myvar = dict(sku=strSku)
    results = g_db.select('tb_w_skus_limit_perday', myvar, where="Sku=$sku", what="LimitNum, TodayNum")
    if len(results) == 0:
        return False
    row = results[0]
    return row.LimitNum > 0 and row.TodayNum >= row.LimitNum

#分享结果
class shareresult:
    def GET(self):
        i = web.input(uid="", mid="", shareid="")
        return self.shareResult(i.uid, i.mid)

    def POST(self):
        i = web.input(uid="", mid="", shareid="")
        return self.shareResult(i.uid, i.mid)

    def shareResult(self, strUser, strMachineID):
        try:
            nResult = -1
            nTimes = 0
            nScore = 2
            if CMD_AddScore(strUser, 4, nScore) == False:#分享加积分类型是4
                nResult = 1
                nScore = 0
            nResult = 0
            strInfo = json.dumps({"code":nResult, "times":nTimes, "score":nScore}, ensure_ascii=False)
            return strInfo
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + "," + fp.getvalue())
            return ErrResult(E_EXCEPTION, ES_EXCEPTION)

g_nCount = 0
#自检
class check:
    def GET(self):
        strInfo = ""
        try:
            #检测JSS
            strInfo = strInfo + "check jss...\n"
            strInfo = strInfo + "add score to account...\n"
            bRet = CMD_AddScore("逗兜囝", 4, 1)
            if bRet:
                strInfo = strInfo + "SUCCESS\n"
            else:
                strInfo = strInfo + "FAIL\n"
            strInfo = strInfo + "add vip level 1 to account...\n"
            bRet = CMD_AddVip("逗兜囝", 1)
            if bRet:
                strInfo = strInfo + "SUCCESS\n"
            else:
                strInfo = strInfo + "FAIL\n"
            strInfo = strInfo + "check jss OK\n\n"

            #检测dbservice
            strInfo = strInfo + "check dbservice...\n"
            strInfo = strInfo + "add power game coin to account...\n"
            bRet = CMD_AddPowerGameCoin("supershowplayer", 1)
            if bRet:
                strInfo = strInfo + "SUCCESS\n"
            else:
                strInfo = strInfo + "FAIL\n"
            strInfo = strInfo + "check dbservice OK\n\n"

            #检测数据库
            strInfo = strInfo + "check db...\n"
            strInfo = strInfo + "have skus of default channel...\n"
            bRet = HaveSkusOfChannel("default")
            if bRet:
                strInfo = strInfo + "SUCCESS\n"
            else:
                strInfo = strInfo + "FAIL\n"
            strInfo = strInfo + "check db OK\n\n"

            return strInfo
        except Exception, e:
            g_logE.error(self.__class__.__name__ + "," + str(session.aid) + ",exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            fp = StringIO.StringIO()
            traceback.print_exc(file = fp)
            strInfo = strInfo + "\nexception:\n" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1])
            strInfo = strInfo + "\ntraceback:\n" + fp.getvalue()
            return strInfo
