# -*- coding: utf-8 -*-

'''
    思路：如果是左括号，则入栈；
         右括号，则先检查栈： 
            若栈空，则说明此右括号多余；
            栈不空，则右括号和栈顶元素(最后一次入栈的元素)比较，若不匹配，则返回False
         表达式检验结束时，检查栈： 若栈不空，则说明左括号有多余；

    思路二： 先检查s长度，如果长度是奇数，则直接返回False；
                        如果长度是偶数，则按照思路（一）的方法进行检验；
'''

def isValid(s):
    """
    :type s: str
    :rtype: bool
    """
    # '(', ')', '{', '}', '[' and ']'
    s_list = list(s)
    match_dict = {')':'(',']':'[','}':'{'}
    left_parenthese_stack = []

    for ch in s_list:
        if ch not in match_dict:
            # 左括号入栈
            left_parenthese_stack.append(ch)
        else:
            # 如果是右括号
            if left_parenthese_stack:
                left_ch = left_parenthese_stack.pop()
                # 检查栈顶(最后一次入栈)元素是否匹配
                if match_dict[ch] != left_ch:
                    return False
            else:
                # 右括号多余
                return False
    print (left_parenthese_stack)
    # 检查左括号是否多余
    if not left_parenthese_stack:
        return True
    else:
        return False


if __name__ == '__main__':
    print (isValid('['))