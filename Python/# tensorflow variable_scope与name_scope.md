# tensorflow variable_scope与name_scope.md

* 以下内容摘自[初涉深度学习](https://zhuanlan.zhihu.com/p/38341993)

tf.name_scope() 主要是用来管理命名空间的，这样子让我们的整个模型更加有条理。tf.name\_scope可以让变量有相同的命名，只是限于tf.Variable的变量。而 tf.variable_scope() 的作用是为了实现变量共享，它和 tf.get_variable() 来完成变量共享的功能。


* [name_scope API](https://www.tensorflow.org/api_docs/python/tf/name_scope)


* 资料一： [知乎问题](https://www.zhihu.com/question/54513728/answer/515912730)中**人工智能101学院**的回答

    * 对于使用tf.Variable来说，tf.name_scope和tf.variable_scope功能一样，都是给变量加前缀，相当于分类管理，模块化。对于tf.get_variable来说，tf.name_scope对其无效，也就是说tf认为当你使用tf.get_variable时，你只归属于tf.variable_scope来管理共享与否。

* 资料二：[一个附有代码的很好的解释](https://github.com/yongyehuang/Tensorflow-Tutorial/blob/master/example-notebook/Tutorial_03_1%20The%20usage%20of%20%20name_scope%20and%20variable_scope.ipynb)