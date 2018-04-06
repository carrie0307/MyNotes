# mysql_mode

------

## SQL mode

* SQL Mode 定义了两个方面
    * MySQL应支持的SQL语法 (SQL语法支持类)
    
    * 应该在数据上执行何种确认检查 （数据检查类）

* [官方手册对sql mode的描述](https://dev.mysql.com/doc/refman/5.6/en/sql-mode.html)

* [Mysql sql_mode说明及引起的相关问题](http://seanlook.com/2016/04/22/mysql-sql-mode-troubleshooting/)

* [Mysql升级5.7后GROUP BY 出错](http://www.520sz.com/mysql-5-7-10-group-by-error.html)

* [Mysql5.7 默认打开 Only_full_group_by 的问题与解决方案](https://blog.csdn.net/Peacock__/article/details/78923479)

## 问题描述

今天在mysql 5.7 执行如下sql语句时，出现了报错信息：

```sql
SELECT domain,any_value(ip),count(*) FROM domain_ip_relationship GROUP BY domain;
```

* 报错

```
Expression #3 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'cash.sdb_login_log.id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

* 报错信息核心解释

由于sql_model=only_full_group_by的限制了，导致在以往MYSQL版本中能正常查询的SQL，在5.7不能用，这里具体来说就是**select的列都要在group中，或许本身是聚合列（SUM,AVG,MAX,MIN）才行**

* ONLY_FULL_GROUP_BY(SQL语法支持类) 解释

对于GROUP BY聚合操作，如果在SELECT中的列、HAVING或者ORDER BY子句的列，没有在GROUP BY中出现，那么这个SQL是不合法的。是可以理解的，因为不在 group by 的列查出来展示会有矛盾。


## 解决方法

* 方法一：any_value

MySQL的**any_value(field)函数，主要的作用就是抑制ONLY_FULL_GROUP_BY值被拒绝**。当语句修改为如下时，没有出现错误。

```sql

SELECT domain,any_value(ip),count(*) from domain_ip_relationship group by domain;
```

* 方法二：修改sql_mode

```
#查看sql_mode的语法
select @@GLOBAL.sql_mode;
select @@SESSION.sql_mode;
```


```
#修改sql_mode的语法
SET GLOBAL sql_mode = 'modes';
SET SESSION sql_mode = 'modes';
# 或者 set sql_model=‘’;
```




