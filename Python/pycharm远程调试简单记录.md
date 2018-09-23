## Pycharm远程调试简单记录

* 注意，需要是pycharm专业版

很多教程首先进行deployment configuration设定，这里直接从Interpret开始步骤。

* 从 Setting里的Interpret进行服务器连接

* 完成连接后会进行deployment configuration的选择，若无已建立好的连接，则重新建立即可。

* 建立好后会有一个选择“Create new ....”，目前是按照这个选择的，选择后会有上一步已建立好configuration 的一个 copy出来，注意在这里重新设置好deployment 的路径。

* 完成上一步后，下一窗口会选择sync-folders，**这里应该就是真正同步的路径了**，一定注意选择。

* 最后一个窗口应该可以看到当前路径和Map Path，如果Map Path不正确则进行修正。

* 个人感觉，总之使所有服务器端的路径都是目的的同步路径就好。

* 然后开始运行，如果本地代码还没有同步到Map Path，则会显示“ Python helpers are not copied yet to the remote host. Please wait until remote interpreter initialization finishes. ” ， 需等待上传完成。

* 当profect较大时，可先通过其他方式将代码上传到指定路径；之后每次运行的时候都是将修改的内容进行自动的增量上传即可。

* 注意在deployment的option里选择 “每次 Ctrl S 自动上传同步”

* 以后用pycharm打开其他新project可能会要求选择interpret,根据需求选择本地或远程Interpret即可。