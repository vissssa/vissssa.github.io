---
title: Storm集群搭建
tags:
  - storm
  - zookeeper
  - deploy
categories:
  - env
date: 2019-5-15
---
# Zookeeper安装与部署
**首先,根据zookeeper的原理,他必须至少是三个,且为奇数,因为它的master主线程死了可以自动选举出一个,要求是剩下的节点必须大于总共的半数**
试验机是3台centos6.4虚拟机,首先下载所需的zookeeper的压缩包,接着解压
```
>> tar -zxvf zookeeper-3.4.9.tar.gz
>>  zookeeper-3.4.9 /usr/local/
>> cd /usr/local/
>> mv zookeeper-3.4.9/ zookeeper
>> cd zookeeper/
>> cd conf/
>> cp zoo_sample.cfg zoo.cfg
>> vim zoo.cfg
```
修改配置文件
```
`# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.

dataDir=/usr/local/zookeeper/data   #这里需要修改

# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
server.0=192.168.1.114:2888:3888
server.1=192.168.1.116:2888:3888
server.2=192.168.1.132:2888:3888

```
接着可以把zookeeper加入到环境变量(全程root用户)
```
export ZOOKEEPER_HOME=/usr/local/zookeeper
export PATH=$PATH:$ZOOKEEPER_HOME/bin
```

再根据配置文件中个个节点对应的server.x,在$ZOOKEEPER_HOME下建立data文件夹
```
>> vim myid

x

```
~~**最后关闭防火墙即可**~~
~~service iptables stop~~
开放指定端口

```
>> vim /etc/sysconfig/iptables

# Firewall configuration written by system-config-firewall
# Manual customization of this file is not recommended.
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT

-A INPUT -m state --state NEW -m tcp -p tcp --dport 2181 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 2888 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 3888 -j ACCEPT

-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
COMMIT

>> service iptables restart

>> cd /usr.local/zookeeper/bin

>> zkServer.sh start  开启服务
>> zkServer.sh status 查看状态是否开启以及它的身份
>> zkServer.sh stop   关闭服务
```
检测某端口是否开放可以使用
```
>> telnet 192.168.1.114 2181
```

# Storm安装与部署

三台虚拟机,分别为nimbus,supervisor01,supervisor02
以nimbus为例
**我们的版本选择为storm版本是1.1，zookeeper3.4.9，java1.8。**
```
>> java -version  --> 1.7   # 当前版本1.7

>> sudo yum install java-1.8.0-openjdk
>> java -version  -->  1.8  # 所需版本
```
接着开始安装
```
>> wget http://mirror.bit.edu.cn/apache/storm/apache-storm-1.1.2/apache-storm-1.1.2.tar.gz
>> tar zxvf apache-storm-1.1.2.tar.gz
>> mkdir storm_data
>> cd apache-storm-1.1.2
```

配置文件编辑
```
>> vim conf/storm.yaml

storm.zookeeper.servers:
    - "192.168.1.114"
    - "192.168.1.116"
    - "192.168.1.132"
storm.local.dir: "/home/123/Desktop/storm_data"
storm.local.hostname: "192.168.1.125"
# storm.local.hostname: "192.168.1.129"
# storm.local.hostname: "192.168.1.131"
# 根据每台机子的ip地址自定义
nimbus.seeds: ["192.168.1.125"]
# 可以指定多个作为备用

supervisor.slots.ports:
    - 6700
    - 6701
    - 6702
    - 6703

# 两台supervisor的额外配置
# supervisor.childopts: -verbose:gc -XX:+PrintGCTimeStamps -XX:+PrintGCDetails -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.port=9998
```
配置完成,接下来只需要把这两个文件夹同步到两个supervisor中即可


安装配置完成,接下来就是部署,首先开启需要开启的端口,接着:
```
nimbus:

nohup bin/storm ui >/dev/null 2>&1 &
# 图形化控制面板  默认是当前服务器的8080端口,如果需要在控制面板需要看日志,则需要在各storm上开启logviewer,且防火墙放开8000端口

nohup bin/storm nimbus >/dev/null 2>&1 &


supervisor

nohup bin/storm supervisor >/dev/null 2>&1 &
```




Zookeeper集群负责Nimbus节点和Supervior节点之间的==通信==，监控各个节点之间的状态。
