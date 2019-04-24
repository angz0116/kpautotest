# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import datetime
interfaceNo = "addReceiveAddr"
name = "添加收货地址"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 添加收货地址(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, rewardid, recipient, provinceid, cityid, countyid, address, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.rewardid = str(rewardid)
        self.recipient = str(recipient)
        self.provinceid = str(provinceid)
        self.cityid = str(cityid)
        self.countyid = str(countyid)
        self.address = str(address)



    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """添加收货地址"""
    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")
        # 奖励ID
        self.rewardid = get_excel("rewardid", self.No, interfaceNo)
        # 收货人姓名
        self.recipient = get_excel("recipient", self.No, interfaceNo)
        # 收货人手机号
        self.mobile = get_excel("mobile", self.No, interfaceNo)
        # 省份ID
        self.provinceid = get_excel("provinceid", self.No, interfaceNo)
        # 城市ID
        self.cityid = get_excel("cityid", self.No, interfaceNo)
        # 县级市ID
        self.countyid = get_excel("countyid", self.No, interfaceNo)
        # 详细地址
        self.address = get_excel("address", self.No, interfaceNo)
        self.data = {
            "reward_id": self.rewardid,
            "recipient": self.recipient,
            "mobile": self.mobile,
            "province_id": self.provinceid,
            "city_id": self.cityid,
            "county_id": self.countyid,
            "address": self.address,
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
            self.assertEqual(self.retcode, 0, self.logger.info("是否添加收货地址"))
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

