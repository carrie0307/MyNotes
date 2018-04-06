# Python中IPy模块的基本使用

------

直接通过代码来说明

```python

#coding=utf-8
'''
Python中P地址处理模块IPy的学习
'''
import IPy


'''区分出IPv4和IPv6'''
print IPy.IP('10.0.0.0/8').version()
print IPy.IP('::1').version()

'''输出指定的网段的IP个数和所有的IP地址清单'''
# ip = IPy.IP('192.168.0.0/16')
# print ip.len()
# for x in ip:
#     print x


'''反向解析名称、ip类型转换等'''
ip = IPy.IP('192.168.1.20')
print ip.reverseNames()               #反向解析地址格式
# ['20.1.168.192.in-addr.arpa.']
print ip.iptype()                     #私网类型
# 'PRIVATE'
print IPy.IP('8.8.8.8').iptype()          #公网类型
# 'PUBLIC'
print IPy.IP('8.8.8.8').int()             #转换为整型格式
# 134744072
print IPy.IP('8.8.8.8').strHex()          #转换为十六进制格式
# '0x8080808'
print IPy.IP('8.8.8.8').strBin()          #转换成二进制格式
# '00001000000010000000100000001000'
print IPy.IP('0x8080808')           #十六进制转换为IP格式
# 8.8.8.8
print IPy.IP(134744072)             #整型格式转换为IP格式
# 8.8.8.8

'''IP方法也支持网络地址的转换，例如根据IP和掩码产生网段格式'''

print IPy.IP('192.168.1.0').make_net('255.255.255.0')
# 192.168.1.0/24
print IPy.IP('192.168.1.0/255.255.255.0',make_net=True)
# 192.168.1.0/24
print IPy.IP('192.168.1.0-192.168.1.255',make_net=True)
# 192.168.1.0/24


'''通过strNormal方法指定不同wantprefixlen参数值以定制不同输出类型的网段，输出类型为字符串'''
print IPy.IP('192.168.1.0/24').strNormal(0)   #无返回
# '192.168.1.0'
print IPy.IP('192.168.1.0/24').strNormal(1)   #prefix格式
# '192.168.1.0/24'
print IPy.IP('192.168.1.0/24').strNormal(2)   #decimalnetmask格式
# '192.168.1.0/255.255.255.0'
print IPy.IP('192.168.1.0/24').strNormal(3)   #lastIP格式
# '192.168.1.0-192.168.1.255'


'''比较IP大小'''
print IPy.IP('10.0.0.0/24') < IPy.IP('12.0.0.0/24')
# True

'''判断IP地址和网段是否包含于另一个网段中'''

'192.168.1.100' in IPy.IP('192.168.1.0/24')
# True
IPy.IP('192.168.1.0/24') in IP('192.168.0.0/16')
# True

'''判断两个网段是否存在重叠（overlaps方法）'''
IPy.IP('192.168.0.0/23').overlaps('192.168.1.0/24')
# 1
IPy.IP('192.168.1.0/24').overlaps('192.168.2.0/24')
# 0

```
