# -*- coding: utf-8 -*-

''' 
    方法一：
    1 根据每个字符串长度进行排序，获取最短字符串un_prefix = str[0]
    2 从长到段尝试un_prefix的前缀：如果它在每个元素中都出现了，则说明它就是子串；特别说明的是，Pyhton中''是任何字符串的子串

    方法二：
    1 用默认方法对字符串进行排序，得到的排序结果是按照字符拍的，例如 ['abc','ac','a'] - ['a', 'abc', 'ac'] ，['abc','b','dd'] - ['abc', 'b', 'dd']
    2 接下来只比较第一个和最后一个元素的最长公共子串即可
'''

'''
    学到的用法：
    1 reversed()
    2 sorted(list,key = len) 直接根据元素长度进行排序

    注意： 
    为了能遍历最后一个字符，注意range(len(str) + 1)  (注意+1)
'''

def longestCommonPrefix_1(strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ''
        strs = sorted(strs, key=len)
        un_prefix = strs[0]
        for i in reversed(range(len(un_prefix) + 1)):
            flag = True
            # 逐步减小子串长度
            prefix = un_prefix[:i]
            for item in strs:
                if prefix != item[:i]:
                    flag = False
                    continue
            if flag:
                # flag=True,说明前缀在每个子串都出现了
                return prefix

def longestCommonPrefix_2(strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ''
        strs = sorted(strs)
        first = strs[0]
        last = strs[len(strs) - 1]
        length = min(len(first),len(last))
        res = []
        # 只比较第一个和最后一个字符的最长前缀
        for i in reversed(range(length + 1)):
            print (first[:i])
            if first[:i] == last[:i]:
                print (first[:i])
                return first[:i]





if __name__ == '__main__':
    print (longestCommonPrefix_1(["c","acc","ccc"]))
    print (longestCommonPrefix_2(["c","acc","ccc"]))
    # strs = ['abc','b','dd']
    # print (sorted(strs))