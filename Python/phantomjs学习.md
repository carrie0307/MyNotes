# phantomjs使用实例--腾讯网站安全检测结果爬取

------

最初此文是在2017.08写的，在2018.01使用到phantomjs时又有了一些感触，故补充。


### 此次爬取学到及以后要注意的地方：
* 对网页上想爬取的内容，首先选中**查看元素**,然后再看整体页面。这次出现的情况是，自己始终认为网站判断结果html上没有，而直接查看的确也显示没有；但对网站检测结果**查看元素**,则看到了html的结果；
 ![直接查看网页源码，无检测结果](http://ouzh4pejg.bkt.clouddn.com/image/png/js.pngload_score.png)
**注意这里的onclick函数，出发了响应的js。虽然此文后续没有通过js获取结果，但查找这种函数所在源文件分析js代码应该是必要的。**

* 有时直接打开已包含提交值的网页还是找不到对应的结果，需要用phantomjs模拟输入与点击过程，才可以获取到数据；例如，腾讯电脑管家爬取时，用phantomjs打开https://guanjia.qq.com/online_server/result.html?url=baidu.com并不能获取到包含结果的源代码，必须要模拟通过首页https://guanjia.qq.com/online_server/result.html提交数据与点击button的过程，才能获得数据。

* 时延:有时网页不能立刻加载出来，会导致无法获取到数据。因此在driver.get(url)与page=driver.page_source的之间需要设定一定的时延。


![查看元素后，看到了响应的结果](http://ouzh4pejg.bkt.clouddn.com/image/png/js.pngscore_img.png)

* 接上，查看元素的结果无法从源码直接获得，但却可以查看到，因此要想到用**phantomjs模拟浏览器的操作：发送要检测的域名**，如下代码`L56--L61`,同时要考虑页面加载完全的等待问题。关于等待，有三种方式，参见[此文](http://blog.csdn.net/zahuopuboss/article/details/52987953)。

* 关于timeout()：之前给phantomjs设置了超时，但有些页面总会一直卡死。因此设置了timeout()来限制时间。超时后报错，捕获异常继续进行新的处理;

* phantomjs性能优化：为了稳定没有尝试多进程跑phantomjs，但为了加快效率，在获取100条记录后才关闭driver(driver.close(),driver.quit()),关于此参见[此文](https://zhuanlan.zhihu.com/p/25507989)。

* kill 进程问题：在连续运行phantomjs后，quit()可能产生异常，因此在except中获取有关phantomjs的进程id，直接kil。

* 关于`L21`的map,网站加载图片的不同，刚好对应了不同类型的网站。这是从js代码里找到的对应关系。虽然此次数据的爬取并为获取动态js内容，但是**查看相关动态获取js，总还是有一定帮助的**。这里对应的js代码为https://3gimg.qq.com/tele_safe/cgi/js/query.url.score.js?20131128，在寻找上图的onclick()函数时发现.
![](http://ouzh4pejg.bkt.clouddn.com/js.png)


```python
# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from timeout import timeout
import os
import MySQLdb
import Queue

'''
1.png -- 1
2.png，3.png -- 2 危险
48_money.png -- 2 危险
6.png -- 4 未知
'''

domains_q = Queue.Queue()
webscan_map = {'1.png': '1', '2.png': '2', '3.png': '2', '6.png': '4', '48_money.png': '2'}

conn = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
cur=conn.cursor()
def get_domains():
    '''
    获取要处理的域名
    '''
    global domains_q
    SQL = "SELECT ID, domain FROM domain_index WHERE source = '103' and ID not in (SELECT ID from other_info)"
    cur.execute(SQL)
    result = cur.fetchall()
    domains_q = Queue.Queue()
    for item in result:
        domains_q.put([int(item[0]), str(item[1])])
# cur.close()
# conn.close()

def kill_process():
    '''
    杀掉phantomjs的进程
    '''
    print 'kill processes ...\n'
    r = os.popen("ps -ef|grep 'phantomjs' |grep -v grep |awk '{print $2}'") # 获取执行结果
    text = r.read()
    r.close()
    pids = text.split('\n')
    for pid in pids:
        cmd = "kill " + pid
        print cmd
        os.system(cmd)


@timeout(10) # 防止卡死的情况
def phantomjs_get_html(driver):
    '''
    通过phantomjs获取判断结果的页面
    '''
    driver.get("https://guanjia.qq.com/online_server/webindex.html")
    driver.find_element_by_id("search_site").send_keys(str(domain))
    driver.find_element_by_id("search_button").click()
    driver.implicitly_wait(5) # 隐式等待10s
    page = etree.HTML(driver.page_source)
    return page


def get_judge_res(page):
    '''
    从判断将结果页面中获取判断结果
    '''
    global webscan_map
    url = page.xpath('//*[@id="score_img"]/img/@src')[0]
    img = str(str(url).split('/')[-1]) # 获取图片名称（编号）
    qq_judge = webscan_map[img]
    return qq_judge



def save_res(res_list):
    '''
    存储结果
    '''
    print 'save res ...\n'
    for item in res_list:
        # sqlstr = "INSERT INTO other_info(ID,web_judge_result) VALUES(%s,'%s')" %(item[0], item[1])
        sqlstr = "UPDATE other_info SET web_judge_result = '%s' WHERE ID = %s" %(item[1], item[0])
        cur.execute(sqlstr)
    conn.commit()
    print 'res saved ...\n'


if __name__ == '__main__':
    counter = 0
    get_domains()
    res_list = []
    driver = webdriver.PhantomJS(executable_path="/usr/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
    while True:
        if not domains_q.empty():
            ID, domain = domains_q.get()
        else:
            break
        try:
            page = phantomjs_get_html(driver)
            qq_judge = get_judge_res(page)
            res_list.append([ID,qq_judge])
            print 'NO.' + str(counter) + '  ' + domain + '  ' + qq_judge
        except:
            # 可能出现卡死导致的Timeout
            # page.xpath('//*[@id="score_img"]/img/@src')提取不到或判断结果为load.gif
            domains_q.put([ID, domain])
            continue
        counter += 1
        if counter%99 == 0:
            try:
                save_res(res_list)
            except Exception, e:
                print str(e)
                print '存储出错 ...'
            res_list = []
            try:
                driver.close()
                driver.quit()
            except: #  不能正常关闭则杀掉进程
                kill_process()
            finally:
                driver = webdriver.PhantomJS(executable_path="/usr/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
    save_res(res_list)
    cur.close()
    conn.close()

```

