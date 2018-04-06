# Ajax基础整理

------

## POST
**基础代码**
```javascript
$.ajax({
      type:"post",
      
       //要请求的url
      url:"/ip_scatter_off",
      
      //通过post传递的数据，注意一定要以这样的“字典”形式传递
      data:{ 
            'domain':'baidu.com',
            'id':'001'
            },
            
      cache:false,
      
      success:function(data1){
          /*
            成功后所执行的代码
            data1是从ip_scatter_off页面获得的数据
          */
          deal_data(data1);
      },
      error:function(){
          /*
          post失败所执行的代码
          */
      
          alert("error!");
      },
});

```
以以上代码为例，如果对应tornado框架，对应的handler如下，注意post函数：

```python
# coding=utf-8
import tornado.web
from methods.db_operation import ip_change

class ipScatter_OffHandler(tornado.web.RequestHandler):
    def get(self):
        ip_change_res = ip_change('www-4s.cc')

        self.write(ip_change_res)

    def post(self):
        # 根据data中的Key获取参数
        domain = self.get_argument('domain')
        ip_change_res = ip_change(domain)
        # 这是写给ip_scatter_of页面post的数据，也就是js中data1所获得的
        self.write(ip_change_res) 

```

## GET

#### 无参数传递
**基础代码**
```javascript
$.ajax({
    type:"get",
    url:"/ip_scatter_off",
    cache:false,
    success:function(data1){
        /*
        请求成功后所执行的代码
        
        data1即是所请求页面上的全部内容
        */
        deal_data(data1);

    },
    error:function(){
    /*
        请求失败后所执行的代码
    */
        alert("error!");
    },

});
```
以上代码为例，如果对应tornado框架，对应的handler如下，注意get函数：

```python
# coding=utf-8
import tornado.web
from methods.db_operation import ip_change

class ipScatter_OffHandler(tornado.web.RequestHandler):
    def get(self):
        ip_change_res = ip_change('www-4s.cc')
        # 如果页面原本为空，write()函数内容就是js的data1的内容
        self.write(ip_change_res) 

    def post(self):
        # 根据data中的Key获取参数
        domain = self.get_argument('domain')
        ip_change_res = ip_change(domain)
        # 这是写给ip_scatter_of页面post的数据，也就是js中data1所获得的
        self.write(ip_change_res) 
```
