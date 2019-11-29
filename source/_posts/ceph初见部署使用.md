---
title: ceph初见部署使用
tags:
  - ceph
  - deploy
categories:
  - cloud
date: 2019-5-15
description: 对象存储部署经验
abbrlink: 23c544ee
---
> 有鉴于官网教程不能对我这样的初学者有较好的帮助，在经历很多坑和查询资料，反复搭建数次后，总结了一套可以成功搭建的方法，但并不是官网最新版本的部署方法。

原理图以及官方推荐系统等我就不写了，直接步入主题

# 准备环节

### 1、系统节点信息

|    host    |    roles     |      ip       | volumes |                 core                 |
| :--------: | :----------: | :-----------: | :-----: | :----------------------------------: |
| ceph-admin | ceph-deploy  | 192.168.1.127 |         | CentOS Linux release 7.5.1804 (Core) |
| ceph-node1 | mon<br />osd | 192.168.1.129 | 10G+20G | CentOS Linux release 7.5.1804 (Core) |
| ceph-node2 | mon<br />osd | 192.168.1.126 | 10G+20G | CentOS Linux release 7.5.1804 (Core) |
| ceph-node3 | mon<br />osd | 192.168.1.128 | 10G+20G | CentOS Linux release 7.5.1804 (Core) |

### 2、环境配置

##### 1、首先需要关闭SELINUX，然后开启需要的防火墙端口，此处节省时间直接关闭

```bash
>> sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
>> setenforce 0
>> systemctl stop firewalld
>> systemctl disable firewalld
```

官方不推荐root部署，这里也是为了迅速可用，直接root登录

##### 2、配置HOST

```bash
>> vim /etc/hosts

192.168.1.127 ceph-admin
192.168.1.129 ceph-node1
192.168.1.126 ceph-node2
192.168.1.128 ceph-node3
```

如需更方便，可以添加.ssh的相关配置。

然后建立ceph-admin到各个节点的信任ssh通信，在ceph-admin上:

```bash
>> ssh-keygen
# 一直回车即可
...
ssh-copy-id root@ceph-admin
ssh-copy-id root@ceph-node1
ssh-copy-id root@ceph-node2
ssh-copy-id root@ceph-node3

```

之所以要拷贝到自身，请看后面

##### 3、更新系统源头，全部节点更新为aliyun，虽然新的centos的系统源会自动寻找最快的mirrors，但我们还是选择aliyun吧（😝）

```bash
>> rm -rf /etc/yum.repos.d/*.repo
>> curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
>> curl -o /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
>> sed -i '/aliyuncs/d' /etc/yum.repos.d/CentOS-Base.repo
>> sed -i 's/$releasever/7/g' /etc/yum.repos.d/CentOS-Base.repo
>> sed -i '/aliyuncs/d' /etc/yum.repos.d/epel.repo
>> yum clean all
>> yum makecache fast
```

##### 4、NTP配置

分布式系统很重要的一个点，时钟同步，如果这一步不完成，ceph将会不允许任何i/o操作，本人在这一步有过一些很奇怪的问题，包括不能使用官方服务器、上次可以这次莫名其妙就不行等。

所有节点安装NTP：

```bash
>> yum install -y ntp
```

ceph-admin配置：注释掉官方自带的服务器

```bash
>> vim /etc/ntp.conf

#server 0.centos.pool.ntp.org iburst
#server 1.centos.pool.ntp.org iburst
#server 2.centos.pool.ntp.org iburst
#server 3.centos.pool.ntp.org iburst

# 允许局域网访问，但不允许修改
restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
# 来自中国授时中心
server 0.cn.pool.ntp.org
server 1.cn.pool.ntp.org
# 以上服务不行时，允许使用自己当前时间为服务器时间
server 127.127.1.0 minpoll 4
fudge 127.127.1.0 stratum 0

>> vim /etc/ntp/step-tickers
#0.centos.pool.ntp.org
127.127.1.0
```

其他节点配置：

```bash
>> vim /etc/ntp.conf
#server 0.centos.pool.ntp.org iburst
#server 1.centos.pool.ntp.org iburst
#server 2.centos.pool.ntp.org iburst
#server 3.centos.pool.ntp.org iburst
server 192.168.1.127
```

然后所有节点启动服务并且设置为开机启动

```bash
>> systemctl enable ntpd ; systemctl start ntpd
```

最后查看状态

```bash
>> ntpq -p

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ceph-admin      209.97.168.88    3 u   65   64  377    0.315  -238.63 151.966
```

当所有node节点显示`*`时才是正确的，可以稍等一会查看信息，一般是十几秒同步一次

# 正式搭建

### 1、安装ceph-deploy

这是官方提供的用于简单搭建ceph框架的python脚本([github](https://github.com/ceph/ceph-deploy))，这里选择yum下载(ceph-admin)：

```bash
>> yum install http://mirrors.163.com/ceph/rpm-jewel/el7/noarch/ceph-deploy-1.5.38-0.noarch.rpm
...
>> ceph-deploy --version
1.5.38
```

### 2、创建集群的准备

继续ceph-admin中准备环节：

```bash
>> mkdir my-cluster
>> cd my-cluster
>> ceph-deploy new ceph-node1 ceph-node2 ceph-node2
...
>> vim ceph.conf

[global]
fsid = 9f1ae8b0-7d7a-45b9-9b19-663ced7397a1
mon_initial_members = ceph-node1, ceph-node2, ceph-node3
mon_host = 192.168.1.129,192.168.1.126,192.168.1.128
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx
# 添加以下内容
mon_clock_drift_allowed = 5
osd_journal_size = 20480
public_network = 192.168.1.0/24
```

### 3、创建集群

开始在各个节点安装ceph，还是在ceph-admin上：

```bash
>> ceph-deploy install --release jewel --repo-url http://mirrors.163.com/ceph/rpm-jewel/el7 --gpg-url http://mirrors.163.com/ceph/keys/release.asc ceph-admin ceph-node1 ceph-node2 ceph-node3
...
```

之所以在admin节点安装是为了一些配置和后续直接在admin上测试。

安装完成后检查成功与否：

```bash
>> ceph -v

ceph version 10.2.11 (e4b061b47f07f583c92a050d9e84b1813a35671e)
```

在ceph-admin上也配置权限查看ceph信息

```bash
>> ceph-deploy admin ceph-master
```

对了，我们是root用户，如果是自定义用户的话，可能需要对秘钥文件进行权限配置：

```bash
>> chmod +r /etc/ceph/ceph.client.admin.keyring
```

### 4、配置集群

初始化mon，须知道，ceph-deploy的这些操作需要在`my-cluster`目录下，读取我们`new`创建的`ceph.conf`文件。

```bash
>> ceph-deploy mon create-initial
...
```

各个节点查看当前ceph情况：

```bash
ceph -s
```

当然是报错的，因为没有osd呢，所以开始准备osd吧

### 5、OSD准备

osd节点上：

```bash
>> lsblk

NAME            MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda               8:0    0   20G  0 disk
├─sda1            8:1    0    1G  0 part /boot
└─sda2            8:2    0   19G  0 part
  ├─centos-root 253:0    0   17G  0 lvm  /
  └─centos-swap 253:1    0    2G  0 lvm  [SWAP]
sdb               8:16   0   10G  0 disk
sdc               8:32   0   20G  0 disk
sr0              11:0    1 1024M  0 rom
```

/dev/sdb我准备用来作为日志硬盘，/dev/sdc作为osd存储硬盘，根据流程来，首先给日志盘分区：

```bash
>> fdisk /dev/sdb
...
# 输入n分区，其它默认，只分一个区，输入p查看当前分区，w结束分区

>> chown ceph:ceph /dev/sdb1
# 给日志硬盘操作权限，给admin来初始化使用
```

### 6、添加OSD

ceph-admin上执行以下：

```bash
>> ceph-deploy osd create ceph-node1:/dev/sdc:/dev/sdb1 ceph-node2:/dev/sdc:/dev/sdb1 ceph-node3:/dev/sdc:/dev/sdb1
```

再查看`ceph  -s`即可看到健康情况

```bash
>> ceph osd tree
# 查看当前osd健康
```

