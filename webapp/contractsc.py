# -*- coding:utf-8 -*-
import unittest

from utils.baseBrowser import BaseBrowser
from webapp.comlogin import test_comLogin
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
'''
签约菜单，admin登录
'''
class test_contractsc():
	def __init__(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
	'''
	进入“监控流程”菜单
	'''
	def test_hysc(self):
		# 进入“借款系统”,与哪个环境
		httpname = "LOANJC5"
		systemname = "loan"
		# 根据用户名，密码，登录方法
		test_comLogin.test_login(self.driver, "11059349", "Cs654321", httpname, systemname)
		#关闭第一个菜单
		self.driver.find_element_by_id("firstMenu0").click()
		time.sleep(5)
		#打开系统管理菜单
		self.driver.find_element_by_id("firstMenu8").click()
		#打开签约管理菜单
		self.driver.find_element_by_xpath("//span[text()=' 签约管理']").click()
		#等待元素可见
		#WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//li[text()='监控流程']")))
		# 打开监控流程菜单
		#self.driver.find_element_by_xpath("//li[text()='监控流程']").click()
		intoId  = "120154570318"
		time.sleep(3)
		# 进入“监控流程”页面
		self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src, 'toQueryPage')]"))
		# 进入“监控流程-待办监控”页面
		#查询条件“任务名称”
		self.driver.find_element_by_name("intoAppId").send_keys(intoId)
		#点“查询”按钮，查询出该待办任务信息
		self.driver.find_element_by_xpath("//span[text()='查询']").click()
		time.sleep(3)
		self.driver.find_element_by_xpath("//input[@type='radio']").click()
		self.driver.find_element_by_link_text("合同下载").click()
		time.sleep(3)
		self.driver.find_element_by_xpath("//span[text()='PC电子签章']").click()
		qrbtn = self.driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]/span[text()='确认']")
		qrbtn.click()

if __name__=='__main__':
	csc =test_contractsc()
	csc.test_hysc()