# JavaScript基本操作

------

## 数组

**数组遍历**
```javascript
var data =  ['168168cc.com','4909.com','baidu.com','taobao.com'];
for(var i=0;i<data.length;i++){
		document.write(data[i]);
	}
```
**声明空数组并赋值**
```javascript
var cars=new Array();
cars[0]="Saab";
cars[1]="Volvo";
cars[2]="BMW";

//或者 (condensed array):
var cars=new Array("Saab","Volvo","BMW");
```

**数组截取**
```javascript
var data =  ['168168cc.com','4909.com','baidu.com','taobao.com'];

 //截取data[1]开始的内容 [4909.com,baidu.com,taobao.com]
data.slice(1);

//截取data[1]到data[2]的内容[4909.com,baidu.com]
data.slice(1,3); 
```

**数组拼接**
```javascript
var a = [1,2,3,4,5,6,7,8,9]
var b = ["foo","bar","baz","bam","bun","fun"]
var c = a.concat( b );// [1,2,3,4,5,6,7,8,9,"foo","bar","baz","bam","bun","fun"]
a = b = null; // 'a'和'b'就被回收了
```

**数组循环插入**
```javascript
var a = [1,2,3,4,5,6,7,8,9]
var b = ["foo","bar","baz","bam","bun","fun"]
for (var i=0; i < b.length; i++) {
    a.push( b[i] );
}
```

**首尾插入元素**
```javascript
var data =  ['168168cc.com','4909.com','baidu.com','taobao.com'];

//首部插入
data.unshift('qq.com');
//[qq.com,168168cc.com,4909.com,baidu.com,taobao.com]

//尾部插入
data.push('sohu.com');
//[qq.com,168168cc.com,4909.com,baidu.com,taobao.com,sohu.com]
```

##对象

**基本**
```javascript
var person={firstname:"John", lastname:"Doe", id:5566};

//对象属性有两种寻址方式：
name=person.lastname;
name=person["lastname"]; 

```
**对象遍历**
```javascript
var data = {'AIPC':23,'dfasd':323,'ccc':'333'};
	for (value in data){
			document.write(value);		
	}
```

**结合数组遍历**
```javascript
var json = [{dd:'SB',AA:'东东',re1:123},{cccc:'dd',lk:'1qw'}];
for(var i=0,l=json.length;i<l;i++){
    for(var key in json[i]){
        alert(key+':'+json[i][key]);
    }
}
```

