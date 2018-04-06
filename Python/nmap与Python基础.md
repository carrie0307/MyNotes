# NMAP与Python 

------
通过python中的nmap扫描端口，这里简单记录一下基本代码，并将结果的含义进行记录;实际看到扫描方式、类型有很多，以后再补充吧。


## NMAP基本参数

[Nmap参数详解](https://zhuanlan.zhihu.com/p/25612351)

* 列举出几个重要的：
    * -F 对nmap-services文件中列举的默认端口进行扫描
        * [nmap-services](https://svn.nmap.org/nmap/nmap-services)
        * [nmap版本和服务探测](https://nmap.org/man/zh/man-version-detection.html))

    *  -sV ： 开放版本探测，可以直接使用 -A  同时打开 操作系统探测和版本探测 
    
    * -O: 启用操作系统检测，-A 来同时启用操作系统检测和版本检测
    
    * -A ：OS 识别,版本探测,脚本扫描和 traceroute 
    
## 扫描方式说明

* [nmap扫描方式](https://vxhly.github.io/2016/09/usage-of-nmap/)

* -sT TCP 连接扫描（s ==> 哪种类型扫描；T ==> TCP 类型）
端口扫描中最稳定的，利用的是 TCP 三次握手。TCP 扫描通常用于收集有关目标的更多信息，但是会和目标主机建立一个完成的 TCP 连接。

* -sS SYN 连接扫描（s ==> 哪种类型扫描；S ==> SYN 类型）
TCP 两次握手（隐藏扫描，速度快，nmap 缺省参数）

* -sA ACK 连接扫描（s ==> 哪种类型扫描；A ==> ACK 类型）
ACK 扫描，用于确定 TCP 端口是否被防火墙过滤

* -sU UDP 连接扫描（s ==> 哪种类型扫描；U ==> UDP 类型）

    * -sV UDP 扫描中添加版本扫描信息（V ==> 版本信息）

    * 不存在 -Pn 参数（从 UDP 协议去理解，你发了就 ok 管他收没收到）

* 扫描 IP 段
    

## 基本代码
```python
#-*- coding:utf-8 -*-
"""
    nmap扫描获取主机与80,443端口状态
    学习：http://xiaix.me/python-nmapxiang-jie/
          http://www.tianfeiyu.com/?p=1360
          nmap结果含义： https://www.jianshu.com/p/069c2cee75b0
          nmap,zmap,masscan比较 http://www.freebuf.com/sectool/119340.html
         nmap入门精讲 http://www.cnblogs.com/st-leslie/p/5115280.html
    默认是tcp方式扫描
"""
import nmap # 导入 nmap.py 模块
import datetime


'''
baidu.com   111.13.101.208
520820.com  192.5.6.30
365635.com  112.121.172.146

nm = nmap.PortScanner()
nm.scan(hosts,22,25,80)
# nm.scan(hosts, ports, args)  eg.nm.scan(host,22-443,'-Pn -A')
'''

def get_nmap_state(ip):
    """
    核心函数
    param ip:要扫描的ip
    """
    ip_info = {}
    nm = nmap.PortScanner()
    res = nm.scan(ip,parts = '80,443',arguments='-A -Pn')
    # 源码中默认argument是Sv；
    if res['scan']:
        ip_info['state'] = res['scan'][ip]['status']['state']
        for port in res['scan'][ip]['tcp']:
            ip_info['state'+str(port)] = res['scan'][ip]['tcp'][port]['state']
    ip_info['state_insert_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return ip_info


if __name__ == '__main__':
    ip = '103.35.149.52'
    # ip = '1.2.4.8'
    print get_nmap_state(ip)

```

## 结果解释

|状态|说明|
|:--:|:--:|
|Open|端口开启，数据有到达主机，有程序在端口上监控|
|Closed|端口关闭，数据有到达注册，没有程序在端口上监控|
|Filtered|数据没有到达主机，返回结果为空，数据被防火墙或IDS过滤|
|Unfiltered|数据有到达主机，但是不能识别端口当前状态|
|Open\|Filtered|端口没有返回值，主要发生在UDP,IP,FIN,NULL和Xmas扫描中|
|Closed\|Filtered|只发生在IP ID idle扫描|



---

2018.01.24

