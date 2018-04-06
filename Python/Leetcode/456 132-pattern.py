# -*- coding: utf-8 -*-
# Python3

# Time:  O(n)
# Space: O(n)

# Given a sequence of n integers a1, a2, ..., an,
# a 132 pattern is a subsequence ai, aj, ak such that i < j < k and
# ai < ak < aj. Design an algorithm that takes a list of n numbers as
# input and checks whether there is a 132 pattern in the list.
#
# Note: n will be less than 15,000.
#
# Example 1:
# Input: [1, 2, 3, 4]
#
# Output: False
#
# Explanation: There is no 132 pattern in the sequence.
# Example 2:
# Input: [3, 1, 4, 2]
#
# Output: True
#
# Explanation: There is a 132 pattern in the sequence: [1, 4, 2].
# Example 3:
# Input: [-1, 3, 2, 0]
#
# Output: True
#
# Explanation: There are three 132 patterns in the sequence: [-1, 3, 2], [-1, 3, 0] and [-1, 2, 0].


# 这里自己添加了将132-pattern输出


'''
    本质： 三个数字，一个下标最大的数，两个下标比它小雀一个比它大，一个比它小


    1 先找到下标最大的数st[-1]，记为 ak
    2 再通过nums[i] > st[-1]找到比下标最大的数大的数
    3 再通过nums[i] < ak找到比下标最大的数小的数，且这个数是三个数中下标最小的，如果可以进行到这里，则返回True
'''

def modify_find132pattern(nums):
    """
    想尝试如何输出132pattern，但总是不能完全输出
    :type nums: List[int]
    :rtype: bool
    """
    ak = float("-inf")
    st = []
    res_list = []
    max_index_nums = [] # 下标最大数的集合
    temp = []
    for i in reversed(range(len(nums))):
        
        # ak 初值是负无穷， 因此当出现比ak小的值时，说明之前以及执行过ak = st.pop() 即满足了j < k  且 ak(st[-1]即ak) < aj(num[i]),因此这里找到一个比ak小
        # if nums[i] < ak:
        if max_index_nums and nums[i] < min(tuple(max_index_nums)):
           for j in range(len(res_list)):
                print (res_list[j])
                res_list[j].insert(0,nums[i])
                # 这里的nums[i]就是比下标最大的数小的数
               
        else:
            while st and nums[i] > st[-1]:
            # for k in reversed(range(i)):
            #     print (nums[k])
            #     while st and nums[k] > st[-1]:
                # 每次 st[-1] (及st.pop())得到的都是当前对应下表最大的数，因此要找一个下标比它小雀比他大的数
                #  根据遍历方式，每个nums[i] 对应的下标都比st[-1]对应的下表小，因此找到num[i] > st[-1]即 找到了 j < k 且 a[k] < a[j]
                # ak就是构成的三个数中下标最大的数字
                ak = st.pop()
                max_index_nums.append(ak)
                print ('ak:', ak)
                print (nums[i],ak)
                res_list.append([nums[i],ak])
            print ('--')
        st.append(nums[i])
    return res_list


def myfind132pattern(nums):
    """
    :type nums: List[int]
    :rtype: bool
    From: https://github.com/kamyu104/LeetCode/blob/master/Python/132-pattern.py
    """
    ak = float("-inf")
    st = []
    for i in reversed(xrange(len(nums))):
        # ak 初值是负无穷， 因此当出现比ak小的值时，说明之前以及执行过ak = st.pop() 即满足了j < k  且 ak(st[-1]即ak) < aj(num[i]),因此这里找到一个比ak小
        if nums[i] < ak:
            return True
        else:
            while st and nums[i] > st[-1]:
                # 每次 st[-1] (及st.pop())得到的都是当前对应下表最大的数，因此要找一个下标比它小雀比他大的数
                #  根据遍历方式，每个nums[i] 对应的下标都比st[-1]对应的下表小，因此找到num[i] > st[-1]即 找到了 j < k 且 a[k] < a[j]
                # ak就是构成的三个数中下标最大的数字
                ak = st.pop()
        st.append(nums[i])
    return False


if __name__ == '__main__':
    print (find132pattern([-1, 3, 2, 0]))
    # print (find132pattern([3, 1, 4, 2]))
    # print find132pattern([1,2,3,4])