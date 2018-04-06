# 本机全部出口ip

------

这个问题的本源是，想探究在校园局域网中，每次向外部请求时的出口ip是否相同？尤其是在**直接使用socket连接的情况下**。但是socket通过getaddrinfo(gethostname(),None)每次获得的都是127.0.0.1，后来在网上找到了几个方法，先记录一下。

## Python访问外部网站获取

直接上代码

```python
# coding:utf-8
'''
	通过连续向http://city.ip138.com/ip2city.asp提取网页上显示的本机的出口ip
'''

import re,urllib2


class Getmyip:
        
    def getip(self):
    	i = 0
        while True:
            if i > 10:
                break
            try:
                myip = self.visit("http://city.ip138.com/ip2city.asp")
                print str(i) + ':' + myip
                i += 1
            except:
                continue
    
    def visit(self, url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            string = opener.read()
        return re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',string).group(0)

getmyip = Getmyip()
localip = getmyip.getip()

```

## curl获取

通过一下几个网址来获取

* ip.cn
* ipinfo.io
* cip.cc
* ifconfig.me
* myip.ipip.net

```shell

# 通过ip.cn查询
curl ip.cn

# 通过cip.cc查询
curl cip.cc

# 通过myip.ipip.net查询
curl myip.ipip.net

# 通过config.me查询
curl ifconfig.me
# ifconfig.me官网列出了一些参数，根据参数不同查询内容不同，例如ifconfig.me/ua 查询UA,ifconfig.me/port 查询端口，ifconfig.me/all可以查询全部的内容

# 通过http://members.3322.org/dyndns/getip查询
curl http://members.3322.org/dyndns/getip

```


