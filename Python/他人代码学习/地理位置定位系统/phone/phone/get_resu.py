# coding=utf-8
'''
基于数据结构对电话进行解析
'''
import  MySQLdb
import re
from hashmap1 import MyHash
from  format_phone import Deal_phone
from  qianduan_format import WebFormat
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
输入一个电话，
输出这个电话的标准格式、地理位置、类型、是否中国（0表示中国，1不是，但有些是中国的号码，可能国际代码处写的国外的）
类型：1为正常解析，2为异常解析（如位数不对或者是有些补0有些去0才解析成功），
	  3位解析不了的
'''

class GetRes(object):
	def __init__(self):
		self.myhash = MyHash()
		self.dealphone=Deal_phone()
		self.file_object = open('phone.txt', 'rb') #手机号
		self.lines = self.file_object.readlines()
		self.file_object.close()
	##将供手机号码解析的地理位置源录入hashmap中
	def ini(self):
		for line in self.lines:
			s=line.strip().split('\t')
			code=int(s[0])
			pro=s[1]
			city=s[2]
			self.myhash.insert(code, pro, city)

	##根据手机号码的前7位，返回对应的地理位置
	def phone_pos(self,code):
		li=self.myhash.get(code)
		if(li):
			return li
		else:
			return None

	##找固定电话的地理位置,此处的phone_right一定是首位为0的
	def tel_pos(self,phone_right):
		flag=0
		for i in self.dealphone.list_tel:
			quhao = i[0]
			length = len(quhao)
			phone_quhao = phone_right[0:length]  # 补0之后的区号位
			if (quhao == phone_quhao):  # 存在该区号，说明为固定电话
				flag = 1
				return i[1],i[2]
		if (flag== 0):
			return None

	#输入任意给定的电话，返回地理位置及标准格式
	def analysis_phone(self,phone):
		global flag1  # 表示是否为中国的,0表示中国，1表示外国
		global type  # 表示电话类型
		flag1 = 0
		type = 0
		s='0'
		pro=None
		city=None
		form_pho=self.dealphone.get_type(phone)
		format_phone=form_pho[1]
		phone_left=format_phone.split('.')[0]
		phone_right=format_phone.split('.')[1]
		ll=len(phone_right)
		phone_right_fir=phone_right
		if(ll>=2):
			#先当固话处理
			if(phone_right[0]!='0'):
				phone_right=s+phone_right
				type=2
			elif(phone_right[0:2]=='00'):
				phone_right=phone_right[1:]
				type=2
			else:
				if(len(phone_right)==11 or len(phone_right)==12):
					type=1
				else:
					type=2
			if(phone_right[1]=='0'):#最多去完两0之后还是0，则直接当解析失败
				type=3
			else: #开始固话解析
				if(len(phone_right)>=3):
					li=GetRes.tel_pos(self,phone_right)
					if(li):
						pro=li[0]
						city=li[1]
						l = WebFormat()
						city = l.change_city(pro, city)
					else:
						#当手机号解析
						if(ll>=7):
							if(phone_right_fir[0]=='1'):
								if(ll==11):
									type=1
								else:
									type=2
							elif(phone_right_fir[0]=='0' and phone_right_fir[1]=='1'):
								phone_right_fir=phone_right_fir[1:]
								type=2
							elif(phone_right_fir[0:2]=='00' and phone_right_fir[3]=='1'):
								phone_right_fir=phone_right_fir[2:]
								type=2
							else:
								type=3
							if(type!=3):
								if(len(phone_right_fir)>=7):
									##开始解析手机
									code=phone_right_fir[0:7]
									code=int(code)
									li=GetRes.phone_pos(self,code)
									if(li):
										pro=li[0]
										city=li[1]
										l = WebFormat()
										city = l.change_city(pro, city)
									else:
										type=3
								else:
									type=3
						else:
							type=3
				else:
					type=3
		else:
			type=3
		if(phone_left=="+86"):
			flag1=1
		return format_phone,pro,city,type,flag1

if __name__ == "__main__":
	phone='+1.5734272439'
	g=GetRes()
	g.ini()  # 将电话解析源初始化到hashmap中
	li=g.analysis_phone(phone)
	for i in li:
		print i
























