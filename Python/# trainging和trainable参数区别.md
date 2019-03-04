# trainging和trainable参数区别

还是没看懂。。。

* 摘自[https://stackoverflow.com/questions/50209310/significance-of-trainable-and-training-flag-in-tf-layers-batch-normalization](https://stackoverflow.com/questions/50209310/significance-of-trainable-and-training-flag-in-tf-layers-batch-normalization)

    * **training** controls whether to use the training-mode batchnorm (which uses statistics from this minibatch) or inference-mode batchnorm (which uses averaged statistics across the training data). 

    * **trainable** controls whether the variables created inside the batchnorm process are themselves trainable.


* API文档解释

    * training: Either a Python boolean, or a TensorFlow boolean scalar tensor (e.g. a placeholder). Whether to return the output in **training mode (normalized with statistics of the current batch)** or in **inference mode (normalized with moving statistics)**. NOTE: make sure to set this parameter correctly, or else your training/inference will not work properly.

    * trainable: Boolean, if True also add variables to the graph collection GraphKeys.TRAINABLE_VARIABLES (see tf.Variable).