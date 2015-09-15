#coding=utf8
from TexasSyncSocket import TexasSyncSocket
import TexasConfig

#加万能豆
def CMD_AddPowerGameCoin(strUserName, nCoin):
    print("CMD_AddPowerGameCoin user:" + strUserName + ",coin:" + str(nCoin) + " ...")
    s = TexasSyncSocket()
    if s.Connect(TexasConfig.DBSERVER_HOST, TexasConfig.DBSERVER_PORT) == False:
        return False
    ret = s.PowerGameCoinChange(strUserName, nCoin)
    print(ret)
    s.Close()

    if ret[0] != 0:
        return False
    print("CMD_AddPowerGameCoin user:" + strUserName + ",coin:" + str(nCoin) + " OK")
    return True

strUser = "chaim0415"
CMD_AddPowerGameCoin(strUser, 8000000)
