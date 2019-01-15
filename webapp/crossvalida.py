# -*- coding:utf-8 -*-
from utils.baseBrowser import BaseBrowser
from webapp.comlogin import test_comLogin
from selenium.webdriver.support.select import Select
import time,unittest
from service.myglobal import get_value
from utils.baseLog import MyLog as Log
log = Log.get_log()
logger = log.logger
'''
第二步，进件管理-交叉质检菜单，11036813苗双伟
'''
class test_crossValida(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
		logger.info("第二步************************crossvalida.py，进件管理-交叉质检，11036813，苗双伟")
	'''
	用另外一个角色进行“交叉质检”
	'''
	def test_crossValida(self):
		try:
			#通过第一步进件申请，得到进件编号
			intoappId = get_value()
			#intoappId = "130154629556"
			logger.info("通过第一步进件申请，得到进件编号："+intoappId)
			# 进入“借款系统”,与哪个环境
			httpname = "LOANJC5"
			systemname = "loan"
			# 根据用户名，密码，登录方法
			test_comLogin.test_login(self.driver, "11036813", "Cs654321", httpname, systemname)
			# 关闭第一个菜单“客户管理”菜单
			self.driver.find_element_by_id("firstMenu0").click()
			time.sleep(3)
			# 打开需要展示的“进件管理”菜单
			self.driver.find_element_by_id("firstMenu1").click()
			time.sleep(5)
			self.driver.find_element_by_xpath("//span[text()=' 交叉质检']").click()
			time.sleep(3)
			# 进入“交叉质检”iframe页面
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'queryEachCheckLbTIntoInfo')]"))
			time.sleep(3)
			self.driver.find_element_by_name("intoAppId").send_keys(intoappId)
			self.driver.find_element_by_xpath("//span[text()='查询']").click()
			time.sleep(3)
			# 选中第一条数据
			self.driver.find_element_by_xpath("//input[@type='radio']").click()
			# 点击“质检”按钮
			self.driver.find_element_by_link_text("质检").click()
			# 退出“交叉质检”iframe
			self.driver.switch_to.default_content()
			time.sleep(3)
			# 通过质检按钮，进入另外一个“交叉质检”iframe
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'eachCheckLbTIntoInfo')]"))
			# 质检结果“通过”
			Select(self.driver.find_element_by_id("eachCheckResultCode")).select_by_value("10")
			time.sleep(5)
			# 点“提交”按钮
			self.driver.find_element_by_id("doSubmitInto").click()
			# 退出该“交叉质检”iframe
			self.driver.switch_to.default_content()
		except Exception as err:
			logger.info("交叉质检错误信息：")
			logger.error(err)
	@classmethod
	def tearDownClass(self):
		# 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
		BaseBrowser.quit_browser(self.driver)
if __name__=='__main__':
	unittest.main()
	#cva = test_crossValida()
	#cva.test_crossValida()
