#!/usr/bin/python
# encoding:utf-8
"""
DNS探测程序
"""
import config
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

THREAD_NUM = config.THREAD_NUM
TIMEOUT = config.TIMEOUT

# DNS type
# Authoritative Name server=1
# Authoritative Name server(with recursive service)=2
# The Recursive Name Server=3
# unknow =4

DNSSERVERTYPE = ["1", "2", "3", "4"]


def ip2long(ipstr):
    """
    Ip turn to long
    """
    return struct.unpack("!I", socket.inet_aton(ipstr))[0]


def long2ip(ip):
    """
    long turn to Ip
    """
    return socket.inet_ntoa(struct.pack("!I", ip))


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

    while count * THREAD_NUM < ip_count:
        ips = list_ip[count * THREAD_NUM: (count + 1) * THREAD_NUM]

        for ip in ips:
            server = ip #long2ip(ip)
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
                #print a, "send to IP:", server
            except socket.error, reason:
                print reason

        while 1:
            try:
                r, w, e = select.select([s], [], [], TIMEOUT)
                if not len(r):
                    break
                (reply, from_address) = s.recvfrom(65535)
                u = Lib.Munpacker(reply)
                r = Lib.DnsResult(u, {})
                if r.header['ra'] == 1 and r.header['aa'] == 0:
                    print from_address, "递归服务器"
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[2], 'other': r.header['status']})
                elif r.header['ra'] == 1 and r.header['aa'] == 1:
                    print from_address, "权威服务器(递归服务)"
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[1], 'other': r.header['status']})
                elif r.header['ra'] == 0 and r.header['aa'] == 1:
                    print from_address, "权威服务器"
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[0], 'other': r.header['status']})
                else:
                    print from_address, "服务器类型探测失败：未知服务器", r.header['status']
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[3], 'other': r.header['status']})

            except socket.error, reason:
                print reason

            except DNS.Error as e:
                print e

        ips = []
        count = count + 1
    s.close()
    return result

"""将结果存入到文件中"""


def main():
    results =[]
    list_ip  =  ['8.8.8.8']
    results = batch_server_detect(list_ip)  # 探测ip段

    for re in results:
        print re

if __name__ == '__main__':
    main()
