# Ubuntu上mongo安装记录

------


## 基本安装步骤

* 注：以root去安装(sudo su 输入密码进入root； 在服务器上root安装root启动，能避免很多由于权限导致的问题)

* [官方文档](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

* [简书一篇参考文章](https://www.jianshu.com/p/5598f1dcbb98)

## sudo apt-get install -y mongodb-org 后的说明

* 以上步骤完成后，会默认设置日志和数据存储文件夹是`/var/lib/mongodb`和`/var/log/mongodb`

* 启动
    ```
    sudo service mongod start
    ```
    
* 可能出现的异常
    ```
    Failed to start mongod.service: Unit mongod.service not found
    ```
    
* 解决：
    * [参考自](https://askubuntu.com/questions/921753/failed-to-start-mongod-service-unit-mongod-service-not-found?rq=1)
    * 
    ```
    sudo systemctl enable mongod
    sudo service mongod restart
    ```

* 检测是否启动成功

    * 在日志`/var/log/mongodb/mongod.log`看是否有如下记录：
    ```
    [initandlisten] waiting for connections on port 27017
    ```

    * 查看进程
    
    ```shell
    ps -ef | grep mongo
    root     23945 23931  0 17:03 pts/4    00:00:00 grep --color=auto mongo
root     28249     1 32 Apr08 ?        1-22:38:47 mongod -f /etc/mongodb.conf
    ```
    
    这样即可说明mongo已在运行了。


* 本地连接测试

```
mongo --host 127.0.0.1:27017
```

* 其他主机连接测试

    * 自己在安装时遇到的问题是，本机可以连接，但其他主机无法连接。根据资料应当修改配置文件，即`root     28249     1 32 Apr08 ?        1-22:38:47 mongod -f /etc/mongodb.conf`中的mongodb.conf

    * 参考资料：[如何让其他主机连接Mongodb](https://segmentfault.com/q/1010000002923686)

    * 但实际解决问题时，将`mongodb.conf`中bind_ip设置为0.0.0.0导致了本机也无法访问。于是查看了已运行的mongo服务器的配置文件，将`bind_ip=127.0.0.1`和`port=27017`都注释掉后，实现了其他主机的连接[补充，在6月13号服务器重启后无法远程连接时,将bind_ip改为了0.0.0.0恢复了远程连接，非常玄学。。。]。 
    
    * 注： 修改配置文件后，sudo service mongod restart 重新启动服务器。
    
    


