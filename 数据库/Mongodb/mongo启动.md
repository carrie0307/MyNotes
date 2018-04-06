http://blog.csdn.net/wangqing_12345/article/details/77527182

说明的一点，当自动安装时，一般不用指定--dbpath和--logpath，系统会自动指定并写入在mongodb.conf。当显示读取不到--dbpath,--logpath时，需要手动令启动时读取mongodb.conf文件，从而获得--dbpath和--logpath，命令：/usr/loca/mongodb/bin/mongod -f mongodb.conf
