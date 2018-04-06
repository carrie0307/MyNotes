# DNS基础整理Ⅱ

------

## 资源记录
* A
* NS
* CNAME：别名，一个有趣的解释:让张三住到李四家里，这时张三李四是同一个地址
* PTR
* MX
* SOA(起始授权机构):表明了DNS服务器之间的关系。SOA记录表明了谁是这个区域的所有者
```
比如51CTO.COM这个区域。一个DNS服务器安装后，需要创建一个区域，以后这个区域的查询解析，都是通过DNS服务器来完成的。现在来说一下所有者，我这里所说的所有者，就是谁对这个区域有修改权利。常见的DNS服务器只能创建一个标准区域，然后可以创建很多个辅助区域。标准区域是可以读写修改的。而辅助区域只能通过标准区域复制来完成，不能在辅助区域中进行修改。而创建标准区域的DNS就会有SOA记录，或者准确说SOA记录中的主机地址一定是这个标准区域的服务器IP地址。

上文摘自 SOA记录和NS记录的通俗理解 http://bbs.51cto.com/thread-908637-1.html
```
* SRV:记录了哪台计算机提供了哪个服务这么一个简单的信息
```
if you have two Web servers in your domain, you can create SRV resource records specifying which hosts serve as Web servers, and resolvers can then retrieve all the SRV resource records for the Web servers.
```

* AAAA: ipv6记录

* TXT:域名的附加文本信息，最常用的是格式，主要用途是反垃圾邮件


* 参考

[https://technet.microsoft.com/en-us/library/cc958958.aspx](https://technet.microsoft.com/en-us/library/cc958958.aspx)

[DNS A CNAME PTR SOA 有什么区别](http://www.diantansuo.com/what-is-different-dns-record-types?utm_source=qq&utm_medium=social)

[DNS标准资源记录](https://caibaoz.com/blog/2013/01/02/dns-standard-resource-records/)

## .zone文件
* ZONE文件是DNS上保存域名配置的文件,存在于权威DNS上

* 区域文件是**名称服务器**存储其**所知道的域名的信息**的方式。名称服务器知道的每个域名都存储在区域文件中。对于名称服务器来说，大多数请求都不能在它自己服务器中找到区域文件。

* 如果它被配置成可以递归查询，如解析名称服务器，那它会递归找到结果并返回。否则，它会告诉请求者方下一步到哪里查询。

* 名称服务器具有的区域文件越多，它能够权威回答的请求越多

* zonefile 截图
参考自“[文献-Passive DNS系统的实现与应用研究，北京邮电大学，侯勇]中有区域文件的示例”

![](http://ouzh4pejg.bkt.clouddn.com/zone-file.png)

* 参考

    [https://zhuanlan.zhihu.com/p/25925357](https://zhuanlan.zhihu.com/p/25925357)

    [DNS扫盲系列之四:域名迁移和域名配置ZONE文件](http://www.itts-union.com/2990.html)
    
    [文献-Passive DNS系统的实现与应用研究，北京邮电大学，侯勇]中有区域文件的示例


