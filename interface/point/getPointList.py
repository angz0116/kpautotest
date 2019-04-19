# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import datetime
interfaceNo = "getPointList"
name = "获取用户积分明细信息"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 获取用户积分明细信息(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, page, type, uid, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.page = str(page)
        self.type = str(type)
        self.uid = str(uid)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """获取用户积分明细信息"""
    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")
        # 类型
        self.page = get_excel("page", self.No, interfaceNo)
        # 类型
        self.type = get_excel("type", self.No, interfaceNo)
        # 用户id
        self.uid = get_excel("uid", self.No, "login")

        self.data = {
            "page": self.page,
            "type": self.type,
            "uid": self.uid,
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        if self.token == "":
            self.urlq = self.url
            self.logger.info(interfaceNo + ">>>>token为空=====" + self.urlq)
        else:
            self.urlq = self.url + "&&token=" + self.token
            self.logger.info(interfaceNo + ">>>>token=====" + self.urlq)
        req.set_url(self.urlq)
        req.set_data(self.data)
        self.response = req.get()
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
            self.assertEqual(self.retcode, 0, self.logger.info("是否获取用户积分明细信息"))
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
        '''
        set_excel(r'"'+str(self.data)+'"', "请求报文", self.No, interfaceNo)
        set_excel(r'"'+str(self.response)+'"', "返回报文", self.No, interfaceNo)
        '''
        set_excel(self.msg, "预期结果", self.No, interfaceNo)
        set_excel(self.uid, "uid", self.No, interfaceNo)

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

