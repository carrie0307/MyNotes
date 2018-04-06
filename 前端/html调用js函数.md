# HTML调用js文件中$(document).ready内的函数

------

#### 现象

**不能调用jquery中ready里面定义的函数:如下，在html中引入调用显示函数未定义**
```javascript

$(document).ready(function(e) {

function test(){

alert('test!');

}
});
```

#### 解析

**ready也相当于一个函数，即新建一局部函数作用域，外面 当然不可用。和js的onload函数差不多，就比如onload="ready()"**
```javascript
function ready(){
    function test(){
        alert("test!");
    }
}
```

#### 解决办法
解决方法：

* 把要在外面调用的函数test()**从$(document).ready 单独抽出来**，供调用！

* 将要在外部调用的函数的**作用域提升为全局作用域（变量申明）**，在js文件中如下：
```javascript
var test;//定义一全局变量，可省略

$(document).ready(function(e) {
    test=function(){
        alert('test!');
    }
});

test(); //现在可以在外部调用了
```

**注：如果是在html的<script>标签的document.ready()内定义的函数要调用，也可以用同样的方法。**

---
2017.10.19
