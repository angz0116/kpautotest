# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from service.gainName import getFullName
from service.districtcode import gennerator
interfaceNo = "certification"
name = "申请认证"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 申请认证(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, type, typeid, job, typename, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.type = str(type)
        self.typeid = str(typeid)
        self.job = str(job)
        self.typename = str(typename)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """申请认证"""
    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 认证类型 1=协会工作者 2=学会会员 3=企业工作者 4=媒体工作者 5=高校工作者 6=学会工作者
        self.type = get_excel("type", self.No, interfaceNo)
        # 组织ID
        self.typeid = get_excel("typeid", self.No, interfaceNo)
        # 职位 type=2时，非必填
        self.job = get_excel("job", self.No, interfaceNo)
        # 企业名称 type=3时必填
        self.typename = get_excel("typename", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")

        self.data = {
            "type": self.type,
            "type_id": self.typeid,
            "job": self.job,
            "type_name": self.typename,
            "v": "3.11.0",
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
            self.assertEqual(self.retcode, 0, self.logger.info("是否申请认证成功"))
            set_excel("pass", "测试结果", self.No, interfaceNo)
            self.logger.info("测试通过")
        except AssertionError:
            set_excel("fail", "测试结果", self.No, interfaceNo)
            self.logger.error("测试失败")
        self.msg = self.response["msg"]
        self.logger.info(self.msg)

    # 写入xls文件中
    def wr_excel(self):
        '''
        set_excel(r'"'+str(self.data)+'"', "请求报文", self.No, interfaceNo)
        set_excel(r'"'+str(self.response)+'"', "返回报文", self.No, interfaceNo)
        '''
        if "data" in self.response:
            if len(self.response["data"])>0:
                self.authid = self.response["data"]["auth_id"]
                set_excel(self.authid, "authid", self.No, "cancelCrowdAuth")
                set_excel(self.authid, "authid", self.No, "cancelAuth")
        set_excel(self.msg, "预期结果", self.No, interfaceNo)

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

