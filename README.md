# 中文马克思主义文库检索系统

> 马克思、恩格斯、列宁、斯大林的理论，是“放之四海而皆准”的理论。
> 不应当把他们的理论当作教条看待，而应当看作行动的指南。
> 不应当只是学习马克思列宁主义的词句，而应当把它当成革命的科学来学习。
> 不但应当了解马克思、恩格斯、列宁、斯大林他们研究广泛的真实生活和革命经验所得出的关于一般规律的结论，而且应当学习他们观察问题和解决问题的立场和方法。
> —— 毛泽东 <中国共产党在民族战争中的地位> 一九三八年十月十四日

![Github Social Coding](docs/git_social.jpg)

本项目是中文马克思主义著作的全文检索系统。
用户可以输入关键字以及其他信息，以获取匹配程度最高的马克思主义著作原句。

本仓库包含以下内容：

## 内容列表

- [背景](#背景)
- [安装](#安装)
- [使用](#使用)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [使用许可](#使用许可)


## 背景

当我们需要查阅关于某些话题的经典论述时，经常因忘记了具体的措辞而无所适从。
因为我们无法记提供这些名词的精确表述，所以我们就无法在某些事情发生的时候查一查历史上是否有先辈曾经做出过相关的论述。
我们需要一套可以提供文本关联和推荐排序的搜索系统。

## 安装

### 依赖环境

- `Python 3.7`
- `ElasticSearch 7.5.0`
- `MySQL 8.0`

### 安装方式

1. 下载项目源码到本地，并进入根目录。
    ```
    git clone https://github.com/nevertiree/Communism-Quotes.git 
    cd Communism-Quotes/
    ```

2. 运行`setup.py`文件

    ```
    python setup.py
    ```

3. 配置`ElasticSearch`和`MySQL`信息

## 使用

## 维护者

[@nevertiree](https://github.com/nevertiree)

## 如何贡献

非常欢迎你的加入! 
[提一个Issue](https://github.com/nevertiree/Communism-Quotes/issues/new)
或者提交一个 `Pull Request`.

本项目遵循 [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) 行为规范。

## 使用许可

[MIT](LICENSE) @ Nevertiree
