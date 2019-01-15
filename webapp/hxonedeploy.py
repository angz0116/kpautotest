# -*- coding:utf-8 -*-
from utils.baseBrowser import BaseBrowser
from webapp.comlogin import test_comLogin
from utils.baseDB import ConfigDB
from utils.baseUtils import *
import time,unittest
from service.myglobal import get_value
from utils.baseLog import MyLog as Log
log = Log.get_log()
logger = log.logger
#数据库连接信息
sqldb = ConfigDB()
'''
第六步，核心-合作调配-调配业务-一次调配，hxjauser，管理员
'''
class test_nondeploy(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
		logger.info("第六步************************hxonedeploy.py，合作调配-调配业务-一次调配，hxjauser，管理员")

		'''
		打开合作调配-调配业务-一次调配菜单及页面
		'''
	def openmenu(self):
		# 进入“信审系统”,与哪个环境
		httpname = "COREJC5"
		systemname = ""
		# 用核心管理员登录
		test_comLogin.test_login(self.driver, "hxjauser", "Cs654321", httpname, systemname)
		time.sleep(3)
		# 关闭第一个菜单“系统管理”
		self.driver.find_element_by_id("firstMenu0").click()
		time.sleep(3)
		# 打开“合作调配”菜单
		self.driver.find_element_by_id("firstMenu2").click()
		# 打开“合作调配-调配业务”菜单
		self.driver.find_element_by_xpath("//span[text()=' 调配业务']").click()
		# 打开“合作调配-调配业务-一次调配”页面
		self.driver.find_element_by_xpath("//li[text()='一次调配']").click()
		# 进入该“一次调配”页面的iframe
		self.driver.find_element_by_xpath("//iframe[contains(@src,'toQueryPage')]")
		time.sleep(3)
	'''
	点“一次调配”按钮，测试案例case
	'''
	def test_deploy(self):
		try:
			#得到进件编号
			#intoappId = get_value()
			intoappId = "130154629585"
			logger.info("通过第一步进件申请，得到进件编号：" + intoappId)
			loanstatu = self.check_sql(intoappId)
			if loanstatu =="" or loanstatu != "CL_001":
				logger.info("未在核心系统找到该进件编号的调配信息！")
			else:
				self.openmenu()
				self.onedeployclick(intoappId)
		except Exception as  err:
			BaseBrowser.quit_browser(self.driver)
			logger.info("核心-一次调配错误信息：")
			logger.error(err)

	#点击“一次调配”按钮的方法
	def onedeployclick(self, intoappId):
		try:
			self.driver.find_element_by_name("intoAppId").send_keys(intoappId)
			self.driver.find_element_by_xpath("//span[text()='查询']").click()
			time.sleep(3)
			self.driver.find_element_by_xpath("//input[@type='checkbox']").click()
			self.driver.find_element_by_link_text("一次调配").click()
			# 进入“一次调配” 页面的iframe
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'goTiaoPei')]"))
			self.driver.find_element_by_xpath("//input[@type='radio']").click()
			self.driver.find_element_by_xpath("//span[text()='保存']").click()
			time.sleep(3)
			self.driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]/span[text()='确认']").click()
			self.driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]/span[text()='关闭']").click()
		except Exception as err:
			logger.info("点击“一次调配”按钮触发的定位错误信息：")
			logger.error(err)

	# 根据sql查询在数据库中的信息
	def check_sql(self, intoappId):
		sqldb.dbname = "CORE5DB" #CL_001 未调配
		self.SQL = get_sql("COREDB", "t_c_cl_appinfo", "intoappId") % intoappId
		logger.info(self.SQL)
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			if self.res is None:
				self.loanstatu = ""
			else:
				self.loanstatu = str(self.res[0])
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()
		return self.loanstatu

	@classmethod
	def tearDownClass(self):
		# 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
		BaseBrowser.quit_browser(self.driver)
if __name__=='__main__':
	unittest.main()