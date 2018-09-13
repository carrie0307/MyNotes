# Python文件路径说明

**切记：不要用相对路径！！！不要用手动写的路径！！！！**

**切记：不要用相对路径！！！不要用手动写的路径！！！！**

**切记：不要用相对路径！！！不要用手动写的路径！！！！**

**原因**: python代码中的当前目录实际时**运行代码时终端的目录**，而不是Python文件所在的目录，因此在代码中使用系统自动生成的绝对路径时十分必要的。

## Python中各类路径的获取

```python

import os
import sys

# 以运行终端路径为终点的绝对路径
vfile =os.path.abspath('.')
print (vfile)
# os.path.join()在路径后进行添加
print (os.path.join(vfile,'root'))
# 以当前文件为终点的绝对路径
path = os.path.abspath(os.path.dirname(__file__))
# 当前文件所在目录的上一级目录
print (os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


# 在引用包时，通过sys.path.append进行目录更换
sys.path.append(common_assis.absolute_path) 

```

## Python绝对路径的获取

```shell
which python
```