title: gitlab-runner-ssh_on_ubuntu18.04
entitle: 'gitlab-runner'
categories: deploy
date: 2019-05-20 10:38:00
tags:
    - deploy
    - cicd
keywords: gitlab-runner
description: gitlab-runner的executor为ssh时在的一些补充
---
需求是利用gitlabci的流程在编译打包成功后直接在开发机上部署，所以直接在ubuntu18.04上安装gitlab-runner，而不是docker运行，此处选择ssh的方式部署到远程服务器，**注意**：此处待验证是否可以同时ssh到多个机器部署。
这个坑在于官方并不完善，以下步骤必须完成，否则会有两个问题:
```bash
$ sudo docker-compose pull && sudo docker-compose up -d
sudo: no tty present and no askpass program specified
ERROR: Job failed: Process exited with: 1. Reason was:  ()
```
```bash
ERROR: Preparation failed: ssh: unsupported key type "OPENSSH PRIVATE KEY"
Will be retried in 3s ...
```

解决方案两点：
1、生成秘钥
```bash
> ssh-keygen -t rsa -C "dev-110" -b 4096
...
> ssh-copy-id localhost({node-ip})
```
拷贝~/.ssh/id_rsa.pub并上传到gitlab设置的SSH Keys中

2、更改sudo设置
```bash
# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL

# 修改为
%sudo   ALL=(ALL:ALL) NOPASSWD: ALL
```

另外gitlab-runner的配置文件为
```bash
concurrent = 1
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "dev"
  url = "http://gitlab/"
  token = "3c4c563580ee515093b1ca8b7929b0"
  executor = "ssh"
  [runners.custom_build_dir]
  [runners.ssh]
    user = "vissssa"
    password = "123"
    host = "localhost"
    port = "22"
    identity_file = "/home/vissssa/.ssh/id_rsa"
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
```
