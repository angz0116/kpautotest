# -*- coding: utf-8 -*-
from selenium import webdriver
import os,time
from service.gainBank import getCMBbankCardNo
#获取html
def getdriver():
	driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
	driver.maximize_window()
	return driver
#保存html
def savehtml(fileName,htmlContext,pid):
	direname = os.path.dirname(os.path.dirname(__file__))
	localPath = direname+"\\savefile\\"+fileName+"{}.html".format(pid)
	fh = open(localPath, "w" ,encoding="utf-8")
	fh.write(htmlContext)
	fh.close()
#打开html
def openhtml(fileName,pid):
	direname = os.path.dirname(os.path.dirname(__file__))
	absPath = direname + "\\savefile\\" + fileName + "{}.html".format(pid)
	absUrl = "file:///" + os.path.abspath(absPath)#返回绝对路径,返回一个文件在当前环境中的绝对路径，这里file 一参数
	url = absUrl.replace("\\", "/")
	return url
#打开开户页面
def openaccount(fileName,pid):
	driver = getdriver()
	#获取打开文件地址
	url = openhtml(fileName,pid)
	driver.get(url)
	driver.find_element_by_xpath("//*[@id='nextBtn']").click()
	time.sleep(3)
#打开绑定银行卡页面
def openbindBank(fileName,pid):
	driver = getdriver()
	# 获取打开文件地址
	url = openhtml(fileName, pid)
	driver.get(url)
	time.sleep(3)
	#driver.find_element_by_link_text("我知道了").click()
	driver.find_element_by_xpath("//*[@id='sendSmsVerify']").click()
	driver.find_element_by_xpath("//*[@id='alertLayer-2']/div[2]/a").click()
	driver.find_element_by_xpath("//*[@id='smsCode']").send_keys("111111")
	driver.find_element_by_xpath("//*[@id='password']").send_keys("abc123456")
	driver.find_element_by_xpath("//*[@id='confirmPassword']").send_keys("abc123456")
	driver.find_element_by_xpath("//*[@id='nextButton']").click()
#打开充值页面
def openrecharge(fileName, pid):
	driver = getdriver()
	# 获取打开文件地址
	url = openhtml(fileName, pid)
	driver.get(url)
	time.sleep(3)
	driver.find_element_by_xpath("//*[@id='password']").send_keys("abc123456")
	driver.find_element_by_xpath("//*[@id='nextButton']").click()
	driver.quit()
#打开提现页面
def openwithdraw(fileName, pid):
	driver = getdriver()
	#获取打开文件地址
	url = openhtml(fileName, pid)
	driver.get(url)
	time.sleep(3)
	driver.find_element_by_xpath("//*[@id='sendSmsVerify']").click()
	driver.find_element_by_xpath("//*[@id='alertLayer-2']/div[2]/a").click()
	driver.find_element_by_xpath("//*[@id='smsCode']").send_keys("111111")
	driver.find_element_by_xpath("//*[@id='password']").send_keys("abc123456")
	driver.find_element_by_xpath("//*[@id='nextButton']").click()
#打开激活页面
def openactivate(fileName, pid , mobile):
	driver = getdriver()
	# 获取打开文件地址
	url = openhtml(fileName, pid)
	driver.get(url)
	#time.sleep(3)
	#应判断假如已绑定银行卡，则该字段不应再输入#//*[@id="bankcardNo"]
	bankcard = driver.find_element_by_id("bankcardNo").text
	print("-----bankcard=="+bankcard)
	if bankcard == "" :
		bankcardNo = getCMBbankCardNo()
		print("bankcardNo===="+bankcardNo)
		driver.find_element_by_xpath("//*[@id='bankcardNo']").send_keys(bankcardNo)
		driver.find_element_by_xpath("//*[@id='mobile']").send_keys(mobile)
	time.sleep(3)
	driver.find_element_by_xpath("//*[@id='sendSmsVerify']").click()
	driver.find_element_by_xpath("//*[@id='alertLayer-2']/div[2]/a").click()
	driver.find_element_by_xpath("//*[@id='smsCode']").send_keys("111111")
	driver.find_element_by_xpath("//*[@id='password']").send_keys("abc123456")
	driver.find_element_by_xpath("//*[@id='confirmPassword']").send_keys("abc123456")
	driver.find_element_by_xpath("//*[@id='nextButton']").click()
#打开变更银行卡预留手机号页面
def opencphone(fileName , pid):
	driver = getdriver()
	#获取打开文件地址
	url = openhtml(fileName , pid)
	driver.get(url)
#打开存管客户验证交易密码
def opencheckpwd(fileName , pid):
	driver = getdriver()
	#获取打开文件地址
	url = openhtml(fileName , pid)
	driver.get(url)
#打开授权管理页面
def openauthorize(fileName , pid):
	driver = getdriver()
	#获取打开文件地址
	url = openhtml(fileName , pid)
	driver.get(url)
	driver.find_element_by_xpath("//*[@id='password']").send_keys("abc123456")
	driver.find_element_by_xpath("//*[@id='nextButton']").click()