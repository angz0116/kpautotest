from utils.baseUtils import *
from utils.baseHttp import ConfigHttp
req = ConfigHttp()
"""
获取验证码的方法
"""
"""
获取验证码的方法
"""
def getVerifyCode(No,interfaceNo ,mobile):
    url = "http://api.scimall.vip/test/getCode?no_check=1"#application/json
    # 手机号
    countryCode = get_excel("countrycode", No, interfaceNo)
    data = {
        "mobile": mobile,
        "country_code": countryCode
    }
    req.set_data(data)
    response = req.getyz(url)
    try:
        retcode = response["data"]["code"]
        set_excel(retcode, "verifycode", No, interfaceNo)
        return retcode
    except Exception as ex:
        print(ex)
        print("获取验证码错误！")


