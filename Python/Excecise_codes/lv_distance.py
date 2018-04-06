# -*- coding: utf-8 -*-
from __future__ import division
'''
Levenshtein 编辑距离
参考： 1. 编辑距离（Levenshtein距离）详解（附python实现） http://blog.csdn.net/luo123n/article/details/9999481
      2. 字符串编辑距离（Levenshtein距离）算法  https://www.cnblogs.com/BlackStorm/p/5400809.html

大致看懂了，略有模糊
'''


def levenshtein(first,second):
    if len(first) > len(second):
        first,second = second,first
    if len(first) == 0:
        return len(second)
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    # 生成second_length 列， first_length 行 的矩阵
    distance_matrix = [range(second_length) for x in range(first_length)]
    for item in distance_matrix:
        print item
    print '\n'
    for i in range(1,first_length):
        for j in range(1,second_length):
            '''
            distance_matrix[i][j]： 用不同方法令s1中前i个字符组成的串和s2中前j个字符组成的串相同的编辑距离
            IDEA： 这里有动态规划的思想
            '''
            # 在 first前i-1个字符与second前j个字符相同的情况下(distance_matrix[i-1][j])，删除first中第i个字符(+1)
            deletion = distance_matrix[i-1][j] + 1
            # 在 first前i个字符与second前j-1个字符相同的情况下(distance_matrix[i-1][j])，在second插入新的字符作为第j个字符
            insertion = distance_matrix[i][j-1] + 1
            # 在 first前i-1个字符与second前j-1个字符相同的情况下(distance_matrix[i-1][j])
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                # 当第一个字符串的第i个字符不等于第二个字符串的第j个字符时
                substitution += 1
            # distance_matrix[i][j]是s1中前i个字符组成的串，和s2中前j个字符组成的串的编辑距离
            distance_matrix[i][j] = min(insertion,deletion,substitution)

    return distance_matrix[first_length-1][second_length-1]


def calculate_similarity(edit_distance,str1,str2):
    '''
    根据字符串编辑距离计算相似度
    param: edit_distance 编辑距离
    param: str1: 字符串1
    param: str2: 字符串2
    return: similarity: 相似度
    '''
    length1 = len(str1)
    length2 = len(str2)
    similarity = edit_distance / max(length1, length2)
    return similarity




if __name__ == '__main__':
    str1,str2 = 'books','cooked'
    edit_distance = levenshtein(str1,str2)
    print 'distance: ', edit_distance
    print calculate_similarity(edit_distance,str1,str2)
