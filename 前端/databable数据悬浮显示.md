# datatable数据悬浮显示

------

## 方法一 
通过layer实现（需要下载layer.js)

## 方法二 columnDefs中的render方法
**具体参见[http://bbs.csdn.net/topics/392046175](http://bbs.csdn.net/topics/392046175)**
```javascript
var t = $('#table-id').DataTable({
            /*
            其他属性
            */
            columns: [
            
        ],
        //"columnDefs":可以对各列内容进行处理，从而显示想显示的内容
        columnDefs: [
            {
            "targets": [2], //对第二列数据进行处理
            "data": "category",
            "render": function(data, type, full) {
                var category = data + "类地址"; //这里可以对显示数据进行处理
                return category;
                }
            },
            
            {
            "targets": [4], //对第四列数据进行s处理
            "data": "domains",
            "render": function(data, type, full) {
                var domain_data="";
                var domain_num;
                if (domain_type != "all")
                {

                    for(var i=0;i<data.length;i++)
                    {
                        domain_data = domain_data + data[i] + '\n';
    	            }
                    return "<a title='"+domain_data+"' href=''>"+data.length+"</a>";
                    //title的内容是悬浮显示的
                    //<a>标签中间的内容是实际显示的
                    //这里的<a>标签也可以换做<span>
                }
        ],

        });


```
