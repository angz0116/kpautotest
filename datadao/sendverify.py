from utils.baseUtils import *
from utils.baseHttp import ConfigHttp
req = ConfigHttp()
"""
获取发送验证码的方法
@:param action是注册或登录 
@:param ftype是手机号或邮箱类型
@:param account是手机号或邮箱
@:param countrycode是手机号国家编码
"""
def getSendverify(logger,action ,ftype, account, countrycode):
    logger.info("==========获取发送验证码 START=======")
    req.httpname = "KPTEST"
    url = "/account/sendverify"
    data = {
        "type": ftype,
        "action": action,
        "account": account,
        "country_code": countrycode,
        "system": "3",
        "device_model": "HUAWEI P10",
        "v": "3.11.2",
        "channel": "5"
    }
    req.set_url(url, data, token="")
    req.set_data(data)
    response = req.post()

    try:
        retcode = response["code"]
        if retcode==0:
            logger.info("发送短信成功")
        elif retcode==10019:
            logger.info("注册账号已经存在")
        else:
            logger.info("发送短信失败")
        logger.info("==========获取发送验证码 END=======")
        return retcode

    except Exception as ex:
        logger.info("==========获取发送验证码 失败=======")
        print(ex)
        print("获取发送验证码错误！")


