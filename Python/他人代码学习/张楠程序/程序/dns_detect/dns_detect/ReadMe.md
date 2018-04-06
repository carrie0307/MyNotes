#### 一，项目文件介绍
	1、DNS为库文件
	2、IpSource存放输入文件
	3、DnsResult存放探测结果
	4、config.py为配置文件
	5、mul_detector.py为程序运行文件
	6、ReadMe.md为项目简介

#### 二，程序功能
	通过组包发送DNS查询报文，判断所探测IP是否为DNS服务器

#### 三，输入数据
	1、输入文件格式为txt文件，在IpSource文件夹中
	2、程序通过读入IP段进行探测
	3、数据格式如下：
	      121.12.0.0 
	      121.13.255.255
	      ......
	4、其中config.py配置文件，用来配置程序每次发包次数以及超时时间，默认每次发包5000,超时时间为3秒

#### 四，输出数据
	输出结果文件保存在DnsResult文件夹中，其中有两类文件
	1、.txt文件为探测结果文件，包含是DNS服务器的数据
	2、Run.log文件，保存本次探测详细，包括运行时间，探测DNS个数，IP个数等信息

#### 五，运行环境
	1、运行环境Linux,python2.7即可
	2、运行mul\_detector.py  运行命令：python mul_detector.py input.txt output
	其中，input.txt为输入文件（保存在IpSource中），输出文件为output_***.txt（保存在DnsResult中）,其中***为程序运行时间，会自动添加
	3、运行dnsDetectTwice.py，该程序两次探测某个IP段，与单次运行进行比较

####筛选出DNS递归服务器
输入文件为txt格式，文件为dns_detect的输出文件
输出文件为txt格式，文件内容为DNS递归服务器
运行:python dns_recursion.py new_shandong_201603011023.txt ip_shandong.txt
其中new_shandong_201603011023.txt为输入文件，ip_shandong.txt为输出文件