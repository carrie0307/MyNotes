#!/usr/bin/python
# encoding:utf-8
"""
DNS探测程序
"""
import socket
import select
import struct
import DNS
import random
import time
import datetime
import sys
sys.path.append('..')
from DNS import Lib
from DNS import Type
from DNS import Class
from DNS import Opcode
THREAD_NUM = ['1','50','100','200','300','350','400','450','500','550','600','700','800','900','1000']
TIMEOUT = 1
current_time = time.strftime("%Y%m%d%H%M", time.localtime())
fw_path = './DnsResult/' + \
        sys.argv[2] + '_' + current_time + '.txt'  # 输出结果文件
fw_name = fw_path
fw = open(fw_name, "a")  # 追加方式打开文件
# DNS type
# Authoritative Name server=1
# Authoritative Name server(with recursive service)=2
# The Recursive Name Server=3
# unknow =4

DNSSERVERTYPE = ["1", "2", "3", "4"]

def batch_server_detect(list_ip=[]):
    '''
    batch dns detect , each time sends 'num' packets
    '''

    # TID为随机数
    tid = random.randint(0, 65535)
    # 端口为53,UDP
    port = 53
    # 操作为查询
    opcode = Opcode.QUERY
    # Tpye类型为A
    qtype = Type.PTR
    # 查询类，一般为IN
    qclass = Class.IN
    # 期望递归
    rd = 1

    # 建立一个UDP套接字（SOCK_DGRAM，代表UDP，AF_INET表示IPv4）
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_port = random.randint(1024, 65535)
    # socket绑定到指定IP地址和接口上
    s.bind(('', source_port))
    ip_count = len(list_ip)
    count = 0
    result = []

    for ip in list_ip:
        server = ip
        m = Lib.Mpacker()
        m.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)
        ip_tips = server.split(".")
        qname = ip_tips[3] + '.' + ip_tips[2] + \
             '.' + ip_tips[1] + '.' + ip_tips[0]
        qname += '.in-addr.arpa'
        m.addQuestion(qname, qtype, qclass)
        request = m.getbuf()
        try:
            a = s.sendto(request, (server, port))
            print a, "send to IP:", server
        except socket.error, reason:
            print reason

    while s:
        try:
            r, w, e = select.select([s], [], [], TIMEOUT)
            if not len(r):
                break
            (reply, from_address) = s.recvfrom(65535)
            u = Lib.Munpacker(reply)
            r = Lib.DnsResult(u, {})
            if r.header['ra'] == 1 and r.header['aa'] == 0:
                print from_address, "递归服务器"
                result.append(from_address[0])
            elif r.header['ra'] == 1 and r.header['aa'] == 1:
                print from_address, "权威服务器(递归服务)"
                result.append(from_address[0])
            else:
                pass
        except socket.error, reason:
            print reason

        except DNS.Error as e:
            print e
    fw.write('**********'+str(len(result))+'**********'+'\n')
    result=[]
    ips = []

"""将结果存入到文件中"""



"""Demo"""


def main():

    starttime = datetime.datetime.now()
    dns_count = 0
    fr_path = './IpSource/' + sys.argv[1]  # 输入文件
    
    fr = open(fr_path, 'r')
    fw_name = fw_path
    fo = open('./DnsResult/' + 'Run.log', 'a')  # 运行日志文件

    ip_list = fr.readlines()
    print ip_list[0]
    list_ip=[]
    for j in range(0,len(THREAD_NUM)):
    	fw.write('Sent package num :'+ str(THREAD_NUM[j])) 
    	for i in range(0,int(THREAD_NUM[j])):
    		list_ip.append(ip_list[i])
    	batch_server_detect(list_ip)  # 探测ip段
    	list_ip=[]
    endtime = datetime.datetime.now()
    print 'Dns detect finished'
    print '探测结果文件：' + sys.argv[2] + '_' + current_time + '.txt'
    print >> fo, '探测结果文件：' + sys.argv[2] + '_' + current_time  + '.txt'
    print '程序开始运行时间:' + str(starttime)
    print >>fo, '程序开始运行时间:' + str(starttime)
    print '程序结束运行时间:' + str(endtime)
    print >>fo, '程序结束运行时间:' + str(endtime)
    print '程序运行时间(seconds)：' + str((endtime - starttime).seconds)
    print >>fo,  '程序运行时间(seconds)：' + str((endtime - starttime).seconds)
    print '程序运行时间(minutes)：' + str(round((endtime - starttime).seconds / 60.0, 2))
    print >>fo,  '程序运行时间(minutes)：' + \
        str(round((endtime - starttime).seconds / 60.0, 2))
    print >>fo, '------------------------------------------------------------------------------------------------'
    fo.close()

if __name__ == '__main__':
    main()
