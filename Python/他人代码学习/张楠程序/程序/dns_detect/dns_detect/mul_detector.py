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
            server = long2ip(ip)
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
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[2], 'other': r.header['status']})
                elif r.header['ra'] == 1 and r.header['aa'] == 1:
                    print from_address, "权威服务器(递归服务)"
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[1], 'other': r.header['status']})
                else:
                    pass
                '''elif r.header['ra'] == 0 and r.header['aa'] == 1:
                    print from_address, "权威服务器"
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[0], 'other': r.header['status']})
                else:
                    print from_address, "服务器类型探测失败：未知服务器", r.header['status']
                    result.append(
                        {'ip': from_address[0], 'type': DNSSERVERTYPE[3], 'other': r.header['status']})'''
                

            except socket.error, reason:
                print reason

            except DNS.Error as e:
                print e

        ips = []
        count = count + 1
    s.close()
    return result

"""将结果存入到文件中"""


def write2file(results, fw_name):
    """
    Write result of dns to file(*.txt)
    """

    fw = open(fw_name, "a")  # 追加方式打开文件

    for result in results:
        fw.write(str(result) + '\n')

    fw.close()

"""Demo"""


def main():

    starttime = datetime.datetime.now()
    current_time = time.strftime("%Y%m%d%H%M", time.localtime())
    if len(sys.argv) < 3:
        print 'Wrong,format'
        sys.exit(0)
    ip_count = 0
    dns_count = 0
    fr_path = './IpSource/' + sys.argv[1]  # 输入文件
    fw_path = './DnsResult/' + \
        sys.argv[2] + '_' + current_time + '.txt'  # 输出结果文件
    fr = open(fr_path, 'r')
    fw_name = fw_path
    fo = open('./DnsResult/' + 'Run.log', 'a')  # 运行日志文件

    ip_list = fr.readlines()
    lines = len(ip_list)
    fr.close()
    if not lines:
        print 'There are not ips to detect'
        return

    for i in xrange(0, lines, 2):

        results = []
        list_ip = []
        start_ip = ip_list[i].strip()
        end_ip = ip_list[i + 1].strip()

        try:
            long_start_ip = ip2long(start_ip)
            long_end_ip = ip2long(end_ip)
            ip_count = ip_count + (long_end_ip - long_start_ip)
        except:
            print 'Wrong ip format,please check it'
            continue

        """将ip段随机，形成ip池"""
        for i in range(long_start_ip, long_end_ip + 1):
            list_ip.append(i)
        random.shuffle(list_ip)

        results = batch_server_detect(list_ip)  # 探测ip段
        dns_count = dns_count + len(results)
        write2file(results, fw_name)  # 将探测结果存入文件

    endtime = datetime.datetime.now()
    print 'Dns detect finished'
    print '探测结果文件：' + sys.argv[2] + '_' + current_time + '.txt'
    print >> fo, '探测结果文件：' + sys.argv[2] + '_' + current_time  + '.txt'
    print 'Sent package num :' + str(THREAD_NUM)
    print >>fo, 'Sent package num :' + str(THREAD_NUM)
    print '共探测IP数量：' + str(ip_count)
    print >> fo, '共探测IP数量：' + str(ip_count)
    print '共得到DNS数量：' + str(dns_count)
    print >>fo, '共得到DNS数量：' + str(dns_count)
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
