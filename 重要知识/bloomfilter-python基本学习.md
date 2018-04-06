# Bloomfilter 基本学习
---

## 基本内容

其他原理不再赘述，列出一下几点：

* 作用：检测一个元素是不是集合中的一个成员

* 核心：用(若干个)**哈希函数**的方法，将一个元素映射到一个 长度为m的阵列上的(若干个)一个点，当(该元素哈希值所对应的若干个点)这个点是 1 时，那么这个元素在集合内，反之则不在集合内。

* 优点：空间和时间效率都很高

* 缺点：当检测的元素很多的时候可能有**冲突**(导致**错判“在集合内”的概率就越大了**)

* 缺点解决：使用 k 个哈希 函数对应 k 个点，如果所有点都是 1 的话，那么元素在集合内，如果有 0 的话，元素则不在集合内。

* 百度百科对此讲解十分清楚：[Bloomfilter](https://baike.baidu.com/item/bloom%20filter/6630926?fr=aladdin)

## Pyhton代码

* 代码转载自[CSDN-Python写的BloomFilter](http://blog.csdn.net/demon24/article/details/8537665)

* 写代码方面这里学习到的有：
    
    * BloomFilter初始化时把每个实例化的SimpleHash对象加入到了列表中，之后通过循环列表就可以调用不同seed对应的hash函数；这一点在写代码方面值得学习；

    * isContaions(self, value)函数中ret初值为True，与根据hash得到的每一位上结果相与，若最终结果为False，则说明至少有一位为False，则说明没有添加此元素；
    
* 其他要注意的地方已在代码中添加了注释；

* 很多时候bloomfilter与redis结合使用，可参见[基于Redis的bloomfilter去重-附python代码](http://blog.csdn.net/bone_ace/article/details/53107018)

```python
#_*_coding:utf_8
# http://blog.csdn.net/demon24/article/details/8537665
import BitVector
import os
import sys

class SimpleHash():

    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            # seed不同使hash方法不同
            ret += self.seed*ret + ord(value[i])
        return (self.cap-1) & ret # QUESTION:???

class BloomFilter():

    def __init__(self, BIT_SIZE=1<<25):
        self.BIT_SIZE = 1 << 25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.bitset = BitVector.BitVector(size=self.BIT_SIZE)
        self.hashFunc = []

        for i in range(len(self.seeds)): # 将每个种子对应的hash 对象加入列表，以便以后调用
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))

    def insert(self, value):
        for f in self.hashFunc:
            loc = f.hash(value)
            self.bitset[loc] = 1 # 置该位为1

    def isContaions(self, value):
        if value == None:
            return False
        ret = True
        for f in self.hashFunc:
            # f是具体(seed不同)的每个hash对象
            loc = f.hash(value)
            ret = ret & self.bitset[loc] # 每个位上结果相与，如果有一位为False，则最终结果为False，说明可以添加进去
        return ret

def main():
    fd = open("url.txt")
    bloomfilter = BloomFilter()
    while True:

        url = fd.readline()
        if cmp(url, 'exit') == 0: #if url is equal exit break
            break
        if bloomfilter.isContaions(url) == False:
            bloomfilter.insert(url)
        else:
            print url
            break
            print 'url :%s has exist' % url

main()



"""
测试所用url:url.txt
http://zhidao.baidu.com/question/456449926.html
http://www.baidu.com/s?word=Python+%E5%AD%97%E6%AF%8D%E8%BD%AC%E6%8D%A2%E6%88%90%E6%95%B4%E6%95%B0&tn=sitehao123&ie=utf-8
http://www.hao123.com/
http://www.baidu.com/
http://www.sina.com.cn/
http://sports.sina.com.cn/g/premierleague/
http://zhidao.baidu.com/question/456449926.html
http://www.hao123.com/
http://hi.baidu.com/zjw0358/item/5dc673f8027cd814ff3582cc
http://video.baidu.com/v?ct=301989888&rn=20&pn=0&db=0&s=22&word=Python+%D7%D6%C4%B8%D7%AA%BB%BB%B3%C9%D5%FB%CA%FD
http://www.hao123.com/redian/tongzhi.htm
http://www.oschina.net/code/snippet_16840_2001
http://www.sina.com.cn/
exit
"""

```


---
2018.01.26
