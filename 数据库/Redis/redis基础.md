# Redis 基础

------

在ubuntu安装redis后，通过**redis-server**运行起redis服务器，再运行**redis-cli**运行起redis客户端，由此可进行命令操作。

* redis 键

```redis
# 设置键值为runoobkey，值为redis
redis 127.0.0.1:6379> SET runoobkey redis
OK

# 获取某个键对应value
redis 127.0.0.1:6379> GET runoobkey
"redis"

# 删除某个键
redis 127.0.0.1:6379> DEL runoobkey
(integer) 1
```

* redis 字符串

```
# 获取某个键对应value
redis 127.0.0.1:6379> GET runoobkey
"redis"
```

其他略去

* redis hash

Redis hash 是一个string类型的field和value的映射表，hash特别适合用于存储对象

```redis
# 设置键名为run，对应的name是"redis tutorial"，description是"redis basic commands for caching"  ... 
127.0.0.1:6379> HMSET run name "redis tutorial" description "redis basic commands for caching" likes 20 visitors 23000

# 获取name的内容
127.0.0.1:6379> HGET run name
"redis tutorial"

# 查看所有内容
127.0.0.1:6379> HGETALL run
1) "name"
2) "redis tutorial"
3) "description"
4) "redis basic commands for caching"
5) "likes"
6) "20"
7) "visitors"
8) "23000"



```

