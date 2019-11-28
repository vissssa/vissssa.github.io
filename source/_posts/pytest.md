---
title: pytest
tags:
  - python
categories:
  - artifact
date: 2019-5-15
description: python的单元测试
---
国际惯例，先上官方文档: [pytest](https://docs.pytest.org/en/stable/contents.html)

经常使用的单元测试一般是自带的unittest或者是文档测试，下面是他们简单的例子
```
# content of unittest_demo.py
import unittest

def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)

if __name__ == '__main__':
    unittest.main()

$ python3 unittest_demo.py
```
```
# content of doctest_demo.py
def square(x):
    """返回x的平方

    >>> square(2)
    4
    >>> square(-1)
    4
    """

    return x * x

if __name__ == '__main__':
    import doctest
    doctest.testmod()

$ python3 doctest_demo.py
```

可见这两个都比较繁琐或者配置比较复杂，所以我选择使用pytest这个第三方库
```
pip install -U pytest
```
好了可以使用了

需要注意的是："pytest(py.test)"会执行所有test_*.py或者*_test.py文件，或者pytest -q test_xx.py来指定，-q == quiet，结果不显示不相关的东西

```
# content of test_sample.py
def func(x):
    return x + 1

def test_answer1():
    assert func(3) == 4

def test_answer2():
    assert func(4) == 5
```
```
# content of test_class.py
class TestClass(object):
    def test_one(self):
        x = 'this'
        assert 'h' in x

    def test_two(self):
        x = 'hello'
        assert hasattr(x, 'format')

```
```
# content of test_sysexit.py
import pytest

def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()
```
