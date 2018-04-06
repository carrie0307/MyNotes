# 关于TTL

------

TTL，即DNS资源记录在递归服务器中缓存的时间；在获取时会发现递归DNS和NS服务器都能获取到TTL值，但从递归DNS获取的TTL值是会变的，因此实际的TTL值应该都从NS服务器来获取；

## 以www.baidu.com的A记录为例：

* 向1.2.4.8(CNNIC递归DNS)请求
```python
import DNS
"""获取记录超时时间"""
timeout = 20
"""CNNIC DNS"""
server = '1.2.4.8'
req_obj = DNS.Request()
answer_obj = req_obj.req(name='www.baidu.com', qtype=DNS.Type.A, server=server, timeout=timeout)
for i in answer_obj.answers:
    	print i

第一次获取[Output]
{'name': 'www.baidu.com', 'data': 'www.a.shifen.com', 'typename': 'CNAME', 'classstr': 'IN', 'ttl': 1059, 'type': 5, 'class': 1, 'rdlength': 15}
{'name': 'www.a.shifen.com', 'data': '180.149.131.98', 'typename': 'A', 'classstr': 'IN', 'ttl': 186, 'type': 1, 'class': 1, 'rdlength': 4}
{'name': 'www.a.shifen.com', 'data': '180.149.132.151', 'typename': 'A', 'classstr': 'IN', 'ttl': 186, 'type': 1, 'class': 1, 'rdlength': 4}

第二次获取[Output]
{'name': 'www.baidu.com', 'data': 'www.a.shifen.com', 'typename': 'CNAME', 'classstr': 'IN', 'ttl': 1003, 'type': 5, 'class': 1, 'rdlength': 15}
{'name': 'www.a.shifen.com', 'data': '180.149.132.151', 'typename': 'A', 'classstr': 'IN', 'ttl': 61, 'type': 1, 'class': 1, 'rdlength': 4}
{'name': 'www.a.shifen.com', 'data': '180.149.131.98', 'typename': 'A', 'classstr': 'IN', 'ttl': 61, 'type': 1, 'class': 1, 'rdlength': 4}
```

**很明显可以看到TTL值在变**

* 向www.baidu.com的NS获取
```python

import DNS
"""获取记录超时时间"""
timeout = 20
"""阿里114DNS"""
server = '1.2.4.8'
req_obj = DNS.Request()
# 首先获取www.baidu.com的NS记录
answer_obj = req_obj.req(name='www.baidu.com', qtype=DNS.Type.NS, server=server, timeout=timeout)
for i in answer_obj.answers:
    	print i

"""
[Output]在此可以看到至获取到了www.baidu.com的CNAME记录，因此将fqdn再上推一级，对baidu.com获取NS
{'name': 'www.baidu.com', 'data': 'www.a.shifen.com', 'typename': 'CNAME', 'classstr': 'IN', 'ttl': 923, 'type': 5, 'class': 1, 'rdlength': 15}
 """  
 
answer_obj = req_obj.req(name='baidu.com', qtype=DNS.Type.NS, server=server, timeout=timeout)
for i in answer_obj.answers:
    	print i
"""    	
[Ouptupt]
{'name': 'baidu.com', 'data': 'ns2.baidu.com', 'typename': 'NS', 'classstr': 'IN', 'ttl': 15714, 'type': 2, 'class': 1, 'rdlength': 6}
{'name': 'baidu.com', 'data': 'ns7.baidu.com', 'typename': 'NS', 'classstr': 'IN', 'ttl': 15714, 'type': 2, 'class': 1, 'rdlength': 6}
{'name': 'baidu.com', 'data': 'ns3.baidu.com', 'typename': 'NS', 'classstr': 'IN', 'ttl': 15714, 'type': 2, 'class': 1, 'rdlength': 6}
{'name': 'baidu.com', 'data': 'ns4.baidu.com', 'typename': 'NS', 'classstr': 'IN', 'ttl': 15714, 'type': 2, 'class': 1, 'rdlength': 6}
{'name': 'baidu.com', 'data': 'dns.baidu.com', 'typename': 'NS', 'classstr': 'IN', 'ttl': 15714, 'type': 2, 'class': 1, 'rdlength': 6}

稍后如果在通过1.2.4.8获取NS,会发现其TTL值也是变的
"""

# 然后任选一个NS来获取A记录的TTL
"""
第一次获取[Output]
{'name': 'www.baidu.com', 'data': 'www.a.shifen.com', 'typename': 'CNAME', 'classstr': 'IN', 'ttl': 1200, 'type': 5, 'class': 1, 'rdlength': 15}

第二次获取[Output]
{'name': 'www.baidu.com', 'data': 'www.a.shifen.com', 'typename': 'CNAME', 'classstr': 'IN', 'ttl': 1200, 'type': 5, 'class': 1, 'rdlength': 15}

这里实际是通过NS服务器获得了www.baidu.com的CNAME(www.a.shifen.com)；如果要再进一步获取www.baidu.com，则需要先获取www.a.shifen.com的NS(思路同上获取www.baidu.com的NS),然后向其NS查询www.a.shifen.com的A记录；此时得到的就可以作为www.baidu.com的A记录
"""
```

## 总结

### TTL
* 向递归服务器请求所得的TTL值是会变的，因此要**向权威DNS去请求真实的TTL值**

### NS获取
当向某递归DNS获取某FQDN(eg. www.baidu.com)的NS记录时，如果获取不到，则将此域名向上推一级进行获取(eg. 对baidu.com进行获取);获取不到就以此类推，直到达到了顶级域；

### A记录获取
当向NS请求某FQDN(eg.www.baidu.com)的A记录时，如果获取到的是其CNAME,则接下来要先获取其CNAME的NS,然后向其NS请求A记录，将这个结果作为FQDN的A记录；

---

2018.01.24
