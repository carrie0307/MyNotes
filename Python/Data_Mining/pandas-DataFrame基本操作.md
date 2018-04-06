# DataFrame基本操作
作者：是蓝先生
链接：http://www.jianshu.com/p/682c24aef525
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

------

## 将数据转化为DataFrame
* e.g.1
```python
import pandas as pd

df = pd.DataFrame(np.arange(1, 13).reshape(3, 4), 
                  columns=['A', 'B', 'C', 'D'])
```

* e.g.2
```python
import pandas as pd
df = pd.DataFrame([
            ['green', 'M', 10.1, 'class1'], 
            ['red', 'L', 13.5, 'class2'], 
            ['blue', 'XL', 15.3, 'class1']])

df.columns = ['color', 'size', 'price', 'classlabel']
```
e.g.2输出的结果：
```
   color size  price classlabel
0  green   XL   10.1     class1
1    red    L   13.5     class2
2   blue    M   15.3     class1
```

## 数据查看
```python
df = DataFrame(data);
df.head(6)表示显示前6行数据，若head()中不带参数则会显示全部数据。
df.tail(6)表示显示后6行数据，若tail()中不带参数则也会显示全部数据。
```

* 查看DataFrame的index，columns以及values
```python
df.index ; df.columns ; df.values 即可
```

* describe()函数对于数据的快速统计汇总
```python
# 对每一列数据进行统计，包括计数，均值，std，各个分位数等。
df.describe()
```

* 对数据的转置
```python
df.T
```

* 对轴进行排序

```python
df.sort_index(axis=1,ascending=False)；
# 其中axis=1表示对所有的columns进行排序，下面的数也跟着发生移动。后面的ascending=False表示按降序排列，参数缺失时默认升序。
```

* 对DataFrame中的值排序
```python
df.sort(columns='x')
# 即对df中的x这一列，从小到大进行排序。注意仅仅是x这一列，而上面的按轴进行排序时会对所有的columns进行操作。
```

## 选择对象

* 选择特定列和行的数据
```python
df['x'] 那么将会返回columns为x的列，注意这种方式一次只能返回一个列。df.x与df['x']意思一样。
```
* 取行数据，通过切片[]来选择
```python
df[0:3] 
# 则会返回前三行的数据。
```

* loc是通过标签来选择数据
```python
df.loc['one']
# 则会默认表示选取行为'one'的行；

df.loc[:,['a','b'] ] 
# 表示选取所有的行以及columns为a,b的列；

df.loc[['one','two'],['a','b']] 
# 表示选取'one'和'two'这两行以及columns为a,b的列；

df.loc['one','a']与df.loc[['one'],['a']]
# 作用是一样的，不过前者只显示对应的值，而后者会显示对应的行和列标签。
```

* iloc则是直接通过位置来选择数据,这与通过标签选择类似
```python
'''df.iloc[,]逗号前后是对行与列进行选择操作的分界线'''

'''对行的操作与下同理，处理逗号前的数字即可'''

df.iloc[:,1]
# 显示所有行，index为1那一列的数据（index起始为0）

df.iloc[:,1,3]
# 显示所有行，index为1和index为3这两列的数据（index起始为0）

df.iloc[:,1:3]
# 显示所有行，index从1到3列（不包括3）的数据（index起始为0）

'''-------------------------------------'''

df.iloc[1:2,1:2] 
# 则会显示第一行第一列的数据;(切片后面的值取不到)

df.iloc[1:2] 
# 即后面表示列的值没有时，默认选取行位置为1的数据;

df.iloc[[0,2],[1,2]] 
# 即可以自由选取行位置，和列位置对应的数据。
```

* 使用条件来选择,使用单独的列来选择数据
```python
df[a.c>0]
# 表示选择c列中大于0的数据

使用where来选择数据
df[a>0]
# 表直接选择a中所有大于0的数据

# 使用isin()选出特定列中包含特定值的行
df1=df.copy()
df1[df1['one'].isin(['2','3'])] 
# 表显示满足条件：列one中的值包含'2','3'的所有行。
```

## 设置值（赋值）

**赋值操作在上述选择操作的基础上直接赋值即可**
e.g.
```python
df.loc[:,['a','c']]=9 
# 即将a和c列的所有行中的值设置为9

df.iloc[:,[1,3]]=9
# 也表示将a和c列的所有行中的值设置为9
```

* 同时也依然可以用条件来直接赋值
```python
df[a>0]=-a
# 表示将df中所有大于0的数转化为负值
```

## 读入csv文件
```python
df = pd.read_csv(file_path, header=None)
```

## 写入csv文件
dataframe可以使用to_csv方法方便地导出到csv文件中，如果**数据中含有中文，一般encoding指定为"utf-8"**,否则导出时程序会因为不能识别相应的字符串而抛出异常，index指定为False表示不用导出dataframe的index数据。

```python
df.to_csv(file_path, encoding='utf-8', index=False)

df.to_csv(file_path, index=False)

```

## 行列迭代

```python
# -*- coding:utf-8 -*-

import pandas as pd

data = {'state':['Ohio', 'Ohio', 'Ohio', 'Nevada','Nevada'],
        'year':[2000, 2001, 2002, 2011, 2002],
        'pop':[1.5, 1.7, 3.6, 2.4, 2.9]}
df = pd.DataFrame(data)

print df
'''
   pop   state  year
0  1.5    Ohio  2000
1  1.7    Ohio  2001
2  3.6    Ohio  2002
3  2.4  Nevada  2011
4  2.9  Nevada  2002
'''

for ix, row in df.iterrows():
    # ix代表行号，row代表该行所有列的内容
    print ix,row
    print '\n'

'''
0 pop       1.5
state    Ohio
year     2000
Name: 0, dtype: object


1 pop       1.7
state    Ohio
year     2001
Name: 1, dtype: object


2 pop       3.6
state    Ohio
year     2002
Name: 2, dtype: object


3 pop         2.4
state    Nevada
year       2011
Name: 3, dtype: object


4 pop         2.9
state    Nevada
year       2002
Name: 4, dtype: object

'''

for ix, col in df.iteritems():
    # ix代表第几行(从0开始),col代表每一列的内容
    print ix,col
    print '\n'

'''

pop 0    1.5
1    1.7
2    3.6
3    2.4
4    2.9
Name: pop, dtype: float64


state 0      Ohio
1      Ohio
2      Ohio
3    Nevada
4    Nevada
Name: state, dtype: object


year 0    2000
1    2001
2    2002
3    2011
4    2002
Name: year, dtype: int64

'''
```

---
2017.12.21

