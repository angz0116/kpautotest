# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import time
from datadao.sendverify import getSendverify
from datadao.queryverify import query_sql
from service.gainPhone import createPhone
interfaceNo = "bindMobile"
name = "绑定手机号"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 绑定手机号(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, mobile, flag, countrycode,password, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.countrycode = str(countrycode)
        self.mobile = str(mobile)
        self.password = str(password)
        self.flag = str(flag)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """绑定手机号"""
    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 国家编码
        self.countrycode = get_excel("countrycode", self.No, interfaceNo)
        # flag为1时，则重新生成新手机号；flag为2时，则从excel中读取已存在的
        self.flag = get_excel("flag", self.No, interfaceNo)
        # 根据flag进行判断，手机号是否生成新手机号
        if (self.flag == "1"):
            # 重新生成新手机号
            self.telphone = createPhone()
        else:
            # 从excel中获取手机号
            self.telphone = get_excel("mobile", self.No, interfaceNo)
        # 密码
        self.password = get_excel("password", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")
        # 获取验证码的方法
        getSendverify(self.logger, "reg", "mobile", self.telphone, self.countrycode)
        time.sleep(10)
        # 从数据库中查询验证码
        self.verifycode = query_sql(self.logger, self.telphone, self.countrycode)
        self.data = {
            "country_code": self.countrycode,
            "mobile": self.telphone,
            "verify": self.verifycode,
            "pass": self.password,
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
            self.assertEqual(self.retcode, 0, self.logger.info("是否绑定手机号成功"))
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

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

