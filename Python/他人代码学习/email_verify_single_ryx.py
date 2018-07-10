# !/usr/bin/python

"""
RYX邮箱有效性验证代码，通过核心函数verify_sigaddr()对待验证邮箱进行验证；
注:代码中注释均为自己学习添加，非作者原注释。

由于邮箱的退信机制和发信异常处理机制，当邮箱地址无效时，发送一封测试邮件可能会产生的现象有两个
    1 邮件服务器发回一封系统退信
    2 产生错误异常(SMTP的异常smtplib.SMTPRecipientsRefused和smtplib.SMTPServerDisconnected)

三种核心服务：SMTP，IMAP服务和POP3服务；在本代码中应用如下：
1. 用SMTP登陆邮箱并发送邮件；
2. 用IMAP服务读取邮箱中邮件数量(并写入日志)，通过邮箱数量比对判断是否有新邮件(为是否有退信邮件奠定基础)；
3. 用POP3服务读取邮箱中的最新邮件。

关于SMTP,IMAP和POP3,可参考以下三文
https://www.zhihu.com/question/24605584
http://help.163.com/09/1223/14/5R7P6CJ600753VB8.html
https://blog.csdn.net/kavensu/article/details/8085409
"""

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import poplib
import smtplib
import re
import random
import imaplib
import time
import MySQLdb
import sys
import extend
import robot

db = MySQLdb.connect(user="root", passwd="", host="localhost", db="email")
cursor = db.cursor()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def alter_list(list, addr):
    # 将原有表中挂掉的邮箱换一个
    list_all = ['1115771363@qq.com', 'hitwh140420117@163.com', 'jizhongyi111@126.com', 'hitwh140420117@yeah.net',
                'hitwh140420117@sina.com', 'hitwh140420117@sohu.com', '18816311125@189.cn']
    while True:
        alter_addr = random.sample(list_all, 1)[0]
        if alter_addr not in list:
            # list[list.index(addr)]=alter_addr
            # list.pop(list.index(addr))
            list.append(alter_addr)
            break


def LoginMail(hostname, user, password):
    """
    功能:通过IMAP读取邮箱邮件数量，判断是否有新邮件
    通过IMAP服务读取邮件数量，并写入本地日志中。每次通过当前邮件数量与日志中上次邮件数量比对来盘多是否有新的邮件。
    """
    new = 0
    r = imaplib.IMAP4_SSL(hostname)
    r.login(user, password)
    x, y = r.status('INBOX', '(MESSAGES UNSEEN)')
    allmes, unseenmes = mes, unmes = re.match(r'.*\s+(\d+)\s+.*\s+(\d+)', y[0].decode('utf-8')).groups()
    tomail = ('%s have  %s message, %s is unseenmes' % (user, allmes, unseenmes))
    with open("tomail.txt", 'r') as f:  # 从最后一行开始读
        a = reversed(f.readlines())
    for line in a:
        line_man = line.strip()
        if user in line_man:
            s = re.findall('\d+', line_man)  # list的倒数第二个元素是邮件数量
            if allmes != s[-2]:  # 有新邮件
                with open('tomail.txt', 'a+') as f:
                    f.write(tomail + '\n')
                new = 1
            break
    r.logout()
    return new


# 取回新邮件并解析

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def print_info(msg, indent=0):
    flag = 0
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
                    if re.match(r'(p|P)ost(M|m)aster@\w+.(c(om|n)|net)', addr):
                        flag = 1
                    # 表示是一封系统退信
            print('%s%s: %s' % ('  ' * indent, header, value))
        print('\n')
    return flag


def verify_sigaddr(task_name, verify_addr, verify_option, extend_option, bt_option):
    """
    param:task_name:
    param:verify_addr:待验证邮箱地址
    param:verify_option
    param:extend_opeion:
    param:bt_option:
    """

    count = 0
    flag = True
    model_qq = r'\d{5,11}@qq.com'  # 匹配QQ邮箱:5到11位的数字作为邮箱名
    model_163_126 = r'[a-zA-Z][a-zA-Z0-9\_]{4,16}[a-zA-Z0-9]@1(63|26).com'  # 匹配163,126邮箱：6到18位，以字母开头，以字母或数字结尾，可由字母数字下划线组成
    model_yeah = r'[a-zA-Z][a-zA-Z0-9\_]{4,16}[a-zA-Z0-9]@yeah.net'  # yeah.net,规则与163相同
    model_sina = r'[a-z0-9][a-z0-9\_]{2,14}[a-z0-9]@sina.com'  # 匹配新浪邮箱：4到16位，字母小写或数字或下划线，下划线不能在结尾
    model_sohu = r'[a-zA-Z][a-zA-Z0-9\_]{5,15}@sohu.com'  # 匹配搜狐邮箱：6到16位，字母开头，字母数字下划线
    model_189 = r'\d{11}@189.cn'  # 用电话号码命名
    model_edu = r'[a-zA-Z0-9]\w*@\w+.edu.cn'  # 高校邮箱

    # list_all=['1115771363@qq.com','hitwh140420117@163.com','jizhongyi111@126.com','hitwh140420117@yeah.net','hitwh140420117@sina.com','hitwh140420117@sohu.com','18816311125@189.cn']

    verifyList = {}
    list = []
    print (verify_option)
    # 根据验证选项确定用什么邮箱进行验证？？
    if verify_option.find('0') >= 0:
        list.append('jizhongyi111@126.com')
        verifyList['126'] = 1
    if verify_option.find('1')  >= 0:
        list.append('hitwh140420117@163.com')
        verifyList['163'] = 1
    if verify_option.find('2') >= 0:
        list.append('1115771363@qq.com')
        verifyList['qq'] = 1
    if verify_option.find('3') >= 0:
        list.append('hitwh140420117@sina.com')
        verifyList['sina'] = 1
    if verify_option.find('4') >= 0:
        list.append('hitwh140420117@sohu.com')
        verifyList['sohu'] = 1
    if verify_option.find('5') >= 0:
        list.append('18816311125@189.cn')
        verifyList['189'] = 1
    if verify_option.find('6') >= 0:
        list.append('hitwh140420117@yeah.net')
        verifyList['yeah'] = 1

    print (list)
    new_list = []  # 收到新邮件的邮箱

    for from_addr in list:
        temp = from_addr[from_addr.find('@') + 1: from_addr.find('.')]
        if from_addr == '1115771363@qq.com':
            password = 'xxrlardzgvezhihg'  # 授权码的问题
            smtp_server = 'smtp.qq.com'
            imap_server = 'imap.qq.com'
            # pop3_server='pop.qq.com'
            password_imap = 'zoxreyhbujdnbacc'
        elif from_addr == 'hitwh140420117@163.com':
            password = 'RaoYuXin1234'
            smtp_server = 'smtp.163.com'
            imap_server = 'imap.163.com'
            # pop3_server='pop.163.com'
            password_imap = 'RaoYuXin1234'
        elif from_addr == 'jizhongyi111@126.com':
            password = 'jizhongyi111'
            smtp_server = 'smtp.126.com'
            imap_server = 'imap.126.com'
            # pop3_server='pop.126.com'
            password_imap = 'jizhongyi111'
        elif from_addr == 'hitwh140420117@yeah.net':
            password = 'RaoYuXin1234'
            smtp_server = 'smtp.yeah.net'
            imap_server = 'imap.yeah.net'
            # pop3_server='pop.yeah.net'
            password_imap = 'RaoYuXin1234'
        elif from_addr == 'hitwh140420117@sohu.com':
            password = 'yaoyuxin1234'
            smtp_server = 'smtp.sohu.com'
            imap_server = 'imap.sohu.com'
            # pop3_server='pop3.sohu.com'
            password_imap = 'yaoyuxin1234'
        elif from_addr == 'hitwh140420117@sina.com':
            password = 'yaoyuxin1234'
            smtp_server = 'smtp.sina.com'
            imap_server = 'imap.sina.com'
            # pop3_server='pop.sina.com'
            password_imap = 'yaoyuxin1234'
        elif from_addr == '18816311125@189.cn':
            password = 'raoyuxin1234'
            smtp_server = 'smtp.189.cn'
            imap_server = 'imap.189.cn'
            # pop3_server='pop.189.cn'
            password_imap = 'raoyuxin1234'
        try:
            msg = MIMEText('hello,send by Python..', 'plain', 'utf-8')
            msg['From'] = _format_addr('您的好友<%s>' % from_addr)
            msg['To'] = _format_addr('管理员<%s>' % verify_addr)
            msg['Subject'] = Header('来自朋友的问候。。。。', 'utf-8').encode()
            server = smtplib.SMTP(smtp_server, 25)
            # server.set_debuglevel(1)#打印通信进程
            server.starttls()
            # 登录发信邮箱
            server.login(from_addr, password)
            try:
                server.sendmail(from_addr, [verify_addr], msg.as_string())
            except smtplib.SMTPDataError:
                alter_list(list, from_addr)
                continue
            # server.sendmail(from_addr,[verify_addr],msg.as_string())
            server.quit()
            print(from_addr, '已投递')
            time.sleep(1)
            try:
                # 通过LoginMail函数借助IMAP服务读取邮件数量判断是否有新邮件
                is_new = LoginMail(imap_server, from_addr, password_imap)  # 当is_new==1时，说明有新邮件，遂检查是否是退信
            except Exception as e:
                print(e)
                continue
            print(is_new)
            if is_new == 1:  # 如果存在新邮件，则取回检查是否是退信
                new_list.append(from_addr)
        except smtplib.SMTPRecipientsRefused:  # 邮箱异常处理
            print(from_addr, '验证其无效')
            verifyList[temp] = '2'
            flag = False
        except smtplib.SMTPServerDisconnected:  # 挂了一个邮箱
            print(from_addr, '连接失败，换一个邮箱进行验证')
            verifyList[temp] = -1
            alter_list(list, from_addr)
            #print(list)
            continue
        except smtplib.SMTPSenderRefused:
            alter_list(list, from_addr)

    # print(new_list)
    for new_mail in new_list:
        try:
            if new_mail == '1115771363@qq.com':
                password = 'xxrlardzgvezhihg'  # 授权码的问题
                pop3_server = 'pop.qq.com'
            elif new_mail == 'hitwh140420117@163.com':
                password = 'RaoYuXin1234'
                pop3_server = 'pop.163.com'
            elif new_mail == 'jizhongyi111@126.com':
                password = 'jizhongyi111'
                pop3_server = 'pop.126.com'
            elif new_mail == 'hitwh140420117@yeah.net':
                password = 'RaoYuXin1234'
                pop3_server = 'pop.yeah.net'
            elif new_mail == 'hitwh140420117@sohu.com':
                password = 'yaoyuxin1234'
                pop3_server = 'pop3.sohu.com'
            elif new_mail == 'hitwh140420117@sina.com':
                password = 'yaoyuxin1234'
                pop3_server = 'pop.sina.com'
            elif new_mail == '18816311125@189.cn':
                password = 'raoyuxin1234'
                pop3_server = 'pop.189.cn'
            # 通过邮箱POP服务取回邮箱中最新的邮件
            server = poplib.POP3_SSL(pop3_server)
            server.user(new_mail)
            server.pass_(password)
            # print('Message:%s. Size:%s'%server.stat())
            resp, mails, octects = server.list()
            # print(mails)

            index = len(mails)
            resp, lines, octects = server.retr(index)

            # msg_cotent=b'\r\n'.join(lines).decode('utf-8')
            try:
                msg_cotent = b'\r\n'.join(lines).decode('GBK')  # 获得整个邮件的原始文本
            except UnicodeDecodeError:
                msg_cotent = b'\r\n'.join(lines).decode('utf-8')
            # msg_cotent=b'\r\n'.join(lines).decode('GBK')#获得整个邮件的原始文本
            msg = Parser().parsestr(msg_cotent)  # 把邮件解析为message对象
            is_backmail = print_info(msg)
            # print(is_backmail) print_info在输出的同时对邮件解析，判断是否是退信
            # 检查是否是退信邮件
            if is_backmail == 1:
                print(new_mail, '验证其无效\n')
                verifyList[temp] ="3"
                count = count + 1
            server.quit()
        except Exception as e:
            print(e)
            print(new_mail)
            continue


    # print('共有',count,'个邮箱通过交叉验证证明',verify_addr,'无效')
    if extend_option == '1':
        try:
            temp_dict = extend.extend(task_name)
            extend.exaddr_verify(temp_dict)
        except Exception as e:
            print (e)

    if bt_option == '1':
        try:
            robot.mutilTrack(task_name)
        except Exception as e:
            print(e)

    print(verifyList)
    temp = []
    for i in verifyList.keys():
        temp.append(i+':'+ str(verifyList[i]))
    print (temp)
    db = MySQLdb.connect(user="root", passwd="", host="localhost", db="email")
    cursor = db.cursor()
    if flag == False:
        sql = 'update verify_email set status= "1",result="0",detail="%s" where email="%s";' % (str(temp), verify_addr)
        cursor.execute(sql)
        db.commit()
    elif flag == True and count > len(list)/2:
        sql = 'update verify_email set status= "1",result="0",detail="%s" where email="%s";' % (str(temp), verify_addr)
        cursor.execute(sql)
        db.commit()
    else:
        sql = 'update verify_email set status= "1",result="1",detail="%s" where email="%s";' % (str(temp), verify_addr)
        cursor.execute(sql)
        db.commit()


    return True

if __name__ == '__main__':
    sql = "select * from verify_email where status= '0' and task='%s'" % (sys.argv[1])
    cursor.execute(sql)
    result = cursor.fetchone()
    verify_sigaddr(result[6], result[0], result[1], result[2], result[7])
    sql = 'update task set status= "1"where taskName="%s";' % (sys.argv[1])
    cursor.execute(sql)
    db.commit()