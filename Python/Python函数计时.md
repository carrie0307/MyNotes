# Python函数计时

[参考文章](http://www.cnblogs.com/masako/p/6807166.html)

### 使用threading的timer定时器
```Python
    from threading import timer
    import time
    
    def time_limit(interval):
        def wraps(func):
            def time_out():
                raise RuntimeError()
    
            def deco(*args, **kwargs):
                timer = Timer(interval, time_out) # interval是时限，time_out是达到实现后触发的动作
                timer.start()
                res = func(*args, **kwargs)
                timer.cancel()
                return res
            return deco
        return wraps
        
    @time_limit(5)
    def time_test(run_time):
        time.sleep(run_time)
        
    
    if __name__ == '__main__':
    time_test(7)
    
```

**解释**:这其实跑了`两个线程`。一个是运行time_test()的主线程，一个是用来计时的线程Timer(interval,time_out)。当run_time>interval时，达到时限后，计时进程会`触发Timer中定义的动作（例如这里的timeout函数)`,但是`主线程还是继续运行，不会终止`(这就说明，无法用此方法处理有些运行中可能卡死的函数）。

### 信号量机制
```Python
    # coding:utf-8
    import time
    import signal
    
    
    def time_limit(interval):
        def wraps(func):
            def handler(signum, frame):
                # print signum
                raise RuntimeError()
            def deco(*args, **kwargs):
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)
                res = func(*args, **kwargs)
                signal.alarm(0)
                return res
            return deco
        return wraps
    
    
    @time_limit(2)
    def time_test(time_interval):
        time.sleep(time_interval)
        print '------'
    
    
    if __name__ == '__main__':
        try:
            time_test(5)
        except RuntimeError:
            print 'stop ...'


```
***解释***：这里是用了信号量机制，signal.alarm(interval)设置超时间隔，signal.signal(signal.SIGALRM, handler)中的handler是超时后触发的动作。需要`在handler中引发异常，否则无法终止time_test()函数`，handler中raise的异常可以通过time_test来捕获，这样可以终止time_test函数，在进行其他的处理。</br>
***问题***：handler函数中两个参数好像是必须要有的，否则就报错。</br>
***问题***：`实际应用中,由于是多线程,而signal不能在子线程中使用,也就是说，上例中@time_limit(2)所装饰的函数time_test必须是在主线程中才可以的。`

### from timeout import timeout方法
可以直接pip install timeout,然后from timeout import timeout,在需要的函数前@timeout(n)即可.</br>
***问题***：这个timeout同样不能用于子线程，根据使用报错判断，其原理应该与signal是一致的。


2017.08.19
