---
title: Storm集群与Python项目的实践
tags:
  - storm
  - python
  - deploy
categories:
  - env
date: 2019-5-15
---
目前主流的使用Storm的demo语言是Java,但我们使用的是Python,则需要引入一些第三方库,这里我选择的是**Streamparse**
# 安装Streamparse
根据[官方文档](http://streamparse.readthedocs.io/en/master/quickstart.html)来进行一个安装部署
因为我们是一个Centos6.4的版本,所以很需要注意一些必备工具的版本,jdk1.7+,然后下载安装**lein**
需要注意的是使用普通用户,否则submit后续会有问题

*Download the lein script (or on Windows lein.bat)
Place it on your $PATH where your shell can find it (eg. ~/bin)
Set it to be executable (chmod a+x ~/bin/lein)
Run it (lein) and it will download the self-install package*

安装的lein会放在~/.lein中,如果构建项目时出现有关问题,可以先去删除重装

## 安装Python3.6

centos6.4自带的2.6是不在Streamparse的支持范围内的,所以我们直接升级到3.6.6
使用源码安装(yum 没有3.6)
```
>> yum install zlib-devel bzip2-devel openssl-devel ncurese-devel gcc zlib

>> wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz

>> tar zxvf Python-3.6.6.tgz
>> cd Python-3.6.6

>> ./configure --prefix=/usr/local/python3
>> make
>> sudo make install
>> make clean
>> make distclean

# 再添加到环境变量中（后续virtualenv需要）
>> vim /etc/profile
export PATH="$PATH:/usr/local/python3/bin"

# 更改软链接
>> mv /usr/bin/python /usr/bin/python.bak
>> ln -s /usr/local/python3/bin/python3 /usr/bin/python3.6
>> ln -s /usr/bin/python3.6 /usr/bin/python
>> ln -s /usr/local/python3/bin/pip3 /usr/bin/pip

# 需注意，此时yum是不能使用的（yum update无效），原因是它依赖于python2.6
>> vim /usr/bin/yum
#!/usr/bin/python  --->>   #!/usr/bin/python2.6

#　最后就是安装virtualenv
pip install virtualenv
```

## Demo
环境搭建完毕，开始demo
```
>> sparse quickstart wordcount
>> sparse run
```
当前目录生成一个简单的demo项目,并模拟运行
这时会报错（＝＝！），为啥呢，我也不知道，改就完事了
```
# 第一个要改得是版本，把里面的版本改为你安装的storm版本
>> vim project.clj
# 第二个是py执行文件，加入两个options参数
>> vim fabfile.py
def pre_submit(topology_name, env_name, env_config,   options):
    """Override this function to perform custom actions prior to topology
    submission. No SSH tunnels will be active when this function is called."""
    pass


def post_submit(topo_name, env_name, env_config,   options):
    """Override this function to perform custom actions after topology
    submission. Note that the SSH tunnel to Nimbus will still be active
    when this function is called."""
    pass
```
此时应当可以运行了
模拟通过就开始上传到集群了，修改config.json
```
{
    "serializer": "json",
    "topology_specs": "topologies/",
    "virtualenv_specs": "virtualenvs/",
    "envs": {
        "prod": {
            "user": "root",
            "ssh_password": "123123",
            "nimbus": "192.168.1.125",
            "workers": ["192.168.1.129", "192.168.1.131"],
            "log": {
                "path": "/var/log/storm/streamparse",
                "file": "pystorm_{topology_name}_{component_name}_{task_id}_{pid}.log",
                "max_bytes": 1000000,
                "backup_count": 10,
                "level": "info"
            },
        "virtualenv_root": "/data/virtualenvs/"
        }
    }
}
```
说明：user填写root，为了获得权限来创建日志文件和虚拟环境
然后就是正式上传运行了
```
>> sparse submit

# 此时会先在几个workers中检测虚拟环境并安装需要的库，requirements.txt在virtualenv/下
# 检测且通过则会将本地项目打包并上传到nimbus中进行任务分发，原理应该是topologies中的py文件的定义
```
还需要注意的是nimbus和supervisor之间的联系，这是绕过zopkeeper的，是spouts和bolts之间的emit发射函数，所以需要开启端口，分别是nimbus的6627和supervisor的6700
可以在nimbus的ＵＩ页面来查看项目运行情况，以及任务分布以及状态．
