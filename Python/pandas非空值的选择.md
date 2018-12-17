# pandas非空值的选择

## 关键函数

* df.notna()   为Nan的将为

* df.isnull().any()


```python
df = pd.DataFrame({'age': [5, 6, np.NaN],
                  'born': [pd.NaT, pd.Timestamp('1939-05-27'),
                           pd.Timestamp('1940-04-25')],
                   'name': ['Alfred', 'Batman', ''],
                   'toy': [None, 'Batmobile', 'Joker']})
print(df)
"""
   age       born    name        toy
0  5.0        NaT  Alfred       None
1  6.0 1939-05-27  Batman  Batmobile
2  NaN 1940-04-25              Joker

"""

# 为True的说明包含了空值
print (df.isnull().any())
"""
age      True
born     True
name    False
toy      True
dtype: bool

"""

print (df['age'].notna())
# notna() 不是空值的将返回True
"""
0     True
1     True
2    False
Name: age, dtype: bool

"""

print (df[df['age'].notna()])
# 选取出age不为空的行
"""
   age       born    name        toy
0  5.0        NaT  Alfred       None
1  6.0 1939-05-27  Batman  Batmobile
"""

```

* 要注意的是，df['age'].notna()得到的age列上的值为True或False,需要通过df[df['age'].notna()]才能得到具体的neritic