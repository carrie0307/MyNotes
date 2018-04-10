# coding=utf-8

class MyHash(object):

	def __init__(self, length=300000):
		self.length = length
		self.items = [[] for i in range(self.length)]

	def hash(self, key):
		"""计算该key在items哪个list中，针对不同类型的key需重新实现"""
		return key % self.length

	def equals(self, key1, key2):
		"""比较两个key是否相等，针对不同类型的key需重新实现"""
		return key1 == key2

	def insert(self, key, value1,value2):
		index = self.hash(key)
		if self.items[index]:
			for item in self.items[index]:
				if self.equals(key, item[0]):
					# 添加时若有已存在的key，则先删除再添加（更新value）
					self.items[index].remove(item)
					break
		self.items[index].append((key, value1,value2))
		return True

	def get(self, key):
		index = self.hash(key)
		if self.items[index]:
			for item in self.items[index]:
				if self.equals(key, item[0]):
					return item[1],item[2]
		# 找不到key，则抛出KeyError异常
		else:
			return None

	def __setitem__(self, key, value1,value2):
		"""支持以 myhash[1] = 30000 方式添加"""
		return self.insert(key, value1,value2)

	def __getitem__(self, key):
		"""支持以 myhash[1] 方式读取"""
		return self.get(key)



if __name__ == "__main__":
	myhash = MyHash()
	code=11
	s1='福建'
	s2='厦门'
	myhash.insert(code ,s1,s2)
	li= myhash.get(11)
	if(li):
		print li[0]
		print li[1]
	else:
		print '找不到'