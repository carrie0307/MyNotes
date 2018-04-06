# Mongo相关内容

---

## 基本操作

基本操作见 mongo_test.py

## 备份与恢复

#### 备份

在本地使用 27017 启动你的mongod服务。打开命令提示符窗口，进入MongoDB安装目录的bin目录输入命令mongodump:

>mongodump

```
mongodump -h dbhost -d dbname -o dbdirectory
```

#### 恢复

```
mongorestore -h <hostname><:port> -d dbname <path>
```

## 引用式关系

引用式关系是设计数据库时经常用到的方法，假设有用户数据和用户地址两类数据，则这种方法会**把两类数据分开，通过引用文档的 id 字段来建立关系**。

```python
{
   "_id":ObjectId("52ffc33cd85242f436000001"),
   "contact": "987654321",
   "dob": "01-01-1991",
   "name": "Tom Benzamin",
   "address_ids": [
      ObjectId("52ffc4a5d85242602e000000"),
      ObjectId("52ffc4a5d85242602e000001")
   ]
}
```

以上实例中，用户文档的 address_ids字段包含用户地址的对象id（ObjectId）数组。

我们可以读取这些用户地址的对象id（ObjectId）来获取用户的详细地址信息。

这种方法需要**两次查询**，第一次查询用户地址的对象id（ObjectId），第二次通过查询的id获取用户的详细地址信息。

```python
result = db.users.findOne({"name":"Tom Benzamin"},{"address_ids":1})
addresses = db.address.find({"_id":{"$in":result["address_ids"]}})
```

## 索引

#### ensureIndex() 方法

* mongo使用ensureIndex() 来创建索引，语法格式如下：

```
db.COLLECTION_NAME.ensureIndex({KEY:1})
```

语法中 Key 值为你要创建的索引字段，1为指定按升序创建索引，-1为降序




* 创建单个索引

```
db.collection.ensureIndex({a:1})
```

在a字段上创建一个升序的索引(对于单个字段的索引，升序或是降序都一样)。

* 创建复合索引

```
db.collection.ensureIndex({a:1,b:-1})
```

* 创建稀疏索引
```
db.collection.ensureIndex({a:1},{sparse:true})
```

索引中将**不包含没有a字段**的文档。


* 创建唯一索引

```
db.collection.ensureIndex({a:1},{unique:true})
```

为a字段建立唯一索引。

* 当mongo要索引一个字段时，如果一篇文档中没有这个字段，这篇文档就会被索引为null，因为唯一索引不能有重复值，所以**必须和稀疏索引配合使用**，如：

```
db.collection.ensureIndex({a:1},{unique:true,sparse:true})
```

* 复合索引也可以加唯一限制，如：

```
db.collection.ensureIndex({a:1,b:1},{unique:true})
```

* 在后台创建索引

```
db.collection.ensureIndex({a:1},{background:true})
```

* 丢弃重复数据

要强制在一个**有重复数据的字段上创建唯一索引**，可以使用dropDups选项，这会强制mongo在创建唯一索引时**删除重复数据（危险操作）**，如：

```
db.collection.ensureIndex({a:1},{dropDups:true})
```

* 查看某个**库上**的所有索引

```
db.system.index.find()
```

* 查看某个**表上**的所有索引

```
db.collection.getIndexes()
```


* 删除表上的**某个**索引

```
db.collection.dropIndex({a:1})
```

* 删除表上的**所有**索引

```
db.collection.dropIndexes()
```
 
* 重建索引

```
db.collection.reIndex()
```

* 参考文章

[菜鸟教程](http://www.runoob.com/mongodb/mongodb-indexing.html)

[mongo索引小结](http://sdu-wizard.iteye.com/blog/1771611)

[mongo索引相关知识](https://www.cnblogs.com/zhoujinyi/p/4665903.html)

## 查询分析

#### expalin

```
db.users.find({gender:"M"},{user_name:1,_id:0}).explain()
```

结果集中几个重要字段：

* indexOnly: 如果为 true ，表示我们使用了索引。

* cursor：
    
    * 如果**使用了索引**，MongoDB 中索引存储在**B树结构**中，所以是 BtreeCursor 类型的游标

    * 如果**没有使用索引，游标的类型是BasicCursor**
    
    * 这个键还会给出你所使用的索引的名称，你通过这个名称可以查看当前数据库下的system.indexes集合（系统自动创建，由于存储索引信息，这个稍微会提到）来得到索引的详细信息。
    
    * n：当前查询返回的文档数量。

    * nscanned/nscannedObjects：表明当前这次查询一共扫描了集合中多少个文档，我们的目的是，让这个数值和返回文档的数量越接近越好。

    * millis：当前查询所需时间，毫秒数。

    * indexBounds：当前查询具体使用的索引

#### hint

**强制 MongoDB 使用一个指定的索引**，例如，指定了使用 gender 和 user_name 索引字段来查询：

```
db.users.find({gender:"M"},{user_name:1,_id:0}).hint({gender:1,user_name:1})
```

## 数据库设计

#### 范式化 -- 完全分离(更新效率高)

```
{
     "_id" : ObjectId("5124b5d86041c7dca81917"),
     "title" : "如何使用MongoDB", 
      "author" : [ 
               ObjectId("144b5d83041c7dca84416"),
              ObjectId("144b5d83041c7dca84418"),
              ObjectId("144b5d83041c7dca84420"),
     ]
 }

```

位作者的信息需要修改时，范式化的维护优势就凸显出来了，我们无需考虑此作者关联的图书，直接进行修改此作者的字段即可。

#### 反范式化 -- 完全内嵌(查询效率高)

```

View Code
{
       "_id" : ObjectId("5124b5d86041c7dca81917"),
       "title" : "如何使用MongoDB",
       "author" : [
                {
                    　　　　 "name" : "丁磊"
                   　　　　  "age" : 40,
                     　　　　"nationality" : "china",
                },
                {
                   　　　　  "name" : "马云"
                  　　　　   "age" : 49,
                   　　　　  "nationality" : "china",
                },
                {
                   　　　　  "name" : "张召忠"
                  　　　　   "age" : 59,
                  　　　　   "nationality" : "china",
                },
      ]
  }

```

在查询的时候直接查询图书即可获得所对应作者的全部信息，但因一个作者可能有多本著作，当修改某位作者的信息时时，我们需要遍历所有图书以找到该作者，将其修改。

#### 不完全范式化 -- 部分内嵌

```

{
       "_id" : ObjectId("5124b5d86041c7dca81917"),
       "title" : "如何使用MongoDB",
       "author" : [ 
               {
                     　　　　"_id" : ObjectId("144b5d83041c7dca84416"),
                   　　　　  "name" : "丁磊"
                },
                {
                    　　　　 "_id" : ObjectId("144b5d83041c7dca84418"),
                  　　　　   "name" : "马云"
                },
                {
                    　　　　 "_id" : ObjectId("144b5d83041c7dca84420"),
                   　　　　  "name" : "张召忠"
                },
      ]
  }

```

这种方式，既保证了查询效率，也保证的更新效率。但这样的方式显然要比前两种较难以掌握，难点在于需要与实际业务进行结合来**寻找合适的提取字段**。如同示例3所述，名字显然**不是一个经常修改的字段**，这样的字段如果提取出来是没问题的，但如果提取出来的字段是一个**经常修改的字段（比如age）的话，我们依旧在更新这个字段时需要大范围的寻找并依此进行更新**。

**上面三个示例中，第一个示例的更新效率是最高的，但查询效率是最低的，而第二个示例的查询效率最高，但更新效率最低**


参考自[mongodb高级篇 -- 性能优化](http://www.jianshu.com/p/b77a33fbe824)

## 主键

* mongo默认_id为主键，当需要自定义主键值时，在insert时直接令 _id是所需要的值即可；

* mongo数据库要求必须有_id字段，即不可修改 _id字段名

## mongo优化

#### 监控找出慢语句

* mongodb可以通过profile来监控数据，进行优化

```python

# 命令来实时配置
db.setProfilingLevel(级别)   

'''
level有三种级别
0 – 不开启
1 – 记录慢命令 (默认为>100ms)
2 – 记录所有命令
'''

#设置级别
drug:PRIMARY> db.setProfilingLevel(2)

#设置级别和时间
drug:PRIMARY> db.setProfilingLevel(1,200)
{ "was" : 2, "slowms" : 100, "ok" : 1 }

db.getProfilingLevel()命令来获取当前的Profile级别

# 关闭Profiling
drug:PRIMARY> db.setProfilingLevel(0)

```

* 查看profile的结果

自己本机上未试验

```
db.system.profile.find(); 

db.system.profile.find({millis:{$gt:500}})
```

#### expalin & hint

见上 (可以用explain对慢语句进行分析)

#### 索引

* 为指定按**升序**创建索引，若以降序来创建索引指定为-1即可。

```
>db.col.ensureIndex({"title":1})
```

* 复合索引

ensureIndex() 方法中也可以设置多个字段创建索引（关系型数据库中称作复合索引）。
```
>db.col.ensureIndex({"title":1,"description":-1})

```

#### 数据库设计

见上

#### 读写分离


#### 热数据法


---

有关索引的其他内容（索引注意事项、索引对性能的优化） 以及性能优化的其他方法，之后整理。

2017.11.21




