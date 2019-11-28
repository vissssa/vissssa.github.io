---
title: k8s权威指南demo
tags:
  - k8s
categories:
  - cloud
date: 2019-5-15
description: k8s初探
---

1. 创建一个虚拟linux环境，本次是centos7

2. 关闭防火墙

   ```bash
   $ systemctl disable firewalld
   $ systemctl stop firewalld
   $ service iptables stop
   ```

3. 安装etcd和k8s，docker会自动安装

   ```bash
   $ yum install -y etcd kubernetes
   ```

4. 加上认证

   ```bash
   $ openssl genrsa -out /tmp/service_account.key 2048

   $ vim /etc/kubernetes/apiserver
   KUBE_API_ARGS="--secure-port=0 --service-account-key-file=/etc/kubernetes/service_account.key"

   $ vim /etc/kubernetes/controller-manager
   KUBE_CONTROLLER_MANAGER_ARGS="--service_account_private_key_file=/etc/kubernetes/service_account.key"
   ```

5. 修改pod镜像的地址，因为原地址

   ```
   Error syncing pod, skipping: failed to "StartContainer" for "POD" with ErrImagePull: "image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request.  details: (open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory)"
   # 需要ca验证 但是本地安装rhsm并没有用
   ```

   所以更换为`docker search pod-infrastructure `，并修改k8s配置文件

   ```bash
   $ vim /etc/kubernetes/kubelet
   KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image=docker.io/tianyebj/pod-infrastructure:latest"
   $ systemctl restart kubelet
   ```

6. 编写k8s的service和rc文件

   ```bash
   $ vim mysql-rc.yaml

   apiVersion: v1
   kind: ReplicationController  # 副本控制器 RC，kubectl生成的是rc
   metadata:
     name: mysql	# rc的名称，全局唯一
   spec:
     replicas: 1   # pod的副本数量
     selector:
       app: mysql	# 符合目标的Pod拥有此标签
     template:		# 根据此模板创建Pod的副本(实例)
       metadata:
         labels:
           app: mysql	# Pod副本拥有的标签，对应RC的selector
       spec:
         containers:	# Pod内容器的定义部分
         - name: mysql	# 容器名称
           image: docker.io/mysql:5.7    #!!mysql必须老版本最好5.7，新版本问题很大需要额外的环境配置
           ports:
           - containerPort: 3306	# 容器应用监听的端口号
           env:					# 注入容器内的环境变量
           - name: MYSQL_ROOT_PASSWORD
             value: "123456"

   $ vim mysql-svc.yaml

   apiVersion: v1
   kind: Service	# k8s的 Service
   metadata:
     name: mysql	# Service的全局唯一名称
   spec:
     ports:
     - port: 3306
     selector:
       app: mysql

   $ vim myweb-rc.yaml

   apiVersion: v1
   kind: ReplicationController
   metadata:
     name: myweb
   spec:
     replicas: 1
     selector:
       app: myweb
     template:
       metadata:
         labels:
           app: myweb
       spec:
         containers:
         - name: myweb
           image: kubeguide/tomcat-app:v1
           ports:
           - containerPort: 8080

   $ vim myweb-svc.yaml

   apiVersion: v1
   kind: Service
   metadata:
     name: myweb
   spec:
     type: NodePort
     ports:
       - port: 8080
         nodePort: 30001	# 对外暴露的端口
     selector:
       app: myweb
   ```

7. 编写k8s的启动脚本和domo的启动脚本

   ```bash
   $ vim k8s.sh

   #!/bin/bash

   systemctl $1 etcd
   systemctl $1 docker
   systemctl $1 kube-apiserver
   systemctl $1 kube-controller-manager
   systemctl $1 kube-scheduler
   systemctl $1 kubelet
   systemctl $1 kube-proxy

   $ vim demo.sh

   #!/bin/bash

   kubectl $1 -f /root/kube-demo/mysql-rc.yaml
   kubectl $1 -f /root/kube-demo/mysql-svc.yaml
   kubectl $1 -f /root/kube-demo/myweb-rc.yaml
   kubectl $1 -f /root/kube-demo/myweb-svc.yaml

   $ chmod 755 k8s.sh
   $ chmod 755 demo.sh
   ```

8. 启动demo项目

   ```bash
   $ ./k8s.sh start/stop
   $ ./demo.sh create/delete
   ```

9. 打开localhost:30001可看到tomcat的页面，/demo的页面以下：

![k8sDemo](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/pics/k8sDemo%E5%AE%8C%E6%88%90%E9%A1%B5%E9%9D%A2.png)
