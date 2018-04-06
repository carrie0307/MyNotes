# -*- coding: utf-8 -*-

"""
1)根据自定义的域名字符串相似性原则判断两个域名字符串是否相似
2)将相似的规则提取成枚举模式

在similar_domain_cluster中调用： 根据判别是否相似的结果和枚举模式，更新mongo_db.clusters_table 表

flag, mode = Domains_Match().match('2020534.com', '0020524.com')
flag = 1 说明相似
mode 是枚举模式
"""
import sys
from tldextract import extract

class Domains_Match():
    """
    1)根据自定义的域名字符串相似性原则判断两个域名字符串是否相似
    2)将相似的规则提取成枚举模式
    """
    def delete_match(self,long_str,short_str):
        """
        对长度相差一的域名对进行匹配
        :param long_str:
        :param short_str:
        :return:
        """
        if len(long_str)-len(short_str)!=1:
            sys.exit(-1)
        idx = -1
        s = ''
        for i, r in enumerate(zip(long_str[:-1], short_str)):
            ch1, ch2 = r
            if ch1 == ch2:
                s+=ch1
            else:
                idx = i
                break

        if idx == -1 or s+''.join(list(long_str)[idx+1:])==short_str:
            return 1
        else:
            return 0

    def select_symbol(self,c1,c2):

        if c1.isdigit() and c2.isdigit():
            # c1,c2都是数字通配为#
            return '#'
        elif c1.isalpha() and c2.isalpha():
            # c1,c2都是字母通配为#
            return '*'
        else:
            # c1,c2不同为数字和字母通配为$
            return '$'

    def short_match(self,str1,str2):
        """
        第一个字符不等
        短字符匹配 长度小于３
        :param str1:
        :param str2:
        :return:
        """
        if len(str1)==2:
            if str1[1]==str2[1]:
                return self.select_symbol(str1[0], str2[0])+str1[1]
            else:
                return self.select_symbol(str1[0], str2[0])+self.select_symbol(str1[1], str2[1])
        else:
            return self.select_symbol(str1[0], str2[0])

    def jump_match(self,str1,str2,i):
        """
        :param str1: domain1 的主域名部分
        :param str2: domain2 的主域名部分
        :param i:出现不同字符的位置下标i (第i个元素不等)
        :return:flag：
        :return:mode: 根据str1 和 str2 不同的类型写出的包含通配符的mode
        """
        # str2 中第一个和 str1 不同的字符
        b = str2[i]
        mode = list(str1)
        new_str = list(str1)
        idx_list = []
        count = 0
        # 从出现不同的那一位开始遍历
        for j,r in enumerate(zip(str1[i:],str2[i:])):
            # count 是 str1, str2中不相同字符的总数
            if r[0]!=r[1]:
                count+=1
                # i + j 是str1 和 str2 字符不同的位
                idx_list.append(i+j)
        a_list = set()
        b_list = set()
        # print idx_list
        # print 'counter: ', count
        for j in idx_list:
            # a_list是str1中与str2不同的字符
            a_list.add(str1[j])
            # b_list是str2中与str1不同的字符
            b_list.add(str2[j])

            # 根据str1 和 str2 中字符不同的类型将mode中对应的字符替换为不同的通配符
            mode[j] = self.select_symbol(str1[j],str2[j])
            # 把str1中每一个和str2不同的位上的字符都置为了 第一次出现不同时str2那一位上的字符 (为为了辅助判断是不是不同的字符时同一个)
            new_str[j] = b

        # mode = ''.join(mode) 是str1 将与str2 不同的字符换为通配符后的字符串
        if count>=3: # 有三个或三个以上字符不同的情况下
            '''
            a_list.add(str1[j]) == 0 说明 str1 中与str2 出现不同字符位置上的字符是相同的 ；
            b_list.add(str1[j]) == 0 同理
            eg. str1 = 'abcdcf', str2 = 'abzdzh' 此时a_list = ('c') b_list = ('z')
            '''
            # str1 和 str2 有三个或三个以上位置字符不同 但这些字符相同
            if len(a_list)==1 and len(b_list)==1 and ''.join(new_str)==str2:
                flag = 1
                mode = ''.join(mode)+'&'
            else:
                flag = 0
                mode = str1
        elif count == 2: # 有2个字符不同的情况下
            flag = 1
            if len(a_list)==1 and len(b_list)==1 and ''.join(new_str)==str2:
            # str1 和 str2 有 2 个位置字符不同 且这2个字符相同
                mode = ''.join(mode)+'&'
            else:
            # str1 和 str2 有 2 个字符不同 且这2个字符不同
                mode = ''.join(mode)
        else:
            flag = 1
            mode = ''.join(mode)

        '''
        flag = 1 对应的情况：
        1）str1 和 str2 有三个或三个以位置上字符不同 但这些字符相同 - 则mode是 不同的那个字符通配 + 顶级域通配
        2）str1 和 str2 有两个位置上字符不同 但这些字符相同 - 则mode是 不同的那个字符通配 + 顶级域通配
        3） str1 和 str2 有一个位置上字符不同 - 新mode是 不同的那个字符通配

        flag = 0 对应的情况：
        1） str1 和 str2 有三个或三个以位置上字符不同 但这些字符不全是相同 - 则mode是 原 domain1 的主体部分
        2） str1 和 str2 有两个位置上字符不同 且这2个字符不同
        '''
        return flag,mode

    def match(self,domain1,domain2):
        """
        &:连续指示符
        #:数字通配符
        *:字母通配符
        $:数字/字母通配符
        %:顶级域通配符
        :param domain1:
        :param domain2:
        :return:
        """
        flag = 0
        mode = domain1
        if domain1 == domain2:
            sys.exit(-1)
        else:
            str1 = extract(domain1)
            '''
            domain1 : 2020504.com'
            str1:  ExtractResult(subdomain='', domain='2020504', suffix='com')
            '''
            str2 = extract(domain2)

            # 比较顶级域（后缀）
            if str1.suffix!=str2.suffix:
                if str1.domain == str2.domain:
                    flag = 1
                    mode = str1.domain+'.%'#枚举顶级域
            else:
                # 域名的主体部分长度相同
                if len(str1.domain)-len(str2.domain)==0:
                    idx = -1
                    prefix = ''
                    for i, r in enumerate(zip(str1.domain, str2.domain)):
                        '''
                        i: 第i个字符
                        r： str1.domain, str2.domain 的字符对
                        eg. domain1 : 2020504.com'; domain2:'0020524.com'; i:  0 r:  ('2', '0')
                        '''
                        # 当匹配到两个域名同一位置第一次出现不同字符时
                        if r[0] != r[1]:
                            # 用idx记录下出现不同字符的位置
                            idx = i
                            break
                        else:
                            prefix += r[0]
                    flag,mode = self.jump_match(str1.domain,str2.domain,idx)
                    if flag:
                        mode = mode+'.'+str1.suffix

            return flag,mode

if  __name__ == "__main__":
    # print Domains_Match().match('000x38.com', '000a38.com')
    # print Domains_Match().match('0000524.com','00001524.com')
    # print Domains_Match().match('00111524.com', '00221524.com')
    # print Domains_Match().match('00aaa1524.com', '00bbb1524.com')
    # print Domains_Match().match('2020504.com', '0020524.com')
    flag, mode = Domains_Match().match('2020534.com', '0020524.com')
