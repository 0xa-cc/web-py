#coding=utf8

import socket
import struct
import sys

GAME_ID = 25011
GAMEID_OF_POWERGAMECOIN = 39990

GLID_ACK = 0x80000000
GLID_BASESERVICEEX = 0x00005000
GLID_POWERGAMECOIN_CHANGE = 0X4000C#(GLID_BASESERVICEEX+12)

class TexasSyncSocket():
    def __init__(self):
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_socket.settimeout(30.0)
        self.m_strIP = ""

    def Connect(self, host, port):
        try:
            self.m_socket.connect((host, port))
            self.m_strIP = self.m_socket.getsockname()[0]
            print(self.m_strIP)
            return True
        except Exception, e:
            print("exception:" + str(sys.exc_info()[0]) + "," + str(sys.exc_info()[1]))
            return False

    #按指定格式发送消息，并等待消息应答
    def SendAndWait(self, dwMsgID, strMsgBody):
        try:
            strHeader = struct.pack('II', dwMsgID, len(strMsgBody))
            self.m_socket.send(strHeader+strMsgBody)

            strHeader = self.m_socket.recv(12)
            if len(strHeader) == 0:
                print("Disconnected,recv len 0")
                return (-1, 0)
            elif len(strHeader) != 12:
                print("Recv header error")
                return (-2, 0)
            ayHeader = struct.unpack('III', strHeader)
            dwType = ayHeader[0]
            dwLength = ayHeader[1]
            dwResult = ayHeader[2]
            # print("type:" + str(dwType) + ",len:" + str(dwLength) + ",ret:" + str(dwResult))
            strData = self.m_socket.recv(dwLength)
            # print(repr(strData))
            if len(strData) != dwLength:
                print("Recv body error")
                return (-3, dwType)
            if dwResult != 1:
                return (-4, dwType)
            return (0, dwType, strData)
        except Exception, e:
            return (-5, 0)
        
    def Close(self):
        self.m_socket.close()

    def PowerGameCoinChange(self, strUserName, nGameCoin):
        # strData = struct.pack('20sIi16siIi', strUserName.encode('gb18030'), GAMEID_OF_POWERGAMECOIN, nGameCoin, self.m_strIP, 8, 15339001, 1)#旧的消息格式，只支持32位豆
        strData = struct.pack('20sIq16siIii', strUserName.encode('gb18030'), GAMEID_OF_POWERGAMECOIN, nGameCoin, self.m_strIP, 8, 15339001, 1, 0)
        ret = self.SendAndWait(GLID_POWERGAMECOIN_CHANGE, strData)
        if ret[0] != 0:
            return (-1, 0)
        if ret[1] != GLID_POWERGAMECOIN_CHANGE | GLID_ACK:
            return (-2, 0)
        # ack = struct.unpack('I', ret[2])
        # print(len(ret[2]))
        # print(repr(ret[2]))
        ack = struct.unpack_from('q64s', ret[2], 4)
        # print(ack)
        return (0, ack[0])

if __name__ == "__main__":
    pass
    s = TexasSyncSocket()
    if s.Connect("172.28.14.11", 6000) == True:
        ret = s.PowerGameCoinChange("#gltest01", 1)
        print(ret)
        s.Close()


