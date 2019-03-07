state_is_tuple说明

* [先读这篇：区分RNN中的output与state](https://zhuanlan.zhihu.com/p/28919765)
    
    * LSTM中注意区分output和state,state是hidden和C构成的tuple

* [tensorflow之rnn](http://www.voidcn.com/article/p-zoybvvcg-ys.html)

* 目前发现有state_is_tuple的常用接口有tf.nn.rnn_cell.BasicLSTMCell/tf.contrib.rnn.BasicLSTMCell,[文档](https://www.tensorflow.org/api_docs/python/tf/nn/rnn_cell/BasicLSTMCell)和tf.nn.rnn_cell.MultiRNNCell/tf.contrib.rnn.MultiRNNCell,[文档](https://www.tensorflow.org/api_docs/python/tf/nn/rnn_cell/MultiRNNCell)

* 注意，RNNcelll没有这个参数，文档[https://www.tensorflow.org/api_docs/python/tf/nn/rnn_cell/BasicRNNCell]

* LSTM中，默认state_is_tuple=True
    
    * state_is_tuple: If True, accepted and returned states are 2-tuples of the c_state and m_state. If False, they are concatenated along the column axis. The latter behavior will soon be deprecated.

* MultiRNNCell中，默认state_is_tuple=True

    * state_is_tuple: If True, accepted and returned states are n-tuples, where n = len(cells). If False, the states are all concatenated along the column axis. This latter behavior will soon be deprecated.