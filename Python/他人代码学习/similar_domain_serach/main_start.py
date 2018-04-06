# -*- coding: utf-8 -*-

"""
聚类相似域名，并产生其他相似域名
"""
from load_domains import load_cur_domains
from similar_domain_cluster import cluster
from generate_valid_domain import generate_similar_domains

def main(max_ct):
    #将配置文件中的测试项更改为正式,开始运行
    import time
    count = 0
    while int(max_ct)>count:
        print "%dth generate similar domains..."%count
        domains = load_cur_domains(config_domains=True)
        cluster(domains)
        generate_similar_domains(
            config_modes=True,
            threads_num=10
        )
        count+=1
        print 'sleep 2 hours...'
        time.sleep(7200)

def exper_main():
    # 将配置文件中的测试项置为True,开始运行
    from load_domains import load_samples
    from datetime import datetime
    t1 = datetime.now()
    domains = load_samples()
    cluster(domains)
    generate_similar_domains(
        config_modes=True,
        threads_num=10
    )
    t2 = datetime.now()
    print t2 - t1

if __name__ == "__main__":
    exper_main()