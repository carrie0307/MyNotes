# urllib2相关整理

本文内容参考整理自如下几篇：

[爬虫养成记-urllib2的调试和处理](https://segmentfault.com/a/1190000008226223)</br>

[Python爬虫入门 系列文章](http://python.jobbole.com/81332/)

[cookielib和urllib2模块相结合模拟网站登录](http://www.cnblogs.com/sysu-blackbear/p/3629770.html)

## 构造Requests
urlopen参数可以传入一个request请求,它其实就是一个Request类的实例，构造时需要传入Url,Data等等的内容。代码可以如下：
```python
import urllib2
 
request = urllib2.Request("http://www.baidu.com")
response = urllib2.urlopen(request)
print response.read()
```
推荐这样写，可以在构建请求时还需要加入好多内容；</br>
通过构建一个request，服务器响应请求得到应答，这样显得逻辑上清晰明确。

**增加headers**:
```python
import urllib  
import urllib2  
 
url = 'http://www.server.com/login'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
values = {'username' : 'cqc',  'password' : 'XXXX' }  
headers = { 'User-Agent' : user_agent }  
data = urllib.urlencode(values)  
request = urllib2.Request(url, data, headers)  
response = urllib2.urlopen(request)  
page = response.read()
```

#### POST
传送data，代码如下:
```python
import urllib
import urllib2

# 定义一个字典，名字为values,设置了username和 password
values = {"username":"1016903103@qq.com","password":"XXXX"}

# 用urllib的urlencode方法将字典编码，命名为data,以便传入request的参数
data = urllib.urlencode(values) 

url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
request = urllib2.Request(url,data)
response = urllib2.urlopen(request)
print response.read()
```

#### GET
GET方式可以直接把参数写到网址上面，直接构建一个带参数的URL出来即可,代码如下:
```python
import urllib
import urllib2

values={}
values['username'] = "1016903103@qq.com"
values['password']="XXXX"
data = urllib.urlencode(values) 
url = "http://passport.csdn.net/account/login"
geturl = url + "?"+data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
print response.read()
```
如果`print geturl`，打印输出一下url，就能够发现输出是原的url加？以及编码后的参数的结果
```
http://passport.csdn.net/account/login?username=1016903103%40qq.com&password=XXXX
```

## 设置Proxy

用代码([来源](http://www.cnblogs.com/BigFishFly/p/6337136.html))说明用法：
```python
import urllib2

proxy_handler=urllib2.ProxyHandler({'http':'http://username:password@proxyhk.huawei.com:8080', 'https':'https:// username:password @proxyhk.huawei.com:8080'})

opener=urllib2.build_opener(proxy_handler)

# 安装不同的opener对象作为urlopen()使用的全局opene
urllib2.install_opener(opener)

req=urllib2.Request('http://www.baidu.com/')
conn=urllib2.urlopen(req)
print conn.read()

```

## Cookie相关
**方法一**：

代码([摘自](http://www.cnblogs.com/sysu-blackbear/p/3629770.html))如下：
```python
#!/usr/bin/env python
#-*-coding:utf-8-*-

import urllib
import urllib2
import cookielib

#获取Cookiejar对象（存在本机的cookie消息）
cj = cookielib.CookieJar()

#自定义opener,并将opener跟CookieJar对象绑定
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#安装opener,此后调用urlopen()时都会使用安装过的opener对象
urllib2.install_opener(opener)

url = "http://www.baidu.com"   
urllib2.urlopen(url)

```

**方法二**：

* 具体参见[Python爬虫入门（6）：Cookie的使用](http://python.jobbole.com/81344/)

* 根据一些积累，HTTPError 302可通过cookie解决



## urllib2的超时处理
**方法一: 直接设置timeout**
```python
import urllib2

response = urllib2.urlopen(url, timeout=10)
```
**方法二:全局socket设置**
```python
import urllib2
import socket
socket.setdefaulttimeout(5) 

response = urllib2.urlopen(url)
```

## urllib2异常处理
由于在一次信息获取中需要对获取情况进行较为细致的区分，因此记录此文

#### HTTPError & URLError
**URLError**

* 网络无连接，即本机无法上网
* 连接不到特定的服务器
* 服务器不存在

eg. 访问一个完全不存在的网址会出现URLError

**HTTPError**

* HTTPError是URLError的子类。用于处理Http相关的错误。

* HTTPError除了reson属性外还有code属性，即对应的状态码。

**对二者进行捕获时，由于HTTPError是URLError的子类，因此在捕获Exception的时候需要将子类放在前面避免Exception先被父类捕获**

如下是自己写的一段代码：
```python
try:
    response = urllib2.urlopen(url, timeout=2)
    res_q.put([ID, response.code])
except urllib2.HTTPError, e:
    res_q.put([ID, e.code])
except urllib2.URLError, e:
    print e.reason
    if str(e.reason) == 'timed out':
        res_q.put([ID, -2])
    else:
        res_q.put([ID, -3])
except:
    res_q.put([ID, -4]) # -4表示请求有误

```

## 解压/解码处理

urllib2获取响应可能存在压缩包问题，在此处理；同时处理编码问题

```python

req = urllib2.urlopen(url)

def decode_str(self,response):
    """
    对获取到的信息进行解码(包括解压，解压后才可以解码)
    """
    try:
        page_source = response.read()
        # print page_source
    except Exception,e:
        print '{0}:{1}'.format('parse error',e)
        return None
    information = response.info()
    encode_type = information.getheader('Content-Encoding')
    if encode_type == 'gzip':
        buf = StringIO(page_source)
        gf = gzip.GzipFile(fileobj=buf)
        page_source = gf.read()
    else:
        encode_type = chardet.detect(page_source)['encoding']
        if encode_type:
            self.info['encode_type'] = encode_type
            decode_type = self.select_decode_type(encode_type)
            page_source = page_source.decode(decode_type, 'ignore')

    return page_source


def select_decode_type(self,encode_type):
    ''' 
    被decode_str()调用
    '''
    if encode_type.find('utf-8')!=-1 or encode_type.find('UTF-8')!=-1 :
        decode_type = 'utf-8'
    elif encode_type.find('UTF-16')!=-1 :
        decode_type = 'utf-16'
    elif encode_type in ['GB2312','gb2312','gbk','GBK','GB18030','gb18030']:
        decode_type = 'gb18030'
    else:
        decode_type = encode_type

    return decode_type

```

## 使用DebugLog
可以通过下面的方法把 Debug Log打开，这样收发包的内容就会在屏幕上打印出来，方便调试.这个也不太常用，仅提一下。

```python
import urllib2
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://www.baidu.com')
```

运行结果如下
![](http://ouzh4pejg.bkt.clouddn.com/urllib-log.png)

---
2017.08.28

