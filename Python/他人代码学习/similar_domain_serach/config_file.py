# -*- coding: utf-8 -*-

'''
    功能：基础配置文件
'''

#IS_TEST
IS_TEST = True

#mongo conn settings
mongo_ip = '172.29.152.151'

#mysql conn settings
DBs={
    '172.29.152.249':{
    'user':'root',
    'passwd':'platform',
    'port':3306,
    'db':'mds_new',
    'charset':'utf8',
    'host':'172.29.152.249'
    },
    '172.26.253.3': {
        'user': 'root',
        'passwd': 'platform',
        'port':3306,
        'charset': 'utf8',
        'host': '172.26.253.3',
        'db':'wxb'
    }
}
DB = DBs['172.29.152.249']
#modes file name
cur_modes_file_name = 'cur_modes.pkl'
old_modes_file_name = 'old_modes.pkl'
#existed domain set file name
existed_domains_file_name = 'load_file/existed_domains.pkl'
#exper samples file name
samples_file_name = 'exper_file/www577789.com_sample.pkl'
#tld list file name
tld_list_fn = 'req_file/tld_list.pkl'
#dns server file name
dns_server_file_name = 'req_file/dns_servers.txt'
