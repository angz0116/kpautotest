# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import datetime
interfaceNo = "tourist"
name = "游客注册登录接口"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 游客注册登录(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url,appsource,appversion, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.appsource = str(appsource)
        self.appversion = str(appversion)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """游客注册登录"""
    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 2. ios, android
        self.appsource = get_excel("appsource", self.No, interfaceNo)
        # app版本号
        self.appversion = get_excel("appversion", self.No, interfaceNo)
        # 获取当前时间
        now = datetime.datetime.now()
        # uuid手机识别号唯一标识
        uuid = now.strftime('%Y%m%d') + str(random.randint(0, 9000000))
        self.data = {
            "app_source":self.appsource,
            "uuid": uuid,
            "app_version": self.appversion,
            "system": "5",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        req.set_url(self.url)
        req.set_data(self.data)
        self.response = req.post()
        print(self.response)
        try:
            self.retcode = self.response["code"]
        except Exception:
            self.logger.error("报文返回为空！")
            print("报文返回为空！")
        self.check_result()
        self.wr_excel()

    # 检查数据结果
    def check_result(self):
        try:
            self.assertEqual(self.retcode, 0, self.logger.info("游客注册登录"))
            set_excel("pass", "测试结果", self.No, interfaceNo)
            self.logger.info("测试通过")
        except AssertionError:
            set_excel("fail", "测试结果", self.No, interfaceNo)
            self.msg = self.response["msg"]
            self.logger.error("测试失败")
        self.msg = self.response["msg"]
        self.logger.info(self.msg)

    # 写入xls文件中
    def wr_excel(self):
        set_excel(self.data, "请求报文", self.No, interfaceNo)
        set_excel(self.response, "返回报文", self.No, interfaceNo)
        set_excel(self.msg, "预期结果", self.No, interfaceNo)

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

