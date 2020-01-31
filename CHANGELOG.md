# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Version](https://semver.org/spec/v2.0.0.html).

Added Changed Deprecated Removed Fixed Security

## [Unreleased]

## [0.0.3] - 2020-01-31

### Add 
- 增加了检索部分，在`es_query.py`文件中

### Changed
- 对没有句号结尾的句子进行整合
- 把插入数据的文件名改成 `es_insert.py` 

## [0.0.2] - 2020-01-15

实现了基于`ElasticSearch`的检索引擎，版本是`7.5.0`。
使用了`ik`分词插件，使用了`ik_max_word`进行分词。
使用`bulk`进行批量导入。

## [0.0.1] - 2020-01-14

实现了基于`MongoDB`的检索引擎。
首先用`lxml`提取`HTML`中的文本信息，然后做简单的文本清洗。
把语料存入`MongoDB`中，每个记录是一个自然段，其他信息包括文章名称、发表日期和出处等等。
查询时直接使用`MongoDB`内自带的全文查询模块。

这个版本只能在命令行上运行，不支持`Web`前端。
目前还没有实现大量查询结果的排序。

总之，这至少可以用。

