# -*- coding: utf-8 -*-

"""
导出模式
"""

from pymongo import MongoClient
from config_file import mongo_ip,IS_TEST
from config_file import cur_modes_file_name,old_modes_file_name
import os
import pickle

if IS_TEST:
    cm_file_name = 'exper_file/' + cur_modes_file_name
    om_file_name = 'exper_file/' + old_modes_file_name
    mongo_db = MongoClient(mongo_ip, 27017).domain_set
else:
    cm_file_name = 'load_file/' + cur_modes_file_name
    om_file_name = 'load_file/' + old_modes_file_name
    mongo_db = MongoClient(mongo_ip, 27017).new_mal_domain_profile

def config_modes_pkl():
    """
    未跑完cur中的模式不能又执行这个函数
    :return: 
    """
    print "config mode..."
    clusters_table = mongo_db.clusters_table
    if not os.path.isfile(om_file_name):
        with open(om_file_name,'wb') as f:
            pickle.dump(([],[]),f)
    with open(om_file_name, 'rb') as f:
        old_add_modes,old_existed_domains = pickle.load(f)

    res = clusters_table.find({},{'_id':0,'modes':1,'existed_similar_domains':1})

    new_add_modes = []
    new_existed_domains = []
    for rs in res:
        for mode in rs['modes']:
            if mode not in new_add_modes:
                new_add_modes.append(mode)
                new_existed_domains.append(rs['existed_similar_domains'])

    add_modes = []
    existed_domains= []
    for mode,exist_domain in zip(new_add_modes,new_existed_domains):
        if mode not in old_add_modes:
            add_modes.append(mode)
            existed_domains.append(exist_domain)

    with open(cm_file_name, 'wb') as f:
        pickle.dump((add_modes,existed_domains), f)

    old_add_modes = old_add_modes+add_modes
    old_existed_domains = old_existed_domains+existed_domains
    with open(om_file_name, 'wb') as f:
        pickle.dump((old_add_modes,old_existed_domains), f)
    print "config mode over..."

def load_cur_modes(config_modes=True):
    """
    导出当前最新的模式集
    :return: 
    """
    if not os.path.isfile(cm_file_name) or config_modes:
        config_modes_pkl()
    with open(cm_file_name, 'rb') as f:
        return pickle.load(f)