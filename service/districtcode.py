# -*- coding: utf-8 -*-
import os,random
from datetime import date,timedelta
# 随机生成身份证号
BASE_DIR = os.path.dirname(os.path.dirname(__file__))#返回文件路径,返回当前python执行脚本的执行路径，这里__file__为固定参数
DC_PATH = BASE_DIR + "/districtcode.txt"
def getdistrictcode():
	with open(DC_PATH) as file:
		data = file.read()
		districtlist = data.split('\n')
	for node in districtlist:
		if node[10:11] != ' ':
			state = node[10:].strip()
		if node[10:11] == ' ' and node[12:13] != ' ': #[12:13]市辖区，县
			city = node[12:].strip()#区，县（如静海县，魏县）
		if node[10:11] == ' ' and node[12:13] == ' ':
			district = node[14:].strip()#区，县，市（东城区，延庆县，辛集市）
			code = node[0:6]#获取区域码，如东城区110101
			codelist.append({"state": state, "city": city, "district": district, "code": code})

def gennerator():
	global codelist
	codelist = []
	if not codelist:
		getdistrictcode()
	id = codelist[random.randint(0, len(codelist))]['code']  # 地区项
	id = id + str(random.randint(1980, 1990))  # 年份项
	da = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
	id = id + da.strftime('%m%d')
	id = id + str(random.randint(100, 300))  # ，顺序号简单处理
	i = 0
	count = 0
	weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
	checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '4', '9': '3','10': '2'}  # 校验码映射
	for i in range(0, len(id)):
		count = count + int(id[i]) * weight[i]
	return id + checkcode[str(count % 11)]  # 算出校验码