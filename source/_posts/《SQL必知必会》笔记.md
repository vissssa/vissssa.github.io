title: 《SQL必知必会》笔记
entitle: 'sql'
categories: deep
date: 2019-06-18 13:44:00
tags:
    - sql
    - deep
keywords: sql
description: 极客时间课程《SQL必知必会》的一些记录
---

### SQL功能

- DDL，Data Definition Language，数据定义语言，创建、删除和修改数据库和表
- DML，Data Manipulation Language，数据操作语言，增加、删除和修改表中数据
- DCL，Data Control Language，数据控制语言，定义访问权限和安全级别
- DQL，Data Query Language，数据查询语言，顾名思义

### SQL执行过程

#### Oracle

![](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/hexo/oracle01.png)

语法就是SQL的拼写，语义则是分析操作对象是否存在

**共享池检查**就是维护一个内存池，缓存SQL语句和执行计划，每次通过计算SQL语句的Hash值去缓存池查询，若有则`软解析`，若无则`硬解析`

硬解析就是重新建立解析树和执行计划，软解析就是使用已有的解析树和执行计划，所以效率方面不可同日而语

**ps**: 上述缓存的内容被称为库缓存，可以决定是硬解析和软解析，它还存在一个数据字典缓冲区，存储对象定义，如表、视图、索引，当解析SQL语句时会从中提取数据。

#### MySQL

![](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/hexo/mysql01.jpg)

基本与Oracle相同，除了没有共享池，多了个缓存查询(8.0版本后去除了)。

非常不同的是MySQL使用的是C/S架构，分层设计

![](https://vissssa-imgs-1252712312.cos.ap-shanghai.myqcloud.com/hexo/mysql02.png)

上述流程属于SQL层，存储层可以以插件的形式选择引擎，常用的是`InnoDB`和`MyISAM`，区别就是前者支持事务、行级锁、外键等，后者查询快、功能少，所以一般后者用来查询，前者用来操作。

### MySQL调试

通过开启`profiling`收集信息

```mysql
# 查询是否开启，为1则开启，为0则关闭
SELECT @@profiling;

# 开启
SET profiling;

SELECT * FROM user;

# 展示所有profiles
SHOW profiles;
# 展示上一条
SHOW profile;
```
