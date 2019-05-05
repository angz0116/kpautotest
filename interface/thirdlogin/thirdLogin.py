# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
import datetime
interfaceNo = "thirdLogin"
name = "三方登录"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 三方登录(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, type, nick, avatar, sex, unionid, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.type = str(type)
        self.nick = str(nick)
        self.avatar = str(avatar)
        self.sex = str(sex)
        self.unionid = str(unionid)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """三方登录"""
    def test_body(self):
        req.httpname = "KPTEST"
        self.url = get_excel("url", self.No, interfaceNo)
        # 类型 1=微信，2=微博，3=QQ
        self.type = get_excel("type", self.No, interfaceNo)
        # 第三方用户名
        self.nick = get_excel("nick", self.No, interfaceNo)
        # 头像url地址
        self.avatar = get_excel("avatar", self.No, interfaceNo)
        # 性别 1=男，2=女，3=保密
        self.sex = get_excel("sex", self.No, interfaceNo)
        # uuid手机识别号唯一标识
        # 获取当前时间
        now = datetime.datetime.now()
        self.uuid = now.strftime('%Y%m%d') + str(random.randint(0, 9000000))
        # unionid
        self.unionid = get_excel("unionid", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")
        # 手机型号
        self.unionid  = get_excel("unionid", self.No, interfaceNo)
        self.data = {
            "type":self.type,
            "nick": self.nick,
            "avatar": self.avatar,
            "sex": self.sex,
            "uuid": self.uuid,
            "union_id": self.unionid,
            "app_version": "3.11.0",
            "system": "3",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        req.set_url(self.url, self.data, self.token)
        req.set_data(self.data)
        self.response = req.post()
        try:
            print(self.response)
            if self.response is None:
                self.retcode= 1
                self.msg = "报文返回为空"
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
            self.assertEqual(self.retcode, 0, self.logger.info("是否三方登录成功"))
            set_excel("pass", "测试结果", self.No, interfaceNo)
            self.logger.info("测试通过")
        except AssertionError as ex:
            print("实际结果！=预期结果：")
            print(ex)
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

