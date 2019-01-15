# -*- coding:utf-8 -*-
import unittest

from utils.baseBrowser import BaseBrowser
from webapp.comlogin import test_comLogin
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from service.myglobal import get_value
from utils.baseLog import MyLog as Log
log = Log.get_log()
logger = log.logger
'''
第三步，系统管理-流程管理-监控流程菜单，admin登录
'''
class test_monitorFlow(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		time.sleep(600)
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
		logger.info("第三步************************monitorflow.py，系统管理-流程管理-监控流程，amdin，管理员")
	'''
	进入“监控流程”菜单
	'''
	def test_monitorflow(self):
		try:
			# 通过第一步进件申请，得到进件编号
			intoappId = get_value()
			#intoappId = "130154629574"
			logger.info("通过第一步进件申请，得到进件编号：" + intoappId)
			# 进入“信审系统”,与哪个环境
			httpname = "LOANJC5"
			systemname = "credit"
			# 根据用户名，密码，登录方法
			test_comLogin.test_login(self.driver, "admin", "Cs654321", httpname, systemname)
			# 关闭第一个菜单
			self.driver.find_element_by_id("firstMenu0").click()
			time.sleep(5)
			# 打开系统管理菜单
			#集成3firstMenu16
			#self.driver.find_element_by_id("firstMenu16").click()
			self.driver.find_element_by_id("firstMenu9").click()
			# 控制拉动滚动条，可见流程管理
			version = self.driver.find_element_by_xpath("//span[text()=' 定时任务']")
			self.driver.execute_script("arguments[0].scrollIntoView();", version)
			time.sleep(3)
			# 打开流程管理菜单
			self.driver.find_element_by_xpath("//span[text()=' 流程管理']").click()
			# 等待元素可见
			WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//li[text()='监控流程']")))
			# 打开监控流程菜单
			self.driver.find_element_by_xpath("//li[text()='监控流程']").click()
			time.sleep(3)
			# 进入“监控流程”页面
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src, 'myProcessMonitor.jsp')]"))
			# 进入“监控流程-待办监控”页面
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src, 'monitorTodo.jsp')]"))
			# 查询条件“任务名称”
			self.driver.find_element_by_name("busInfoName").send_keys(intoappId)
			# 点“查询”按钮，查询出该待办任务信息
			self.driver.find_element_by_xpath("//span[text()='查询']").click()
			time.sleep(3)
			# 选中该待办任务
			self.driver.find_element_by_xpath("//input[@type='checkbox']").click()
			# 点“批量换人”按钮
			self.driver.find_element_by_link_text("批量换人").click()
			# 退出该“监控流程”页面
			self.driver.switch_to.default_content()
			# 退出该“监控流程-待办监控”页面
			self.driver.switch_to.default_content()
			time.sleep(3)
			# 进入“转移任务”页面
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'updateAssignee.jsp')]"))
			# 进入“组织结构树”页面
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'sysUserSelect.jsp')]"))
			# 点击“组织机构树-捷越联合”
			self.driver.find_element_by_xpath("//span[text()='捷越联合']").click()
			time.sleep(3)
			# 输入查询条件“编码”
			self.driver.find_element_by_xpath("//input[contains(@id,'userNofname')]").send_keys("11043892")
			# 点“查询”按钮
			self.driver.find_element_by_xpath("//button[contains(@id,'fname')]/span[2]").click()
			time.sleep(3)
			# 选中该条数据
			self.driver.find_element_by_xpath("//input[@type='radio']").click()
			# 点“确认”按钮，提交
			self.driver.find_element_by_link_text("确认").click()
			# 点弹出框“确定”按钮
			self.driver.switch_to.alert.accept()
			time.sleep(3)
			self.driver.switch_to.alert.accept()
			# 退出“组织结构树”页面
			self.driver.switch_to.default_content()
			# 退出“转移任务”页面
			self.driver.switch_to.default_content()
		except Exception as err:
			logger.info("第三步，监控流程，批量换人错误信息：")
			logger.error(err)
	@classmethod
	def tearDownClass(self):
		# 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
		BaseBrowser.quit_browser(self.driver)
if __name__=='__main__':
	unittest.main()
	#mflow =test_monitorFlow()
	#mflow.test_monitorflow()