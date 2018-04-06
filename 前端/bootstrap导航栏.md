# Bootstrap导航栏

------
整理自[菜鸟教程](http://www.runoob.com/bootstrap/bootstrap-navbar.html)


**主要是有关折叠特性的记录与添加**，这里铁杵核心的html代码

```html
<!DOCTYPE html>
<html>
<head>
	<!---引入必要的js和css-->
</head>
<body>

<nav class="navbar navbar-default" role="navigation">
	<div class="container-fluid"> 
	<div class="navbar-header">
	    <!--下拉功能按钮-->
		<button type="button" class="navbar-toggle" data-toggle="collapse"
				data-target="#example-navbar-collapse">
			<span class="sr-only">切换导航</span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
		</button> 
		<!--总的导航栏-->
		<a class="navbar-brand" href="#">菜鸟教程</a>
	</div>
	<div class="collapse navbar-collapse" id="example-navbar-collapse">
	    <!--具体的每一栏内容-->
		<ul class="nav navbar-nav">
		    <!--普通的一栏-->
		    <!--class="active"表示默认被选中的一栏,下图看到颜色是加深的->
			<li class="active"><a href="#">iOS</a></li>
			<li><a href="#">SVN</a></li>
			<!--折叠可下拉的一栏-->
			<li class="dropdown">
				<a href="#" class="dropdown-toggle" data-toggle="dropdown">
					Java <b class="caret"></b>
				</a> <!--折叠可下拉-->
				<ul class="dropdown-menu">
					<li><a href="#">jmeter</a></li>
					<li><a href="#">EJB</a></li>
					<li><a href="#">Jasper Report</a></li>
					<li class="divider"></li>
					<li><a href="#">分离的链接</a></li>
					<li class="divider"></li> <!--分割线-->
					<li><a href="#">另一个分离的链接</a></li>
				</ul>
			</li>
		</ul>
	</div>
	</div>
</nav>

</body>
</html>

```

例图：
![](http://ouzh4pejg.bkt.clouddn.com/bootstrap-nva.png)

---

2017.10.09

