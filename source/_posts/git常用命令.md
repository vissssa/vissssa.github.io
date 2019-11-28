---
title: git常用命令
tags:
  - git
categories:
  - deep
date: 2019-5-15
description: 运维方面经验
---

#### 1、建立联系

首先在git代码存储网站上(github,gitlab,coding等)配置SSH公钥

要添加一个 SSH 密钥, 需要生成一个或使用一个现有的 key:

1. To generate a new SSH key pair, use the following command:

   ```bash
   >> ssh-keygen -o -t rsa -C "v*****a@163.com" -b 4096
   ```

   然后回车就完事了

2. 查看并复制你的ssh key:

   ```bash
   >> cat ~/.ssh/id_rsa.pub

   ssh-rsa AAAA********* v*****a@163.com
   ```

3. 添加到git管理网站即可



#### 2、初始化git配置

```bash
>> git config --global user.email "v*****a@163.com"
>> git config --global user.name "v*****a"
```



#### 3、初始化本地项目

```bash
>> cd project
>> git init
Initialized empty Git repository in /home/**/project/.git/
>> git add .
>> git commit -m "初始化"
>> git remote add origin git@git.dev.tencent.com:v*****a/project.git
>> git push -u originls

```



#### 4、后续修改

```bash
>> vim .gitignore
__pycache__/

>> git add .gitignore
>> git commit -m "add gitignore"
>> git push
```



## 某些不能在IDE或者sourcetree上处理的需求

1. 强制从远端拉取代码覆盖本地

   ```bash
   >> git fetch --all
   >> git reset --hard origin/master
   >> git pull
   ```

2. `fetch` + `merge` = `pull`，拉取远端仓库的commit历史，再与本地进行merge合并

3. 删除本地以及远端的文件或文件夹

   ```bash
   >> git rm foo/settings.py
   >> git rm **/__pycache__
   >> git rm **/**/__pycache__

   >> git commit -m '删除'
   >> git push
   ```

