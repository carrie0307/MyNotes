# -*- coding: utf-8 -*-

'''
    功能: gevent 模型
'''

import gevent
from gevent import monkey
monkey.patch_all()

def run_gevent(func,*args,**kwargs):

    threads = [gevent.spawn(func,thread_id,*args) for thread_id in range(kwargs.get('threads_num'))]
    try:
        gevent.joinall(threads)
    except KeyboardInterrupt:
        print '[WARNING] User aborted.'

def _print(thread_id,j,k):
    print thread_id,j,k

if __name__ =="__main__":
    run_gevent(_print,2,3,threads_num=5)
