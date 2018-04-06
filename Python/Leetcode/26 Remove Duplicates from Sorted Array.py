#-*- coding: utf-8 -*-

def removeDuplicates_1(A):
    """
    :type nums: List[int]
    :rtype: int
    """
    # 注意： 输入的数组是已经a sorted array，因此不会有[1,2,3,2]这样导致返回数组为[1,2,3,2]的情况出现
    if not A:
        return 0
    # newtail是记录不重复元素的下标
    newTail = 0
    # 注意： 这样的方法不额外增加内存空间
    for i in range(1, len(A)):
        print 'i:', i
        print 'tail:', newTail
        # 每当遇到不同元素时，就令new_tail后推一位
        if A[i] != A[newTail]:
            newTail += 1
            A[newTail] = A[i]
    # 所以不重复元素的长度是newTail+1
    return A, newTail + 1

def removeDuplicates(nums):
    if not nums:
        return 0

    duplicate = 0
    for i in range(1,len(nums)):
        if nums[i] == nums[i - 1]:
            duplicate += 1
        # 有几个元素重复了，就把当前的i回退几位
        nums[i - duplicate] = nums[i]

    # 注意，不可以是 return i - length + 1 ,因为当输入只有一个元素时eg,[1]，i 不会进入循环，因此会出错
    return len(nums) - duplicate



if __name__ == '__main__':
    nums = [1,2,1,4]
    print removeDuplicates_1(nums)
