# Bootstrap-Panel

------
**本文参考自[菜鸟教程-bootstrap-panel](http://www.runoob.com/bootstrap/bootstrap-panels.html)**

**表格式、列表式的面板，具体可详见上文**

## 要引入的文件
```html
 <!-- 新 Bootstrap 核心 CSS 文件 -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
     
    <!-- 可选的Bootstrap主题文件（一般不使用） -->
    <script src="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap-theme.min.css"></script>
     
    <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
    <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
    
    <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
    <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
```
## 普通panel
```html
<!DOCTYPE html>
<html>
<head>
    <!--这里引入相应的文件-->
	<meta charset="utf-8"> 
</head>

<body>
    <div class="panel panel-default">
    	<div class="panel-body">
    		这是一个基本的面板(这里是面板内容）
    	</div>
    	<div class="panel-footer">面板脚注</div>
    </div>
</body>
</html>
```

## 带颜色主题的面板
```javascript
<!DOCTYPE html>
<html>
<head>
    <!--这里引入相应的文件-->
	<meta charset="utf-8"> 
</head>

<body>
<!-深蓝色--->
<div class="panel panel-primary">
	<div class="panel-heading">
		<h3 class="panel-title">面板标题</h3>
	</div>
	<div class="panel-body">
		这是一个基本的面板
	</div>
</div>

<!-浅绿色--->
<div class="panel panel-success">
	<div class="panel-heading">
		<h3 class="panel-title">面板标题</h3>
	</div>
	<div class="panel-body">
		这是一个基本的面板
	</div>
</div>

<!-浅蓝色--->
<div class="panel panel-info">
	<div class="panel-heading">
		<h3 class="panel-title">面板标题</h3>
	</div>
	<div class="panel-body">
		这是一个基本的面板
	</div>
</div>

<!-浅黄色--->
<div class="panel panel-warning">
	<div class="panel-heading">
		<h3 class="panel-title">面板标题</h3>
	</div>
	<div class="panel-body">
		这是一个基本的面板
	</div>
</div>

<!-浅粉色--->
<div class="panel panel-danger">
	<div class="panel-heading">
		<h3 class="panel-title">面板标题</h3>
	</div>
	<div class="panel-body">
		这是一个基本的面板
	</div>
</div>
</body>
</html>
```
**颜色示例**
![](http://ouzh4pejg.bkt.clouddn.com/bootstrap-panel-color.PNG)
