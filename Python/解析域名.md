# 解析URL及URL中的域名信息

## 解析url：urlparse

```
from urlparse import urlparse
from urlparse import urlunparse # urlparse的逆过程
from urlparse import urljoin

o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
print o
'''
[Output]:
ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment='')
'''
# 在以上基础上，还可以获取**端口**和**主机名**
print o.port
# [Output]: 80
print o.hostname
# [Output]:www.cwi.nl

# 将解析后的url复原
o = [:]
print urlunparse(0)
# [Output]: http://www.cwi.nl:80/%7Eguido/Python.html

base_url = 'http://www.cwi.nl/%7Eguido/Python.html'
print urljoin(base_url, 'FAQ.html')
# [Output]: 'http://www.cwi.nl/%7Eguido/Python.html'
```

## 从url中解析域名

```python
import tldextract
url = 'http://www.baidu.com'
# 或去接输入一个域名tldextract.extract('baidu.com')
tldextract.extract(url)
'''
[Output]:ExtractResult(subdomain='www', domain='baidu', suffix='com')
'''
tldextract.extract(url).registered_domain
'''
[Output]:baidu.com
'''
```
