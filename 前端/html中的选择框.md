# html中的选择框

------

## 方法一：<select>

* **html代码**

```html
<select id="bili">
  <option value="volvo">Volvo</option>
  <option value="saab">Saab</option>
  <option value="opel">Opel</option>
  <option value="audi">Audi</option>
</select>
```

* **js代码**

```javascript
//需要引入jQuery
$(document).ready(function(){
    var text;
    var value;
    $("#bili").change(function(){
     text = $("#bili").find("option:selected").text();//选中的文本
     value = $("#bili").find("option:selected").val();//选中的值
      /*
      	其他相关操作
      */
    });
});

```


## 方法二：bootstrap类 + button + li

* **html代码**

```html
 <div class="btn-group">
 <!--class="btn-group"是bootstrp中的一个类，因此需要引入bootstrap-->

	<button id="type-button" type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">赌博
		<span class="caret"></span>
	</button>
	<ul class="dropdown-menu" role="menu">
	    <!--option_select(param)函数在js代码中定义，通过option_select改变选中的内容，并触发相关函数-->
		<li><a onclick="option_select('Gamble');">赌博</a></li>
		<li><a onclick="option_select('Porno');">色情</a></li>
		<li><a onclick="option_select('all');">全部</a></li>
		<li class="divider"></li>
	</ul>

</div>
```

* **js代码**

```javascript
//当button被点击时，会出发此函数
 option_select=function(param){

    $('#type-button').text = param;
    var type_dict = {"Gamble":"赌博", "Porno":"色情", "all":"全部"}
    //改变button上显示的内容
    document.getElementById("type-button").innerHTML=type_dict[param];
    /*
        要进行的其他操作
    */
    }

```

