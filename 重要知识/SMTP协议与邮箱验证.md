# SMTP简单复习与邮箱有效性验证

------

### 简单概述

总体来说，邮箱有效性验证参考于此文[如何校验邮件地址的有效性第二篇 ：原理一](https://blog.csdn.net/u011628250/article/details/72895998),即**通过与邮件服务器建立连接后，基于SMTP协议向邮件服务器进行验证**。

不同的是，上文中是通过模拟邮件发送，通过RCPT TO命令进行的，而实际SMTP协议提供了命令进行邮箱存在性验证，即**VEFY命令**。关于SMTP协议下的命令，具体可参见[SMTP命令行介绍](https://blog.csdn.net/mergerly/article/details/17421949)。


### 与服务器交互

大体内容与[命令行发送邮件](https://www.cnblogs.com/fanyong/p/3498670.html)类似，但依旧自己进行整理。接下来演示根据SMTP协议约定，与SMTP服务器建立连接并进行基本交互的步骤：

* 获取邮件服务器地址(这里不属于SMTP协议)
根据DNS解析获取MX记录即可，这一过程可借助nslookup命令或dig命令进行。

* 通过telnet与邮件服务器建立连接
假设163邮件服务器地址是163mx03.mxmail.netease.com，则通过telnet命令与其25端口建立连接**telnet 163mx03.mxmail.netease.com 25**

* 通过HELO进行“打招呼”
“打招呼”命令：HELO 163mx03.mxmail.netease.com，完成打招呼后，可进行邮箱登陆或验证。

* 邮箱登陆与邮件发送
完成打招呼后，通过“AUTH LOGIN”进行登录。根据服务器响应内容，依次输入邮箱用户名和邮箱密码的base64编码进行登陆。然后，即可通过MAIL FROM和RCPT TO等命令进行邮件发送，具体可参见[命令行发送邮件](https://www.cnblogs.com/fanyong/p/3498670.html)。

要注意的是，[如何校验邮件地址的有效性第二篇 ：原理一](https://blog.csdn.net/u011628250/article/details/72895998)就是通过这里的RCTP TO命令的返回内容，来确定邮箱地址有效性的。

* VEFY命令
根据指令格式，**VEFY 邮箱用户名**(eg.VERY tom@163.com)即可进行邮箱验证，但总是返回**502 Command not Implemented**。后来在一篇文章读到，出于安全起见服务器常会屏蔽VEFY命令，这应该是返回502的原因。

## 其他
* 与SMTP服务器交互时，注意服务器返回码的含义；

* 在命令行中与SMTP服务器交互时，命令不可更改，不可重输；因此建议将要输入的内容先写入文档中，然后直接进行粘贴即可。