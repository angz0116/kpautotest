# -*- coding:utf-8 -*-
from utils.baseDB import ConfigDB
from utils.baseUtils import *
sqldb = ConfigDB()
'''
查询科界app验证码
'''
#查询验证码的方法
def query_sql(logger, mobile,countrycode):
    sqldb.dbname = "KMPLUGIN"
    try:
        logger.info("==========查询验证码 START=======")
        # 假如是国内手机号则直接按照手机号查询，如果是国外，得加上国家编码
        if countrycode=="86":
            newmobile = mobile
        else:
            newmobile = str(countrycode)+str(mobile)
        SQL = get_sql("KMPLUGIN", "verify_log", "mobile")%(newmobile)
        cursor = sqldb.executeSQL(SQL)
        res = sqldb.get_all(cursor)
        if len(res)>0:
            # 如果是多条数据，是从数据库中取出最新的一条短信信息（元祖存放的数据）
            content = res[0]
            # 从最新短信中，得到字符串
            tupres = content[0]
            # 再从字符串中，通过切片得到短信验证码
            result =tupres[6:10]
            logger.info("==========查询验证码 END=======")
            return result
        else:
            logger.info("==========查询到该手机号的验证码信息=======")
            print("未查询到该手机号的验证码信息")
            return "1111"
    except Exception:
        print("SQL查询结果为空！")
        logger.info("==========查询验证码 失败=======")

    sqldb.closeDB()




