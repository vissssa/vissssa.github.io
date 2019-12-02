---
title: google和github的搜索技巧
categories: 搜索技巧
tags:
  - 技巧
  - deep
keywords: google github 搜索技巧
date: 2019-12-2 15:03:00
---
> 比较简单且直接的搜索方式就是敲上几个关键词，然后回车，等待搜索引擎的反馈
>
> 但是这样的搜索是比较低效且浪费搜索引擎的强大功能的，为了不辜负google和github的好意，
>
> 我们需要了解并使用高阶点的搜索技巧。
<!-- more -->
## Google

google的搜索技巧不太复杂，可能是因为本来结果就已经足够的好，但是有时候我们需要更`精确`或者`特殊`的结果，所以来看看吧

> baidu的搜索技巧基本和google一样，个人觉得没什么不好，起码可以节省学习成本(手动滑稽)

> 运算符后不要带空格

1. 善用标签栏，比如切换到图片，只看最近一个月的结果等

2. 其实我们可以使用google搜索来代替自建站内搜索，只需要使用`site:vissssa.club  xxx`即可，他只会显示该网站的结果，比较适用于搜索github或者stackoverflow等网站

3. 精确匹配，使用`"flask python"`，可以确保flask出现在python之前，去掉空格则会只展示`flaskpython`的结果

4. 数字区间`20..30`之间的所有数字

5. 相关网站`related:v2ex.com`

6. **重要且强大的功能**，google会自带缓存，使用`cache:{url}`可以查看该页面的缓存，当遇到搜索结果404的时候，可以使用该`终结技`来试试，有可能能有意外收获

7. 合理利用`与/或`，默认是使用的`与`，但当我们需要`或`时，只需要在关键词中间加上`张宇 OR 张学友`(大写)即可

8. `+ - ~`有的时候，google会选择性的忽略一些单词，比如“and”、“the，”、“where”、“how”、“what”、“or”等，这时候我们可以使用`+how`来强调这个单词是我需要的，有时候，我们需要忽略某个结果，使用`apple -mobile`来过滤掉苹果手机，还有时候，我们需要获取某个单词的近义词`~elderly`，所得到的页面就会不仅是包括“elderly”这个词，还会有包括“senior”、“older”、“aged”等等词的页面，对了可以使用组合技`~elderly -elderly`来排除掉你已经知道的结果，只获取近义词

9. 一个运算符列表（**注意**：把all去掉，即`allinanchor` --> `inanchor`就是单关键词搜索）

   | 运算符      | **用途**                                                     | **用法**                      |
   | :---------- | :----------------------------------------------------------- | :---------------------------- |
   | allinanchor | 限制搜索的词语是网页中链接内包含的关键词（可使用多个关键词） | allinanchor:keyword1 keyword2 |
   | allintext   | 限制搜索的词语是网页内文包含的关键词（可使用多个关键词）     | allintext:keyword1 keyword2   |
   | allintitle  | 限制搜索的词语是网页标题中包含的关键词（可使用多个关键词）   | allintitle:keyword1 keyword2  |
   | allinurl    | 限制搜索的词语是网页网址中包含的关键词（可使用多个关键词）   | allinurl:keyword1 keyword2    |
   | filetype    | 限制所搜索的文件一个特定的格式                               | filetype:pdf                  |
   | site        | 限制所进行的搜索在指定的域名或网站内                         | site:domain                   |

   

## Github

> github的搜索相对比较复杂，因为涉及到一些运算对象的变化，比如几大范围(title, description, readme等)，和一些stars、趋势的指标，但是能更方便筛选出你需要的repo

> 官方文档在https://help.github.com/cn/github/searching-for-information-on-github
>
> 这里我主要记录一些比较常用的方法

1. **关键词搜索**， 通过repo_name、description、readme来精确筛选，比如在description中搜索微服务回避其他的更好，语法为`in:description`

2. 搜索repo的一些限定符，用法均为`user:vissssa`

   | 限定符               | 示例                                                         |
   | -------------------- | ------------------------------------------------------------ |
   | user:USERNAME        | [**user:defunkt forks:>100**](https://github.com/search?q=user%3Adefunkt+forks%3A>%3D100&type=Repositories) 匹配来自 @defunkt、拥有超过 100 复刻的仓库。 |
   | org:ORGNAME          | [**org:github**](https://github.com/search?utf8=✓&q=org%3Agithub&type=Repositories) 匹配来自 GitHub 的仓库。 |
   | followers:*n*        | [**node followers:>=10000**](https://github.com/search?q=node+followers%3A>%3D10000) 匹配拥有 10,000 或更多关注者并且提及 "node" 一词的仓库。<br />[**styleguide linter followers:1..10**](https://github.com/search?q=styleguide+linter+followers%3A1..10&type=Repositories) 匹配拥有 1 到 10 个关注者并且提及 "styleguide linter" 一词的的仓库。 |
   | forks:*n*            | [**forks:>=205**](https://github.com/search?q=forks%3A>%3D205&type=Repositories) 匹配具有至少 205 个fork的仓库。 |
   | stars:*n*            | [**stars:10..20**](https://github.com/search?q=stars%3A10..20+size%3A<1000&type=Repositories) 匹配具有 10 到 20 个星号 的仓库。 |
   | created:*YYYY-MM-DD* | [**webos created:<2011-01-01**](https://github.com/search?q=webos+created%3A<2011-01-01&type=Repositories) 匹配具有 "webos" 字样、在 2011 年之前创建的仓库。 |
   | pushed:*YYYY-MM-DD*  | [**css pushed:>2013-02-01**](https://github.com/search?utf8=✓&q=css+pushed%3A>2013-02-01&type=Repositories) 匹配具有 "css" 字样、在 2013 年 1 月之后收到推送的仓库。 |
   | language:*LANGUAGE*  | [**rails language:javascript**](https://github.com/search?q=rails+language%3Ajavascript&type=Repositories) 匹配具有 "rails" 字样、以 JavaScript 编写的仓库。 |

3. 还可以根据issue、pr、commit和主题(topic)来搜索，但是比较少见，就不提了

4. 在代码中搜索

   | 限定符                   | 示例                                                         |
   | ------------------------ | ------------------------------------------------------------ |
   | in:file                  | [**octocat in:file**](https://github.com/search?q=octocat+in%3Afile&type=Code) 匹配文件内容中出现 "octocat" 的代码。 |
   | in:path                  | [**octocat in:path**](https://github.com/search?q=octocat+in%3Apath&type=Code) 匹配文件路径中出现 "octocat" 的代码。<br />[**octocat in:file,path**](https://github.com/search?q=octocat+in%3Afile%2Cpath&type=Code) 匹配文件内容或文件路径中出现 "octocat" 的代码。 |
   | path:*PATH/TO/DIRECTORY* | [**console path:app/public**](https://github.com/search?q=console+path%3A"app%2Fpublic"+language%3Ajavascript&type=Code)匹配目录中的代码 |
   | language:*LANGUAGE*      | [**display language:scss**](https://github.com/search?q=display+language%3Ascss&type=Code) 匹配标记为 SCSS 且含有 "display" 字样的代码。 |
   | filename:*FILENAME*      | [**filename:linguist**](https://github.com/search?utf8=✓&q=filename%3Alinguist&type=Code) 匹配名为 "linguist" 的文件。 |
   | extension:*EXTENSION*    | extension:txt匹配文件扩展名                                  |
   |                          |                                                              |

   