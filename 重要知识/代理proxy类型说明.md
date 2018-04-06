# 代理IP类型说明

------
以下内容转载自[proxy代理类型](http://gohom.win/2016/01/20/proxy-type/)

## 透明代理

```
REMOTE_ADDR = Proxy IP
HTTP_VIA = Proxy IP
HTTP_X_FORWARDED_FOR = Your IP
```
透明代理虽然可以直接“隐藏”你的IP地址，但是还是可以从HTTP_X_FORWARDED_FOR来查到你是谁

## 匿名代理
```
REMOTE_ADDR = proxy IP
HTTP_VIA = proxy IP
HTTP_X_FORWARDED_FOR = proxy IP
```
匿名代理比透明代理进步了一点：别人只能知道你用了代理，无法知道你是谁。

## 混淆代理
```
REMOTE_ADDR = Proxy IP
HTTP_VIA = Proxy IP
HTTP_X_FORWARDED_FOR = Random IP address

```
与匿名代理相同，如果使用了混淆代理，别人还是能知道你在用代理，但是会得到一个假的IP地址，伪装的更逼真

## 高匿代理
```
REMOTE_ADDR = Proxy IP
HTTP_VIA = not determined
HTTP_X_FORWARDED_FOR = not determined
```

高匿代理让别人根本无法发现你是在用代理，所以是最好的选择。

* 解释
    高度匿名代理不改变客户机的请求，这样在服务器看来就像有个真正的客户浏览器在访问它，这时客户的真实IP是隐藏的，服务器端不会认为我们使用了代理。

    普通匿名代理能隐藏客户机的真实IP，但会改变我们的请求信息，服务器端有可能会认为我们使用了代理。不过使用此种代理时，虽然被访问的网站不能知道你的ip地址，但仍然可以知道你在使用代理，当然某些能够侦测ip的网页仍然可以查到你的ip。
    
    透明代理，它不但改变了我们的请求信息，还会传送真实的IP地址。

