# Tornado整理

------


关于**MVC**的一些基本概念不再细说，这里直接整理一些以前自己模糊的概念；

使用Tornado时，整体框架如下：
```
/.
|
handlers
|
methods
|
statics
|
templates
|
application.py
|
server.py
|
url.py
```
基于如上的架势，后面的事情就是在这个基础上添加具体内容了

上述每个目录和文件的作用（当然，可以进行响应的改动）：

* handlers：这个文件夹中放所谓的后端 Python 程序，**主要处理来自前端的请求，并且操作数据库。**

* methods：这里准备放一些**函数或者类**，比如用的最多的读写数据库的函数，这些函数**被 handlers 里面的程序**使用。

* statics：这里准备放一些**静态文件**，比如图片，css 和 javascript 文件等。
* templates：这里放**模板文件，都是以 html 为扩展名的，它们将直接面对用户**。

* url.py文件
```python
#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""

import sys     #utf-8，兼容汉字
reload(sys)
sys.setdefaultencoding("utf-8")

from handlers.index import IndexHandler    #假设已经有了

url = [
    (r'/', IndexHandler),
]
```
url.py 文件主要是**设置网站的目录结构**。

from handlers.index import IndexHandler，虽然在 handlers 文件夹还没有什么东西，为了演示如何建立**网站的目录结**构，假设在 handlers 文件夹里面已经有了一个文件 index.py，它里面还有一个类 IndexHandler。在 index.py 文件中，将其引用过来。

变量 url 指向一个列表，在列表中列出**所有目录和对应的处理类**。比如 (r'/', IndexHandler),，就是约定网站**根目录index.html的处理类是 IndexHandler**，即来自这个目录的 **get()** 或者 **post()** 请求，均有 **IndexHandler 类中相应方法来处理。**

其他目录的方法，如上同理可得。

* application.py
```python
#!/usr/bin/env Python
# coding=utf-8

from url import url

import tornado.web
import os

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "statics"),
    debug = True,
    cookie_secret = '*****************************'
    )

application = tornado.web.Application(
    handlers = url,
    **settings
    )

```
applicaion.py完成了**对网站系统的基本配置，建立网站的请求处理集合**。

from url import url 是**将 url.py 中设定的目录引用过来**。

**setting **引用了一个字典对象，里面约定了**模板和静态文件的路径**，即声明已经建立的文件夹"templates"和"statics"分别为模板目录和静态文件目录；此外，setting 中还有 debug、cookie_secret等选项；

接下来的 application 就是一个**请求处理集合对象**。请注意 tornado.web.Application() 的参数设置：
```
tornado.web.Application(handlers=None, default_host='', transforms=None, **settings)
# handlers指向设定目录的文件
# **settings 即为上述文件中设定的settings
```

* server.py
这个文件的作用是**将 tornado服务器运行起来，并且囊括前面两个文件中的对象属性设置**。

```python
#!/usr/bin/env Python
# coding=utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver

from application import application

from tornado.options import define, options

define("port", default = 8000, help = "run on the given port", type = int)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print "Development server is running at http://127.0.0.1:%s" % options.port
    print "Quit the server with Control-C"

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
    
```
**如上，就完成了tornado的相关全部基本架构内容**。

此后，不进行系统整理，进行逐个点的整理：

* 1.在templates中的html里引用statics/js下d的javascript文件时，距离说明格式如下（这样不易有路径错误）：
```html
<script src="{{static_url("js/jquery.min.js")}}"></script>
<script src="{{static_url("js/文件名.js")}}"></script>
```

* 2.jquery的获取：[官网https://jqueryui.com/）](https://jqueryui.com/）)下载即可。

* 3.handlers、methods都将被作为模块引用，因此需要在文件夹下加入**空文件__init__.py**。

* 4. handlers文件夹内每个具体页面的py文件，都有**class 页面名Handler**的一个类，以index.html的handler为例进行说明：

```python
# coding=utf-8
import tornado.web

'''
当访问根目录的时候（不论输入 localhost:8000，还是 http://127.0.0.1:8000，或者网站域名），
就将相应的请求交给了 handlers 目录中的 index.py 文件中的 IndexHandler 类的 get() 方法来处理，
'''

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        '''
        处理get请求
        '''
        name = 'Lucy'
        # self.render("index.html", user=name)
        self.render("index.html") # 向请求者反馈网页模板，并且可以向模板中传递数值
        # good_id = self.get_argument('id') # get也可以获得参数，但是参数从url获取

    def post(self):
        '''
        处理post请求（请求可在js中由ajax发出）
        '''
        name = self.get_argument("name") # 获取参数
        job = self.get_argument("job")
        print 'job is ' + str(job)
        self.write("welcome you: " + name) # 不做处理的话，会直接通过js弹窗弹出显示
        # self.write(username) # 后端向前端返回数据。这里返回的实际上是一个字符串，也可返回 json 字符串
        
```

