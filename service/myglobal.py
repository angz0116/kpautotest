# -*- coding:utf-8 -*-
# 告诉编译器这是全局变量intoappId
global intoappId

def set_value(value):
	# 告诉编译器我在这个方法中使用的intoappId是刚才定义的全局变量intoappId,而不是方法内部的局部变量.
	global intoappId
	intoappId = value

def get_value():
	# 同样告诉编译器我在这个方法中使用的intoappId是刚才定义的全局变量intoappId,并返回全局变量a,而不是方法内部的局部变量.
	global intoappId
	return intoappId