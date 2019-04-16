# -*- coding:utf-8 -*-
from utils.baseDB import ConfigDB
from utils.baseUtils import *
sqldb = ConfigDB()
'''
查询科界app验证码
'''
#查询验证码的方法
def query_sql(mobile):
    sqldb.dbname = "KMPLUGIN"
    try:
        SQL = get_sql("KMPLUGIN", "verify_log", "mobile")%(mobile)
        cursor = sqldb.executeSQL(SQL)
        res = sqldb.get_all(cursor)
        print(res)
        if len(res)>0:
            content = res[0]
            result = content[6:10]
            return result
        else:
            return "0000"
            print("未查询到该手机号的验证码信息")
    except Exception:
        print("SQL查询结果为空！")
        return "0000"
    sqldb.closeDB()






