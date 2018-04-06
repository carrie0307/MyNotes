# Datatables基础使用整理

------
## 重要网站
* Datatables官网 [http://datatables.club/](http://datatables.club/)
* Datatables设置列表 [http://datatables.club/reference/option/](http://datatables.club/reference/option/)
* Datatables中文手册[http://datatables.club/manual/](http://datatables.club/manual/)

## 要引入的文件

在datatables官网[http://datatables.club/manual/install.html](http://datatables.club/manual/install.html)下方有响应js、css压缩包的下载链接

下载解压后，**media**文件夹内的js、css已足够一般的使用，一般引入的有一下一些：
```html
<!--第一步：引入Javascript / CSS （CDN）-->
<!-- DataTables CSS -->
<link rel="stylesheet" type="text/css" href="media/css/jquery.dataTables.css">

<!-- jQuery -->
<script type="text/javascript" charset="utf8" src="media/js/jquery.js"></script>

<!-- DataTables -->
<script type="text/javascript" charset="utf8" src="media/js/jquery.dataTables.js"></script>
```

或者，也可以通过**官方CDN**来引入
```html
<!-- DataTables CSS -->
<link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/1.10.13/css/jquery.dataTables.css">

<!-- jQuery -->
<script type="text/javascript" charset="utf8" src="http://code.jquery.com/jquery-1.10.2.min.js"></script>

<!-- DataTables -->
<script type="text/javascript" charset="utf8" src="http://cdn.datatables.net/1.10.13/js/jquery.dataTables.js"></script>

```


## 基础使用

**基础HTML代码**
```html
<!--第二步：添加如下 HTML 代码-->
<table id="table_id_example" class="display">
    <thead>
    <tr>
        <th>时间</th>
        <th>ip</th>
        <th>ip数量</th>
    </tr>
    </thead>
    <!--当动态加载数据时，tbody中数据空白即可，具体在js中处理-->
    <tbody>
    <tr>
        <td>---</td>
        <td>---</td>
    </tr>
    <tr>
        <td>---</td>
        <td>---</td>
    </tr>
    </tbody>
</table>
```

**js基础初始化**
```javascript
<script>
    <!--第三步：初始化Datatables-->
    $(document).ready(function () {
        $('#table_id_example').DataTable();
    });
</script>
```

**一些重要选项与设置**
```javascript
var t = $('table_id_example').DataTable({
                //DT不可以reinitial,如果需要重新加载，则要加上destroy
                destroy:true,
                
                //每页显示数据条数
                pageLength: 10, 
                
                //禁止分页（默认是打开的）
                paging: false，
                
                //ajax方式获取数据
                ajax: {//datatable默认为get方法请求
                //指定数据源
                url: "http://www.gbtags.com/gb/networks/uploads/a7bdea3c-feaf-4bb5-a3bd-f6184c19ec09/data.txt"
                        }
                
                //具体要显示的数据（共四种获取数据方式，这里写的是从js中获取）
                data: dataSet,                       
                
                //具体的每一列，data是代码中索引这一列的名称
                columns: [{
                    "data": null //此列不绑定数据源，用来显示序号
                },
                {
                    "data": "time"
                },
                {
                    "data": "ip"
                },
                {
                    "data": "ip_num"
                },
            ],
            
                //"columnDefs":可以对各列内容进行处理，从而显示想显示的内容
                columnDefs: [
                    {
                    //对第3（序号列是第0列）列处理
                    "targets": [3],
                    
                    //第3列的索引名是ip_num
                    "data": "ip_num",
                    
                    //对这一列数据显示上的操作
                    "render": function(data, type, full) {
                        /*
                        给表格内容加上了链接
                        return "<a title='"+data+"' href='/update?t_unid=" + data + "'>"+data+"</a>";
                        */
                        
                        //把数据+10后再显示
                        return data+10;
                        }
                    },
                    
                    //要显示的列的数量，（序号列是第0列）
                    {"targets": 3},
                ]
            });
            
            //对首列加上序号
            t.on('order.dt search.dt',
            function() {
                t.column(0, {
                    "search": 'applied',
                    "order": 'applied'
                }).nodes().each(function(cell, i) {
                    cell.innerHTML = i + 1;
                });
            }).draw();

```

**这里要注意dataSet的格式**
```javascript
[
{"time":   , "ip":   , "ip_num":    },
{"time":   , "ip":   , "ip_num":    },
{"time":   , "ip":   , "ip_num":    },
]
```

**数据获取**
数据获取部分主要参考自[此文](https://www.iteblog.com/archives/1257.html)

datatables数据获取共有**四种方式**

* HTML中静态数据
* Ajax 动态请求
* Javascript源码中获得
* Server-side processing

所能处理数据有三种形式：

* 数组(Arrays [])
* 对象(objects {})
* 实例(new myclass())

**重点了解对象(objects {})的使用即可**



* HTML中静态数据
这种方法只需在<tbody>中写入相应的数据即可， 因此不做示例；

* Ajax动态请求
以上文**基础设置**中的ajax请求为例，需要注意的是，datatables的**ajax默认请求方式是get**，且要注意**所请求数据的格式**；

```javascript
$('table_id_example').DataTable({
    ajax: {//datatable默认为get方法请求
         //指定数据源
        url: "http://www.gbtags.com/gb/networks/uploads/a7bdea3c-feaf-4bb5-a3bd-f6184c19ec09/data.txt"
           }
```

这里给出所请求数据，重点在于学习其格式：
```javascript
    {
    "data": [
        {
            "id": 1, 
            "url": "http://www.gbtags.com/gb/index.htm", 
            "title": "Online Program knowledge share and study platform"
        }, 
        {
            "id": 2, 
            "url": "http://www.gbtags.com/gb/listcodereplay.htm", 
            "title": "Share Code Gbtags"
        }, 
        {
            "id": 3, 
            "url": "http://www.gbtags.com/gb/gbliveclass.htm", 
            "title": "Online live Gbtags"
        }, 
        {
            "id": 4, 
            "url": "http://www.gbtags.com/gb/explore.htm", 
            "title": "Explorer Gbtags"
        }
    ]
}
```

* Javascript源码中获得
dataTable支持读取和解析JavaScript 中的数组。我们只需要将 JavaScript 数组传递给dataTable的data属性即可。
```javascript
var dataSet = [
    ['Trident','Internet Explorer 4.0','Win 95+','4','X'],
    ['Trident','Internet Explorer 5.0','Win 95+','5','C'],
    ['Trident','Internet Explorer 5.5','Win 95+','5.5','A'],
    ['Trident','Internet Explorer 6','Win 98+','6','A'],
];
 
$(document).ready(function() {
    $('#example2').dataTable( {
        "data": dataSet,
        "columns": [
            { "title": "Engine" },
            { "title": "Browser" },
            { "title": "Platform" },
            { "title": "Version", "class": "center" },
            { "title": "Grade", "class": "center" }
        ]
    } );   
} );
```

**要注意的是，这里给出columns的方式与上文不同。columns内给出的都是title,而上文中给出的都是data。目前尚未完全测试，但是以data给出时，传入的数据需要是{}(对象)形式的。**

**需要指出的是，这其实给我们另一种方式：我们可以先ajax请求数据，然后将数据写为{}（对象）或[](数组）的形式，然后将数据传递给datatable的data属性**

* Server-side processing
在服务器端生成需要的数据（一般都是Json格式的），然后返回给前端。而且这种情况我们可以利用dataTable的服务器端翻页。
```javascript
$(document).ready(function() {
    $('#example').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": "../processing.php"
    } );
} );
```

## 要注意的地方
* 引入js文件的时候注意顺序；
* 注意将表格的初始化至于`$(document).ready(function() { } )`函数中;
* datatables不能重复初始化，如有此需求，初始化时加上destroy:true,具体参见此文[http://www.philo.top/1899/11/30/DatatablesNote/](http://www.philo.top/1899/11/30/DatatablesNote/).


----
2017-09-11









