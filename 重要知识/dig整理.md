#　Dig命令解析
---

## Dig

#### 基本含义
dig是linux中的**域名解析工具**，是**domain information groper**的缩写，知道了来源想必大家也就容易记住这条命令了。

#### dig的基本的命令格式
**dig @dnsserver name querytype**
如果没有设置@dnsserver，那么dig就会依次使用/etc/resolv.conf里的地址作为上连DNS服务器

#### 常用参数说明
* +trace 从根域查询一直跟踪直到查询到最终结果，并将整个过程信息输出出来
```
dig +trace www.baidu.com a
查询百度A记录
```
* +nocmd 可以节省输出dig版本信息
```
dig +nocmd www.baidu.com
```
* +short 仅会输出最精简的CNAME信息和A记录
```
dig +short www.baidu.com
```


---

以上内容参考整理自[dig挖出DNS的命令](http://roclinux.cn/?p=2449)


2017.09.30

