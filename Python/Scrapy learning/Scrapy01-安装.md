# Scrapy01-安装
---


## 安装scrapy

* 我的测试环境是ubuntu15.04, Python2.7

**根据查资料以及[参考](https://github.com/yidao620c/scrapy-cookbook/blob/master/source/scrapy-01.md),安装主要包括以下**


先安装一些依赖软件
```
yum install python-devel
yum install libffi-devel
yum install openssl-devel
```

然后安装pyopenssl库
```
pip install pyopenssl
```

安装xlml
```
yum install python-lxml
yum install libxml2-devel
yum install libxslt-devel
```

安装service-identity
```
pip install service-identity
```

安装twisted
```
pip install scrapy
```

安装scrapy
```
pip install scrapy -U
```

测试scrapy
```
scrapy bench
```

实际我在安装时，只运行了sudo pip install scrapy，应该是其他依赖库等，在平时都已经安装好了的缘故。

**2017.8.23**
