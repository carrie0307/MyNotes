#-*- coding: utf-8 -*-

import re
import os

def _load_sub_names(options={'full_scan':True,'file':'subnames.txt'}):

    filename = options.get('file')
    if options.get('full_scan') and filename == 'subnames.txt':
        _file = 'dict/subnames_full.txt'
    else:
        if os.path.exists(filename):
            _file = filename
        elif os.path.exists('dict/%s' % filename):
            _file = 'dict/%s' % filename
        else:
            exit(-1)
    wildcard_list = []
    regex_list = []
    lines = set()
    with open(_file) as f:
        for line in f.xreadlines():
            sub = line.strip()
            if not sub or sub in lines:
                continue
            if sub.find('{alphnum}') >= 0 or sub.find('{alpha}') >= 0 or sub.find('{num}') >= 0:
                sub = sub.replace('{alphnum}', '[a-z0-9]')
                sub = sub.replace('{alpha}', '[a-z]')
                sub = sub.replace('{num}', '[0-9]')
                if sub not in wildcard_list:
                    wildcard_list.append(sub)
                    regex_list.append('^' + sub + '$')
            else:
                lines.add(sub)
    #print wildcard_lines #['{alphnum}', '{alphnum}{alphnum}', '{alphnum}{alphnum}{alphnum}']
    #print wildcard_list #['[a-z0-9]', '[a-z0-9][a-z0-9]', '[a-z0-9][a-z0-9][a-z0-9]']
    #lines  子域
    #print len(normal_lines)
    #print len(lines)
    # ^[a-z0-9]$|^[a-z0-9][a-z0-9]$|^[a-z0-9][a-z0-9][a-z0-9]$
    # =>{alphnum}/{alphnum}{alphnum}/{alphnum}{alphnum}{alphnum}
    normal_lines = list(lines)
    pattern = '|'.join(regex_list)
    if pattern:
        _regex = re.compile(pattern)
        if _regex:
            for line in normal_lines[:]:
                if _regex.search(line):
                    normal_lines.remove(line)
    print len(normal_lines)

def _load_next_sub(options={'full_scan':True}):
    """
    枚举子域
    :param options: next_sub.txt/next_sub_full.txt
    :return: 
    """
    #next_sub.txt 添加子域集
    #next_sub_full.txt  枚举一位及两位的子域且添加已存子域
    next_subs = [] #子域列表
    _set = set() #已存集合
    _file = 'dict/next_sub.txt' if not options.get('full_scan') else 'dict/next_sub_full.txt'
    with open(_file) as f:
        for line in f:
            sub = line.strip()
            if sub and sub not in next_subs:
                tmp_set = {sub}#待检测子域
                while len(tmp_set) > 0:
                    # print "++++start+++++"
                    item = tmp_set.pop()
                    # print item
                    if item.find('{alphnum}') >= 0:
                        # print "-----start-----"
                        for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                            elem = item.replace('{alphnum}', _letter, 1)
                            # print elem
                            tmp_set.add(elem)
                        # print "-----end-----"
                    elif item.find('{alpha}') >= 0:
                        # print '*******'
                        for _letter in 'abcdefghijklmnopqrstuvwxyz':
                            tmp_set.add(item.replace('{alpha}', _letter, 1))
                    elif item.find('{num}') >= 0:
                        # print '-------'
                        for _letter in '0123456789':
                            tmp_set.add(item.replace('{num}', _letter, 1))
                    elif item not in _set:#出现新的子域
                        # print "===start==="
                        # print item
                        # print "===end==="
                        next_subs.append(item)  # 添加新的子域
                        _set.add(item)#标记为已添加
                    # print "++++end+++++"
    print len(_set)
    print len(next_subs)



if __name__ == "__main__":
    _load_next_sub()