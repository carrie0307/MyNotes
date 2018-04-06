# -*- coding: utf-8 -*-

'''
    功能：根据元素数量和线程数量对元素分组
'''

def divide_items(items,threads_num=5):
    '''
    功能：根据元素数量和线程数量对元素进行划分
    param: items: 待分组元素的列表
    param: threads_num: 线程数量
    return: results: 分组后的元素
    return: len(results): 元素被分为的组数
    '''

    if threads_num<=len(items):
        #  每个线程多少
        trader = len(items) // threads_num
        # 余数
        remainder = len(items) % threads_num
        # 用 trader * threads_num 得到恰取整的元素数量
        A = items[:trader * threads_num]

        if remainder != 0:
            # B 是余数对应的元素
            B = items[trader * threads_num:]
        else:
            B = []

        index = 0
        results = []
        while index < trader * threads_num:
            results.append(A[index:index + trader])
            index = index + trader
        # 给results的最后一个列表（即最后一组的数据）加上余数对应的元素
        results[-1].extend(B)
    else:
        # 当线程数大于元素数量时，不进行划分
        results = [item for item in items]

    return results,len(results)

if __name__=="__main__":
    print divide_items(range(11))
    '''
    实际运行时，第 j 个线程，就运行  resutls 中下标为 j 的列表中的元素
    当 items = range(11), threads_num = 5 时， results = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9, 10]] ， len(results) = 5
    当 items = range(11), threads_num = 20 时, results = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] ， len(results) = 11
    '''
