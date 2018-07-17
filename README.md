# 简介

Python3 实现批量查询网站的百度权重以及收录情况，利用的是站长之家的SEO查询接口，所以本脚本相当于是一个爬虫，用来批量提取数据信息。

# 依赖安装

到项目下使用`pip`来安装相关依赖

```shell
cd seo/
pip install -r requirements.txt
```

# 使用方法

`-r`：手动选择包含域名列表的文件

```shell
python3 seo.py -r /Users/sqlsec/Temp/domain.txt
```

# 脚本演示

![](http://image.3001.net/images/20180717/15318170426637.png)  