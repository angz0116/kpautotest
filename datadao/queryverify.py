# -*- coding:utf-8 -*-
from utils.baseDB import ConfigDB
from utils.baseUtils import *
sqldb = ConfigDB()
'''
查询科界app验证码
'''
class queryVerify():
    #查询验证码的方法
    def query_sql(self , mobile):
        sqldb.dbname = "KMPLUGIN"
        try:
            self.SQL = get_sql("KMPLUGIN", "verify_log", "mobile") % (mobile)
            cursor = sqldb.executeSQL(self.SQL)
            res = sqldb.get_all(cursor)
            if(len(res)!=0):
                content = res[0]
                return content
            else:
                print("未查询到该手机号的验证码信息")
        except Exception:
            print("SQL查询结果为空！")
        sqldb.closeDB()

