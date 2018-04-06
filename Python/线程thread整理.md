# Python多线程整理
---

## 基础用法
* 1.用函数来包装（本质也是调用threading模块）</br>
#### 示例代码

```Python
# -*- coding: UTF-8 -*-
import threading
import time
 
# 为线程定义一个函数
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, time.ctime(time.time()) )
 
# 创建两个线程
try:
   t1 = threading.Thread(target=print_time, args = ("Thread-1", 4, )) # 创建好了线程
   t1.start()  # 让线程跑起来（执行targetd处的函数)
   t2 = threading.Thread(target=print_time, args = ("Thread-2", 4, )) # 创建好了线程
   t2.start() # 让线程跑起来（执行targetd处的函数)
except:
   print "Error: unable to start thread"
 
while 1:
   pass
```
###### 其他设置：

```Pyton
t1 = threading.Thread(target=print_time, args = ("Thread-1", 4, )) # 创建好了线程

t1.setDaemon(True) # 设置当主线程退出后，t1线程也强制退出，不再执行；默认为False；

t1.start() # 让t1线程跑起来；

# 阻塞主进程无法执行join以后的语句,专注执行该线程,必须等待线程执行完毕之后才能执行其后主线程的语句；
t1.join()  # join可以设置时限

```
关于join和setDaemon的区别，可[参考此文](http://blog.csdn.net/zhangzheng0413/article/details/41728869/)

* 2.用类来包装</br>
使用Threading模块创建线程，直接从threading.Thread继承，然后重写__init__方法和run方法：
#### 示例代码

```Python

#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import threading
import time
 
exitFlag = 0
 
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name
 
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threading.Thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
 
# 创建新线程
thread1 = myThread(1, "Thread-1", 1) # 之前的target函数（即实际要执行的函数）被至于了类中的run()方法中调用
thread2 = myThread(2, "Thread-2", 2)
 
# 开启线程
thread1.start()
thread2.start()
 
print "Exiting Main Thread"

```

## 多线程同步
[参考文章1](http://blog.csdn.net/hehe123456zxc/article/details/52264829)


* Lock & RLock:互斥锁 用来保证多线程访问共享变量的问题
* Semaphore对象：Lock互斥锁的加强版，可以被多个线程同时拥有，而Lock只能被某一个线程同时拥有。
* Event对象: 它是线程间通信的方式，相当于信号，一个线程可以给另外一个线程发送信号后让其执行操作。
* Condition对象：其可以在某些事件触发或者达到特定的条件后才处理数据

#### Lock
Lock是最基础的锁，这里不多做解释
###### 示例代码
```Python
# encoding: UTF-8
import threading
import time
 
data = 0
lock = threading.Lock()
 
def func():
    global data
    print '%s acquire lock...' % threading.currentThread().getName()
    
    # 调用acquire([timeout])时，线程将一直阻塞，
    # 直到获得锁定或者直到timeout秒后（timeout参数可选）。
    # 返回是否获得锁。
    if lock.acquire():
        print '%s get the lock.' % threading.currentThread().getName()
        data += 1
        time.sleep(2)
        print '%s release lock...' % threading.currentThread().getName()
        
        # 调用release()将释放锁。
        lock.release()
 
t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t3 = threading.Thread(target=func)
t1.start()
t2.start()
t3.start()

```

####Rlock
**关于Rlock可以参照这篇文章，虽然代码看得明白，但是不懂什么时候要用到。**</br>
[参考文章2](http://www.cnblogs.com/huxi/archive/2010/06/26/1765808.html)

#### Semaphore(共享对象访问)
设定**多个线程访问同一个对象**;当semaphore次数用完，某个无法acquire的线程将会阻塞在semaphore.acquire()处，直到有锁释放

###### 示例代码

```Python
# -*- coding: UTF-8 -*-
import threading
import time

semaphore = threading.Semaphore(3) # 设定3个线程访问同一个对象;当semaphore次数用完，某个无法acquire的线程将会阻塞在semaphore.acquire()处，直到有锁释放

def func():
    if semaphore.acquire():
        # for i in range(3):
        time.sleep(1)
        print (threading.currentThread().getName() + '获取锁\n')
        semaphore.release()
        print (threading.currentThread().getName() + ' 释放锁\n')



for i in range(5):
  t1 = threading.Thread(target=func)
  t1.start()
  
```

###### 上段代码运行结果
![](http://ouzh4pejg.bkt.clouddn.com/semaphore.PNG)
在运行结果中可以看到，前三个线程都可以获取到锁，待前三个线程释放锁后，第4、5个线程才可以获取到锁。

#### Event
threading.Event 实现**线程间通信**</br>
使用threading.Event可以**使一个线程等待其他线程的通知，我们把这个Event传递到线程对象中**</br>
也可以用来让主线程控制其他线程执行

Event内部包含了一个标志位，初始的时候为false。</br>
可以使用使用set()来将其设置为true；</br>
或者使用clear()将其从新设置为false；</br>
可以使用is_set()来检查标志位的状态；</br>
另一个最重要的函数就是**wait(timeout=None)**，用来在**wait语句处阻塞当前线程**，直到event的内部标志位被设置为true或者timeout超时。如果内部标志位为true则wait()函数理解返回。</br>

###### 示例代码

```Python
# -*- coding: UTF-8 -*-
import threading
import time

class MyThread(threading.Thread):
    def __init__(self, signal):
        threading.Thread.__init__(self)
        self.singal = signal

    def run(self):
        print " %s,等待event-signal ..."%self.name
        self.singal.wait()
        print "%s, 获取event-signal..." %self.name

if __name__ == "__main__":
    singal = threading.Event()
    for t in range(0, 3):
        thread = MyThread(singal)
        thread.start()

    print "\nmain thread sleep 3 seconds...\n "
    time.sleep(3)

    singal.set() # signal被设置为true
    print "\nsingal is True ... \n"
    
```

###### 执行结果
![](http://ouzh4pejg.bkt.clouddn.com/event-signal.PNG)
由运行结果可发现，qevent标志位默认false，所以起初三个线程都在等待；</br>
待主线程将标志位置为true后，三个线程都获得了signal，从而线程可以开始运行wait()语句后的内容

#### Condition锁
较之lock的锁，condition的锁在获得锁后，能够在**条件变量，即这种机制是在满足了特定的条件后，线程才可以访问相关的数据,否则设置为wait**

**Condition.wait([timeout]):**</br>
线程挂起，直到收到一个notify通知或者超时（可选的，浮点数，单位是秒s）才会被唤醒继续运行。</br>
wait()在**必须在已获得Lock前提下才能调用在**，否则会触发RuntimeError。</br>
在**调用wait()会释放Lock在**，直至该线程被Notify()、NotifyAll()或者超时线程又重新获得Lock

**Condition.notify():**</br>
唤醒一个挂起的线程（如果存在挂起的线程）。注意：notify()方法不会释放所占用的琐。

**Condition.notify_all()**</br>
**Condition.notifyAll()**</br>
唤醒所有挂起的线程（如果存在挂起的线程）。注意：这些方法不会释放所占用的琐

###### 示例代码

```Python
# -*- coding: UTF-8 -*-
from threading import Thread, Condition
import time
import random

queue = [1,2,3,4,5]
MAX_NUM = 5
condition = Condition()

class ProducerThread(Thread):
    def run(self):
        nums = range(5)
        global queue
        while True:
            print "Producer 获取锁...\n"
            condition.acquire()
            print "Producer 加锁...\n"
            if len(queue) == MAX_NUM:
                print "Queue full, producer is waiting"
                condition.wait()
                print "Space in queue, Consumer notified the producer"
            num = random.choice(nums)
            queue.append(num)
            print "Produced", num
            condition.notify()
            condition.release()
            print 'Producer 释放锁。。。\n'
            time.sleep(random.random())


class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            print 'Consumer 获取锁...\n'
            condition.acquire()
            print "Consumer 加锁...\n"
            if not queue:
                print "Nothing in queue, consumer is waiting"
                condition.wait()
                print "Producer added something to queue and notified the consumer"
            num = queue.pop(0)
            print "Consumed", num
            condition.notify()
            condition.release()
            print 'Consumer 释放锁。。。\n'
            time.sleep(random.random())


ProducerThread().start()
ConsumerThread().start()

```

###### 执行结果（部分）
![](http://ouzh4pejg.bkt.clouddn.com/conditon.PNG)
如图可见，Producer获得锁后，由于队列以满，所以先wait（wait时会暂时释放锁）</br>
然后Consumer获取到锁，并消费掉一个元素，并且notify正在wait的Producer线程</br>
被唤醒的Producer生产一个元素（Produced 0）,并释放锁


## 线程池threadpool
[参考文章1--最简单使用](http://blog.csdn.net/u011734546/article/details/51460703)</br>
[参考文章2--讲解内容再充裕的一篇](http://blog.csdn.net/shawpan/article/details/52013448)

要提到的是，threadpool模块较老，根据[参考文章2](http://blog.csdn.net/shawpan/article/details/52013448),pypi上也建议使用**multiprocessing**代替它。

```Python
# -*- coding: UTF-8 -*-
import threadpool
import time

def test_func(li):
    print "数字是： " + str(li) + " \n"
    # print "数字是： " + str(li[0]) + " " + str(li[1]) + " \n"

# Step1: 定义了一个线程池，表示最多可以创建poolsize这么多线程
pool = threadpool.ThreadPool(5)

# Step2: 调用makeRequests创建了要开启多线程的函数，以及函数相关参数和回调函数.其中回调函数可以不写，default是无，也就是说makeRequests只需要2个参数就可以运行
# requests = threadpool.makeRequests(some_callable, list_of_args, callback)
requests = threadpool.makeRequests(test_func, ([9,3,4,5]))
# 注意，这里list_of_args相当于传递了4个请求的参数；传递请求的数量是由参数个数控制的。
# 同时传递多个参数的方法还没试出来，但是可以将多个参数合为一个传递([[9,3],[4,5]])

# Step3: 将所有要运行多线程的请求扔进线程池，一下两种写法都可以
[pool.putRequest(req) for req in requests]
# ---------------------or-------------------------
for req in requests:
    print '---'
    pool.putRequest(req)

# Step4:等待所有的线程完成工作后退出
pool.wait()

```
**个人感觉**：线程池用list_of_args实现了线程间的同步，起到了原来Queue的作用。认为在参数个数为1且多个线程运行同一个函数的情况下使用线程池。

---

2017.08.21

