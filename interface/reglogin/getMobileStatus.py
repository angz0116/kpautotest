# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import time
from datadao.sendverify import getSendverify
from datadao.queryverify import query_sql

interfaceNo = "getMobileStatus"
name = "检测账号是否注册"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 检测账号是否注册(unittest.TestCase):
    def setParameters(self, No, 测试结果, 测试案例, 请求报文, 返回报文,url, mobile, status, secretkey,预期结果):
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
        self.countrycode = get_excel("countrycode", self.No, "register")
        # 获取验证码的方法
        self.veresult = getSendverify(self.logger, "login", "mobile", self.mobile, self.countrycode)
        if self.veresult == 0:
            time.sleep(10)
            # 从数据库中查询验证码
            self.verifycode = query_sql(self.logger, self.mobile, self.countrycode)
        print("用户注册接口手机号==" + self.mobile)
        self.data = {
            "username": self.mobile,
            "verify": self.verifycode,
            "source": "1",
            "country_code":self.countrycode,
            "app_version": "8.0.0",
            "system": "3",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        req.set_data(self.data)
        req.set_url(self.url, self.data, token="")
        self.response = req.post()
        try:
            print(self.response)
            self.retcode = self.response["code"]
        except Exception:
            self.logger.error("报文返回为空！")
            print("报文返回为空！")
        self.check_result()
        self.wr_excel()

    def check_result(self):
        try:
            self.assertEqual(self.retcode, 0, self.logger.info("是否注册成功"))
            self.assertEqual(self.secretkey, "",self.logger.info("登录授权码为空"))
            if self.retcode==0:
                self.status = self.response["data"]["status"]
                # 登录授权码
                self.secretkey = self.response["data"]["secret_key"]
            else:
                self.status = 2
                self.secretkey = ""
            set_excel("pass", "测试结果", self.No, interfaceNo)
            self.logger.info("测试通过")
        except AssertionError as ex:
            print("实际结果！=预期结果：")
            print(ex)

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
        set_excel(self.status, "status", self.No, interfaceNo)
        set_excel(self.secretkey, "secretkey", self.No, interfaceNo)
        set_excel(self.msg, "预期结果", self.No, interfaceNo)
    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()

