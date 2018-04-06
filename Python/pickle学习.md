# Python pickle模块

------

## 解释

* From: https://www.cnblogs.com/pzxbc/archive/2012/03/18/2404715.html
　　
python的pickle模块实现了基本的**数据序列和反序列化**。通过pickle模块的序列化操作我们能够将程序中运行的对象信息保存到文件中去，**永久存储**；通过pickle模块的反序列化操作，我们能够从文件中创建上一次程序保存的对象。

* 自己理解的解释

假设现在遍历某个列表，需要对每个元素进行一次操作，该操作都**需要依赖某种关系**，因此我们想到将**该关系存储下来，这样对每个元素操作时，直接读取调用即可。**

## 示例

* 假设当前有各省名称对应文件locate.txt如下：

```
渝 重庆 重庆市
宁 银川 宁夏回族自治区
贵 贵阳 贵州省
台 台北 台湾省
澳 澳门 澳门特别行政区
川 成都 四川省
皖 合肥 安徽省
鲁 济南 山东省
冀 石家庄 河北省
青 西宁 青海省
沪 上海 上海市
辽 沈阳 辽宁省
粤 广州 广东省
陕 西安 陕西省
港 香港 香港特别行政区
津 天津 天津市
吉 长春 吉林省
滇 昆明 云南省
鄂 武汉 湖北省
藏 拉萨 西藏自治区
赣 南昌 江西省
晋 太原 山西省
浙 杭州 浙江省
琼 海口 海南省
桂 南宁 广西壮族自治区
黑 哈尔滨 黑龙江省
苏 南京 江苏省
黔 贵阳 贵州省
闽 福州 福建省
新 乌鲁木齐 新疆维吾尔自治区
云 昆明 云南省
蒙 呼和浩特 内蒙古自治区
京 北京 北京市
蜀 成都 四川省
豫 郑州 河南省
甘 兰州 甘肃省
湘 长沙 湖南省
```

要实现icp地理位置转换，则需要建立如下关系

```python
{"渝": {"province": "重庆市", "main_pos": "重庆"}, "宁": {"province": "宁夏回族自治区", "main_pos": "银川"}, "贵": {"province": "贵州省", "main_pos": "贵阳"}, "台": {"province": "台湾省", "main_pos": "台北"}, "澳": {"province": "澳门特别行政区", "main_pos": "澳门"}, "川": {"province": "四川省", "main_pos": "成都"}, "皖": {"province": "安徽省", "main_pos": "合肥"}, "鲁": {"province": "山东省", "main_pos": "济南"}, "冀": {"province": "河北省", "main_pos": "石家庄"}, "青": {"province": "青海省", "main_pos": "西宁"}, "沪": {"province": "上海市", "main_pos": "上海"}, "辽": {"province": "辽宁省", "main_pos": "沈阳"}, "粤": {"province": "广东省", "main_pos": "广州"}, "陕": {"province": "陕西省", "main_pos": "西安"}, "港": {"province": "香港特别行政区", "main_pos": "香港"}, "津": {"province": "天津市", "main_pos": "天津"}, "吉": {"province": "吉林省", "main_pos": "长春"}, "滇": {"province": "云南省", "main_pos": "昆明"}, "鄂": {"province": "湖北省", "main_pos": "武汉"}, "藏": {"province": "西藏自治区", "main_pos": "拉萨"}, "赣": {"province": "江西省", "main_pos": "南昌"}, "晋": {"province": "山西省", "main_pos": "太原"}, "浙": {"province": "浙江省", "main_pos": "杭州"}, "琼": {"province": "海南省", "main_pos": "海口"}, "桂": {"province": "广西壮族自治区", "main_pos": "南宁"}, "黑": {"province": "黑龙江省", "main_pos": "哈尔滨"}, "苏": {"province": "江苏省", "main_pos": "南京"}, "黔": {"province": "贵州省", "main_pos": "贵阳"}, "闽": {"province": "福建省", "main_pos": "福州"}, "新": {"province": "新疆维吾尔自治区", "main_pos": "乌鲁木齐"}, "云": {"province": "云南省", "main_pos": "昆明"}, "蒙": {"province": "内蒙古自治区", "main_pos": "呼和浩特"}, "京": {"province": "北京市", "main_pos": "北京"}, "蜀": {"province": "四川省", "main_pos": "成都"}, "豫": {"province": "河南省", "main_pos": "郑州"}, "甘": {"province": "甘肃省", "main_pos": "兰州"}, "湘": {"province": "湖南省", "main_pos": "长沙"}}
```

每次建立以上关系很麻烦，因此我们将以上关系编码后保存下来

* pickle.dump(obj, file, [,protocol])
默认协议是0，这里先不讨论，具体需要时再查吧

* 示例代码

```python

'''建立关系的操作'''
# 假设以上关系保存在字典data_relationship中
data_relationship

# 将以上关系写入data.pkl文件(写入后打开data.pkl是已序列化后的内容)
output = open('data.pkl', 'wb')
pickle.dump(data_relationship, output)
output.close()
'''
另一种写法
with open('data.pkl', 'wb') as f:
    data_relationship = pickle.dump(data_relationshi,f)
'''

# 这样只要一次读取出关系即可，省略了每次建立关系的麻烦；
```

一次完成关系的保存后，以后直接读取data.pkl即可获得关系

```python

# 读出以上关系(读出的是已反序列化后的内容，输出data_relationship即是以上字典)
pkl_file = open('data.pkl', 'rb')
data_relationship = pickle.load(pkl_file)
'''
另一种写法
with open('data.pkl', 'rb') as f:
    data_relationship = pickle.load(f)
```


