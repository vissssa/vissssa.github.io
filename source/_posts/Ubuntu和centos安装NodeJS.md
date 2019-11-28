---
title: Ubuntu和centos安装NodeJS
tags:
  - ubuntu
  - centos
  - nodejs
categories:
  - env
date: 2019-5-15
---
Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行环境，其使用了一个事件驱动、非阻塞式 I/O 的模型，使其轻量又高效。
Node.js 的包管理器 npm，是全球最大的开源库生态系统，功能及其强大。

本篇讲述的是通用安装且简单无脑，那就是使用NVM(Node version manager),github开源的项目, root下

```shell
$ curl https://raw.githubusercontent.com/creationix/nvm/vx.x.x/install.sh | bash
$ source ~/.bash_profile

# 列出支持的node版本
$ nvm list-remote

# 选择版本安装
$ nvm install v10.xx.xx
```

具体的功能我没仔细研究，感觉很像是pyenv



~~这篇文章介绍如何在ubuntu环境下安装node环境。~~

我使用的系统是ubuntu 16.04，不过在其他版本的系统中应该也适用。
### 安装python-software-properties
首先需要安装依赖包python-software-properties。
```
$ sudo apt-get install python-software-properties
```
### 添加PPA
网站deb.nodesource.com维护了nodejs的各版本安装包的PPA，我们可以从该网站上下载执行导入。
```
$ curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
```
### 安装nodejs和npm
接下来安装nodejs，安装完成之后npm也自动安装好了。
```
$ sudo apt-get install nodejs
```
安装完成之后我们查看一下nodejs和npm的版本。
```
$ node -v
v8.11.3
$ npm -v
5.6.0
```
### 配置npm仓库
因为国内的网络环境，直接从npm官方源安装软件包速度会比较慢，甚至导致安装不成功。
我们可以安装nrm工具，用于管理软件源。
```
$ sudo npm install -g nrm
```
安装完成之后，列出可用的软件源
```
$ nrm ls
* npm ---- https://registry.npmjs.org/
  cnpm --- http://r.cnpmjs.org/
  taobao - https://registry.npm.taobao.org/
  nj ----- https://registry.nodejitsu.com/
  rednpm - http://registry.mirror.cqupt.edu.cn/
  npmMirror  https://skimdb.npmjs.com/registry/
  edunpm - http://registry.enpmjs.org/
```
在国内，我们可以使用taobao的源，速度还相对不错。
```
$ nrm use taobao
Registry has been set to: https://registry.npm.taobao.org/
```
