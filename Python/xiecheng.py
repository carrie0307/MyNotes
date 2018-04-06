# -*- coding:utf-8 -*-

'''
协程记录

# https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868328689835ecd883d910145dfa8227b539725e5ed000
# https://www.cnblogs.com/bradleon/p/6106595.html
1  yield并不包含任何value，它接受外部.send()方法传过来的value.
2  先通过next(),start这个coroutine.之后每一次调用send(),将参数通过yield传入line中。同时相当于自动运行.next()到下一个value. 最终调用.close()关闭这个协程。
'''


import time

def consumer():
    r = ''
    while True:
        n = yield r # 通过yeild来接受send的内容记为n，再将comsumer()要返回的内容r通过yield发给produce
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        time.sleep(1)
        r = '200 OK'

def produce(c):
    c.next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n) # c是send的目标函数。每次send就相当于调用了一次目标函数
        print('[PRODUCER] Consumer return: %s' % r)
    c.close() 

if __name__=='__main__':
    c = consumer()
    produce(c)
    '''
    [PRODUCER] Producing 1...
	[CONSUMER] Consuming 1...
	[PRODUCER] Consumer return: 200 OK
	[PRODUCER] Producing 2...
	[CONSUMER] Consuming 2...
	[PRODUCER] Consumer return: 200 OK
	[PRODUCER] Producing 3...
	[CONSUMER] Consuming 3...
	[PRODUCER] Consumer return: 200 OK
	[PRODUCER] Producing 4...
	[CONSUMER] Consuming 4...
	[PRODUCER] Consumer return: 200 OK
	[PRODUCER] Producing 5...
	[CONSUMER] Consuming 5...
	[PRODUCER] Consumer return: 200 OK
    '''

    

