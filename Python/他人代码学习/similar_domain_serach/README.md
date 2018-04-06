# similar_domain_search

------

## 代码结构说明
.
├── config_file.py      // 基础配置文件

├── divide_items.py    // 根据线程数量对待处理域名分组

├── domain_match_rule.py    // 域名相似性判断与获取枚举模式

├── exper_file

│   ├── cur_modes.pkl

│   ├── old_modes.pkl

│   └── www577789.com_sample.pkl

├── generate_valid_domain.py   // 根据枚举模式生成并验证新域名

├── gevent_model.py           // gevent 模型

├── load_domains.py           

├── load_file

│   └── existed_domains.pkl

├── load_modes.py


├── main_start.py            // 主函数

├── req_file

│   ├── dns_servers.txt     // dns服务器列表

│   └── tld_list.pkl        // 顶级域列表

└── similar_domain_cluster.py   // 根据域名相似性聚类(生成mode)
