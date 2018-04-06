#!usr/bin/python
#encoding:utf-8
"""
修改原来ip顺序发送，将ip打乱，形成ip池，随机发送ip
两次查询
"""
from DNS import Lib
import socket
import select
from DNS import Type
from DNS import Class
from DNS import Opcode
import struct
import DNS
import sys
sys.path.append('..')
import random
import time
import datetime

THREAD_NUM = 5000


def ip2long(ipstr): 
    return struct.unpack("!I", socket.inet_aton(ipstr))[0]

def long2ip(ip): 
    return socket.inet_ntoa(struct.pack("!I", ip))

#DNS服务器类型
DNSSERVERTYPE = ["Authoritative Name server","Authoritative Name server(with recursive service)","The Recursive Name Server","unknow"]

def batch_server_detect(ip_source=[]):
    '''
    batch dns detect , each time sends 'num' packets
    '''

    #TID为随机数
    tid = random.randint(0,65535)
    #端口为53,UDP
    port = 53
    #操作为查询
    opcode = Opcode.QUERY
    #Tpye类型为A
    qtype = Type.PTR
    #查询类，一般为IN
    qclass = Class.IN
    #期望递归
    rd = 1
        
    #建立一个UDP套接字（SOCK_DGRAM，代表UDP，AF_INET表示IPv4）
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_port = random.randint(1024, 65535)
    #socket绑定到指定IP地址和接口上
    s.bind(('', source_port))

    ip_count = len(ip_source)
    count = 0
    result=[]
    ip_detected = []

    while count * THREAD_NUM < ip_count:
        ips = ip_source[count * THREAD_NUM : (count + 1) * THREAD_NUM]
        for ip in ips:

            m = Lib.Mpacker()
            m.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)
            ip_tips = ip.split(".")
            qname = ip_tips[3]+'.'+ip_tips[2]+'.'+ip_tips[1]+'.'+ip_tips[0]
            qname += '.in-addr.arpa'
            m.addQuestion(qname,qtype,qclass)
            request = m.getbuf()

            try:
                a = s.sendto(request,(ip, port))
                print a,"send to IP:",ip
            except socket.error,reason:
                print  reason

        while 1:
            try:
                r,w,e = select.select([s], [], [],3)
                if not len(r):
                    break
                (reply, from_address) = s.recvfrom(65535)
                u = Lib.Munpacker(reply)
                r = Lib.DnsResult(u,{})
                if r.header['ra']==1 and r.header['aa']==0:
                    print from_address,"递归服务器"
                    result.append({'ip':from_address[0],'type':DNSSERVERTYPE[2],'other':r.header['status']})
                    ip_detected.append(from_address[0])
                elif r.header['ra']==1 and r.header['aa']==1:
                    print from_address,"权威服务器(递归服务)"
                    result.append({'ip':from_address[0],'type':DNSSERVERTYPE[1],'other':r.header['status']})
                    ip_detected.append(from_address[0])
                elif r.header['ra']==0 and r.header['aa']==1:
                    print from_address,"权威服务器"
                    result.append({'ip':from_address[0],'type':DNSSERVERTYPE[0],'other':r.header['status']})
                    ip_detected.append(from_address[0])
                else:
                    print from_address,"服务器类型探测失败：未知服务器",r.header['status']
                    result.append({'ip':from_address[0],'type':DNSSERVERTYPE[3],'other':r.header['status']})
                    ip_detected.append(from_address[0])

            except socket.error, reason:
                print reason
                            
            except DNS.Error as e:
                print e
    
        ips = []
        count = count + 1
    s.close()
    return result,ip_detected

"""将结果存入到文件中"""
def write2file(results,fw_name):
    """
    Write result of dns to file(*.txt)
    """
    
    fw = open(fw_name,"a")  #追加方式打开文件

    for result in results:
        fw.write(str(result)+'\n')

    fw.close()

"""Demo"""
def main():

    # if len(sys.argv)<3:
    #     print 'Wrong,format'
    #     sys.exit(0)
    # fr = open(sys.argv[1],"r")
    # fw_name = sys.argv[2]

    current_time = time.strftime("%Y-%m-%d",time.localtime())
    fr = open('shanghai_unicom.txt','r')
    fw_name = current_time + '.txt'
    
    ip_section = fr.readlines()
    lines = len(ip_section)
    if not lines:
        print 'There are not ips to detect'
        return

    for i in xrange(0,lines,2):

        results = []
        ip_source = []
        ip_detected = []
        ip_no_detected = []

        start_ip = ip_section[i].strip()
        end_ip = ip_section[i+1].strip()

        try:
            long_start_ip = ip2long(start_ip)
            long_end_ip   = ip2long(end_ip)
        except:
            print 'Wrong ip format,please check it'
            continue
        
        """将ip段随机，形成ip池"""
        for i in range(long_start_ip,long_end_ip+1):
            ip = long2ip(i)
            ip_source.append(ip)
        random.shuffle(ip_source)
      
        results,ip_detected = batch_server_detect(ip_source)  #探测ip段
        write2file(results,fw_name)                           #将探测结果存入文件
        results = []
        ip_no_detected = list(set(ip_source).difference(set(ip_detected)))
        random.shuffle(ip_no_detected)
        results,ip_detected = batch_server_detect(ip_no_detected)  #探测ip段
        write2file(results,fw_name)

    fr.close()
    
    print 'Dns detect finished'

if  __name__ ==  '__main__':

    starttime = datetime.datetime.now()
    main()
    endtime = datetime.datetime.now()
    print '程序运行时间：' + str((endtime - starttime).seconds)