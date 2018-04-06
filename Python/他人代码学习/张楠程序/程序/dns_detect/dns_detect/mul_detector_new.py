#!/usr/bin/python
# encoding:utf-8
"""
DNS探测程序
"""
import config
import socket
import select
import struct
import random
import time
import datetime
import sys
import re
import string
#import DNS
sys.path.append('..')
THREAD_NUM = config.THREAD_NUM
TIMEOUT = config.TIMEOUT

#DNSSERVERTYPE = ["1", "2", "3", "4"]

def domain_to_byte(domain):
    #print 'old domain',domain
    domaintobyte=''
    split=domain.split('.')    #按点分割，成为一个列表
    for s in split:
        format1='B%ds'%len(s)
        newsplit=struct.pack(format1,len(s),s)
        domaintobyte+=newsplit
    domaintobyte+='\0'
    #print 'new domain',repr(domaintobyte)
    return domaintobyte

def byte_to_domain(byte):
    #print 'old byte',repr(byte)
    i = 0
    string = ''
    while byte[i] !='\x00':
        (length,) = struct.unpack('!h',byte[i:i+2])#it will a furhter byte 
        #length = int(byte[i],16)
        length = length >> 8#get the number we want
        string += byte[i+1:i+length+1]#part of name
        i += length+1
        string +='.'
    return string

def GetFullName(offset, Buf):
    fullRecord = ''
    oneChar = struct.unpack('!B', Buf[offset:offset+1])[0]
    #print oneChar
    if oneChar & 0xc0 == 0xc0 : #指针
        jump = struct.unpack('!h', Buf[offset:offset+2])[0]
        jump = jump & 0x3FFF    #指针指向的地址
        fullRecord += GetFullName(jump, Buf)
    elif oneChar == 0 :         #域名以\0结束
        return '\x00'
    else :                      #域名部分
        fullRecord += Buf[offset:offset+oneChar+1]
        fullRecord += GetFullName(offset+oneChar+1, Buf)
    return fullRecord

class Dnsdgram:
    def __init__(self):
        self.TID = random.randint(-32768,32767)#id number
        print 'tid',self.TID
        self.Flags= 0x0100#QR:0,opcode:0000,AA:0,TC:0,RD:1,RA:0,ZERO:000,RCODE:000
        self.Question = 0x0001#request type
        self.AnswerRRs = 0x0000#Answer
        self.AuthorityRRs = 0x0000#Authority
        self.AdditionalRRs = 0x000#Additional
        self.SearchType = 0x0000#should change
        self.SearchClass = 0x0001#request
        self.Name = ''
    
    def request(self,data):
        if data[2] == 'A':
            self.SearchType = 0x0001
        elif data[2] == 'NS':
            self.SearchType = 0x0002
        elif data[2] == 'CNAME':
            self.SearchType = 0x0005
        elif data[2] == 'MX':
            self.SearchType = 0x0004
        else:
            print 'wrong type'
            return False
        body = domain_to_byte(data[0])#name
        head = struct.pack('!hhhhhh',self.TID,self.Flags,self.Question,self.AnswerRRs,self.AuthorityRRs,self.AdditionalRRs)
        tail = struct.pack('!hh',self.SearchType,self.SearchClass)
        buf = head + body + tail
        #print 'buf '+buf
        return buf
    
    def analyse(self,data):
        if data[:2] == struct.pack('!h',self.TID):
            print 'get the exact bag'
        else:
            print 'not the bag we are looking for'
            return False
        try:
            self.Flags = struct.unpack('!h',data[2:4])[0]#0000 means correct
            #print self.Flags
        except:
            return False 
        errormsg = self.Flags & 0x000F
        if errormsg == 3:
            #print 'State: NXDOMAIN'
            flag='NXDOMAIN'
            return flag
        elif errormsg==5:
            #print 'State: REFUSED'
            flag='REFUSED'
            return flag
        elif errormsg==2:
            #print 'State: SERVFAIL'
            flag='SERVFAIL'
            return flag
        elif errormsg==0:
            #print 'state: NOERROR'
            flag='NOERROR'
        else:
            print 'the dgram did not transmitte correct'
            flag='other'
            return flag
        self.Question = struct.unpack('!h',data[4:6])[0]
        self.AnswerRRs = struct.unpack('!h',data[6:8])[0]
        self.AuthorityRRs = struct.unpack('!h',data[8:10])[0]
        self.AdditionalRRs = struct.unpack('!h',data[10:12])[0]#the above are head section
        bitflag = 12
        while data[bitflag] != '\x00':
            bitflag += 1
        bitflag += 1#for \x00
        length = bitflag - 12#the length of name
        format3 = 'B%ds'%length
        self.SearchType = struct.unpack('!h',data[bitflag:bitflag+2])[0]
        self.SearchClass = struct.unpack('!h',data[bitflag+2:bitflag+4])[0]# this is the question section
        i = 0
        bitflag += 4#for type and class
        print 'Question:',self.Question
        print 'AnswerRRs:',self.AnswerRRs
        print 'AuthorityRRs:',self.AuthorityRRs
        print 'AdditionalRRs:',self.AdditionalRRs
        print 'Type:',self.SearchType
        print 'Class:',self.SearchClass
        if self.AnswerRRs > 0:
            print 'Answer Section:'
            while i < self.AnswerRRs :#or i < self.AuthorityRRs
                gett = self.apart_type(data,bitflag)
                if gett == False:
                    return False
                else:
                    bitflag = gett
                i += 1
        if self.AuthorityRRs > 0:
            print 'Authority Section:'
            i = 0
            while i < self.AuthorityRRs :#or i < self.AuthorityRRs
                gett = self.apart_type(data,bitflag)
                if gett == False:
                    return False
                else:
                    bitflag = gett
                i += 1
        if self.AdditionalRRs > 0:
            print 'Additional Section:'
            i = 0
            while i < self.AdditionalRRs :#or i < self.AuthorityRRs
                get = self.apart_type(data,bitflag)
                if gett == False:
                    return False
                else:
                    bitflag = gett
                i += 1
        return True
    
    def apart_type(self,data,bitflag):
        bitflag += 2#2 for point to name
        if data[bitflag:bitflag+2] =='\x00\x01':#A
            print 'A record:'
            bitflag += 8#2 for type, 2 for class, 4 for ttl
            rlength = struct.unpack('!h',data[bitflag:bitflag+2])[0]
            iptuple = struct.unpack('!BBBB',data[bitflag+2:bitflag+6])
            ipstr = '%d.%d.%d.%d'%iptuple
            bitflag += rlength + 2
            print 'IP:',ipstr
        elif data[bitflag:bitflag+2] =='\x00\x02':#NS
            print'NS record:'
            bitflag += 8#2 for type, 2 for class, 4 for ttl
            rlength = struct.unpack('!h',data[bitflag:bitflag+2])[0]
            fullRecord = GetFullName(bitflag+2,data)
            bitflag += rlength + 2
            sname = byte_to_domain(fullRecord)
            print sname
        elif data[bitflag:bitflag+2] =='\x00\x05':#CNAME
            print 'CNAME record:'
            bitflag += 8#2 for type, 2 for class, 4 for ttl
            rlength = struct.unpack('!h',data[bitflag:bitflag+2])[0]
            fullRecord = GetFullName(bitflag+2,data)
            bitflag += rlength + 2
            sname =  byte_to_domain(fullRecord)
            print sname
        elif data[bitflag:bitflag+2] =='\x00\x04':#MX
            print 'MX record:'
            bitflag += 8#2 for type, 2 for class, 4 for ttl
            rlength = struct.unpack('!h',data[bitflag:bitflag+2])[0]
            fullRecord = GetFullName(bitflag+2,data)
            bitflag += rlength + 2
            sname =  byte_to_domain(fullRecord)
            print sname
        elif data[bitflag:bitflag+2] =='\x00\x06':#SOA
            #print 'SOA record:'
            bitflag += 8#2 for type, 2 for class, 4 for ttl
            rlength = struct.unpack('!h',data[bitflag:bitflag+2])[0]
            fullRecord = GetFullName(bitflag+2,data)
            bitflag += rlength + 2
            sname = byte_to_domain(fullRecord)
            print sname
        else:
            print repr(data[bitflag:bitflag+2])
            #print 'wrong type for Authority'
            return False
        return bitflag
def spilt_check(data):
    result0 = data.split("@")
    if result0[1] =='':
        print 'a'
        return False#do not match the input quire
    result1 = result0[1].split(" ")
    if result1[0] =='':
        print 'b'
        return False#do not match the input quire
    if result1[1] =='':
        print 'c'
        return False#do not match the input quire
    #print 'result:',(result0,result1)
    result = []
    result.append(result0[0])#name like baidu.com
    result.append(result1[0])#address like 8.8.8.8
    result.append(result1[1])#type like a
    pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')#chenck ip
    match = pattern.match(result[1])
    if not match:
        print 'not match'
        return False
    return result#the input data is correct,tpye will be check later
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

def ip2hex (ip):
    return hex(struct.unpack("!I", socket.inet_aton(ip))[0])

def batch_server_detect(list_ip=[]):
    '''
    batch dns detect , each time sends 'num' packets
    '''
    port = 53
    # 建立一个UDP套接字（SOCK_DGRAM，代表UDP，AF_INET表示IPv4）
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_port = random.randint(1024, 65535)
    # socket绑定到指定IP地址和接口上
    s.bind(('', source_port))

    ip_count = len(list_ip)
    count = 0
    result = []
    dnss = Dnsdgram()
    while count * THREAD_NUM < ip_count:
        ips = list_ip[count * THREAD_NUM: (count + 1) * THREAD_NUM]

        for ip in ips:
            server = long2ip(ip)
            a=string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], random.randint(12, 20))).replace(' ','')
            #server='1.2.4.8'
            dname=a+'.'+(ip2hex(str(ip)))+".Babytree.com"
            data=dname+'@'+server+' A'
            #print data
            #data='baidu.com @'+server+' A'
            result1 = spilt_check(data)
            buf = dnss.request(result1)
            try:
                a = s.sendto(buf, (server, port))
                print a, "send to IP:", server
            except socket.error, reason:
                print reason
        while s:
            try:
                r, w, e = select.select([s], [], [], TIMEOUT)
                if not len(r):
                    break
                (reply, from_address) = s.recvfrom(32767)
                #dnss.analyse(reply)
                state=dnss.analyse(reply)
                print state
                #u = Lib.Munpacker(reply)
                #r = Lib.DnsResult(u, {})
                if state==True:
                    k=from_address[0]+'**'+'NOERROOR'
                    result.append(k)
                    print result
                elif state=='NXDOMAIN':
                    k=from_address[0]+'**'+'NXDOMAIN'
                    result.append(k)
                    print result
                elif state=='REFUSED':
                    k=from_address[0]+'**'+'REFUSED'
                    result.append(k)
                    print result
                elif state=='SERVFAIL':
                    k=from_address[0]+'**'+'SERVFAIL'
                    result.append(k)
                    print result
                else:
                    pass
            except socket.error, reason:
                print reason

            '''except DNS.Error as e:
                print e'''

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
        print results
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
