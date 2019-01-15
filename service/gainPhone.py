# -*- coding: utf-8 -*-
import random
# 随机生成手机号码
def createPhone():
	prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153","155", "156", "157", "158", "159", "186",
			   "187", "188"]
	return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
#随机生成座机电话号码
def telePhone():
	tellist = ["8","6","5"]
	return random.choice(tellist)+ "".join(random.choice("0123456789") for i in range(7))