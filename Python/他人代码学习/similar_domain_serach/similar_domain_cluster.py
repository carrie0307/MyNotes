# -*- coding: utf-8 -*-

"""
根据自定义相似度聚类,结合mongo同步进行

根据existed_domains 和 template_domain 的相似性比较和mode， 存入 clusters_table, 然后根据mode来生成新的域名并验证

"""

# QUESTION： existed_domains 和 template_domain 的来源什么区别？？？

from domain_match_rule import Domains_Match
from pymongo import MongoClient
from datetime import datetime
from config_file import mongo_ip,IS_TEST

if IS_TEST:
    mongo_db = MongoClient(mongo_ip, 27017).domain_set
else:
    mongo_db = MongoClient(mongo_ip,27017).new_mal_domain_profile

def cluster(domains):

    print "cluster begin..."
    clusters_table = mongo_db.clusters_table
    #
    dm_class = Domains_Match()
    if len(domains) != 0:
        if clusters_table.find({}, {}).count()==0:
            print '---'
            # clusters_table.insert_one(
            #     {
            #         'templet_domain': domains[0],
            #         'update_time': datetime.now(),
            #         'existed_similar_domains': [],
            #         'modes': []
            #     }
            # )
            domains = domains[1:]
        for i,domain in enumerate(domains):
            match_flag = 0
            # clusters_table表中没有这个domain
            if not clusters_table.find_one({'templet_domain':domain}, {}):
                # print '{0}:{1}'.format(i + 1, domain)
                for rs in clusters_table.find({}, {'_id': 0, 'templet_domain': 1}):
                    match_domain = rs['templet_domain']
                    # 对match_domain,domain进行match匹配后的情况
                    flag,mode = dm_class.match(match_domain,domain)
                    print flag,mode
                    if flag:
                        #  dm_class.match(match_domain,domain)得到flag=1， 则把domain加入到match_domain的existed_similar_domains列表中
                        # existed_domains 是尚未验证的域名 ？？？
                        match_flag = 1
                        clusters_table.update_one(
                            {'templet_domain': match_domain},
                            {
                                '$set': {
                                    'update_time': datetime.now()
                                },
                                '$addToSet': {
                                    'existed_similar_domains': domain,
                                    'modes': mode
                                }
                            },
                            upsert=True
                        )
                if match_flag == 0:
                    clusters_table.insert_one(
                        {
                            'templet_domain': domain,
                            'update_time': datetime.now(),
                            'existed_similar_domains': [],
                            'modes': []
                        }
                    )
    print "cluster end..."

def exper_cluster():
    import pickle
    from config_file import samples_file_name
    with open(samples_file_name,'rb') as f:
        domains = pickle.load(f)
    print len(domains)
    cluster(domains)

if __name__ == "__main__":
    exper_cluster()
