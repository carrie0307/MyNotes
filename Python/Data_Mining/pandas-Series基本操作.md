# Series相关整理

------
http://blkstone.github.io/2015/11/21/pandas-tutorial-1/

http://www.cnblogs.com/renfanzi/p/6420783.html

https://www.dataapplab.com/python-data-wrangling-pandas/


## 创建

#### 从列表创建series

```python
# coding=utf-8
import numpy as np
from pandas import Series,DataFrame

# 创建series， 数据是data列表内容，对应的index(或key)是index中内容
s = Series(data=[1,2,3,4,5], index=['a', 'b', 'c', 'd', 'e'])
print s
'''
a    1
b    2
c    3
d    4
e    5
dtype: int64
'''

print s.index
'''
Index([u'a', u'b', u'c', u'd', u'e'], dtype='object')
'''
```

```python
# coding=utf-8
import numpy as np
from pandas import Series,DataFrame

'''
Series的另一个可选项是name，可指定Series的名称，可用Series.name访问。在随后的DataFrame中，每一列的列名在该列被单独取出来时就成了Series的名称
'''

s = Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'], name='my_series')
print s
print s.name
```

#### 从字典创建Series
```python
# coding=utf-8
import numpy as np
from pandas import Series,DataFrame

d = {'a': 0., 'b': 1, 'c': 2}
print "d is a dict:"
print d
'''
d is a dict:
{'a': 0.0, 'c': 2, 'b': 1}
'''

s = Series(d)
print "s is a Series:"
print s
'''
s is a Series:
a    0.0
b    1.0
c    2.0
dtype: float64
'''

# 用字典创建Series时指定index的情形（index长度不必和字典相同）
s = Series(d, index=['b', 'c', 'd', 'a'])
'''
b    1.0
c    2.0
d    NaN
a    0.0
dtype: float64
'''

# 如果数据就是一个单一的变量，如数字4，那么Series将重复这个变量
s = Series(4., index=['a', 'b', 'c', 'd', 'e'])
'''
a    4.0
b    4.0
c    4.0
d    4.0
e    4.0
dtype: float64
'''

```

## 数据访问
可以和数组一样**使用下**标，也可以像字典一样**使用索引**，还可以**使用一些条件过滤**
```python
s = Series([2,3,4,5,6,7,8,9,10,11],index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
'''
a   2
b   3
c   4
d   5
e   6
f   7
g   8
h   9
i    10
j   11
dtype: float64
'''

# 使用下标访问
print s[0]
'''
2
'''

# 切片访问
print s[:2]
'''
a    2
b    3
'''

# 根据下标选择访问
print s[2,0,4]
'''
c    4
a    2
e    6
dtype: int64
'''

# 根据索引选择访问
print s[['e','i']]
'''
e     6
i    10
dtype: int64
'''

# 根据条件访问
print s[s > 6]
'''
f     7
g     8
h     9
i    10
j    11
dtype: int64
'''
```

## 其他操作

#### 排序
```
s = Series([3,7,9,2,7,10,19,12,13,17],index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
# 输出排序后的结果
print s.order()

'''
d     2
a     3
b     7
e     7
c     9
f    10
h    12
i    13
j    17
g    19
dtype: int64
'''
```

#### 排名
排名（ranking) 跟排序关系密切， 且它会增设一个排名值（从1开始， 一直到数组中有效数据的数量）

```python
s = Series([3,7,9,2,7,10,19,12,13,17],index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
print s.rank()

'''
a     2.0
b     3.5
c     5.0
d     1.0
e     3.5
f     6.0
g    10.0
h     7.0
i     8.0
j     9.0
dtype: float64
'''
```











