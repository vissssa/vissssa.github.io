---
title: python复习笔记
entitle: python interview
categories: interview
tags:
  - interview
  - python
keywords: python
description: python复习笔记(来自于一个repo)
abbrlink: b8ccf74b
date: 2019-11-24 12:30:00
---
### 函数的参数传递

是值传递，只不过(string,tuples,num)不可变，所以函数产生一个新的副本，(dict,list,set)可变，所以会被直接修改
### cls vs self
`cls`是类方法的关键字,`self`是实例方法的关键字，顾名思义，self用在每个建立的实例中，cls可用在所有该类中(包括实例)

```python
class Foo:
    public = '123'
    def __init__(self):
        self.private = '321'

    @classmethod
    def cls_foo(cls):
        return cls.public

    def self_foo(self):
        return self.private
```

### 元类

简单来说就是元类创建类，类创建实例，不常用到，但是oop(面向对象程序设计)中会用到，一个常见的例子就是ORM

```python
from library.api.db import EntityModel, db


class Config(EntityModel):
    module = db.Column(db.String(100))  # 模块
    module_type = db.Column(db.Integer)  # 模块的类型
    content = db.Column(db.Text)  # 内容
    description = db.Column(db.Text)  # 描述
    projectid = db.Column(db.Integer)  # 项目id

```

这里的Config类本身没有任何函数，但是我们可以使用它来CRUD

```python
c = Config(module='test', content='test')
c.save()
```

### 迭代器和生成器

迭代器就是`iterable`可迭代，生成器是`generator`关键词是`yield`，处理大量数据用生成器，需要下标的使用迭代器。

`itertools`这个库很有用

### 鸭子类型

python一个利器，比如file-like，那么stringio,file,socket都当成文件一样来使用，list.extend()后面跟的参数只要是可迭代的即可，无论是string还是list，甚至是dict都可以

所以python没有很多设计模式。

### 重载

重载是为了解决两个问题：

1. 可变参数类型
2. 可变参数个数

在python中并不存在这两个问题，所以不需要函数重载

### 新式类和经典类

python3中只有新式类，简要来说区别是经典类继承是从左到右深度优先，查到底的那种，新式类则是C3算法，广度优先

### 协程
http://wbice.cn/article/coroutine.html#gevent

### 闭包
什么叫做闭包：
1. 必须有一个内嵌函数
2. 内嵌函数必须引用外部函数中的变量
3. 外部函数的返回值必须是内嵌函数  
常用作装饰器，比较类似于一个类，有一个自由变量
