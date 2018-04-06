# Pandas的json处理

------
[参考一-用pandas读写json](http://blog.csdn.net/qq_24683561/article/details/54578275)
[参考二-pandas.DataFrame.to_json按行转json](http://blog.csdn.net/huanbia/article/details/72674832)

# json 转 series
利用JSON字符串创建一个pandas.Series

直接以代码为例说明：

```python
# coding=utf-8
import pandas as pd
import numpy as np
from pandas import Series,DataFrame

# 调用read_json()函数时，既可以向其传递一个JSON字符串，也可以为其指定一个JSON文件的路径
json_str = '{"country":"Netherlands"}'
data = pd.read_json(json_str,typ='series') # 读json，转化为series
print data

'''
country    Netherlands
dtype: object
'''

data["country"] = "Brazil"
data = data.to_json()
print data

'''
{"country":"Brazil"}
'''
```

## DataFrame 转 json


* 如果是Series转json，默认的orient是'index'，orient可选参数有{'split','records','index'}
* 如果是DataFrame转json，默认的orient是'columns'，orient可选参数有 {'split','records','index','columns','values'}
* json的格式如下
```
split，样式为 {index -> [index], columns -> [columns], data -> [values]}

records，样式为[{column -> value}, … , {column -> value}]

index ，样式为 {index -> {column -> value}}

columns，样式为 {index -> {column -> value}}

values，数组样式

table，样式为{'chema': {schema}, 'data': {data}}，和records类似

```

**具体示例如下**
```python
# coding=utf-8
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import json
from pandas.io.json import json_normalize

df = pd.DataFrame([['a', 'b'], ['c', 'd']],
                   index=['row 1', 'row 2'],
                   columns=['col 1', 'col 2'])

print df.to_json(orient='split')

'''
{
"columns":["col 1","col 2"],
"index":["row 1","row 2"],
"data":[["a","b"],["c","d"]]
}

'''

# record, 一行划分数据
print df.to_json(orient='records')
'''
可以看到，实际是以“行”划分了数据

[
{"col 1":"a","col 2":"b"},
{"col 1":"c","col 2":"d"}
]

'''

# index，注意与 records方法结果的区别
print df.to_json(orient='index')
'''
{
"row 1":{"col 1":"a","col 2":"b"},
"row 2":{"col 1":"c","col 2":"d"}
}

'''

# columns, 注意与index方法的比对
print df.to_json(orient='columns')
'''
{
"col 1":{"row 1":"a","row 2":"c"},
"col 2":{"row 1":"b","row 2":"d"}
}
'''


# value, 只获取dataframe中的内容
print df.to_json(orient='values')
'''
[
["a","b"],
["c","d"]
]
'''

# table样式运行有误
print df.to_json(orient='table')

```

---
2017.09.28
