# -*- coding:utf-8 -*-
import unittest
from utils.baseBrowser import BaseBrowser
import time
"""
登录方法
"""
class test_comLogin():
	#根据系统环境，系统名称得到应该使用哪个环境ip
	@staticmethod
	def gainurl(httpname, systemname):
		httpn = httpname[0:4]
		if "LOAN".__contains__(httpn):
			if httpname == "LOANJC1":
				if systemname == "loan":
					url = "dkjc1"
					pro = "loan"
				else:
					url = "fintechjc1"
					pro = "loan-credit"
			elif httpname == "LOANJC2":
				if systemname == "loan":
					url = "dkjc2"
					pro = "loan"
				else:
					url = "fintechjc2"
					pro = "loan-credit"
			elif httpname == "LOANJC3":
				if systemname == "loan":
					url = "dkjc3"
					pro = "loan"
				else:
					url = "fintechjc3"
					pro = "loan-credit"
			elif httpname == "LOANJC4":
				if systemname == "loan":
					url = "dkjc4"
					pro = "loan"
				else:
					url = "fintechjc4"
					pro = "loan-credit"
			elif httpname == "LOANJC5":
				if systemname == "loan":
					url = "dkjc5"
					pro = "loan"
				else:
					url = "fintechjc5"
					pro = "loan-credit"
			comurl = "http://" + url + ".jieyuechina.com/" + pro + "/user/caslogin"
		else:
			if httpname == "COREJC5":
				comurl = "http://172.18.100.89:8080/core-web/user/home"
			else:
				comurl = "http://lc.jieyuechina.com:8080/wmsystem/user/home"
		return comurl

	# 登录
	@staticmethod
	def test_login(driver, userNo, password, httpname, systemname):
		print("=======进入登录login=======")
		# 根据url打开浏览器
		url = test_comLogin.gainurl(httpname, systemname)
		BaseBrowser.open_browser(driver, url)
		driver.find_element_by_xpath("//*[@id='username']").send_keys(userNo)
		driver.find_element_by_xpath("//*[@id='pwd']").send_keys(password)
		driver.find_element_by_xpath("//*[@id='loginForm']/table/tbody/tr[4]/td[4]/div/button").click()
		BaseBrowser.get_window_img(driver, "incoming")
	'''
		# 打开向前金服管理系统-登录页面
		# 截图并保存
	'''

	#点“退出”按钮，退出登录系统
	@staticmethod
	def test_logout(driver):
		#退出
		time.sleep(3)
		driver.find_element_by_xpath(".//*[@title='退出']").click()

	#该方法用来确认元素是否存在，如果存在返回flag = true，否则返回false
	@staticmethod
	def isElementExist(driver,element):
		flag = True
		try:
			driver.find_element_by_class_name(element)
			return flag
		except:
			flag = False
			return flag