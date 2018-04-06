# -*- coding: utf-8 -*-

"""
根据匹配模式生成可用域名
        -:删除指示符
        &:连续指示符

        #:数字通配符
        *:字母通配符
        $:数字/字母通配符
        %:顶级域通配符
"""

# BUG: 通过分组让每个gevent运行不同的元素，为什么不用队列来实现同步呢？？？


# QUESTION： existed_domains,self.existed_domains,domain_queue,add_domains这些什么区别？？？
# QUESTION & BUG: 都是相同字符通配上去，如何 多种组合 进行？？
# QUESTION： 这个方法没有用？？？ generate_by_delete

self.domain_q 验证存在的域名
self.ips_q 验证存在的域名的ip
add_domains 待验证的域名

from copy import copy
import dns.resolver
import pickle
from pymongo import MongoClient
from config_file import mongo_ip
from load_modes import load_cur_modes
from datetime import datetime
from gevent_model import run_gevent
from divide_items import divide_items
from config_file import dns_server_file_name,IS_TEST
from config_file import tld_list_fn

with open(tld_list_fn,'rb') as f:
    tld_list = pickle.load(f)

if IS_TEST:
    mongo_db = MongoClient(mongo_ip, 27017).domain_set
else:
    mongo_db = MongoClient(mongo_ip,27017).new_mal_domain_profile

class GenerateVaildDomain():

    def __init__(self,threads_num):

        # 从预先设定的dns服务器文件中读取dns服务器ip地址
        with open(dns_server_file_name) as f:
            self.dns_resolvers = [dns_resolver.strip() for dns_resolver in f.readlines()]
        self.name_server_num = len(self.dns_resolvers)

        # 待替换字符
        self.general_list = 'abcdefghijklmnopqrstuvwxyz0123456789'
        self.alpha_list = 'abcdefghijklmnopqrstuvwxyz'
        self.digit_list = '0123456789'

        # 线程数量
        self._threads_num = threads_num

        # 根据线程数量初始化出dns的解析器
        self.resolvers = [dns.resolver.Resolver(configure=False) for _ in range(self._threads_num)]
        for i, resolver in enumerate(self.resolvers):
            resolver.lifetime = resolver.timeout = 12.0

        # QUESTION： scan_count定义？？？
        self.scan_count = 0
        self.valid_count = 0

    def set_queue(self):
        # BUG: 队列命名却是queue,这样不好
        # BUG： 为什么self.** 的声明不妨在__init__里面呢？？
        self.domain_queue = [] # validate_domain()  已验证存在域名的队列 QUESTION： 和 add_domains的关系？？？
        self.ips_queue = []    # validate_domain()  已验证存在域名的ip
        self.existed_domains = set()

    def validate_domain(self,domain, j):
        """
        根据dns解析的结果，验证域名是否存在 (被 alidate_domains 调用)
        :param domain:
        :param j:
        :return: ips_list: 对 domain 解析所得的有效ip列表
        """
        ips_list = []
        try:
            answers = self.resolvers[j].query(domain)
        except dns.resolver.NoAnswer, e:
            pass
        except dns.resolver.NXDOMAIN, e:
            pass
        except dns.resolver.NoNameservers, e:
            pass
        except Exception,e:
            pass
        else:
            ips = [answer.address for answer in answers]
            if '1.1.1.1' not in ips and '127.0.0.1' not in ips and '0.0.0.0' not in ips:
                ips_list = ips
                # 验证存在的域名加入self.domain_queue()
                self.domain_queue.append(domain)
                # 将解析得到的ip加入队列
                self.ips_queue.append(ips)

        return ips_list

    def validate_domains(self,j,domains):
        '''
        功能：
        param: j: 线程编号 thread_id
        param: domains: [[dm1, dm2, ..], [dm1, dm2, ..]]
        '''

        self.resolvers[j].nameservers = [self.dns_resolvers[j% self.name_server_num]]
        # 第 j 个线程就取分好组的domains 中第 j 组的域名来运行
        # domain[j] 是列表
        for domain in domains[j]:
            self.validate_domain(domain,j)

    def generate_by_delete(self,templet_domain, exists_domains):
        """
        通过删除一个字符来产生域名
        :param templet_domain:
        :param exists_domains:
        :return:
        """
        domains = set()
        for i in range(len(templet_domain)):
            if i == 0:
                domain = ''.join(list(templet_domain)[1:])
            else:
                domain = ''.join(list(templet_domain)[:i]
                                 + list(templet_domain)[i + 1:])
            # QUESTION： exists_domains
            # QUESTION: self.existed_domains
            if domain not in exists_domains:
                domains.add(domain)
            else:
                self.existed_domains.add(domain)

        return domains

    def generate_domains(self,mode, exists_domains):
        """
        产生有效域名集合
        :param mode: 枚举模式
        :param exists_domains: 该模式下已获取的域名
        :return: 该模式下所有有效域名
        """
        self.set_queue()
        # QUESTION： add_domains含义 ？？？
        add_domains = set()

        if mode.find('%')!=-1:
        # 替换顶级域
            for tld in tld_list:
                str1 = mode
                add_domains.add(str1.replace('%',tld))
        else:
            if mode.find('&') != -1:
            # QUESTION： 连续指示符？？？ 为什么存在连续不连续的问题？？？
                mode = mode.replace('&', '')
                is_continuous = 1
            else:
                is_continuous = 0

            modes = []
            # QUESTION: 不modes不是肯定是一个元素吗？？？
            modes.append(mode)

            while len(modes) != 0:
                # QUESTION： item是每个具体的包含通配符的templage （目前理解是这样）
                item = modes.pop(0)

                # 根据通配符的类型找到要替换第字符列表，置于enumeration
                if item.find('#') != -1:
                    wildcard = '#'
                    enumeration = copy(self.digit_list)
                elif item.find('*') != -1:
                    wildcard = '*'
                    enumeration = copy(self.alpha_list)
                elif item.find('$') != -1:
                    wildcard = '$'
                    enumeration = copy(self.general_list)
                else:
                    if item not in exists_domains:
                        # QUESTION： add_domains 含义？？？  不在exists_domains则说明是待探测的域名？？
                        add_domains.add(item)
                    else:
                        # 注意区分 self.existed_domains 与 existed_domains
                        # QUESTION: item in exists_domains 为什么就要加入到 self.existed_domains ??
                        self.existed_domains.add(item)
                    continue

                for ch in enumeration:
                    str1 = item
                    # print 'str: ', item
                    # QUESTION：
                    '''
                    这样每次通配符都被替换成了相同的字符吗？？ 4107××.com 4107aa.com 4107bb.com 怎么插花通配？？？？？
                    eg. 4107ab.com 4107ac.com ...
                    '''
                    mode = str1.replace(wildcard, ch) if is_continuous else(str1.replace(wildcard, ch, 1))
                    '''
                        print 'mode: ', mode
                        mode:  4107000.com
                        mode:  4107111.com
                        mode:  4107222.com
                        mode:  4107333.com
                        mode:  4107444.com
                         ......
                    '''
                    # QUESTION： 为什么这里mode得到的新域名不加入到add_domains去验证？？？
                    modes.append(mode)

        # items 是分好组的元素， part_num 是分出来的组数
        # 实际运行时，第 j 个线程，就运行  items 中下标为 j 的列表中的元素
        items,part_num = divide_items(list(add_domains),self._threads_num)
        self.scan_count += len(add_domains)
        # 通过gevent来运行
        run_gevent(self.validate_domains,items,threads_num=part_num)
        # 这里add_domains 中加入的是 self.domain_queue中验证已存在的域名
        add_domains = self.domain_queue
        # QUESTION： add_ips 是验证已存在域名的ip？？？
        add_ips = self.ips_queue
        existed_domains = list(self.existed_domains)
        self.valid_count += len(add_domains)
        print '{0}:{1}'.format('scan_count',self.scan_count)
        print '{0}:{1}'.format('valid_count', self.valid_count)

        return add_domains,existed_domains,add_ips

def exper(mode):
    """
    '##&001524.com'
    '00##&1524.com'
    :return:
    """
    import datetime
    t1 = datetime.datetime.now()
    # gvd = GenerateVaildDomain(10)
    gvd = GenerateVaildDomain(5)
    add_domains, existed_domains,add_ips = gvd.generate_domains(mode,[])
    print existed_domains
    # add_domains, add_ips = gvd.generate_domains('00038*.com', ['00038x.com', '00038a.com'])
    for add_domain,add_ip in zip(add_domains,add_ips):
        print add_domain,add_ip
    for existed_domain in existed_domains:
        print existed_domain
    t2 = datetime.datetime.now()
    print t2-t1

def generate_similar_domains(config_modes=True,threads_num=10):

    gvd = GenerateVaildDomain(threads_num)
    similar_domains_table = mongo_db.similar_domains_table
    add_modes, existed_domains_list = load_cur_modes(config_modes=config_modes)
    for i,rs in enumerate(zip(add_modes,existed_domains_list)):
        mode,existed_domains = rs
        print '{0}:{1}'.format(i+1,mode)
        add_domains, existed_domains, add_ips = gvd.generate_domains(mode,existed_domains)
        similar_domains_table.update_one(
            {'mode':mode},
            {
                '$set':{
                    'mode':mode,
                    'insert_time':datetime.now()
                },
                '$addToSet':{
                    'add_domains':{'$each':add_domains},
                    'existed_domains': {'$each': existed_domains},
                    'add_ips': {'$each': add_ips},
                }
            },
            upsert=True
        )

if __name__ == "__main__":
    exper('4107###&.com')
