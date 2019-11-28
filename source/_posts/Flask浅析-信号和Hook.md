title: Flask浅析-信号和Hook
entitle: 'FLask-signals & hook'
categories: Flask
date: 2019-11-28 11:06:00
tags:
    - Flask
    - python
    - deep
keywords: Flask
description: Flask浅析系列
---
由于翻看源码时看到flask根目录下有个`signals.py`文件，且部分代码如下

```python
from blinker import Namespace

# The namespace for code signals.  If you are not Flask code, do
# not put signals in here.  Create your own namespace instead.
_signals = Namespace()


# Core signals.  For usage examples grep the source code or consult
# the API documentation in docs/api.rst as well as docs/signals.rst
request_started = _signals.signal("request-started")
request_finished = _signals.signal("request-finished")
request_tearing_down = _signals.signal("request-tearing-down")

```

故而自然而然的以为我们常用的`@app.before_request`就是通过信号(signal)来触发的，但是顺手全局搜索了`request_started.connect()`，却没有发现代码，所以只能点开`@app.before_request`一探究竟



`app`是`Flask`的实例，所以`before_request`是这个类的函数

```python
class Flask:
    self.before_request_funcs = {}
    @setupmethod
    def before_request(self, f):
        """Registers a function to run before each request.

        For example, this can be used to open a database connection, or to load
        the logged in user from the session.

        The function will be called without any arguments. If it returns a
        non-None value, the value is handled as if it was the return value from
        the view, and further request handling is stopped.
        """
        self.before_request_funcs.setdefault(None, []).append(f)
        return f
```

这里的`@setupmethod`起到了监测debug模式下会重复启动两次会出现的一些错误，按下不表。

这个函数主要是把被装饰的函数放到一个函数字典中，key是None，value是一组被装饰的函数

例如我的项目中，启动的时候会调用`create_app`函数，中间有个`middleware`文件，中间就写了一批被装饰的函数，这样就全放到了这个字典中。



此时项目启动时就已经把需要运行的函数注册进来了，正式进入一个http请求流程，`werkzeug`作为`flask`的基础web服务组件，接收到一个请求时，会调用`app(environ, start_response)`来掉起flask中的 `wsgi_app` (使用的是Flask类的`__call__`魔术方法)

```python
    def wsgi_app(self, environ, start_response):
        ctx = self.request_context(environ)
        error = None
        try:
            try:
                ctx.push()
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:  # noqa: B001
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)
```

这里主要是关于上下文堆栈出栈和错误处理的代码，主要在`full_dispatch_request`中

```python
    def full_dispatch_request(self):
        self.try_trigger_before_first_request_functions()
        try:
            request_started.send(self)
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
        except Exception as e:
            rv = self.handle_user_exception(e)
        return self.finalize_request(rv)
      
   def preprocess_request(self):
        bp = _request_ctx_stack.top.request.blueprint

        funcs = self.url_value_preprocessors.get(None, ())
        if bp is not None and bp in self.url_value_preprocessors:
            funcs = chain(funcs, self.url_value_preprocessors[bp])
        for func in funcs:
            func(request.endpoint, request.view_args)

        funcs = self.before_request_funcs.get(None, ())
        if bp is not None and bp in self.before_request_funcs:
            funcs = chain(funcs, self.before_request_funcs[bp])
        for func in funcs:
            rv = func()
            if rv is not None:
                return rv
```

从这能看到先执行的信号，再执行被装饰的hook函数，所以如果需要某些先于hook触发的函数，不妨使用signals来注册。



最后有flask的特性，当hook函数中有返回值时，直接返回该返回值，不去触发接下来的所有函数，包括之后的路由寻址。



```python
    def finalize_request(self, rv, from_error_handler=False):
        response = self.make_response(rv)
        try:
            response = self.process_response(response)
            request_finished.send(self, response=response)
        except Exception:
            if not from_error_handler:
                raise
            self.logger.exception(
                "Request finalizing failed with an error while handling an error"
            )
        return response
```

与之前相反，response的信号顺序则慢于hook触发，颇有些类似django的middleware的触发顺序