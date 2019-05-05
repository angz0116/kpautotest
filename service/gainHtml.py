# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from utils import readConfig

#获取html, 得到chrome
def getdriver():
	# 创建chrome参数对象
	option = webdriver.ChromeOptions()
	# 把chrome设置成无界面模式
	option.add_argument('--headless')
	driver = webdriver.Chrome(executable_path=readConfig.proDir+"\\chromedriver.exe", options=option)
	driver.maximize_window()
	return driver
#打开html
def openhtml(absPath):
    #返回绝对路径,返回一个文件在当前环境中的绝对路径，这里file 一参数
	url = absPath.replace("\\", "/")
	return url

# 保存截图
def savescreenimg(resultpath):
	driver = getdriver()
	url = openhtml(resultpath)
	driver.get(url)
	time.sleep(3)
	if len(resultpath)>0:
		# 通过切片获取到存储report.html的文件夹
		imgpath = resultpath[:len(resultpath)-11]
		# 把报告截图存放到跟report，log同一目录
		driver.save_screenshot(imgpath + "screenImg.png")
		#pic = ImageGrab.grab()
		#pic.save(imgpath + "screenImg.png")