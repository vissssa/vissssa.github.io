---
title: centos6.4安装mysql并配置远程连接
tags:
  - mysql
  - deploy
  - centos
categories:
  - env
date: 2019-5-15
---
#### 一、查看并卸载老的mysql
1. 查看该操作系统上是否已经安装了mysql数据库
```bash
$ rpm -qa |grep mysql
```
2. mysql的卸载
```bash
$ rpm -e mysql　　//普通删除模式
$ rpm -e --nodeps mysql(mysql-server、mysql-devel)　　//强力删除模式，如果使用上面命令删除时，提示有依赖的其它文件，则用该命令可以对其进行强力删除
```
好吧，就试试rpm -e --nodeps mysql。

通过 rpm -qa | grep mysql 查看是否已经卸载成功！！

#### 二、通过yum来进行mysql的安装
首先我们可以输入 yum list | grep mysql 命令来查看yum上提供的mysql数据库可下载的版本
然后我们可以通过输入yum install -y mysql-server mysql mysql-devel命令，将mysql mysql-server mysql-devel都安装好(注意:安装mysql时我们并不是安装了mysql客户端就相当于安装好了mysql数据库了，我们还需要安装mysql-server服务端才行)
```bash
$ rpm -qi mysql-server
```
#### 三、mysql数据库的初始化及相关配置
我们在安装完mysql数据库以后，会发现会多出一个mysqld的服务，这个就是咱们的数据库服务，我们通过输入**service mysqld start**命令就可以启动我们的mysql服务。
注意：如果我们是第一次启动mysql服务，mysql服务器首先会进行初始化的配置,根据提示来配置我们的密码。
```bash
# 查看mysql开机时是否启动
$ chkconfig --list |grep mysqld
$ chkconfig mysqld on
```

修改mysql的默认密码：

mysql数据库安装完以后只会有一个root管理员账号，但是此时的root账号还并没有为其设置密码，在第一次启动mysql服务时，会进行数据库的一些初始化工作，在输出的一大串信息中，我们看到有这样一行信息 ：

/usr/bin/mysqladmin -u root password 'new-password'// 为root账号设置密码

所以我们可以通过 该命令来给我们的root账号设置密码(注意：这个root账号是mysql的root账号，非Linux的root账号)

mysqladmin -u root password 'root'　　// 通过该命令给root账号设置密码为 root

如果在修改密码的时候报错：mysqladmin: connect to server at 'localhost' failed error: 'Access denied for user 'root'@'localhost' (using password: NO)'
```bash
$ service mysqld stop

$ mysqld_safe --user=mysql --skip-grant-tables --skip-networking &

$ mysql -u root mysql

mysql> UPDATE user SET Password=PASSWORD('newpassword') where USER='root';

mysql> FLUSH PRIVILEGES;

mysql> quit

```

#### 四、mysql数据库的主要配置文件
1. /etc/my.cnf这是mysql的主配置文件
2. /var/lib/mysql  mysql数据库的数据库文件存放位置 (**删除这个文件夹来完成mysql的初始化**)
3. /var/logmysql数据库的日志输出存放位置

#### 五、配置远程连接
设置数据库可以被远程访问

```bash
$ mysql -u root -p

mysql> use mysql;
mysql> grant all privileges on *.* to root@'%' identified by 'rootpassword';
mysql> flush privileges;

$ service mysqld restart
```
配置防火墙允许3306

```bash
$ vim /etc/sysconfig/iptables

-A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT

$ service iptables restart
```
