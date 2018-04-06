# Python 与 DNS

------

用Python进行DNS解析一般有两种方式：

* pip install pydns --- import DNS

* pip install dnspython  --- import dns.resolver

## DNS Response结构

![](http://ouzh4pejg.bkt.clouddn.com/DNSResponse.png)

要注意的是：不是所有DNS服务器都会返回Authority和Additonal信息

例如：114.114.114.114有时获取不到Additonal信息


## pydns 基础代码

```
import DNS

req_obj = DNS.Request()
# 请求×××记录
answer_obj = req_obj.req(name=main_domain, qtype=DNS.Type.××, server=server, timeout=20)
print answer_obj.answers
print answer_obj.authority
print answer_obj.additional
```

### 解释

* qtype是要请求的RR类型

* server是递归或权威NS服务器，域名或IP皆可

* timeout是超时时间

* answer_obj.answers，answer_obj.authority,answer_obj.answers.additional 是对应DNS相应包中的“应答信息”、“授权信息”和“额外信息”。

* 没有在文档或源码中找到预定义好捕获的异常

## dnspython 基本代码

* [官方文档](http://www.dnspython.org/docs/1.14.0/dns.resolver.Resolver-class.html)

```python
resolver = dns.resolver.Resolver(configure=False)
# 令configure=False,从而可以自定义设置ns服务器
resolver.nameservers = ['1.2.4.8']

try:
    # '×××' 是请求的资源记录类型
    resp = resolver.query(domain, '×××' )
    print resp.response.answer
    print resp.response.authority
    print resp.response.additional
    # 当要获取解析结果列表时，可以如下处理
    print [answer.to_text() for answer in resp.response.answer]
    '''
    [u'www.000080.com. 3600 IN CNAME fw.ename.net.']
    '''
except dns.resolver.NoAnswer, e:
    msg = 'Exception msg:NoAnswer'
except dns.resolver.NXDOMAIN, e:
   msg = 'Exception msg:NXDOMAIN'
except dns.resolver.NoNameservers, e:
    msg = 'Exception msg:NoNameservers'
except dns.resolver.Timeout, e:
    msg = 'Exception msg:Timeout'
except:
    msg = 'Exception msg:Unexcepted Errors'
```

### 解释

* 令configure=False从而自定义设置nameserver

* nameserver必须是**IP地址**

* resp.response.answer，resp.response.authority,resp.response.additional 是对应DNS相应包中的“应答信息”、“授权信息”和“额外信息”

* 根据官网文档给出的文档添加了异常处理

* 当请求A记录时，如果存在CNAME,则返回的列表中，会包含CNAME和A记录，这个没有细研究，先记录下来
```python
例如，向1.2.4.8请求www.baidu.com的A记录，返回结果是
[u'www.baidu.com. 541 IN CNAME www.a.shifen.com.', u'www.a.shifen.com. 129 IN A 220.181.111.188\nwww.a.shifen.com. 129 IN A 220.181.112.244']
可以看到先返回了CNAME，然后返回了A记录
```

* answer.to_text() for answer in resp.response.answer得到的列表元素，一般每个元素都是以空格分隔的字符串，从第5个子串起是所请求得到的核心内容

