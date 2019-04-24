# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import datetime
interfaceNo = "addusertag"
name = "添加用户个性标签"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 添加用户个性标签(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url,tagname, touid, token, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.tagname = str(tagname)
        self.touid = str(touid)
        self.token = str(token)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """添加用户个性标签"""
    def test_body(self):
        req.httpname = "KPTEST"

        # 2. ios, android
        self.tagname = get_excel("tagname", self.No, interfaceNo)
        # app版本号
        self.touid = get_excel("touid", self.No, interfaceNo)
        # 获取执行接口的url
        self.url = get_excel("url", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, interfaceNo)

        self.data = {
            "tag_name":self.tagname,
            "to_uid": self.touid,
            #"app_version": self.appversion,
            "system": "5",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        req.set_data(self.data)
        req.set_url(self.url, self.data, self.token)
        self.response = req.post()

        try:
            if self.response is None:
                self.retcode = 1
                self.msg = "报文返回为空！"
            else:
                self.retcode = self.response["code"]
                self.msg = self.response["msg"]
        except Exception:
            self.logger.error("报文返回为空！")
            print("报文返回为空！")
        self.check_result()
        self.wr_excel()

    # 检查数据结果
    def check_result(self):
        try:
            self.assertEqual(self.retcode, 0, self.logger.info("是否添加用户个性标签"))
            set_excel("pass", "测试结果", self.No, interfaceNo)
            self.logger.info("测试通过")
        except AssertionError:
            set_excel("fail", "测试结果", self.No, interfaceNo)
            self.logger.error("测试失败")
        self.logger.info(self.msg)

    # 写入xls文件中
    def wr_excel(self):
        '''
        set_excel(r'"'+str(self.data)+'"', "请求报文", self.No, interfaceNo)
        set_excel(r'"'+str(self.response)+'"', "返回报文", self.No, interfaceNo)
        '''
        set_excel(self.msg, "预期结果", self.No, interfaceNo)

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

