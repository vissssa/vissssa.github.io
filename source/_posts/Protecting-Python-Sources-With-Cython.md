---
title: Protecting-Python-Sources-With-Cython
tags:
  - python
categories:
  - deep
date: 2019-5-15
description: 用来加密代码使用
abbrlink: '5e430375'
---

Protecting your Python sources from unwanted readers is easier said than done, because **.pyc** bytecode is [decompileable](https://github.com/rocky/python-uncompyle6) and the obfuscation is easily reverse-engineered. It took me a while to figure out a proper way to hide Python code…

Meet [**Cython**](http://cython.org/)**,** an **optimizing static compiler** that takes your `.py` modules and translates them to high-performant C files. Resulting C files can be compiled into native binary libraries with no effort. When the compilation is done there’s no way to reverse compiled libraries back to readable Python source code! Cython supports both Python 2 and 3, including the modern **async/await** syntax. From my experience, the only thing it couldn’t do is asynchronous generators.

### 1. Install Cython

Installation is as easy as typing `pip install cython` or `pip3 install cython`(for Python 3).

### 2. Add compile.py

Add the following script to your project folder (as `compile.py`). It will act as a “makefile” for the build:

```
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("mymodule1",  ["mymodule1.py"]),
    Extension("mymodule2",  ["mymodule2.py"]),
#   ... all your modules that need be compiled ...
]
setup(
    name = 'My Program Name',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
```

The script should explicitly enumerate files that you want to be compiled. You can also leave some files uncompiled as well, if you want. Those will still remain `import`able from binary modules.

### 3. Add main.py

Make the entry point Python file for your application. You will import and launch all the compiled logic from there. An entry point file is required because Cython does not generate executable binaries by default (though it is capable to), so you will need a dummy Python file, where you simply import all the compiled logic and run it. It can be as simple as:

```
from logic import main      # this comes from a compiled binary
main ()
```

### 4. Run compile.py

Depending on the Python version you use, run:

```
python compile.py build_ext --inplace
```

…or, for Python 3:

```
python3 compile.py build_ext --inplace
```

The above command will generate `.so` and `.c` files next to your `.py` source files:



![img](https://cdn-images-1.medium.com/max/1600/1*KQCTp5cE9R84Ku_0oaG1Cw.png)

The `.c` files are intermediate sources used to generate `.so` files, which are binary modules you want to distribute. When building on Windows these files will probably have the `.dll` extension (**UPD**: in the comments people suggest that they actually have the `.pyd` extension on Windows).

You can delete `.c` and `.py` files after a successful build and keep the `.so`files only.

Note that `.so`-files contain the target platform in their names (e.g. `darwin`on my MacOS). Obviously, the compiled modules are not cross-platform. If you distribute your program to Ubuntu Linux users, you should compile it on Linux. Otherwise you won’t be able to load these binaries. So you’ll have to compile a platform-specific version of your code for each of your targeted platforms.

Luckily, there are tools like [Vagrant](https://www.vagrantup.com/) that can help reduce all the OS installation burden to a couple of simple commands…

### Setting Up a Different OS Environment Using VirtualBox and Vagrant

Here’s an example of how I’ve managed to compile my project on Ubuntu 16.04, while using MacOS.

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/).
2. Run `export VAGRANT_DEFAULT_PROVIDER=virtualbox` (you can add it to your Bash startup script at `~/.bash_profile` for convenience).
3. Choose an OS here: <https://app.vagrantup.com/boxes/search>. Then click the *New* tab in “How to use” section. You’ll find setup instructions and commands there. Run those commands in your Python project folder:



![img](https://cdn-images-1.medium.com/max/1600/1*s4uPRId_oMQAFqSV1j4WjQ.png)![img](https://cdn-images-1.medium.com/max/2000/1*s4uPRId_oMQAFqSV1j4WjQ.png)

Finally, run `vagrant ssh` to get into a freshly installed Ubuntu console (type `exit` to exit):



![img](https://cdn-images-1.medium.com/max/1600/1*V5nAJ1gFlWbFTxpOPFg8Lw.png)

`cd` to the `/vagrant` folder to see your project files. Then perform steps 1, 4 from this manual, and you’re done:



![img](https://cdn-images-1.medium.com/max/1600/1*peFjOUpkICaIxgvMpXv6VA.png)

For projects with a short build/release cycle, multi-plaform builds could be automated using a CI (Continuous Integration) service, like [TravisCI](https://travis-ci.org/), but that’s a story for another article.

### About the Author

I’m a member of the developer team behind the open-source cross-language [CCXT Library](https://github.com/ccxt-dev/ccxt) (available for JavaScript, Python or PHP). The library is used to connect and trade with more than 100 cryptocurrency exchanges worldwide.
