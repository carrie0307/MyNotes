# 启动与停止相关整理

## 一篇文章
http://blog.csdn.net/wangqing_12345/article/details/77527182

说明的一点，当自动安装时，一般不用指定--dbpath和--logpath，系统会自动指定并写入在mongodb.conf。当显示读取不到--dbpath,--logpath时，需要手动令启动时读取mongodb.conf文件，从而获得--dbpath和--logpath，命令：/usr/loca/mongodb/bin/mongod -f mongodb.conf


## 推荐启动方式

* https://www.jianshu.com/p/f179ce608391


* https://www.jianshu.com/p/9a7ede7c47f5

* 命令: **mongod -f /etc/mongod.conf**

* 在启动后，本地可以通过"mongo"命令登录；

* 关于远程连接
    * 配置IP问题，可参见https://blog.csdn.net/R28_11/article/details/50222669

    * mongod.lock问题: 删掉数据文件夹下的mongod.lock(https://blog.csdn.net/lg_lin/article/details/47706665)


## 停止运行

* https://www.jianshu.com/p/9a7ede7c47f5

* 建议方式：本地登录后，通过"use admin"切换权限；然后通过"db.shutdownServer();"关闭mongo服务器；

* 尽量服务器关闭等问题导致的强关，mongod.lock问题往往由此引起。

## 数据文件恢复

虽然这次恢复失败了，但是找到两篇可参考的文章，记录如下

* mongodb数据恢复https://ruby-china.org/topics/16432

* mongo数据文件备份与恢复https://blog.csdn.net/shmnh/article/details/41921979

## 关于Mongo自动化备份

* https://blog.csdn.net/zwq912318834/article/details/77280573

* http://www.cnblogs.com/geekma/p/4820247.html

## 关于配置文件

* 可通过mongod --help查看各个参数含义；

* [官网对各参数定义](https://docs.mongodb.com/manual/reference/configuration-options/)。比较建议以官网信息为主，尤其是格式和参数名称(这次遇到的问题:"bind_ip"的写法已经不是"bind_ip",而是"bindIp",这一改变mongd --help没有列出，但官网文档是有的)


## 另外
* 关于之前屡次重启失败在日志中找到的记录"shuting down with code 62"，解决方案来自https://stackoverflow.com/questions/47850004/mongodb-shutting-down-with-code62

* mongo官方对于各种异常code的说明:https://docs.mongodb.com/manual/reference/exit-codes/

