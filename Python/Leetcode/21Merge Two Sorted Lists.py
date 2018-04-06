#-*- coding: utf-8 -*-

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

def mergeTwoLists(l1, l2):
    """
    :type l1: ListNode
    :type l2: ListNode
    :rtype: ListNode

    l1,l2代表头节点；
    对于单项向链表来说，一个头节点可以确定整个链表；
    链表由一个个节点构成，确定头节点后可以一个一个添加

    这道题本质是单向链表的合并，输入是2个头节点；
    题的input给了几个数，就是已经在链表中加入了几个节点(自己不用去想怎么创建链表/向链表中添加元素的问题了)

    QUESTION:
    ans的next为空，ans能把所有结点链起来得到链表吗
    但如果写成ans = ListNode(0)
            tmp = ListNode(0)
            ans.next = tmp
            确实会多一个值为0的空结点

    https://www.cnblogs.com/chruny/p/4872779.html
    """

    # 每初始化一个节点，都用0做临时的初值
    ans = ListNode(0)
    tmp = ans

    # ans = ListNode(0)
    # tmp = ListNode(0)
    # ans.next = tmp
    
    # 把ans理解成指向tmp的指针？
    tmp = ListNode(0)
    ans = tmp # tmp


    if l1 == None and l2 == None:
        return None

    while l1 or l2:
        if l2 == None:
            while l1 != None:
                tmp.val = l1.val
                l1 = l1.next
                if not l1:
                    break
                # 每初始化一个节点，都用0做临时的初值
                tmp.next = ListNode(0)
                tmp = tmp.next
            # 注意这里的break
            break

        if l1 == None:
            while l2 != None:
                tmp.val = l2.val
                l2 = l2.next
                if not l2:
                    break
                tmp.next = ListNode(0)
                tmp = tmp.next
            # 注意这里的break
            break

        if l1.val < l2.val:
            tmp.val = l1.val
            l1 = l1.next
        else:
            tmp.val = l2.val
            l2 = l2.next
        tmp.next = ListNode(0)
        tmp = tmp.next

    return ans

