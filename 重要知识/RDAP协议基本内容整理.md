# RDAP协议概要整理

### 协议名称

Registration Data Access Protocol, 注册数据访问协议，是“下一代的WHOIS协议”。

### 提出

2012年5月，CNNIC联合ICANN、Verisign等国际机构，针对现有协议暴露出缺乏国际化支持机制、缺乏数据扩展机制、缺乏安全隐私保护机制等诸多问题而成立专项工作组，推动制订下一代WHOIS协议。

### 相关文档： 

* RFC 7480 - 注册数据访问协议（RDAP）中的HTTP使用

* RFC 7481 - 注册数据访问协议（RDAP）的安全服务

* RFC 7482 - 注册数据访问协议（RDAP）查询格式

* RFC 7483 - 注册数据访问协议（RDAP）的JSON响应

* RFC 7484 - 查找权威注册数据（RDAP）服务

* RFC 7485 - WHOIS注册对象的清单和分析

* 请求方法： HTTP GET / HTTP HEAD

* 返回数据格式： JSON

## 响应情况：

* HTTP 200： 服务器拥有被请求对象信息且正常返回，此时可以获取到Json的注册数据；

* HTTP 3**(重定向)： 当服务器希望通知客户在其他地方找到给定的查询答案，则会返回HTTP301,HTTP302,HTTP303或HTTP307.

* HTTP 4**: 如果服务器返回一个空的结果集或其他否定性信息，则返回HTTP 404;当服务器由于速率限制拒绝回答查询时，它将返回[RFC6585]中所述的429（太多请求）响应代码；如果一个服务器希望通知客户有关信息查询可用，但不能包含该信息响应客户的政策原因，则回应在HTTP的4xx范围内提供适当的响应码。

## 基于RDAP的IP WHOIS请求格式与实例：

* APNIC：

    * 格式：http://rdap.apnic.net/ip/{ip}

    * 实例：http://rdap.apnic.net/ip/111.13.101.208
    * [APNIC关于RDAP相关说明](https://www.apnic.net/about-apnic/whois_search/about/rdap/)
    
* ARIN

    * 格式：http://rdap.arin.net/registry/ip/{ip}

    * 实例：http://rdap.arin.net/registry/ip/172.217.160.110

    * [ARIN关于RDAP相关说明](https://www.arin.net/resources/rdap.html)

* LACNIC:

    * 格式： https://rdap.lacnic.net/rdap/ip/{ip}

    * 实例：https://rdap.lacnic.net/rdap/ip/200.3.14.184 

* AFRINIC:

    * 格式：http://rdap.afrinic.net/rdap/ip/{ip}

    * 实例：http://rdap.afrinic.net/rdap/ip/196.216.2.6   

* RIPE:

    * 格式：http://rdap.db.ripe.net/ip/{ip}

    * 实例：http://rdap.db.ripe.net/ip/51.101.128.81

