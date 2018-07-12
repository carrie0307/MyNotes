# SMTP简单复习与邮箱有效性验证

------

### 简单概述

总体来说，邮箱有效性验证参考于此文[如何校验邮件地址的有效性第二篇 ：原理一](https://blog.csdn.net/u011628250/article/details/72895998),即**通过与邮件服务器建立连接后，基于SMTP协议向邮件服务器进行验证**。

整体来说，可以通过与SMTP服务器的交互，基于**RCPT TO** 或 **VEFY**命令进行验证。关于SMTP协议下的命令，具体可参见[SMTP命令行介绍](https://blog.csdn.net/mergerly/article/details/17421949)。


### 与服务器交互

大体内容与[命令行发送邮件](https://www.cnblogs.com/fanyong/p/3498670.html)类似，但依旧自己进行整理。接下来演示根据SMTP协议约定，与SMTP服务器建立连接并进行基本交互的步骤：

* 获取邮件服务器地址(这里不属于SMTP协议)
根据DNS解析获取MX记录即可，这一过程可借助nslookup命令或dig命令进行。

* 通过telnet与邮件服务器建立连接
假设163邮件服务器地址是163mx03.mxmail.netease.com，则通过telnet命令与其25端口建立连接**telnet 163mx03.mxmail.netease.com 25**

* 通过HELO进行“打招呼”
“打招呼”命令：HELO 163mx03.mxmail.netease.com，完成打招呼后，可进行邮箱登陆或验证。

* 通过MAIL FROM和RCPT TO进行验证
完成打招呼后，通过MAIL FROM:<sender@domain.com>设置发送者邮箱，REPT TO:<verifying email@domain.com>设置接收者邮箱即待验证邮箱；**若verifying email@domain.com存在，则看到服务器返回250 Mail OK；若verifying email@domain.com不存在，则看到服务器返回550 User not found。**

![顺利完成验证的情况](http://ouzh4pejg.bkt.clouddn.com/mail_test1.png)

要注意的是，通过MAIL FROM:<sender@domain.com>设置发送者邮箱时可能存在权限问题(User has not permission)，即邮箱客户端不允许第三方登录的情况。和王ZH同学交流后，可以设置为MAIL FROM:<noreply@verifyemailaddress.com>。

![MAIL FROM权限不允许情况](http://ouzh4pejg.bkt.clouddn.com/mail_test2.png)

* 补充：命令行发邮件
在完成打招呼的基础上，通过“AUTH LOGIN”进行登录。根据服务器响应内容，依次输入邮箱用户名和邮箱密码的base64编码进行登陆(但也可能存在权限问题)。然后，即可通过MAIL FROM和RCPT TO等命令进行邮件发送，具体可参见[命令行发送邮件](https://www.cnblogs.com/fanyong/p/3498670.html)。

要注意的是，[如何校验邮件地址的有效性第二篇 ：原理一](https://blog.csdn.net/u011628250/article/details/72895998)就是通过这里的RCTP TO命令的返回内容，来确定邮箱地址有效性的。

* VEFY命令
根据指令格式，**VEFY 邮箱用户名**(eg.VERY tom@163.com)即可进行邮箱验证，但总是返回**502 Command not Implemented**。后来在一篇文章读到，出于安全起见服务器常会屏蔽VEFY命令，这应该是返回502的原因。

### 补充
* 饶YX
RYX邮箱有效性验证代码的学习，具体见https://github.com/carrie0307/MyNotes/blob/master/Python/%E4%BB%96%E4%BA%BA%E4%BB%A3%E7%A0%81%E5%AD%A6%E4%B9%A0/email_verify_single_ryx.py。

这里一方面用了发送邮件通过返回异常的情况进行判断(根据论文，当代码捕获到SMTP异常时，对应SMTP服务器返回的550错误。)；另一方面用了“退信”机制来判断。

* 王ZH
王ZH通过TELNET登录邮件服务器，借助RCPT TO 命令进行验证，代码具体见https://github.com/carrie0307/MyNotes/blob/master/Python/%E4%BB%96%E4%BA%BA%E4%BB%A3%E7%A0%81%E5%AD%A6%E4%B9%A0/email_verify_telnet_wzh.py。

### 其他
* 与SMTP服务器交互时，注意服务器返回码的含义；

* 在命令行中与SMTP服务器交互时，命令不可更改，不可重输；因此建议将要输入的内容先写入文档中，然后直接进行粘贴即可。