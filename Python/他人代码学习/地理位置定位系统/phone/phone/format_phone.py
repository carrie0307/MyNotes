# coding=utf-8
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
输入一个电话，
输出这个电话的标准格式
'''

class Deal_phone(object):
	def __init__(self):
		self.model1 = '(^[\d(+).\s%x,%|\-*]*$)|(^(%2B))|(^[\d(+).\s%x,%|\-*]*F$)'  # 含各种可出现的符号
		self.model2= '^((\+{1})([0-9]*)(\.{1}))([0-9]*)$'  #最标准的形式，"+数字.数字”（数字部分可为空，先判断是否满足此模板）
		##从文件中取出固话
		self.list_tel = []
		file_object = open('telphone.txt', 'rb')
		lines = file_object.readlines()
		for line in lines:
			s=line.strip().split('\t')
			self.list_tel.append((s[0],s[1],s[2]))
		file_object.close()
	# 判断电话是否是固定电话,此参数中的phone一定是第一位为0的
	def judeg_tel(self, phone):
		flag=0
		for i in self.list_tel:
			lengh = len(i[0])
			if(len(phone)<lengh):return 0
			else:
				quhao = phone[0:lengh]
				if (quhao == i[0]):
					flag=1
					return 1
		if(flag==0):
			return 0

	#判断电话是否为手机号，此参数中的phone第一位一定不是0
	def judge_ph(self,phone):
		model = '^((13[0-9])|(14[5|7|9])|(15([0-3]|[5-9]))|(166)|(17(3|[5-8]))|(18[0-9])|(19[8|9]))\d*$'
		p = re.compile(model)
		m = p.match(phone)
		if m:
			return 1
		else:
			return 0

	#正则表达式判断电话大致类型
	def match_phone(self,phone,model):
		p = re.compile(model)
		m = p.match(phone)
		if m:
			return 1
		else:
			return 0

	##提取各个部分截开的电话号码段进行判断格式化
	def judge_type(self,inner,inner_new,phone_new):
		type=1
		format_phone=None
		leng = len(inner)
		outter = phone_new[leng:]
		if(inner_new=="086"):
			type=11
			format_phone = "+" + inner + "." + outter
		else:
			if (outter == ''):
				type = 14
				format_phone = "+86." + inner
			else:
				if(phone_new>3):
					flag=Deal_phone.judge_ph(self, phone_new) #判断是否为手机号
					if(flag):
						type=13
						format_phone="+86."+phone_new
					else:
						if outter[0] != '0':
							outter_new = "0" + outter
						else:
							outter_new = outter
						if (Deal_phone.judeg_tel(self, inner_new)):  # 括号内是固话区号的
							type = 12
							format_phone = "+86." + phone_new
						elif (Deal_phone.judeg_tel(self, outter_new)):  # 括号外是固话区号的
							type = 12
							if (inner == "0"):
								format_phone = "+86." + phone_new
							else:
								format_phone = "+" + inner + "." + outter
						else:  # 括号内外均不是区号的,判断括号外有没有可能是手机号的
							if (len(outter) >= 3):
								if (outter[0] == "0"):
									outter_new2 = outter[1:]
								else:
									outter_new2 = outter
								if (outter_new2[0] == "1"):
									if (Deal_phone.judge_ph(self, outter_new2)):  # 括号外为手机号的
										type = 13
										format_phone = "+" + inner + "." + outter
									else:  # 括号内外均不是固话，括号外也不是手机号的
										type = 14
										format_phone = "+" + inner + "." + outter
								else:
									type = 14
									format_phone = "+" + inner + "." + outter
							else:
								type = 14
								format_phone = "+" + inner + "." + outter
				else:
					type=14
					format_phone="+86."+phone_new
		return type,format_phone


	##针对不同形式电话初始处理
	def get_format(self,phone):
		type=0
		format_phone=None
		flag=0
		flag = Deal_phone.match_phone(self, phone, self.model2)
		if flag:
			type = 2
			format_phone = phone
		else:
			flag = Deal_phone.match_phone(self, phone, self.model1)
			if flag:
				type = 1
				s1 = re.compile('%2B|%2b')
				phone2 = s1.sub('+', phone)
				s2 = re.compile('%2E|%2e')
				phone2 = s2.sub('.', phone2)
				flag = Deal_phone.match_phone(self, phone2, self.model2)
				if flag:
					type = 2
					format_phone = phone2
				else:
					s3 = re.compile('\-|\(|\)|\s|x|(\+\.)|F')
					phone_new = s3.sub('', phone2)
					if (phone_new):
						flag = Deal_phone.match_phone(self, phone_new, self.model2)
						if flag:  # 1)去上述符号直接成标准型的
							type = 2
							format_phone = phone_new
						##去上述符号未标准的往下处理
						else:
							s3 = re.compile('\-|\(|\)|\s|x|(\+\.)|F|\+|\.')  # 去全部特殊符号
							phone_new = s3.sub('', phone_new)
							if phone_new:
								nums = re.findall(r'\d+', phone2)  # 找各部分数字子串
								if nums:  ##分段进行判断是否为固话还是手机
									inner = nums[0]
									if inner[0] != '0':
										inner_new = "0" + inner
									else:
										inner_new = inner
									li = Deal_phone.judge_type(self, inner, inner_new, phone_new)
									type = li[0]
									format_phone = li[1]
								else:
									type = 14
									format_phone = "+86."
							else:
								type = 14
								format_phone = "+86."
					##去相关符号后没有数字了
					else:
						type = 14
						format_phone = "+86."
			else:
				if(phone.find('ext')==-1):#不含分号
					#把不在允许出现的符号范围内的符号替换成‘’
					s4 = re.compile('[^0-9\-\(\)\s\+\.]')
					phone_new = s4.sub('', phone)
					flag = Deal_phone.match_phone(self, phone_new, self.model1)
					if flag:
						ty_form=Deal_phone.get_format(self,phone_new)
						return ty_form
					else:#含一些更特殊的符号,只能把数字提来（基本走不到这）
						s4 = re.compile('\D')
						phone_new = s4.sub('', phone)
						if phone_new:
							ty_form = Deal_phone.get_format(self, phone_new)
							return ty_form
						else:
							type=14
							format_phone="+86."
				else:
					ll=phone.find('e')
					phone_new=phone[0:ll]
					ty_form = Deal_phone.get_format(self, phone_new)
					return ty_form
		return type, format_phone

	##主函数
	def get_type(self,phone):
		phones = []
		ty_form=()
		type=0
		format_phone=''
		if (phone.find("(FAX)") != -1):
			phones = phone.split("(FAX)")
		elif (phone.find('or') != -1):
			phones = phone.split('or')
		elif (phone.find('OR') != -1):
			phones = phone.split('OR')
		elif (phone.find('/ ') != -1):
			phones = phone.split('/ ')
		else:
			ty_form=Deal_phone.get_format(self, phone)
			type = ty_form[0]
			format_phone = ty_form[1]
		if (phones):
			s=','
			form_ph=''
			for pho in phones:
				ty_form=Deal_phone.get_format(self, pho)
				formp=ty_form[1]
				form_ph=form_ph+formp+s
			type=15
			format_phone=form_ph[:-1]
		return type,format_phone

if __name__ == "__main__":
	phone="=="
	a = Deal_phone()
	li=a.get_type(phone)
	print li[0]
	print li[1]
