#coding=utf8

import md5
import sys
import os

#定义语言
LANG_CN = "cn"
LANG_EN = "en"

#获取脚本文件的当前路径
def GetModulePath():
    # return "/var/www/apps/aow"
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

#版本字符串转换为整型
def Version2Int(strVersion):
    listNum = strVersion.split('.')
    listNum.reverse()
    nMulti = 1
    nVersion = 0
    for strNum in listNum:
        nVersion = int(strNum) * nMulti + nVersion
        nMulti = nMulti * (0xff+1)
    return nVersion

#做一些初始化工作
def Init():
    #设置日志文件
    strLogPath = os.path.join(GetModulePath(), "log")
    if not os.path.exists(strLogPath):
        os.mkdir(strLogPath)
        os.chmod(strLogPath, 0777)

    return True

if __name__ == '__main__':
    print(hex(Version2Int("1.09")))
#    print(EncodePassword("haha@263.com", "123456"))
#    print(GetModulePath())