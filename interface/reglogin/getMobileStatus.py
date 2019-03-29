# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB

from datadao.verifyCode import getVerifyCode

interfaceNo = "getMobileStatus"
name = "检测账号是否注册getMobileStatus"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 检测账号是否注册(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文,url, mobile, status, secretkey,预期结果):
        self.No = str(No)
        self.url = str(url)
        self.mobile = str(mobile)
        self.status = str(status)
        self.secretkey = str(secretkey)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 获取手机号
        self.mobile = get_excel("mobile", self.No, interfaceNo)
        # 国家编码，86中国，其他国外
        self.countryCode = get_excel("countrycode", self.No, "register")
        # 根据注册类型判断是输入验证码或密码
        verityCode = getVerifyCode(self.No, "register", self.mobile)
        print("用户注册接口手机号==" + self.mobile)
        self.data = {
            "username": "18211014921",
            "verify": verityCode,
            "source": "1",
            "country_code":self.countryCode,
            "token": "5",
            "app_version": "8.0.0",
            "system": "3",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        req.set_url(self.url)
        self.response = req.post()
        try:
            print(self.response)
            if self.response["code"]==0:
                self.retcode = self.response["status"]
                self.secretkey = self.response["secret_key"]

            else:
                self.retcode = 2
                self.secretkey = ""
        except Exception:
            self.logger.error("报文返回为空！")
            print("报文返回为空！")
        self.check_result()
        self.wr_excel()

    def check_result(self):
        try:
            self.assertEqual(self.retcode, 1, self.logger.info("注册成功"))
            set_excel("pass", "测试结果", self.No, interfaceNo)
            self.logger.info("测试通过")
        except AssertionError:
            self.assertEqual(self.retcode, 2, self.logger.info("注册失败"))
            self.assertEqual(self.secretkey, "",self.logger.info("登录授权码为空"))
            set_excel("fail", "测试结果", self.No, interfaceNo)
            self.logger.error("测试失败")
    # 写入xls文件中
    def wr_excel(self):
        set_excel(self.data, "请求报文", self.No, interfaceNo)
        set_excel(self.response, "返回报文", self.No, interfaceNo)
        set_excel(self.retcode, "status", self.No, interfaceNo)
        set_excel(self.secretkey, "secret_key", self.No, interfaceNo)
    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

