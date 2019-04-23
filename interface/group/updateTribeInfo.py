# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import datetime
interfaceNo = "updateTribeInfo"
name = "修改部落"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 修改部落(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, tribeid, name, logo, introduce, isCheck, isNotice, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.tribeid = str(tribeid)
        self.name = str(name)
        self.logo = str(logo)
        self.introduce = str(introduce)
        self.isCheck = str(isCheck)
        self.isNotice = str(isNotice)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """修改部落"""
    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")
        # 从getInterestTribeList中获取tribeid
        self.tribeid = get_excel("tribeid", self.No, "getInterestTribeList")
        # 部落名称
        self.name = get_excel("name", self.No, interfaceNo)
        # 部落头像
        self.logo = get_excel("logo", self.No, interfaceNo)
        # 部落介绍
        self.introduce = get_excel("introduce", self.No, interfaceNo)
        # 认证参数
        self.isCheck = get_excel("isCheck", self.No, interfaceNo)
        # 动态通知
        self.isNotice = get_excel("isNotice", self.No, interfaceNo)

        self.data = {
            "tribe_id":self.tribeid,
            "name": self.name,
            "logo": self.logo,
            "introduce":self.introduce,
            "isCheck": self.isCheck,
            "isNotice": self.isNotice,
            "system": "5",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        if self.token == "":
            self.urlq = self.url
            self.logger.info(interfaceNo + ">>>>token为空=====" + self.urlq)
        else:
            self.urlq = self.url + "&token=" + self.token
            self.logger.info(interfaceNo + ">>>>token=====" + self.urlq)
        req.set_url(self.urlq)
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
            self.assertEqual(self.retcode, 0, self.logger.info("是否修改部落成功"))
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
        set_excel(self.tribeid, "tribeid", self.No, interfaceNo)

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

