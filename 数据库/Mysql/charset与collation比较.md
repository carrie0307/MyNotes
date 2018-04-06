# Mysql： charset 与 collation

## 定义 (来自Mysql5.7文档)

[Mysql 5.7文档](https://dev.mysql.com/doc/refman/5.7/en/charset-general.html)

* A character set is a set of symbols and encodings. 
字符集是一组符号和编码。 

* A collation is a set of rules for comparing characters in a character set
排序规则是一组用于比较字符集中的字符的规则

## charset 和 collation 

charset 和 collation有多个级别的设置：服务器级、数据库级、表级、列级和连接级

```mysql
 mysql> show variables like '%character%';  
 
+--------------------------+-------------------------------------------------------  
| Variable_name            | Value  
+--------------------------+-------------------------------------------------------  
| character_set_client     | utf8  
| character_set_connection | utf8  
| character_set_database   | latin1  
| character_set_filesystem | binary  
| character_set_results    | utf8  
| character_set_server     | latin1  
| character_set_system     | utf8  
| character_sets_dir       | D:\database\mysql\mysql-5.5.25-winx64\share\charsets\  

```
在这里可以看到，有服务器层面、连接层面、数据库层面、文件系统层面的编码方式；


## 

```mysql
 mysql> show variables like '%collation%';  
 
+----------------------+-------------------+  
| Variable_name        | Value             |  
+----------------------+-------------------+  
| collation_connection | utf8_general_ci   |  
| collation_database   | latin1_swedish_ci |  
| collation_server     | latin1_swedish_ci |  
+----------------------+-------------------+  

```

* collation是基于某种编码方式进行字符比较的规则

* 可以看到，默认**collation_connection = utf8_general_ci   大小写不敏感校验规则**；
