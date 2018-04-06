# 学到的东西

------

## 设置集合的方法

```python
'''
注意以下2种区别
'''

a = 'test'
set_a = {a}
print set_a
>>>set(['test'])

set_b = set(a)
print set_b
>>> set(['s', 'e', 't'])
```

## 元组可以做字典的键值

## 字符串结尾

```python
test_str = 'aaaabcd'
if test_str.endswith('bcd'):
    print 'ok'

>>> ok
```

## 文件flush

* 关于flush与write：http://blog.csdn.net/fenfeiqinjian/article/details/49444973

* 一般的文件流操作都包含**缓冲机制**，write方法并不直接将数据写入文件，而是先写入内存中**特定的缓冲区**。(待缓冲区内容写入文件，才算真正写入了文件)

* 缓冲区写入文件的2种情况：
    * 正常情况下缓冲区满时，操作系统会自动将缓冲数据写入到文件中

    * 当文件close时，close原理是内部**先调用flush方法来刷新缓冲区，再执行关闭操作**，这样即使缓冲区数据未满也能保证数据的完整性。但如果如果进程意外退出或正常退出时而未执行文件的close方法，缓冲区中的内容将会丢失。

* flush方法是用来刷新缓冲区的，即**将缓冲区中的数据立刻写入文件**，同时清空缓冲区

## 协程 & greenlet & gevent

### 协程

具体参见

* [廖雪峰 - 协程](https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868328689835ecd883d910145dfa8227b539725e5ed000)

* [自己整理的一篇日志](https://github.com/carrie0307/Notes/blob/master/Python/xiecheng.py)

### greenlet

* yield能实现协程，不过实现过程不易于理解，greenlet是在这方面做了改进

* 注意：greenlet要手动切换 ×.switch()

```python

from greenlet import greenlet
import time

def A():
    while 1:
        print('-------A-------')
        time.sleep(0.5)
        g2.switch()

def B():
    while 1:
        print('-------B-------')
        time.sleep(0.5)
        g1.switch()

g1 = greenlet(A)  #创建协程g1
g2 = greenlet(B)

g1.switch()  #跳转至协程g1

```


### gevent

* gevent是第三方库，通过greenlet实现协程，其基本思想是：

    * 当一个greenlet遇到**IO操作时(比如访问网络)，就自动切换到其他的greenlet**，等到IO操作完成，再在适当的时候切换回来继续执行

#### 猴子补丁(monkey-patch)

* [什么是猴子补丁(monkey-patch)](http://blog.csdn.net/handsomekang/article/details/40297775)

* 由于切换是在IO操作时自动完成，所以gevent需要修改Python自带的一些标准库，这一过程在启动时通过monkey patch完成.

```python
# 把socket修改为IO操作
from gevent import monkey; monkey.patch_socket()
# 第二种方法
from gevent import monkey
monkey.patch_all()
```

#### 同步队列

这里介绍2种,文档见[gevent队列文档](http://www.gevent.org/gevent.queue.html)

* gevent.queue.Queue

一般方法使用即可

* 优先级队列
    * 一个子类：class PriorityQueue (Bases: gevent.queue.Queue)使用时注意：
    *  1) put/get时以**tuple形式**进行,self.put((priority,data))    Entries are typically tuples of the form: (priority number, data).
    * 2) **priority越小，优先级越高 A**。文档中说： subclass of Queue that retrieves entries in priority order (lowest first).

#### 一般gevent代码：

```python
from gevent import monkey; monkey.patch_all()
import gevent

gevent_list = [gevent.spawn(targets_function, args),
               gevent.spawn(targets_function, args),
               gevent.spawn(targets_function, args)
            ]

gevent.joinall(gevent_list)
```

#### Pool

```python
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
pool = Pool(size)
for _ in size:
    # apply_async 并行
    # apply 串行
    pool.apply_async(target_function, args)

pool.join()

```
