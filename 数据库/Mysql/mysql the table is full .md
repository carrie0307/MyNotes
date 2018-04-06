# Mysql:The table is full

------

## 查看Mysql下各个表占用硬盘大小

打开MySQL的 information_schema 数据库。在该库中有一个 TABLES 表，其中的主要字段：

* TABLE_SCHEMA : 数据库名

* TABLE_NAME：表名

* ENGINE：所使用的存储引擎

* TABLES_ROWS：记录数

* DATA_LENGTH：数据大小

* INDEX_LENGTH：索引大小

* 表的大小 = 数据大小 + 索引大小

```sql
SELECT TABLE_NAME,DATA_LENGTH+INDEX_LENGTH,TABLE_ROWS FROM TABLES WHERE TABLE_SCHEMA='数据库名' AND TABLE_NAME='表名'
```

### 查看数据库中表的基本信息

```sql
SHOW TABLE STATUS IN db;
```


## 原因1：磁盘空间满

```shell
df -h
```

## 原因2: 超过了配置文件中表大小的显示

配置文件: my.cnf

```shell
locate my.cnf
```
查看配置文件中对表容量的限制，然后进行修改即可。

* tmp_table_size = 256M

* max_heap_table_size = 256M
