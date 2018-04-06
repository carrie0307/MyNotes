# Python装饰器学习
---

[Python装饰器学习（九步入门）](http://www.cnblogs.com/rhcad/archive/2011/12/21/2295507.html)基础部分根据此文来学习的，接下来将根据此文内容进行整理，并添加自己的总结

## 入门九步整理
#### 第一步：最简单的函数，准备附加额外功能
        # -*- coding: UTF-8 -*-
        '''示例1: 最简单的函数,表示调用了两次'''
 
        def myfunc():
            print("myfunc() called.")
 
        myfunc()
        myfunc()
    
**个人感觉**：这里主要是展示最简单基础的情况


#### 第二步：使用装饰函数在函数执行前和执行后分别附加额外功能
        # -*- coding: UTF-8 -*-
        '''示例2: 替换函数(装饰)
        装饰函数的参数是被装饰的函数对象，返回原函数对象
        装饰的实质语句: myfunc = deco(myfunc)'''
         
        def deco(func):
            print("before myfunc() called.")
            func()
            print("  after myfunc() called.")
            return func
         
        def myfunc():
            print(" myfunc() called.")
         
        myfunc = deco(myfunc)
         
        myfunc()
        myfunc()
        
**个人体验**：装饰器其实也就是一个函数，一个用来包装函数的函数，返回一个修改之后的函数对象。第二步就从这最基础的一点上演示了这一特点。

#### 第三步：使用语法糖@来装饰函数
        # -*- coding: UTF-8 -*-
        '''示例3: 使用语法糖@来装饰函数，相当于“myfunc = deco(myfunc)”
        但发现新函数只在第一次被调用，且原函数多调用了一次'''
         
        def deco(func):
            print("before myfunc() called.")
            func()
            print("  after myfunc() called.")
            return func
         
        @deco # 这里就是语法糖，相当与myfunc = deco(myfunc)，这里其实已经执行了myfunc = deco(myfunc)调用了一次函数
        def myfunc():
            print(" myfunc() called.")
         
        myfunc()
        myfunc()
        
#### 第四步： 使用内嵌包装函数来确保每次新函数都被调用
        # -*- coding: UTF-8 -*-
        '''示例4: 使用内嵌包装函数来确保每次新函数都被调用，
        内嵌包装函数的形参和返回值与原函数相同，装饰函数返回内嵌包装函数对象'''

        def deco(func):
            def _deco():
                print("before myfunc() called.")
                func()
                print("  after myfunc() called.")
                # 不需要返回func，实际上应返回原函数的返回值
            return _deco
         
        @deco
        def myfunc():
            print(" myfunc() called.")
            return 'ok'
         
        myfunc()
        myfunc()
**个人体验**： 这里的语法糖处不会直接使myfunc函数执行，但是在后续调用的mufunc()的执行都能看到装饰器的效果。

#### 第五步： 对带参数的函数进行装饰
        # -*- coding: UTF-8 -*-
        '''示例5: 对带参数的函数进行装饰，
        内嵌包装函数的形参和返回值与原函数相同，装饰函数返回内嵌包装函数对象'''
         
        def deco(func):
            def _deco(a, b):
                print("before myfunc() called.")
                ret = func(a, b)
                print("  after myfunc() called. result: %s" % ret)
                return ret
            return _deco
         
        @deco
        def myfunc(a, b):
            print(" myfunc(%s,%s) called." % (a, b))
            return a + b
         
        myfunc(1, 2)
        myfunc(3, 4)
**个人体验**： 较之第四步的部分，在装饰器内层函数_deco()的调用中加上对应func()的参数即可。

#### 第六步：对参数数量不确定的函数进行装饰
        # -*- coding: UTF-8 -*-
        '''示例6: 对参数数量不确定的函数进行装饰，
        参数用(*args, **kwargs)，自动适应变参和命名参数'''
         
        def deco(func):
            def _deco(*args, **kwargs):
                print("before %s called." % func.__name__)
                ret = func(*args, **kwargs)
                print("  after %s called. result: %s" % (func.__name__, ret))
                return ret
            return _deco
         
        @deco
        def myfunc(a, b):
            print(" myfunc(%s,%s) called." % (a, b))
            return a+b
         
        @deco
        def myfunc2(a, b, c):
            print(" myfunc2(%s,%s,%s) called." % (a, b, c))
            return a+b+c
         
        myfunc(1, 2)
        myfunc(3, 4)
        myfunc2(1, 2, 3)
        myfunc2(3, 4, 5)
**个人体验**：较之第五步，将_dect()的参数换为(*args, **kwargs)。但这里想为什么参数不确定的情况，应该是由于同一装饰器可能修饰不同的函数，因此存在有参数不同的情况。

#### 第七步：让装饰器带参数
        # -*- coding: UTF-8 -*-
        '''示例7: 在示例4的基础上，让装饰器带参数，
        和上一示例相比在外层多了一层包装。
        装饰函数名实际上应更有意义些'''
         
        def deco(arg):
            def _deco(func):
                def __deco():
                    print("before %s called [%s]." % (func.__name__, arg))
                    func()
                    print("  after %s called [%s]." % (func.__name__, arg))
                return __deco
            return _deco
         
        @deco("mymodule")
        def myfunc():
            print(" myfunc() called.")
         
        @deco("module2")
        def myfunc2():
            print(" myfunc2() called.")
         
        myfunc()
        myfunc2()
**个人体验**： 将装饰器的参数直接至于装饰器函数最外层即可，要注意语法糖调用时写上参数

#### 第八步：让装饰器带 类 参数
        # -*- coding: UTF-8 -*-
        '''示例8: 装饰器带类参数'''
        class locker:
            def __init__(self):
                print("locker.__init__() should be not called.")
                 
            @staticmethod
            def acquire():
                print("locker.acquire() called.（这是静态方法）")
                 
            @staticmethod
            def release():
                print("  locker.release() called.（不需要对象实例）")
         
        def deco(cls):
            '''cls 必须实现acquire和release静态方法'''
            def _deco(func):
                def __deco():
                    print("before %s called [%s]." % (func.__name__, cls))
                    cls.acquire()
                    try:
                        return func()
                    finally:
                        cls.release()
                return __deco
            return _deco
         
        @deco(locker)
        def myfunc():
            print(" myfunc() called.")
         
        myfunc()
        myfunc()
**个人体验**: 装饰器的参数是类，这样在装饰器内可调用类的静态方法


#### 第九步：装饰器带类参数，并分拆公共类到其他py文件中，同时演示了对一个函数应用多个装饰器
        # -*- coding: UTF-8 -*-
        '''mylocker.py: 公共类 for 示例9.py'''
         
        class mylocker:
            def __init__(self):
                print("mylocker.__init__() called.")
                 
            @staticmethod
            def acquire():
                print("mylocker.acquire() called.")
                 
            @staticmethod
            def unlock():
                print("  mylocker.unlock() called.")
         
        class lockerex(mylocker):
            @staticmethod
            def acquire():
                print("lockerex.acquire() called.")
                 
            @staticmethod
            def unlock():
                print("  lockerex.unlock() called.")
         
        def lockhelper(cls):
            '''cls 必须实现acquire和release静态方法'''
            def _deco(func):
                def __deco(*args, **kwargs):
                    print("before %s called." % func.__name__)
                    cls.acquire()
                    try:
                        return func(*args, **kwargs)
                    finally:
                        cls.unlock()
                return __deco
            return _deco
            
            
        --------------------------------------------------------------------
        
        # -*- coding: UTF-8 -*-
        '''示例9: 装饰器带类参数，并分拆公共类到其他py文件中
        同时演示了对一个函数应用多个装饰器'''
         
        from mylocker import *
         
        class example:
            @lockhelper(mylocker)
            def myfunc(self):
                print(" myfunc() called.")
         
            @lockhelper(mylocker)
            @lockhelper(lockerex)
            def myfunc2(self, a, b):
                print(" myfunc2() called.")
                return a + b
         
        if __name__=="__main__":
            a = example()
            a.myfunc()
            print(a.myfunc())
            print(a.myfunc2(1, 2))
            print(a.myfunc2(3, 4))
            
**个人体验**:这里展示了一个函数多个装饰器的情况

## 其他资料
* 1.[Python装饰器与面向切面编程](http://www.cnblogs.com/huxi/archive/2011/03/01/1967600.html)此文从装饰器的需求入手开始讲解，并介绍了**面向切片编程**的概念；
* 2. 来自知乎[什么时候要用到装饰器](https://www.zhihu.com/question/31265857)

## 存在的问题：
* 1.自己并没有太多用过装饰器，以后还要多练习；
* 2.一般总结的需要使用装饰器的情况：
        ①注入参数（提供默认参数，生成参数）
        ②记录函数行为（日志、缓存、计时什么的）
        ③预处理／后处理（配置上下文什么的）
        ④修改调用时的上下文（线程异步或者并行，类方法）
* 3.**切面编程**、**functools模块**等尚未学习清楚。

### 概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能



