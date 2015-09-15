#coding=utf8

import sys
import shutil
import MySQLdb
import TexasConfig
import traceback
import time

#每天商品限额清除
def Skus_ClearDataPerDay():
    try:
        conn = MySQLdb.connect(host=TexasConfig.DB_HOST,user=TexasConfig.DB_USER,passwd=TexasConfig.DB_PASS,db=TexasConfig.DB_DATABASE, charset='utf8')
    except Exception, e:
        print e
        return False
    cursor = conn.cursor()

    print("update config table...")
    strSql = "update tb_w_skus_limit_perday set TodayNum=0, resetdate=now()"
    if mysql_execute(cursor, strSql) == True:
        print("ok.")
    else:
        print("fail.")

    cursor.execute("commit")

    cursor.close()
    conn.close()

    return True

def mysql_execute(cursor, sql):
    try:
        cursor.execute(sql)
    except Exception, e:
        print e
        return False

    return True

#每天定单数据清除
def Payloads_ClearDataPerDay():
    try:
        conn = MySQLdb.connect(host=TexasConfig.DB_HOST,user=TexasConfig.DB_USER,passwd=TexasConfig.DB_PASS,db=TexasConfig.DB_DATABASE, charset='utf8')
    except Exception, e:
        print e
        return False
    cursor = conn.cursor()

    print("clear tb_w_payload...")
    strSql = "delete from tb_w_payload where recdate<now()-864000"#删除10天前的定单
    if mysql_execute(cursor, strSql) == True:
        print("ok.")
    else:
        print("fail.")

    cursor.execute("commit")

    cursor.close()
    conn.close()

    return True


print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("start...")
Skus_ClearDataPerDay()
Payloads_ClearDataPerDay()
print("complete")

