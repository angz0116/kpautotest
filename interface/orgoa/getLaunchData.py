# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import datetime
interfaceNo = "getLaunchData"
name = "获取菜单及当前组织信息"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 获取菜单及当前组织信息(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, crowdid, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.crowdid = str(crowdid)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """获取菜单及当前组织信息"""
    def test_body(self):
        req.httpname = "KPTEST"
        # 获取执行接口的url
        self.url = get_excel("url", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")
        # crowd_id=0时，初始化crowd_id不为0，切换组织
        self.crowdid = get_excel("crowdid", self.No, interfaceNo)

        self.data = {
            "crowd_id": self.crowdid,
            "v": "3.11.0",
            "system": "5",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        if self.token=="":
            self.urlq = self.url
            self.logger.info(interfaceNo+">>>>token为空====="+self.urlq)
        else:
            self.urlq = self.url+"&token="+self.token
            self.logger.info(interfaceNo + ">>>>token====="+self.urlq)
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
            self.assertEqual(self.retcode, 0, self.logger.info("是否获取菜单及当前组织信息"))
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
        if self.retcode==0:
            if(len(self.response["data"]["recommendCrowd"])>0):
                self.orgid = self.response["data"]["recommendCrowd"][1]["id"]
                set_excel(self.orgid, "crowdid", self.No, "addFollow")
                set_excel(self.orgid, "crowdid", self.No, "delFollow")

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

