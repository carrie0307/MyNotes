#coding=utf-8
from pymongo import *
import json



'''建立连接'''
client = MongoClient()
# 以下方法也可以
client = MongoClient('localhost', 27017)
# client = MongoClient(“mongodb://localhost:27017/”)
'''指定要操作的database和collection'''
db = client.my_test
collection = db.basic_info
'''方法二'''
collection = db['basic_info']
# ‘-’出现在表名时，用方法一无法实现会有误，方法二可以


'''常规操作（以函数来表示）'''
def mongo_insert(collection, mydict):
    '''
    插入操作
    '''
    # e.g. mydict = {'name':'Lucy', 'sex':'female','job':'nurse'} 以此为例子说明
    collection.insert(mydict)
    # collection.insert_one(mydict)
    # collection.insert_many(mydict) # 会报错，.insert_many()时参数必须为 list 形式，做如下包装：
    # mylist = []
    # mylist.append(mydict)
    # collection.insert_many(mylist) # 不会报错


def mongo_query(db, collection,mydict):
    '''
    查询操作
    '''
    # e.g. mydict = {'name': 'Lucy'}
    result = collection.find(mydict)
    '''用for in 便利得到逐项内容，也可以用collection.find(mydict)[index]来获取'''
    # for item in result:
        # print item
    # collection.find_one(mydict)
    '''统计结果总条数'''
    # collection.find().count()
    '''指定大于小于等于等条件进行查询  $lt（小于）， $gt（大于）， $lte（小于等于）， $gte（大于等于）， $ne（不等于）'''
    # collection.find({'age': {'$lt': 30}})
    '''将查询结果按条件排序'''
    # collection.find().sort("age")  # 默认，升序
    # collection.find().sort("age", pymongo.ASCENDING)   # 升序
    # collection.find().sort("age", pymongo.DESCENDING)  # 降序
    '''查询 database中所有collection, 这里的 db 为建立连接后的db = client.test_db '''
    # db.collection_names()
    # db.collection_names(include_system_collections = False): # 不包括系统collection，一般指的是system.indexes
    '''选择性显示，eg.只显示domain的内容'''
    # 注意，id是默认选择的，需要用False说明才可以不显示
    db.collection.find({},{'domain':True, '_id':False})
    '''distinct去重: {}内直接写要选择的字段名即可'''
    dn.collection.distinct({'auth_icp.icp'})
    '''模糊查询(类似sql中的like)'''
    # 查询包含A的记录： SELECT * FROM UserInfo WHERE userName LIKE "%A%"
    db.collection.find({'domain':/A/})
    # 查询以A开头的记录：SELECT * FROM UserInfo WHERE userName LIKE "A%"
    db.collection.find({'domain':/^A/})
    # 查询以A结尾的记录：SELECT * FROM UserInfo WHERE userName LIKE "%A"
    db.collection.find({'domain':/A$/})
    # 查询中如果要匹配'.',需要转义为'\.'
    '''其他模糊查询，需要通过正则表达式实现, regex是实际匹配的正则表达式，同python'''
    db.collection.find({'domain':{'$regex':regex}})
    '''按照某个字段是否存在查询，eg.domain是否存在'''
    db.collection.find({'domain':{'$exists':True}}) # 在mongo中可以将True写作1
    '''
        聚合:group by
        '_id'： 是根据聚合的字段，注意字段要有'$'表示
        'count'： 是自己设定的新的字段名
        {'$sum':1} 是count的属性值，这里表示计算总和
        {$sort}表示对哪个字段采取怎样的排序方式
        注意： aggregate的条件是在列表[]中的

        如下是根据asn字段聚合，并将结果根据count降序排列

        $sum 还可以是 $max, $min, $ave等，具体其他参数与含义参见http://www.runoob.com/mongodb/mongodb-aggregate.html
    '''
    db.collection.aggregate([{'$group':{'_id':'$asn','count':{'$sum':1}}},{'$sort':{'count':-1}}])
    '''另一个例子'''
    db.term.aggregate([
     {$match:{library_id:3607}},
     {$limit:5},
     {$group:{_id:"$version", count: {$sum:1}}},
     {$sort:{count:-1}}
     ])







def mongo_update(collection,condition, set_content):
    '''
    更新操作
    eg. db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}})
    '''
    # condition = {'name': 'Lucy'}
    # set_content = {'$set': {'job':'teacher'}}
    collection.update(condition, set_content)
    '''以上语句只会修改第一条发现的文档，如果你要修改多条相同的文档，则需要设置 multi 参数为 true。'''
    # db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}},{multi:true})
    '''在python里面直接写multi=True即可'''
    # db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}},multi=True)
    '''更新方法二'''
    # temp = collection.find_one({"name":"Lucy"})
    # temp2 = temp.copy()
    # temp["name"] = "Jordan"
    # collection.save(temp)   //或 .update() ，注意参数形式collection.update(temp, temp2)
    '''嵌套时的set：{"_id":"0000001", "hobby":{"piano":"good", "violin":"bad"}}'''
    # collection.update(condition, {'$set': {'hobby.violin':'very good'}})



def mongo_remove(collection,condition):
    '''
    删除操作
    '''
    # condition = {'name':'Luct'}
    # collection.remove(condition)  # 这样会将符合条件的全部删除，删除一条的参数试验后仍旧有误
    '''删除方法二'''
    # temp = collection.find_one(condition)
    # collection.remove(temp) # 即便该temp不存在也不会报错,且如果temp只有一条，则就只删除一条
    # collection.delete_one(temp)


def json_operate(collection,condition):
    '''
    对查询结果进行json操作
    json序列化:json.dumps(i)
    对应的反序列化: json.loads()
    '''
    # condition = {'name': 'Lucy'}
    result = collection.find(condition)
    for i in result:
        del i['_id']    # 不能直接转换，无法识别ObjectId


if __name__ == '__main__':
    mydict = {'name':'Lucy', 'sex':'female','job':'nurse'}
    # mongo_insert(collection, mydict)
    # find_dict = {'name': 'Lucy'}
    # mongo_query(db, collection, find_dict)
    # condition = {'name': 'Lucy'}
    # set_content = {'$set': {'job':'teacher'}}
    # mongo_update(collection,condition, set_content )
    # mongo_remove(collection,condition)
    # json_operate(collection,condition)
