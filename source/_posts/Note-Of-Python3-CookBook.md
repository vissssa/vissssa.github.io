---
title: Note-Of-Python3-CookBook
tags:
  - python
categories:
  - deep
date: 2019-5-15
description: 大量python3的精巧使用方法，可以大幅减少开发时间以及运行效率（时间和空间复杂度），大部分的东西包括内建和第三方模块需要记录，所以写这个笔记。
abbrlink: 887a2def
---

### 数据结构和算法

1. `*`的巧妙使用方法，运用在所有可迭代对象

   ```python
   # 比赛求分数，去掉最大值和最小值求平均数
   >>> a = [10, 8, 7, 1, 9, 5, 10, 3]
   >>> b = sorted(a)
   [1, 3, 5, 7, 8, 9, 10, 10]
   >>> l, *m, h = b
   >>> type(m)
   <class 'list'>
   >>> avg = sum(m)/len(m)
   7.0
   ```

   ps.  `_`一般用于准备垃圾数据，在python终端中也代表上一个你使用的对象

   ```python
   >>> record = ('ACME', 50, 123.45, (12, 18, 2012))
   >>> name, *_, (*_, year) = record
   >>> name
   'ACME'
   >>> year
   2012
   >>>
   ```

2. 只保留n条记录：`collections.deque`不仅仅拥有列表的属性，还可以对表头进行增删，即`appendleft`和`popleft`，更可以指定长度，当满了且新增数据时，会FIFO，删除最先进来的数据

   ```python
   '''
   deque([iterable[, maxlen]]) --> deque object

       A list-like sequence optimized for data accesses near its endpoints.
   '''
   from collections import deque

   def search(lines, pattern, history=5):
       previous_lines = deque(maxlen=history)	# 2
       for line in lines:	# 3	11
           if pattern in line:	# 4
               yield line, previous_lines	# 5
           previous_lines.append(line)	# 10

   # Example use on a file
   if __name__ == '__main__':
       with open('demo.txt') as f:
           for line, prevlines in search(f, 'python', 5):	# 1
               for pline in prevlines:	# 6
                   print(pline, end='')  # 7(第一次没有)
               print(line, end='')	# 8
               print('-' * 20)	# 9
   ```

   另外一些常用的`collections`的功能模块有`defaultdict`：

   ```python
   >>> from collections import defaultdict
   >>> dd = defaultdict(lambda: 'N/A')
   >>> dd['key']
   'N/A'
   ```

   还有`OrderedDict`:

   ```python
   >>> from collections import OrderedDict
   >>> d = dict([('a', 1), ('b', 2), ('c', 3)])
   >>> d # dict的Key是无序的
   {'a': 1, 'c': 3, 'b': 2}
   >>> od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
   >>> od # OrderedDict的Key是有序的
   OrderedDict([('a', 1), ('b', 2), ('c', 3)])
   ```

   但是他的KEY顺序是**插入顺序**，所以还可以做成一个FIFO的有限长度队列出来

   `OrderedDict` 内部维护着一个根据键插入顺序排序的双向链表。每次当一个新的元素插入进来的时候， 它会被放到链表的尾部。对于一个已经存在的键的重复赋值不会改变键的顺序。

   **需要注意的是**，一个 `OrderedDict` 的大小是一个普通字典的**两倍**，因为它内部维护着另外一个链表。 所以如果你要构建一个需要大量 `OrderedDict` 实例的数据结构的时候（比如读取 100,000 行 CSV 数据到一个 `OrderedDict` 列表中去）， 那么你就得仔细权衡一下是否使用 `OrderedDict` 带来的好处要大过额外内存消耗的影响。

3. 查找最大或最小的 N 个元素， `heapq`模块两个方法`nlargest( )`和`nsmallest( )`

   ```python
   import heapq
   nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
   print(heapq.nlargest(3, nums)) # Prints [42, 37, 23]
   print(heapq.nsmallest(3, nums)) # Prints [-4, 1, 2]
   ```

   复杂用法

   ```python
   portfolio = [
       {'name': 'IBM', 'shares': 100, 'price': 91.1},
       {'name': 'AAPL', 'shares': 50, 'price': 543.22},
       {'name': 'FB', 'shares': 200, 'price': 21.09},
       {'name': 'HPQ', 'shares': 35, 'price': 31.75},
       {'name': 'YHOO', 'shares': 45, 'price': 16.35},
       {'name': 'ACME', 'shares': 75, 'price': 115.65}
   ]
   cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
   expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
   ```

   迭代portfolio，每一条作为参数传入lambda，获取它的price作为nsmallest的比较参数。

   实现原理是，将集合数据进行`堆排序`并放入一个列表

   堆数据结构最重要的特征是 `heap[0]` 永远是最小的元素。并且剩余的元素可以很容易的通过调用 `heapq.heappop()` 方法得到， 该方法会先将第一个元素弹出来，然后用下一个最小的元素来取代被弹出元素（这种操作时间复杂度仅仅是 O(log N)，N 是堆大小）。

   **当要查找的元素个数相对比较小的时候**，函数 `nlargest()` 和 `nsmallest()` 是很合适的。 **如果你仅仅想查找唯一的最小或最大（N=1）的元素的话**，那么使用 `min()` 和 `max()` 函数会更快些。 类似的，**如果 N 的大小和集合大小接近的时候**，通常先排序这个集合然后再使用切片操作会更快点 （ `sorted(items)[:N]` 或者是 `sorted(items)[-N:]` ）。 需要在正确场合使用函数 `nlargest()` 和 `nsmallest()` 才能发挥它们的优势 （如果 N 快接近集合大小了，那么使用排序操作会更好些）。

   用heapq的堆排序特性，定义一个优先级队列

   ```python
   import heapq

   class PriorityQueue:
       def __init__(self):
           self._queue = []
           self._index = 0

       def push(self, item, priority):
           heapq.heappush(self._queue, (-priority, self._index, item))
           self._index += 1

       def pop(self):
           return heapq.heappop(self._queue)[-1]

       def queue(self):
           return self._queue

   class Item:
       def __init__(self, name):
           self.name = name

       def __repr__(self):
           return 'Item({!r})'.format(self.name)

   q = PriorityQueue()
   q.push(Item('foo'), 1)
   q.push(Item('bar'), 5)
   q.push(Item('spam'), 4)
   q.push(Item('grok'), 1)
   print(q.queue())
   for i in range(4):
       print(q.pop())

   '''
   [(-5, 1, Item('bar')), (-1, 0, Item('foo')), (-4, 2, Item('spam')), (-1, 3, Item('grok'))]
   Item('bar')
   Item('spam')
   Item('foo')
   Item('grok')
   '''
   ```

   需注意：此处队列不是线程安全的，定义`index`用于同等优先级按添加顺序排序

4. dict的key是可以作为一个集合来进行运算的：

   ```python
   a = {'x' : 1, 'y' : 2, 'z' : 3}
   b = {'w' : 10, 'x' : 11, 'y' : 2}
   # Find keys in common
   a.keys() & b.keys() # { 'x', 'y' }
   # Find keys in a that are not in b
   a.keys() - b.keys() # { 'z' }
   # Find (key,value) pairs in common
   a.items() & b.items() # { ('y', 2) }
   ```

5. 生成器和匿名函数lambda的一个运用

   ```python
   # 保持元素顺序的同时消除重复的值
   def dedupe(items):
       seen = set()
       for item in items:
           if item not in seen:
               yield item
               seen.add(item)
       print(seen)

   a = [1, 5, 2, 1, 9, 1, 5, 10]
   print(list(dedupe(a)))
   # [1, 5, 2, 9, 10]

   # 进阶
   def dedupe_1(items, key=None):
       seen = set()
       for item in items:
           '''
           输入{'x': 1, 'y': 2}
           返回(1, 2)元组
           '''
           val = item if key is None else key(item)
           if val not in seen:
               yield item
               seen.add(val)
       print(seen)

   b = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
   print(list(dedupe_1(b, key=lambda d: (d['x'], d['y']))))
   # [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
   ```

6. 切片对象

   ```python
   >>> a.slice(5, 10, 2)
   >>> a.start
   5
   >>> a.stop
   10
   >>> a.step
   2
   >>> s = 'HelloWorld'
   >>> a.indices(len(s))
   (5, 10, 2)
   >>> for i in range(*a.indices(len(s))):
   ...     print(s[i])
   ...
   W
   r
   d
   >>>
   ```

   你还可以通过调用切片的 `indices(size)` 方法将它映射到一个已知大小的序列上。 这个方法返回一个三元组 `(start, stop, step)` ，所有的值都会被缩小，直到适合这个已知序列的边界为止。 这样，使用的时就不会出现 `IndexError` 异常。

7. 序列中重复次数最多的元素`hashable`

   ```python
   from collections import Counter
   word_counts = Counter(words)
   # 出现频率最高的3个单词
   top_three = word_counts.most_common(3)
   ```

8. 通过某个关键字排序

   通常情况下对字典列表排序或者最大值最小值会使用lambda：

   ```python
   >>> rows = [
       {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
       {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
       {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
       {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
   ]
   >>> rows_by_fname = sorted(rows, key=lambda r: r['fname'])

   >>> min(rows, key=lambda r: r['uid'])
   ```

   但是有一个性能更好的方法，通过使用 `operator` 模块的 `itemgetter` 函数

   ```python
   >>> from operator import itemgetter
   >>> rows_by_fname = sorted(rows, key=itemgetter('fname'))
   >>> min(rows, key=itemgetter('uid'))
   ```

   当需要对一个不支持原生比较的对象排序时，可以使用`operator` 模块的 `attrgetter`函数，原理同上，可以很好地代替lambda，且运用范围更广。

9. 通过某个字段分组

   你有一个字典或者实例的序列，然后你想根据某个特定的字段比如 `date` 来分组迭代访问，`itertools.groupby()` 函数对于这样的数据分组操作非常实用。

   结合上面函数：

   ```python
   from operator import itemgetter
   from itertools import groupby

   rows = [
       {'address': '5412 N CLARK', 'date': '07/01/2012'},
       {'address': '5148 N CLARK', 'date': '07/04/2012'},
       {'address': '5800 E 58TH', 'date': '07/02/2012'},
       {'address': '2122 N CLARK', 'date': '07/03/2012'},
       {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
       {'address': '1060 W ADDISON', 'date': '07/02/2012'},
       {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
       {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
   ]
   # Sort by the desired field first
   rows.sort(key=itemgetter('date'))
   # Iterate in groups
   for date, items in groupby(rows, key=itemgetter('date')):
       print(date)
       for i in items:
           print(' ', i)
   ```

10. 过滤元素，可以使用列表推导式`[n for n in mylist if n > 0]`，当数据源可能比较大时，为了内存需要使用生成器表达式

    ```python
    >>> pos = (n for n ib mylist if n > 0)
    >>> pos
    <generator object <genexpr> at 0x1006a0eb0>
    >>> for x in pos:
    ... print(x)
    ```

    推导式也可以进行一些简单的数据转换等，不仅仅是丢弃数据

    ```python
    >>> import math
    >>> [math.sqrt(n) for n in mylist if n > 0]
    >>> [n if n > 0 else 0 for n in mylist]
    ```

    但是当过滤规则较复杂时，包括一些异常处理等，则使用内置函数`filter( )`函数

    ```python
    values = ['1', '2', '-3', '-', '4', 'N/A', '5']
    def is_int(val):
        try:
            x = int(val)
            return True
        except ValueError:
            return False
    ivals = list(filter(is_int, values))
    print(ivals)
    # Outputs ['1', '2', '-3', '4', '5']
    ```

    额外还有一个 `itertools.compress( )` 值得关注，需要用另外一个相关联的序列来过滤某个序列的时候比较好运用。

11. 字典推导式比较快

    ```python
    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }
    # 这个方式比下面的快，且易于阅读
    p1 = {key: value for key, value in prices.items() if value > 200}
    p1_1 = dict((key, value) for key, value in prices.items() if value > 200)

    tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
    p2 = {key: value for key, value in prices.items() if key in tech_names}
    ```


### 测试、调试和异常

1. 捕获异常，自定义异常或者异常信息显示最好加上原来捕获的异常情况，具体用法是`raise from`

   ```python
   >>> def example():
   ...     try:
   ...             int('N/A')
   ...     except ValueError as e:
   ...             raise RuntimeError('A parsing error occurred') from e
   ...
   >>> example()
   Traceback (most recent call last):
     File "<stdin>", line 3, in example
   ValueError: invalid literal for int() with base 10: 'N/A'

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<stdin>", line 5, in example
   RuntimeError: A parsing error occurred


   >>> # 或者这样
   >>> def example():
   ...     try:
   ...             int('N/A')
   ...     except ValueError:
   ...             print("Didn't work")
   ...             raise
   ...
   >>> example()
   Didn't work
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<stdin>", line 3, in example
   ValueError: invalid literal for int() with base 10: 'N/A'
   ```

2. 性能测试

   可以直接测试整个文件的运行情况，使用`time  python3  foo.py`或者`python3  -m  cProfile  foo.py`，前者过于简洁，后者过于详细，而且一般我们都是针对于少数函数或者代码块来检测性能

   装饰器：

   ```python
   # thistime.py

   import time
   from functools import wraps

   def thistime(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           start = time.perf_counter()
           r = func(*args, **kwargs)
           end = time.perf_counter()
           print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
           return r
       return wrapper
   ```

   ```python
   >>> @thistime
   ... def countdown(n):
   ...     while n > 0:
   ...             n -= 1
   ...
   >>> countdown(10000000)
   __main__.countdown : 0.803001880645752
   >>>
   ```



   代码块

   ```python
   from contextlib import contextmanager

   @contextmanager
   def timeblock(label):
       start = time.perf_counter()
       try:
           yield
       finally:
           end = time.perf_counter()
           print('{} : {}'.format(label, end - start))
   ```

   ```python
   >>> with timeblock('counting'):
   ...     n = 10000000
   ...     while n > 0:
   ...             n -= 1
   ...
   counting : 1.5551159381866455
   >>>
   ```



   极小代码片段

   ```python
   >>> from timeit import timeit
   >>> timeit('math.sqrt(2)', 'import math')
   0.1432319980012835
   >>> timeit('sqrt(2)', 'from math import sqrt')
   0.10836604500218527
   >>>
   ```

   需要提醒的是，`time.perf_counter( )`会是给定平台上最高精度的计时值，但仍是时钟值，所以可以更换为`time.process_time( )`

3. 加速程序运行

   1. **将代码运行在函数中**，一般提升15%-30%的性能，这是因为全局变量和局部变量

   2. **尽可能去掉属性访问**，每一次使用`.`来访问属性会带来额外的开销，会触发特定的`__getattribute__( )`和`__getattr__( )`，会进行字典操作，所以需要使用`from  modele  import  name`来导入，原来代码如下：

      ```python
      import math
      from TimeUtils import timeblock  # 上面自定义的计时器

      def compute_roots(nums):
          result = []
          for n in nums:
              result.append(math.sqrt(n))
          return result

      with timeblock('count'):
          nums = range(1000000)
          for n in range(100):
              r = compute_roots(nums)

      # 结果
      count : 39.508564
      ```

      修改为下：

      ```python
      from math import sqrt
      from TimeUtils import timeblock


      def compute_roots(nums):
          result = []
          result_append = result.append
          for n in nums:
              result_append(sqrt(n))
          return result


      with timeblock('count'):
          nums = range(1000000)
          for n in range(100):
              r = compute_roots(nums)

      # 结果
      count : 26.378584
      ```

      这么大的差距缘由在于大量重复调用，所以遇到这种情况需要调优

4. **局部变量**，承接上一节，修改`compute_roots`：

   ```python
   def compute_roots(nums):
       result = []
       # 定义为局部变量
       l_sqrt = sqrt
       result_append = result.append
       for n in nums:
           result_append(l_sqrt(n))
       return result

   # 结果
   count : 24.394634
   ```

   又有所提升，包括`self.value`如果被某个函数频繁调用，也需要内部转为局部变量`l_value  =  self.value`

5. **避免不必要的抽象**，不要把别的语言(Java)的思想带到Python中，例如：

   ```python
   from timeit import timeit


   class A:
       def __init__(self, x, y):
           self.x = x
           self._y = y

       @property
       def y(self):
           return self._y

       @y.setter
       def y(self, value):
           self._y = value


   a = A(1, 2)
   print(timeit('a.x', 'from __main__ import a'))
   print(timeit('a.y', 'from __main__ import a'))
   # 结果
   0.032640684
   0.11556200499999997
   ```

   需要审视是否需要定义属性访问器。

6. **使用内置的容器**，内置的数据类型比如字符串、元组、列表、集合和字典都是使用C来实现的，运行起来非常快。 如果你想自己实现新的数据结构（比如链接列表、平衡树等）， 那么要想在性能上达到内置的速度几乎不可能，因此，还是乖乖的使用内置的吧。

7. **避免创建不必要的数据结构或复制**

8. 字典的创建

   ```python
   a = {
       'name' : 'AAPL',
       'shares' : 100,
       'price' : 534.22
   }

   b = dict(name='AAPL', shares=100, price=534.22)
   ```

   第二种方法比第一种慢上三倍。
