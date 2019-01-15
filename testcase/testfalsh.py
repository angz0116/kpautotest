#-*-coding:utf-8 -*-
#计算欧几里德距离：
def euclidean(p,q):
#如果两数据集数目不同，计算两者之间都对应有的数
	same = 0
	for i in p:
		if i in q:
			same +=1

	#计算欧几里德距离,并将其标准化
	e = sum([(p[i] - q[i])**2 for i in range(same)])
	return 1/(1+e**.5)
p = [1,8,2,1,1,0,1,4,9,2,1]
q = [1,8,2,1,0,0,1,4,9,2,0]
print(euclidean(p, q))