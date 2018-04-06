# -*- coding: utf-8 -*-
# Python3

'''
    接替解题思路举例,eg.x = 23632, 初值: s = 0

    s = s * 10 + x % 10 = 0 + 2 = 2, x = x / 10 = 2363, x > s
    s = s * 10 + x %10 = 2 * 10 + 3 = 23, x = x / 10 = 236, x > s
    s = s * 10 + x % 10 = 23 * 10 + 6 = 236, x = x / 10 = 23,  x < s

    s / 10 = 23 == x ,所以 x = 23623是一个回文数
'''

def isPalindrome(x):
        """
        :type x: int
        :rtype: bool
        """
        if  x < 0 or (x != 0 and x % 10 == 0):
            return False
        if 0 <= x < 10:
            return True
        s = 0
        while x > s:
            s = s * 10 + (x % 10)
            x = x // 10        

        if x == s or (s // 10 == x):
            return True
        else:
            return False


if __name__ == '__main__':
   print (isPalindrome(1))