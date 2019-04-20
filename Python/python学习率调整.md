# python学习率调整

* https://ptorch.com/docs/1/optim

* https://zhuanlan.zhihu.com/p/39453963

   * torch.optim.lr_scheduler.StepLR(optimizer,step_size=30,gamma=0.9) #每过30个epoch训练，学习率就乘gamma

   * scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,mode='min',factor=0.9) #mode为min，则loss不下降学习率乘以factor，max则反之