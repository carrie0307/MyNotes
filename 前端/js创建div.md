# JS创建div

------
**js创建新的div/元素**
```javascript
// 创建新的div
var div = document.createElement("div");

//设置新的div的id
div.id = "the_div"; 

//设置新div的class
div.className="CssStyle1";//给父div设置class属性  

//设置新创建div的style的内容
div.style.cssText="width:1500px;height:400px; margin-top:50px;" 

/*
    设置div的style另一种方法
    对于dom中原存在的div，也可以用以下方法设置style的一些属性

*/

//给父div的style属性的clear赋值  
div.style.clear="both";

//给父div的style属性的border赋值  
div.style.border="0.5px solid #DBEAF9";

//给父div的style属性的margin-bottom赋值
div.style.margin-bottom="10px"; 

//设置长、宽和背景等
div.style.height = "400px";
div.style.width = "400px";
div.style.backgroundColor = "blue";

//将该div创建在id=main_content的元素下
var cell = document.getElementById("main_content"); 
cell.appendChild(div);

//或直接添加到<body>内
document.body.appendChild(div)； 

//设置div的内容（必须在appendChild将新建div加入dom后，才可以获取）
document.getElementById(div.id).innerHTML = 'Fred Flinstone';
        
```
