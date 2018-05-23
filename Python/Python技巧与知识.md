# Python技巧整理

* 遍历（列表）
* 字典
* 字典和列表输出汉字
* 线程
* 文件
* 时间处理（时间获取、时间运算）
* 排序（列表排序、字典排序）
* debugging
* 生成器
* Map,filter,reduce
* virtualenv
* Counter计数(上次整理到http://book.pythontips.com/en/latest/collections.html#counter)
* torndb
* 私有方法与属性
* 其他(暂时不归入以上几类的）

-----

* 文章推荐：

* [Intermediate Python](http://book.pythontips.com/en/latest/)

------
## 遍历（列表)

#### 遍历一个范围内的数字
```python
for i in [0, 1, 2, 3, 4, 5]:
    print i ** 2
 
for i in range(6):
    print i ** 2
```

**更好的方法**
```python
'''
xrange会返回一个迭代器，用来一次一个值地遍历一个范围。这种方式会比range更省内存。xrange在Python 3中已经改名为range。
'''

for i in xrange(6):
    print i ** 2
```

#### 反向遍历
```python
colors = ['red', 'green', 'blue', 'yellow']
 
for i in range(len(colors)-1, -1, -1):
    print colors[i]
```

**更好的方法**
```python
for color in reversed(colors):
    print color
```

#### 遍历两个集合
```python
names = ['raymond', 'rachel', 'matthew']
colors = ['red', 'green', 'blue', 'yellow']
 
n = min(len(names), len(colors))
for i in range(n):
    print names[i], '--->', colors[i]
 
for name, color in zip(names, colors):
    print name, '--->', color
```
**更好的方法**
```python
for name, color in izip(names, colors):
    print name, '--->', color

# zip在内存中生成一个新的列表，需要更多的内存。izip比zip效率更高。

# 注意：在Python 3中，izip改名为zip，并替换了原来的zip成为内置函数。

'''关于zip函数'''
li = [1,2,3]
li2 = [4,5,6]
li3 = zip(li1,li2)
print li3
'''
输出li3
[(1, 4), (2, 5), (3, 6)]
'''

for i,j in li3:
    print i,j
'''
输出i,j
1 4
2 5
3 6
'''
```

#### 有序地遍历

```python
colors = ['red', 'green', 'blue', 'yellow']

#正序
# sorted(colors):['blue', 'green', 'red', 'yellow']
for color in sorted(colors):
    print colors
 
# 倒序
# sorted(colors, reverse=True):['yellow', 'red', 'green', 'blue']
for color in sorted(colors, reverse=True):
    print colors
```

**自定义排序**
```
# 自定义排序顺序

colors = ['yellow', 'blue', 'green', 'red']
 
def compare_length(c1, c2):
    if len(c1) < len(c2): return -1 #return-1的会被排在前面
    if len(c1) > len(c2): return 1
    return 0
    
colors_2 = sorted(colors, cmp=compare_length)
'''
输出 colors_2
['red', 'blue', 'green', 'yellow']
'''
```

**更好的办法**
```python
print sorted(colors, key=len)
```

## 字典

#### 遍历字典的key
```python
d = {'matthew': 'blue', 'rachel': 'green', 'raymond': 'red'}
 
for k in d:
    print k
 
for k in d.keys():
    if k.startswith('r'):
        del d[k]
```
**在需要修改字典时，用第二种方法（d.keys()把字典里所有的key都复制到一个列表）**

####遍历一个字典的key和value
```python
# 并不快，每次必须要重新哈希并做一次查找
d = {'matthew': 'blue', 'rachel': 'green', 'raymond': 'red'}

for k in d:
    print k, '--->', d[k]
 
# 产生一个很大的列表
for k, v in d.items():
    print k, '--->', v
    
'''
d.items():[('matthew', 'blue'), ('rachel', 'green'), ('raymond', 'red')]
'''
```

**更好的方法**

```
for k, v in d.iteritems():
    print k, '--->', v

# iteritems()更好是因为它返回了一个迭代器。

注意：Python 3已经没有iteritems()了，items()的行为和iteritems()很接近。详情请看文档。
```

#### 用key-value对构建字典
```python
names = ['raymond', 'rachel', 'matthew']
colors = ['red', 'green', 'blue']
 
d = dict(izip(names, colors))
# {'matthew': 'blue', 'rachel': 'green', 'raymond': 'red'}

Python 3: d = dict(zip(names, colors))
```

#### 用字典计数
```python
colors = ['red', 'green', 'red', 'blue', 'green', 'red']
 
# 简单，基本的计数方法。适合初学者起步时学习。
d = {}
for color in colors:
    if color not in d:
        d[color] = 0
    d[color] += 1
 
# {'blue': 1, 'green': 2, 'red': 3}
```
**更好的方法**

```python
d = {}
for color in colors:
    d[color] = d.get(color, 0) + 1

# 稍微潮点的方法，但有些坑需要注意，适合熟练的老手。
import collections
d = collections.defaultdict(int)
for color in colors:
    d[color] += 1
```

#### 用字典分组 — 第I部分和第II部分
```python
names = ['raymond', 'rachel', 'matthew', 'roger',
         'betty', 'melissa', 'judith', 'charlie']
 
# 在这个例子，我们按name的长度分组
d = {}
for name in names:
    key = len(name)
    if key not in d:
        d[key] = []
    d[key].append(name) 
 
# {5: ['roger', 'betty'], 6: ['rachel', 'judith'], 7: ['raymond', 'matthew', 'melissa', 'charlie']}
 
 #　这个例子里也是直接计数
d = {}
for name in names:
    key = len(name)
    d.setdefault(key, []).append(name) # 默认设置为[]，存在列表则添加元素
a = [1,1,2,2,2,3,3]
b = {}
for x in a:
    b[x] = b.setdefault(x, 0) + 1 #默认设置为０，存在则＋１
'''
d: {1: 2, 2: 3, 3: 2}
'''

```

**更好的方法**
```python
import collections
d = collections.defaultdict(list)
for name in names:
    key = len(name)
    d[key].append(name)
```

#### 字典的popitem()是原子的吗？（这里没懂）
```python
d = {'matthew': 'blue', 'rachel': 'green', 'raymond': 'red'}
 
while d:
    key, value = d.popitem()
    print key, '-->', value

# popitem是原子的，所以多线程的时候没必要用锁包着它。
```

#### 连接字典（这里没懂）
```python
import argparse

defaults = {'color': 'red', 'user': 'guest'}
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
namespace = parser.parse_args([])
command_line_args = {k: v for k, v in vars(namespace).items() if v}
 
# 下面是通常的作法，默认使用第一个字典，接着用环境变量覆盖它，最后用命令行参数覆盖它。
# 然而不幸的是，这种方法拷贝数据太疯狂。
d = defaults.copy()
d.update(os.environ)
d.update(command_line_args)
```

**更好的方法**
```python
d = ChainMap(command_line_args, os.environ, defaults)

# ChainMap在Python 3中加入。高效而优雅。
```


## 列表
#### 列表解析和生成器
```python
result = []
for i in range(10):
s = i ** 2
    result.append(s)
print sum(result)
```
**更好的方法**
```python
print sum(i**2 for i in xrange(10))
```

**第一种方法说的是你在做什么，第二种方法说的是你想要什么**

## 文件

#### 如何打开关闭文件
```python
f = open('data.txt')
try:
    data = f.read()
finally:
    f.close()
```

**更好的方法**
```python
with open('data.txt') as f:
    data = f.read()
    print data # 输出文件内容
print data #输出文件内容

#注：以上两个位置输出都可以
```

## 列表和字典直接输出中文

* 输出字典
import json
print json.dumps(icp_locate_map, encoding="UTF-8", ensure_ascii=False)

* 输出列表
import json
print json.dumps(icp_list, encoding="UTF-8", ensure_ascii=False)

## 线程

#### 如何使用锁
```python
# 创建锁
lock = threading.Lock()
 
# 使用锁的老方法
lock.acquire()
try:
    print 'Critical section 1'
    print 'Critical section 2'
finally:
    lock.release()
```

**更好的方法**
```python
# 使用锁的新方法
with lock:
    print 'Critical section 1'
    print 'Critical section 2'
```

## 时间
#### 获取当前时间
```python
import time

print time.time()
'''
Out:1506941717.26
'''

print time.localtime(time.time())
'''
Out:
time.struct_time(tm_year=2017, tm_mon=10, tm_mday=2, tm_hour=18, tm_min=55, tm_sec=17, tm_wday=0, tm_yday=275, tm_isdst=0)
'''

print time.strftime('%Y-%m-%d',time.localtime(time.time())) # 是str类型
'''
Out:2017-10-02
'''
```

* 将指定的struct_time(默认为当前时间)，根据指定的格式化字符串输出
python中时间日期格式化符号：

%y 两位数的年份表示（00-99）

%Y 四位数的年份表示（000-9999）

%m 月份（01-12）

%d 月内中的一天（0-31）

%H 24小时制小时数（0-23）

%I 12小时制小时数（01-12） 

%M 分钟数（00=59）

%S 秒（00-59）

%a 本地简化星期名称

%A 本地完整星期名称

%b 本地简化的月份名称

%B 本地完整的月份名称

%c 本地相应的日期表示和时间表示

%j 年内的一天（001-366）

%p 本地A.M.或P.M.的等价符

%U 一年中的星期数（00-53）星期天为星期的开始

%w 星期（0-6），星期天为星期的开始

%W 一年中的星期数（00-53）星期一为星期的开始

%x 本地相应的日期表示

%X 本地相应的时间表示

%Z 当前时区的名称

%% %号本身 


#### datetime，string转化
**datetime => string**

```python
import datetime
now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')
#输出2017-10-02 19:07:15
```
 
**string => datetime**
```python
t_str = '2012-03-05 16:26:23'
d = datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
```

#### 时间运算

* 两个日期相差(天，秒，小时）
```pyhton
from __future__ import division
import datetime
d1 = datetime.datetime.strptime('2012-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2012-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')
delta = d1 - d2
print delta.days
print delta.seconds # soconds最大范围在一天之内，即小于等于36400

# 求间隔的小时数
delta.days * 24 + delta.seconds / 3600
```

## 排序
#### list排序
```python
# list本身不会被改变
>>> sorted([5, 2, 3, 1, 4])
[1, 2, 3, 4, 5]
```

```python
# 此时list本身将被修改。通常此方法不如sorted()方便，但是如果你不需要保留原来的list，此方法将更有效
>>> a = [5, 2, 3, 1, 4]
>>> a.sort()
>>> a
[1, 2, 3, 4, 5]
```
**list.sort()方法仅被定义在list中，相反地sorted()方法对所有的可迭代序列都有效。**


###### 对元素为元组的列表排序
```python
student_tuples = [
        ('john', 'A', 15),
        ('jane', 'B', 12),
        ('dave', 'B', 10),
]
>>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]


'''方法二：Operator 模块函数'''
from operator import itemgetter, attrgetter
>>> sorted(student_tuples, key=itemgetter(2))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

```

###### 对元素为字典的列表排序
```python
import operator
dd = [
{'name':'John','age':23},
{'name':'Tom','age':25},
{'name':'Mike','age':21}
]
print sorted(dd, key=operator.itemgetter('age'), reverse = True) # 从大到小排序
```

#### 字典排序
```python
dic = {'a':3 , 'b':2 , 'c': 1}

# 根据key排序（从大到小：reverse = True）;asd[0]代表key
print sorted(dic.iteritems(),key = lambda asd:asd[0],reverse = True)

# 根据value排序（从大到小：reverse = True）;asd[1]代表value
print sorted(dic.iteritems(),key = lambda asd:asd[1],reverse = True)
```

* 方法二OrderedDict

```python
from collections import OrderedDict

colours =  {"Red" : 198, "Green" : 170, "Blue" : 160}

# 无序输出
# for key, value in colours.items():
    # print(key, value)

colours = OrderedDict(colours.items()) # 排序

for key, value in colours.items():
    print(key, value)
    
'''
Output:
('Blue', 160)
('Green', 170)
('Red', 198)
'''
```



###### 字典中嵌套字典
```python
import operator

dd = {
'John':{'name':'John','age':23},
'Tom':{'name':'Tom','age':25},
'Mike':{'name':'Mike','age':21}
}

# 根据value中的age从大到小排序
print sorted(dd.iteritems(), key=lambda d:d[1]['age'], reverse = True) 

# 根据key的字符串长度从大到小排序
print sorted(dd.iteritems(), key=lambda d:len(d[0]), reverse = True)




```



## 其他

#### unpack序列
```python
p = 'Raymond', 'Hettinger', 0x30, 'python@example.com'
 
# 其它语言的常用方法/习惯
fname = p[0]
lname = p[1]
age = p[2]
email = p[3]
```

**更好的方法**
```python
p = 'Raymond', 'Hettinger', 0x30, 'python@example.com'
fname, lname, age, email = p
```

#### 更新多个变量的状态（没有看懂）
```python
def fibonacci(n):
    x = 0
    y = 1
    for i in range(n):
        print x
        t = y
        y = x + y
        x = t
```

**更好的方法**
```python
def fibonacci(n):
    x, y = 0, 1
    for i in range(n):
        print x
        x, y = y, x + y

'''
第一种方法的问题

x和y是状态，状态应该在一次操作中更新，分几行的话状态会互相对不上，这经常是bug的源头。
操作有顺序要求
太底层太细节

第二种方法抽象层级更高，没有操作顺序出错的风险而且更效率更高。
'''
```

#### 同时状态更新(没有看懂)
```
tmp_x = x + dx * t
tmp_y = y + dy * t
tmp_dx = influence(m, x, y, dx, dy, partial='x')
tmp_dy = influence(m, x, y, dx, dy, partial='y')
x = tmp_x
y = tmp_y
dx = tmp_dx
dy = tmp_dy
```

**更好的方法**
```
x, y, dx, dy = (x + dx * t,
                y + dy * t,
                influence(m, x, y, dx, dy, partial='x'),
                influence(m, x, y, dx, dy, partial='y'))
```

**效率**

```python
'''
优化的基本原则
除非必要，别无故移动数据
稍微注意一下用线性的操作取代O(n**2)的操作

总的来说，不要无故移动数据
'''
```

#### 连接字符串
```python
names = ['raymond', 'rachel', 'matthew', 'roger',
         'betty', 'melissa', 'judith', 'charlie']
 
s = names[0]
for name in names[1:]:
    s += ', ' + name
print s
```
**更好的方法**
```python
names = ['raymond', 'rachel', 'matthew', 'roger',
         'betty', 'melissa', 'judith', 'charlie']
print ', '.join(names)
```

#### 更新序列
```python
names = ['raymond', 'rachel', 'matthew', 'roger',
         'betty', 'melissa', 'judith', 'charlie']
 
del names[0]
'''
names:['rachel', 'matthew', 'roger', 'betty', 'melissa', 'judith', 'charlie']
'''
# 下面的代码标志着你用错了数据结构 (什么意思？这里没懂）
names.pop(0)
'''
names:['rachel', 'matthew', 'roger', 'betty', 'melissa', 'judith', 'charlie']
'''
names.insert(0, 'mark')
'''
names:['mark', 'rachel', 'matthew', 'roger', 'betty', 'melissa', 'judith', 'charlie']
'''
```


**更好的方法**
```python
import collections  
names = collections.deque(['raymond', 'rachel', 'matthew', 'roger',
           'betty', 'melissa', 'judith', 'charlie'])
del names[0]
print names
'''
Out: deque(['rachel', 'matthew', 'roger', 'betty', 'melissa', 'judith', 'charlie'])
'''
names.popleft()
print names
'''
Out: deque(['matthew', 'roger', 'betty', 'melissa', 'judith', 'charlie'])
'''
names.appendleft('mark')
'''
Out: deque(['mark', 'matthew', 'roger', 'betty', 'melissa', 'judith', 'charlie'])
'''
Out: print names[0]
'''
mark
'''
```

#### 分离出临时的上下文
```python
try:
    os.remove('somefile.tmp')
except OSError:
    pass
```

**更好的方法**
```python
with ignored(OSError):
    os.remove('somefile.tmp')
    
# ignored是Python 3.4加入的, 文档。

# 注意：ignored 实际上在标准库叫suppress(译注：contextlib.supress).
```  
**想法**:以后try...except...的都可以将Error用这样with的方法处理

## debug -- pdb

```
$ python -m pdb my_script.py
```

It would cause the debugger to stop the execution on the first statement it finds. This is helpful if your script is short. You can then inspect the variables and continue execution line-by-line.

#### 命令如下：

只有c学会了怎么用，其他试验后没有看懂含义

* c: continue execution(用c可以一行一行单步调式)

* w: shows the context of the current line it is executing.

* a: print the argument list of the current function

* s: Execute the current line and stop at the first possible occasion.

* n: Continue execution until the next line in the current function is reached or it returns.

#### pdb.set_trace()设置断点

```python
import pdb

def make_bread():
    pdb.set_trace()
    print '----'
    return "I don't have time"

print make_bread()

```

程序会在执行到 pdb.set_trace()时停下来，然后可以通过c一步一步进行执行。

## 生成器

```python

def generator_function():
    for i in range(10):
        yield i
        
b = generator_function()

# 遍历方法：
print b.next()
print next(b)
for i in b:
    print i

# 注：由于b中只放入了10个数字，因此b.next() / next(b)智能执行10次；

# 如果先执行过一次b.next() / next(b)， 则for i in b所遍历的数字将接着b.next() / next(b)输出的内容输出
```

* Map

* filter

filter creates a list of elements for which a function returns true. Here is a short and concise example:

```python
number_list = range(-5, 5)
less_than_zero = list(filter(lambda x: x < 0, number_list))
print(less_than_zero)

# Output: [-5, -4, -3, -2, -1]
```

* reduce

格式：reduce(func, seq[, init])

```python
def f(x, y):
    return x + y

reduce(f, [1, 3, 5, 7, 9])   # 返回25

# 设置初值： 
reduce(f, [1, 3, 5, 7, 9], 100) # 返回125

# 利用lambda
reduce(lambda x,y:x+y,[1, 3, 5, 7, 9])  

```

* virtualenv
 
见[virtual_environment](http://book.pythontips.com/en/latest/virtual_environment.html）

* Counter

```python
from collections import Counter

''' 字符计数 '''

c = Counter('abcasd')
print c
# Output:Counter({'a': 2, 'c': 1, 'b': 1, 's': 1, 'd': 1})

# most_common(n) 按照counter的计数，按照降序，返回前n项组成的list; n忽略时返回全部
>>> Counter('abracadabra').most_common(3)
[('a', 5), ('r', 2), ('b', 2)]

''' 列表计数 '''

c = Counter(['apple', 'pear','pear'])
print c['orange']
# Output: 0
print c['pear']
# Output: 2

# 更新：增加元素
obj = collections.Counter(['11','22'])
obj.update(['22','55'])
print(obj)
#Output：Counter({'22': 2, '11': 1, '55': 1})

# 减去元素: 原来的元素减去新传入的元素
obj = collections.Counter(['11','22','33'])
obj.subtract(['22','55'])
print(obj)
#Output：Counter({'11': 1, '33': 1, '22': 0, '55': -1})


```

# tornodb
一个轻量级的基于MySQLdb封装的一个模块，其是tornado框架的一部分。

```pyhton
import torndb
db = torndb.Connection("127.0.0.1:3306", "test", user="root", password="admin") 
# 默认字符集UTF8，没必要在加上 charset = "utf8" 。

# 具体方法：execute,query,get
```

## 私有属性与方法

* 使用约定的**单下划线“_"和"__"双下划线**作为函数或属性的前缀来标识。使用单下划线还是双下划线，是有很大的区别的。

    * 1 单下划线的函数或属性，在**类定义中可以调用和访问**，**类的实例可以直接访问，子类中可以访问**；以单下划线开头的变量和函数被默认当作是内部函数，使用from module improt *时不会被获取(说明以_开题的函数仅供内部使用，是API中非公开的部分)，但是使用import module可以获取

    * 2  双下划线的函数或属性，在**类定义中可以调用和访问，类的实例不可以直接访问，子类不可访问**。

    * 注意：对于双下划线的函数或属性，Python解释器使用了名字混淆的方法， 将私有的方法"__method"变成了"_classname__method"了，具体看下文示例。

---
## 没有整理的：

* 装饰器和上下文管理
* 调用一个函数直到遇到标记值
* 在循环内识别多个退出点
* 试试创建你自己的ignored上下文管理器。
* 分离临时上下文
* 实现你自己的redirect_stdout上下文管理器。
* Raymond的原则：一行代码的逻辑等价于一句自然语言
(以上来自让你的http://mp.weixin.qq.com/s/XwDMxh7FNyrIFL-wxD1OLA)

---
* 参考

[让你的 Python 代码优雅又地道](http://mp.weixin.qq.com/s/XwDMxh7FNyrIFL-wxD1OLA)




