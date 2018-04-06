# -*- coding: utf-8 -*-

from __future__ import division
import math
'''''
计算给定字符的二进制信息熵（如有小数，保留至小数位后7位）
输入
输入任意一串字符
样例输入
aaaabbcd
输出
计算出字符串的信息熵
样例输出
1.75
'''

def calculate_entropy(string):

    str_list = list(string)
    length =len(str_list)
    # 得到字符串中不重复字符的集合
    str_list_single=list(set(str_list))
    num_list=[]
    for i in str_list_single:
        # 统计每个字符出现的次数
        num_list.append(str_list.count(i))
    list_two=zip(str_list_single,num_list)

    entropy=0
    for j in range(len(list_two)):
        ch = list_two[j][0]
        # 字符ch出现的次数
        appear_num = list_two[j][1]
        # entropy = -(p1*log(2,p1) + p2 * log(2,p2) +　．．．　+p32 *log(2,p32))
        entropy += -1*(float(appear_num/length))*math.log(float(appear_num/length),2)
    if len(str(entropy).split('.')[-1])>=7:
        return '%.7f' %entropy
    else:
        return entropy


def my_calculate_entropy(string):
    '''
    function: 计算string的熵
    :param :string: 待计算字符串
    :return: entropy: 熵值
    核心公式： entropy = -(p1*log(2,p1) + p2 * log(2,p2) +　．．．　+p32 *log(2,p32))
    '''

    str_list = list(string)
    length = len(str_list)
    unique_ch = list(set(str_list))
    counter = {}

    # 统计每个字符出现次数
    for ch in unique_ch:
        # IDEA： 注意str_list.count() 的应用
        counter[ch] = str_list.count(ch)

    entropy = 0
    for ch in counter:
        entropy += -1 * ((counter[ch] / length) * math.log((counter[ch] / length),2))

    entropy = round(entropy, 2)
    return entropy


if __name__ == '__main__':
    string = 'aaaabbcd'
    print calculate_entropy(string)
    print my_calculate_entropy(string)
