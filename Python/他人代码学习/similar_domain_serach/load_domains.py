# -*- coding: utf-8 -*-

"""
导出新域名
"""

from config_file import DB
from config_file import existed_domains_file_name
from config_file import samples_file_name
import os
import pickle
import MySQLdb as mdb

def config_modes_pkl():
    # QUESTION： 什么用？？？
    """
    未跑完cur中的模式不能又执行这个函数
    :return:
    """
    print "config existed domains set..."
    conn = mdb.connect(
        host=DB['host'],
        user=DB['user'],
        passwd=DB['passwd'],
        port = DB['port'],
        db=DB['db'],
        charset=DB['charset']
    )
    cur = conn.cursor()
    if not os.path.isfile(existed_domains_file_name):
        with open(existed_domains_file_name,'wb') as f:
            # QUESTION：文件不存在先写空的？？
            pickle.dump((set(),set()),f)
    with open(existed_domains_file_name, 'rb') as f:
        existed_domains,new_domains = pickle.load(f)
        print existed_domains
    # QUESTION: 都只是普通的域名为什么要写pkl文件？？
    cur.execute('select domain from mds_new.mal_domains')
    res = cur.fetchall()
    new_domains = set()
    for rs in res:
        domain = rs[0]
        if domain not in existed_domains:
            existed_domains.add(domain)
            new_domains.add(domain)
    with open(existed_domains_file_name, 'wb') as f:
        pickle.dump((existed_domains,new_domains), f)
    print "config mode over..."

def load_cur_domains(config_domains=True):
    """
    导出当前最新的域名集
    :return:
    """
    if not os.path.isfile(existed_domains_file_name) or config_domains:
        config_modes_pkl()
    with open(existed_domains_file_name, 'rb') as f:
        return pickle.load(f)[1]

def load_samples():
    with open(samples_file_name,'rb') as f:
        return pickle.load(f)

def update_tld_list():
    # QUESTION: tld 为什么要编码？？？
    from tldextract import extract
    conn = mdb.connect(
        host=DB['host'],
        user=DB['user'],
        passwd=DB['passwd'],
        port = DB['port'],
        db=DB['db'],
        charset=DB['charset']
    )
    cur = conn.cursor()
    cur.execute('select domain from mds_new.mal_domains')
    res = cur.fetchall()
    tld_list = set()
    for rs in res:
        tld_list.add(extract(rs[0]).suffix)
    with open('req_file/tld_list.pkl','wb') as f:
        pickle.dump(tld_list,f)
    with open('req_file/tld_list.pkl','rb') as f:
        tlds = pickle.load(f)
    print tlds

if __name__ == "__main__":
    # config_modes_pkl()
    update_tld_list()
