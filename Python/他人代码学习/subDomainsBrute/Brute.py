#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    原作者 http://www.lijiejie.com
    改写者 吴晓宝
    改写日期 2017.10.9

    思路：构造子域名 - dns解析验证 - 除去内网ip和泛解析所得的ip
"""
# QUESTION:优先级怎么用？？？

import gevent
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.queue import PriorityQueue
'''
gevent.queue的队列：
http://www.gevent.org/gevent.queue.html
1.  queue = gevent.queue.Queue() 一般的同步队列
2. 一个子类：class PriorityQueue (Bases: gevent.queue.Queue)使用时注意：
    1) put时以tuple形式put,self.put((priority,data))    Entries are typically tuples of the form: (priority number, data).
    2) priority越小，优先级越高 A subclass of Queue that retrieves entries in priority order (lowest first).
'''
import sys
import re
import dns.resolver
import time
import os

class SubNameBrute:
    def __init__(self, target, options):
        # 设置优先级
        self.queue = PriorityQueue()
        self.priority = 0

        # 根据参数进行基本设置
        self.target = target.strip()
        self.options = options
        self.ignore_intranet = options.get('ignore_intranet')

        # 是否用大字典
        if self.options.get('subnames_full'):
            outfile_name+='_sfull'
        if self.options.get('next_sub_full'):
            outfile_name += '_nfull'

        # 根据主域名确定结果文件名称
        outfile_name = options.get('file') if options.get('file') else(target)
        self.fname = 'results/'+outfile_name+'.txt'
        self.outfile = open('results/'+outfile_name+'.txt', 'wb')
        self.outfile_ips = open('results/'+outfile_name+'_ip.txt', 'w')

        # 设置dns解析器 （根据预设的线程数量初始化dns resolver）
        # QUESTION: configure = False还是不太明白 为什么要不以/etc/resolv.conf的常规常规配置？？
        self.resolvers = [dns.resolver.Resolver(configure=False) for _ in range(options.get('threads'))]
        for _ in self.resolvers:
            '''
            dns.resolver.Resolver: http://www.dnspython.org/docs/1.14.0/dns.resolver.Resolver-class.html
            dns.resolver.Resolver.lifetime: The total number of seconds to spend trying to get an answer to the question.
            dns.resolver.Resolver.timeout: The number of seconds to wait for a response from a server, before timing out.
            '''
            # QUESTION:lifetime 与 timeout 什么区别？
            _.lifetime = _.timeout = 10.0

        # 加载dns服务器列表
        self._load_dns_servers()
        # self.ex_resolver是备用的在出现except时使用的dns_resolver
        self.ex_resolver = dns.resolver.Resolver(configure=False)
        self.ex_resolver.nameservers = self.dns_servers
        self.logfile = open('results/'+target+'_log.txt','a')

        #set subdomain dct set
        self._load_next_sub()
        self._load_sub_names()

        #set init paras
        self.start_time = time.time()
        self.scan_count = 0
        self.found_count = 0 # 已验证过存在子域名的前缀
        self.STOP_ME = False
        self.ip_dict = {}
        self.found_subs = set()

    def _load_dns_servers(self):
        """
        功能：导入可用的名称服务器 (init初始化时执行)
        :return:
        """
        print '[+] Validate DNS servers ...'
        self.dns_servers = []
        pool = Pool(30)
        for server in open('dns_servers.txt').xreadlines():#xreadlines返回一个生成器
            server = server.strip()
            if server:
                # apply_async 并行
                pool.apply_async(self._test_server, (server,))#apply_async(func[, args[, kwds[, callback]]]) 它是非阻塞
        pool.join()#主进程阻塞，等待子进程的退出
        self.dns_count = len(self.dns_servers)
        sys.stdout.write('\n')
        print '[+] Found %s available DNS Servers in total' % self.dns_count
        if self.dns_count == 0:
            print '[ERROR] No DNS Servers available.'
            sys.exit(-1)

    def _test_server(self, server):
        '''
        功能：检测dns服务器是否可用（_load_dns_servers()在加载dns列表时会探测）
            检测思路：1.已存在域名可成功解析出ip;
                    2.不存在的域名解析则会出错.
        :param server:nameserver
        :return: 无
        '''
        resolver = dns.resolver.Resolver()
        resolver.lifetime = resolver.timeout = 10.0
        try:
            resolver.nameservers = [server]
            existed_domain = 'public-dns-a.baidu.com'
            corrs_ip = '180.76.76.76'
            answers = resolver.query(existed_domain)
            if answers[0].address != corrs_ip:
                raise Exception('incorrect DNS response')
            try:
                non_existed_domain = 'test.bad.dns.lijiejie.com'
                resolver.query(non_existed_domain)
                print '[+] Bad DNS Server found %s' % server
            except:
                self.dns_servers.append(server)
            print '[+] Check DNS Server %s < OK >   Found %s' % (server.ljust(16), len(self.dns_servers))
        except:
            print '[+] Check DNS Server %s <Fail>   Found %s' % (server.ljust(16), len(self.dns_servers))


    def _get_filename(self,option,is_full):
        '''
        功能：构造要打开字典文件的目录
        param: option: 字典的类型 subnames / next_sub
        param: is_full: 决定使用大字典还是小字典
        return: _file: 当前要加载字典的路径
        '''
        has_newdct = self.options.get('new_dct')
        if has_newdct:
            try:
                # 有新字典文件名，则加载新的字典
                next_sub,subnames = has_newdct.split(',')
            except Exception:
                print '[ERROR] Names file not exists: %s' % has_newdct
                exit(-1)
            else:
                # 若新字典名next_sub,subnames加载异常，则打开原来的字典
                self.new_filenames = {
                    'next_sub':'dict/'+next_sub,
                    'subnames':'dict/'+subnames
                }
                filename = self.new_filenames.get(option)
                if os.path.exists(filename):
                    _file = filename
                else:
                    print '[ERROR] Names file not exists: %s' % filename
                    exit(-1)
        elif is_full:
            _file = 'dict/'+option+'_full.txt'
        else:
            _file = 'dict/'+option+'.txt'

        return _file

    def _load_sub_names(self):

        print '[+] Load sub names ...'
        is_full = self.options.get('subnames_full')
        # _file是完整的路径名
        _file = self._get_filename('subnames',is_full)
        normal_lines = []
        wildcard_list = []
        regex_list = []
        lines = set()
        with open(_file) as f:
            wildcard_lines = []
            for line in f.xreadlines():
                sub = line.strip()
                print 'sub:' + sub
                if not sub or sub in lines:
                    continue
                lines.add(sub)
                # 通配符
                # QUESTION：但实际的sub文件中都没有通配符？？？？
                if sub.find('{alphnum}') >= 0 or sub.find('{alpha}') >= 0 or sub.find('{num}') >= 0:
                    # 如果存在某个通配符，则先将其加入到wildcard_lines
                    wildcard_lines.append(sub)
                    sub = sub.replace('{alphnum}', '[a-z0-9]')
                    sub = sub.replace('{alpha}', '[a-z]')
                    sub = sub.replace('{num}', '[0-9]')
                    print 'sun2: ' + sub
                    if sub not in wildcard_list:
                        # QUESTION：为什么替换通配符后还要加入到wildcard_list？？
                        wildcard_list.append(sub)
                        regex_list.append('^' + sub + '$')
                else:
                    # 不存在通配符的加入到normal_lines
                    normal_lines.append(sub)
        pattern = '|'.join(regex_list)
        if pattern:
            _regex = re.compile(pattern)
            if _regex:
                for line in normal_lines[:]:
                    if _regex.search(line):
                        normal_lines.remove(line)

        for item in normal_lines:
            # QUESTION: 为什么遍历时每次要令priority自增？
            self.priority = self.priority+1
            self.queue.put((self.priority, item))

        for item in wildcard_lines:
            # QUESTION： wildcard_lines中元素含有通配符所以优先级低？？？（大数对应低优先级）
            self.queue.put((88888888, item))

    def _load_next_sub(self):
        """
        枚举一、二位子域并添加已存子域
        :return:
        """
        self.next_subs = []
        _set = set()
        is_full = self.options.get('next_sub_full')
        #  _file是nett_sub完整的路径
        _file = self._get_filename('next_sub',is_full)
        with open(_file) as f:
            for line in f:
                sub = line.strip()
                if sub and sub not in self.next_subs:
                    #  利用{alphnum}等通配符组合新的子串
                    # QUESTION:但原文件中的其他子串没有用？
                    tmp_set = {sub} # 相当于tep_set = set(sub)
                    while len(tmp_set) > 0:
                        item = tmp_set.pop()
                        # print 'item: ' + item
                        if item.find('{alphnum}') >= 0:
                            for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                            # for _letter in 'ab89':
                                # 如果是{alphnum}{alphnum}，则将'abcdefghijklmnopqrstuvwxyz0123456789' 两两组合的结果加入了tmp_set
                                tt = item.replace('{alphnum}', _letter, 1)
                                tmp_set.add(tt)
                        elif item.find('{alpha}') >= 0:
                            for _letter in 'abcdefghijklmnopqrstuvwxyz':
                                tmp_set.add(item.replace('{alpha}', _letter, 1))
                        elif item.find('{num}') >= 0:
                            for _letter in '0123456789':
                                tmp_set.add(item.replace('{num}', _letter, 1))
                        elif item not in _set:
                            # 当所有的{alphnum}等通配符都被replace完后，将被加入到_set / self.next_subs
                            # 原文件中不包括通配符的子串直接加入了_set,也加入了self.next_subs
                            _set.add(item)
                            self.next_subs.append(item)


    @staticmethod
    # 判断是否是内网ip
    def is_intranet(ip):
        ret = ip.split('.')
        if len(ret) != 4:
            return True
        if ret[0] == '10':
            return True
        if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
            return True
        if ret[0] == '192' and ret[1] == '168':
            return True
        return False

    def put_item(self, item):
        # 向待检测前缀队列self.queue中添加新的子域名前缀
        num = item.count('{alphnum}') + item.count('{alpha}') + item.count('{num}')
        if num == 0:
            self.priority += 1
            self.queue.put((self.priority, item))
        else:
            # 存在通配符则将优先级设为低级
            self.queue.put((self.priority + num * 10000000, item))

    def _universal_parsing(self,sub,ips):
        # 统计数量，与泛解析有关
        _sub = sub.split('.')[-1]
        # (_sub,ips)前缀与该前缀构成的子域名所得ip QUESTION：这和泛解析什么关系？？？
        '''
        a.b.baidu.com 与 a.baidu.com ，它们的_sub都是'a.',当他们解析到相同的A记录时，
        则有可能其他_sub同为'a.'(最左侧一级为a.)的子域名也会解析到同样的ip，存在泛解析
        '''
        if (_sub, ips) not in self.ip_dict:
            self.ip_dict[(_sub, ips)] = 1
        else:
            self.ip_dict[(_sub, ips)] += 1

        # 计数：一组ips被多少个sub解析到  （如果一组ips被多组sub解析到，则可能是泛解析）
        if ips not in self.ip_dict:
            self.ip_dict[ips] = 1
        else:
            self.ip_dict[ips] += 1

        return True if self.ip_dict[(_sub, ips)] > 3 or self.ip_dict[ips] > 6 else(False)

    def _validate_subdomain(self,j,sub):
        '''
           功能：验证子域名是否存在
        '''

        # 构造新的子域名
        subdmname = sub + '.' + self.target

        try:
            answers = self.resolvers[j].query(subdmname)
        except dns.resolver.NoAnswer:
            try:
                # 出现异常则用备用dns解析器解析
                answers = self.ex_resolver.query(subdmname)
            except dns.resolver.NoAnswer:
                # 如果2次都出现异常，则返回False
                return False
        if answers:
            # 如果得到响应，则将该前缀加入到self.found_subs
            # QUESTION： 验证说明不存在的不用单独存下来吗
            self.found_subs.add(sub)
            # 得到A记录集合
            ips = ', '.join(sorted([answer.address for answer in answers]))
            print ips
            self.cur_ips = ips
            # QUESTION: 只有一个ip且ip是一下其中之一的情况
            if ips in ['1.1.1.1', '127.0.0.1', '0.0.0.0']:
                return False
            #除去内网域名
            # self.ignore_instanet表示是否要进行内网ip过滤
            # SubNameBrute.is_intranet(answers[0].address) 是实际进行是否是内外ip的测算
            # QUESTION: 为什么只对answers[0]中的ip进行测试？？？
            if self.ignore_intranet and SubNameBrute.is_intranet(answers[0].address):
                return False
            # 泛解析
            if self._universal_parsing(sub, ips):
                return False
        else:
            return False

        return True

    def _scan_cname(self,j,subdmname):
        '''
        功能：检测子域名的cname是否是新的子域名，是否可以得到新的前缀
        '''
        try:
            self.scan_count += 1
            # subdmname是已经验证有效的子域名，现获取其cname
            answers = self.resolvers[j].query(subdmname, 'cname')
            cname = answers[0].target.to_unicode().rstrip('.')
            # cname.endswith(self.target)判断cname是不是子域名
            if cname.endswith(self.target) and cname not in self.found_subs:
                # 将是子域名的cname加入到self.found_subs

                self.found_subs.add(cname)
                # 假设cname是'www.a.shifen.com',target是'shifen.com',,则cname_sub是'www.a'
                # 当cname是子域时，将i其前缀再次加入队列，当此前缀在不同级上时，可能构成新的子域
                cname_sub = cname[:len(cname) - len(self.target) - 1]  # new sub
                self.queue.put((0, cname_sub))
        except:
            pass

    def _scan(self, j):
        # 具体运行的核心函数
        self.resolvers[j].nameservers = [self.dns_servers[j % self.dns_count]]

        while not self.queue.empty():
            try:
                # 从队列中获得一个前缀
                item = self.queue.get(timeout=1.0)[1]
                self.scan_count += 1
            except:
                break
            try:
                # 根据_load_sub_names代码，会有包含通配符的sub被加入了queue，因此这里要进行处理
                if item.find('{alphnum}') >= 0:
                    for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                        self.put_item(item.replace('{alphnum}', _letter, 1))
                    continue
                elif item.find('{alpha}') >= 0:
                    for _letter in 'abcdefghijklmnopqrstuvwxyz':
                        self.put_item(item.replace('{alpha}', _letter, 1))
                    continue
                elif item.find('{num}') >= 0:
                    for _letter in '0123456789':
                        self.put_item(item.replace('{num}', _letter, 1))
                    continue
                elif item.find('{next_sub}') >= 0:
                    for _ in self.next_subs:
                        self.queue.put((0, item.replace('{next_sub}', _, 1)))
                    continue
                else:
                    sub = item

                # 如果是已经验证过的，则不进行验证处理
                if sub in self.found_subs:
                    continue

                if self._validate_subdomain(j,sub):
                    cur_sub_domain = sub+'.'+self.target
                    self._scan_cname(j,cur_sub_domain) # 检测子域名的cname中是否包含子域名
                    self.found_count += 1
                    # QUESTON
                    self.outfile.write(cur_sub_domain+'\n')
                    '''
                    关于flush与write：http://blog.csdn.net/fenfeiqinjian/article/details/49444973
                        一般的文件流操作都包含缓冲机制，write方法并不直接将数据写入文件，而是先写入内存中特定的缓冲区。
                        flush方法是用来刷新缓冲区的，即将缓冲区中的数据立刻写入文件，同时清空缓冲区
                        正常情况下缓冲区满时，操作系统会自动将缓冲数据写入到文件中。
                        至于close方法，原理是内部先调用flush方法来刷新缓冲区，再执行关闭操作，这样即使缓冲区数据未满也能保证数据的完整性。
                        如果进程意外退出或正常退出时而未执行文件的close方法，缓冲区中的内容将会丢失
                    '''
                    self.outfile.flush()
                    self.outfile_ips.write(self.cur_ips+'\n')
                    self.outfile_ips.flush()
                    print cur_sub_domain
                    # '{next_sub}.' + sub 目的在于给当前前缀再增加前缀，以构成多级域名
                    self.queue.put((999999999, '{next_sub}.' + sub))

            except (dns.resolver.NXDOMAIN, dns.name.EmptyLabel):
                pass
            except (dns.resolver.NoNameservers, dns.resolver.NoAnswer, dns.exception.Timeout):
                pass
            except Exception:
                pass
            print "scan_count=%s,found_count=%s"%(self.scan_count,self.found_count)

    def run(self):
        # i用来标识是第几个写成，同时在协程中用来选择dns resolver
        threads = [gevent.spawn(self._scan, i) for i in range(self.options.get('threads'))]

        try:
            gevent.joinall(threads)
        except KeyboardInterrupt:
            print '[WARNING] User aborted.'

        self.end_time = time.time()
        s = (self.end_time-self.start_time)
        m = ((self.end_time - self.start_time)/60)
        h = ((self.end_time - self.start_time) / 3600)

        self.logfile.write(self.fname+'\n')
        result = "scan_count=%s,found_count=%s"%(self.scan_count,self.found_count)
        self.logfile.write(result+'\n')
        time_consuming = "time-consuming:%d seconds"%s
        print time_consuming
        self.logfile.write(time_consuming+'\n')
        time_consuming = "time-consuming:%d minutes" % m
        print time_consuming
        self.logfile.write(time_consuming+'\n')
        time_consuming = "time-consuming:%d hours" % h
        print time_consuming
        self.logfile.write(time_consuming+'\n')
        # 统计结果文件中各级域名的数量（self.fname是输出结果的文件名）
        ocount, bcount, tcount, fcount = self.get_distribution(self.fname)

        subdomain_count = '二级域名数量: %d' % ocount
        print subdomain_count
        self.logfile.write(subdomain_count+'\n')
        subdomain_count = '三级域名数量: %d' % bcount
        print subdomain_count
        self.logfile.write(subdomain_count+'\n')
        subdomain_count = '四级域名数量: %d' % tcount
        print subdomain_count
        self.logfile.write(subdomain_count+'\n')
        subdomain_count = '五级域名数量: %d' % fcount
        print subdomain_count
        self.logfile.write(subdomain_count+'\n')

        self.outfile.flush()
        self.outfile.close()
        self.outfile_ips.flush()
        self.outfile_ips.close()

    def get_distribution(self,filename):
        '''
        功能：统计结果文件filename中二级、三级和四级域名的数量
        '''
        with open(filename, 'rb') as f:
            subdomains = [line.strip() for line in f.readlines()]
        ocount = bcount = tcount = fcount = 0
        for domain in subdomains:
            if domain.count('.') == 2:
                ocount += 1
            elif domain.count('.') == 3:
                bcount += 1
            elif domain.count('.') == 4:
                tcount += 1
            else:
                fcount += 1

        return ocount, bcount, tcount, fcount

if __name__ == '__main__':
    options = {
        'new_dct' : False,#use new dct
        'next_sub_full': True,#_full.txt/.txt
        'subnames_full': False,  # _full.txt/.txt
        'ignore_intranet': False,#exclude intranet/not
        'threads': 100,#setting number of thread
        'file': None #output filename.txt/target.txt
    }
    domain = 'baidu.com'
    d = SubNameBrute(target=domain, options=options)
    d.run()
