# Mysql 锁相关内容

------

## 锁相关内容

摘自[mysql解锁与锁表](https://www.cnblogs.com/wanghuaijun/p/5949934.html)

mysql**不同的存储引擎支持不同的锁机制**。比如，MyISAM和MEMORY存储引擎采用的是表级锁（table-level locking）；BDB存储引擎采用的是页面锁（page-level locking），但也支持表级锁；InnoDB存储引擎既支持行级锁（row-level locking），也支持表级锁，但默认情况下是采用行级锁。

* MySQL这3种锁的特性可大致归纳如下：**开销、加锁速度、死锁、粒度、并发性能**
 
    * 表级锁：开销小，加锁快；不会出现死锁；锁定粒度大，发生锁冲突的概率最高,并发度最低。
 
    * 行级锁：开销大，加锁慢；会出现死锁；锁定粒度最小，发生锁冲突的概率最低,并发度也最高。
 
    * 页面锁：开销和加锁时间界于表锁和行锁之间；会出现死锁；锁定粒度界于表锁和行锁之间，并发度一般。


### MyISAM表锁
MyISAM存储引擎**只支持表锁**，这也是MySQL开始几个版本中唯一支持的锁类型。随着应用对事务完整性和并发性要求的不断提高，MySQL才开始开发基于事务的存储引擎，后来慢慢出现了**支持页锁的BDB存储引擎**和**支持行锁的InnoDB存储引擎**（实际 InnoDB是单独的一个公司，现在已经被Oracle公司收购）。但是MyISAM的表锁依然是使用最为广泛的锁类型。接下来将详细介绍MyISAM表锁的使用。

* 查询表级锁争用情况

可以通过检查**table_locks_waited**和**table_locks_immediate**状态变量来分析系统上的表锁定争夺：
```mysql
mysql> show status like 'table%';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| Table_locks_immediate | 2979  |
| Table_locks_waited    | 0     |
+-----------------------+-------+
2 rows in set (0.00 sec))
```
如果**Table_locks_waited的值比较高，则说明存在着较严重的表级锁争用情况**。

 
* 获取InnoDB行锁争用情况    
可以通过检查**InnoDB_row_lock**状态变量来分析系统上的行锁的争夺情况：

```mysql
mysql> show status like 'innodb_row_lock%';
+-------------------------------+-------+
| Variable_name                 | Value |
+-------------------------------+-------+
| InnoDB_row_lock_current_waits | 0     |
| InnoDB_row_lock_time          | 0     |
| InnoDB_row_lock_time_avg      | 0     |
| InnoDB_row_lock_time_max      | 0     |
| InnoDB_row_lock_waits         | 0     |
+-------------------------------+-------+
5 rows in set (0.01 sec)

```

## mysql锁状态查看

* show processlist; 列出进程(前100条）

mysql show processlist命令详解http://www.cnblogs.com/JulyZhang/archive/2011/01/28/1947165.html

* show full processlit; 列出所有的进程

* show open tables;


    * 这条命令能够查看当前有**哪些表是打开的**

    * In_use列表示有**多少线程正在使用某张表**
    
    * Name_locked表示表名**是否被锁**，这一般发生在Drop或Rename命令操作这张表时。

    * 所以这条命令不能帮助解答我们常见的问题：当前某张表是否有死锁，谁拥有表上的这个锁等。
    
* show status like ‘%lock%; 查看服务器状态

*  show engine innodb status; 查看innodb运行时的引擎信息

* show variables like ‘%timeout%’; 查看服务器配置参数

## mysql解锁

* 第一种

```mysql
show processlist;
# 找到锁进程，kill id ;
```

 

* 第二种

```mysql
mysql>UNLOCK TABLES;
```

**锁表**

* 锁定数据表，避免在备份过程中，表被更新
```mysql
mysql>LOCK TABLES tbl_name READ;
```

* 为表增加一个写锁定：
```mysql
mysql>LOCK TABLES tbl_name WRITE;
```
