# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import datetime
interfaceNo = "getChatInfoById"
name = "获取部落成员信息"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 获取部落成员信息(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, tribeid, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.tribeid = str(tribeid)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """获取部落成员信息"""
    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")
        # 部落id
        # 从getInterestTribeList中获取tribeid
        self.tribeid = get_excel("tribeid", self.No, "getInterestTribeList")
        self.data = {
            "tribe_id":self.tribeid,
            "system": "5",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        req.set_url(self.url, self.data, self.token)
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
            self.assertEqual(self.retcode, 0, self.logger.info("是否获取部落成员信息成功"))
            set_excel("pass", "测试结果", self.No, interfaceNo)
            self.logger.info("测试通过")
        except AssertionError as ex:
            print("实际结果！=预期结果：")
            print(ex)
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
        set_excel(self.tribeid, "tribeid", self.No, interfaceNo)

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

