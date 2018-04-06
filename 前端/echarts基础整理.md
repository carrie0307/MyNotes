# Echarts基础整理

以echarts2.0为例
---
[echarts2.0 示例](http://echarts.baidu.com/echarts2/doc/example.html)
[下载地址](http://echarts.baidu.com/)

## 基础使用
* 引入js文件
```html
<script type="text/javascript" src="js/echarts.js"></script>
```

* 引入容器
```html
<div id="chartmain" style="width:600px; height: 400px;"></div>
```

* js初始化
```javascript
<script type="text/javascript">
        //指定图标的配置和数据
        var option = {
            title:{
                text:'ECharts 数据统计'
            },
            tooltip:{
            formatter : function (params) {
            /*
            以下是根据在统一图中会两类数据的柱状图所整理，以后具体应用可作为参考，如有不同还需要进一步调整
            */
            
            //具体表中有几类的数据（series有几项内容）params就有几项内容
            params[i].seriesName 第i类的类别名称
            
            //x,y都是value类型时，第i类x、y轴对应的值
            params[i].value[0]，params[i].value[1] 
            
            //x是category,y是value时，第i类x、y轴对应的内容
            params[i].name，params[i].value[1] 
            
            //换行用</br>实现
            
            //return 内容即为鼠标悬浮到图上对应位置所显示的内容
            
       }
            },
            legend:{
                data:['用户来源']
            },
            xAxis:{
                data:["Android","IOS","PC","Ohter"]
            },
            yAxis:{
                //格式化坐标轴上显示内容
                axisLabel : {
                    formatter: '{value} %'
                    //这样纵轴即会在对应的value后面显示上 % h，x轴同理
                }
            },
            series:[{
                name:'访问量',
                type:'line',
                data:[500,200,360,100]
            }]
        };
        //初始化echarts实例
        var myChart = echarts.init(document.getElementById('chartmain'));

        //使用制定的配置项和数据显示图表
        myChart.setOption(option);
    </script>
```

* 动态配置选项
有时候，xAxis的data、series的数据内容，是通过动态加载获得的，因此需要再次对option进行设置；
```javascript
$.ajax({
    type:"get",
    url:"/ip_scatter_off",
    cache:false,
    success:function(data1){
    
    /*
    以上省略若干代码，主要是对ajax请求所得数据的处理过程；
    
    假设最后得到了category_name、real_series等内容
    
    */
        option.xAxis[0].data=category_name; //设置x轴的显示
        option.series=real_series; //设置真实的数据
        
    /*
        或者，初始设置诗，series{data:[]}data置为空，然后通过option.series[i].data=**直接对data内容赋值
    */

        myChart.setOption(option); //再次设置Option

    },
    error:function(){
        alert("error!");
    },

});
```

## 需要注意的地方：
* 1.xAxis、yAxis的type属性有category和value两种，category不表示数值，value表示数值，一般默认也表示value；

* 2.加载数据给series赋值时一定注意格式，一般series的{}都包含一下几项内容
```javascript
series:[{
                name:'访问量',   //这种类型数据的名称
                type:'line',     //类型，点图、柱图或折现等
                data:[500,200,360,100]  //具体的数据
     }]
     
     /*
     series中有几个{}，就说明图中有几种需要区分表达的数据
     
     */
```
可以整体自定义series，也可以定义好series的name、type等，data写作**“data:[]”**，然后通过option.series[i].data = ××× 赋值

* 3.一般可以直接从[echarts2.0 示例](http://echarts.baidu.com/echarts2/doc/example.html)中粘贴代码，然后再修改就好；

* 4.tooltip 以及  formatter : function (params) 函数，看示例代码大概能明白意思。日后有时间再细致补充。

---
2017.09.10

