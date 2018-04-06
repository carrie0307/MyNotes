# NMAP扫描结果

------

通过python中的nmap扫描端口，这里简单记录一下基本代码，并将结果的含义进行记录;实际看到扫描方式、类型有很多，以后再补充吧。

## 基本代码
```python
#-*- coding:utf-8 -*-
"""
    nmap扫描获取主机与80,443端口状态
    学习：http://xiaix.me/python-nmapxiang-jie/
         http://www.tianfeiyu.com/?p=1360
"""
import nmap # 导入 nmap.py 模块
import datetime


'''
baidu.com   111.13.101.208
520820.com  192.5.6.30
365635.com  112.121.172.146
'''

def get_nmap_state(ip):
    """
    核心函数
    param ip:要扫描的ip
    return ip_info={state:主机状态，state80:80端口状态，state443:443端口状态,'status_insert_time':状态探测时间}
    注意：当扫描结果没有scan字段时，返回{'state80': '0', 'state': '0', 'state443': '0'}
    """
    ip_info = {}
    ip_info = {'state80': '0', 'state': '0', 'state443': '0'}
    nm = nmap.PortScanner()
    res = nm.scan(ip,'80,443')
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

