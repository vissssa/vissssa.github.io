---
title: Rancher安装与部署K8s
tags:
  - rancher
  - k8s
  - deploy
categories:
  - cloud
date: 2019-5-15
description: 使用rancher来安装和部署k8s，官方一直在维护，也很好用
abbrlink: 36f1f294
---

> Rancher Kubernetes Engine(RKE), an extremely simple, lightning fast Kubernetes installer that works everywhere.

安装前提：

- 系统: Ubuntu 16.04 (64-bit)、Red Hat Enterprise Linux 7.5 (64-bit)

- Docker Versions: 1.12.6、1.13.1、17.03.2

- 关闭防火墙


### 一、初始化和安装指定版本Docker

1. 关闭防火墙
2. [安装Docker](指定版本安装Docker.md)



### 二、安装rancher

官网有单节点和高可用rancher的安装方法，这里我们只选择单节点rancher：

```bash
$ docker run -d --restart=unless-stopped -p 80:80 -p 443:443 rancher/rancher
```

然后打开`https://<server_ip>`即可看到以下：

![rancher初始化](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/pics/rancher%E5%88%9D%E5%A7%8B%E5%8C%96.png)

设置密码后可进入主页，这里大量设置是与云服务有关的，包括没有显示的也可以手动添加，等待云服务商的接入，我们这里主要是本地部署自己的k8s集群。

![rancher主页](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/pics/rancher%E4%B8%BB%E9%A1%B5.png)

1. 选择CUSTOM（添加主机自建Kubernetes集群）
2. K8s-rancher版本选择最新发布版

![rancher搭建k8s](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/pics/rancher%E6%90%AD%E5%BB%BAk8s.png)

 接下来就根据你的主机准备情况进行k8s和rancher组件的部署，他会根据你的选择自动生成docker命令，我们这里是在master节点部署etcd和control，kubelet和proxy部署在子节点上，我不太确定apiserver和调度器部署在哪，是不是由rancher组件代替了，后续需要查看文档。

![rancher自动部署](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/pics/rancher%E8%87%AA%E5%8A%A8%E9%83%A8%E7%BD%B2.png)

需要注意的是为了给每个主机加上名称，因为名称唯一，所以每条命令只能在一台机器上部署，否则同名称主机只能识别一个

这里就是部署完成的页面，在这里可以查看Kubeconfig文件和进行kubectl命令行操作，可以打开进行一些测试。

![rancher-k8s仪表盘](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/pics/rancher%E4%BB%AA%E8%A1%A8%E7%9B%98.png)

点击system可以看到kube-system下的一些部署服务，default就是默认的命名空间，这里部署两个简单的服务进行测试

![rancher-k8s-system](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/pics/rancher-k8s-system.png)

registry.cn-shanghai.aliyuncs.com/vissssa/nginx:`frontend`和`zhangyu1`，我在frontend中设定nginx重定向到`http://zhangyu`，那么只要设定另一个服务名称为`zhangyu`即可，kube-dns已经自动部署了，暴露frontend接口：type=NodePort。

![rancher部署服务](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/pics/rancher%E9%83%A8%E7%BD%B2%E4%BB%BB%E5%8A%A11.png)

访问`http://<work_ip>:30000`即可看到结果。结果重定向到了`zhangyu`的nginx服务上。

