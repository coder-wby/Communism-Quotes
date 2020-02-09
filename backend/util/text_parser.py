# -*- coding: utf-8 -*-

""" 文本解析器

"""

import re


def check_contain_chinese(_check_str: str) -> bool:
    """ 判断输入的str是否含有汉字 """
    for ch in _check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def parse_date_str(_date_str):

    # 跳过空白字符串
    if _date_str is None or _date_str == "" or _date_str == r"\s":
        return None

    # 处理日期信息中的空白
    _date_str = _date_str.replace(" ", "")
    _date_str = _date_str.replace("—", "-")
    _date_str = _date_str.replace("—", "-")
    _date_str = _date_str.replace("——", "-")

    # 匹配日期格式 19XX年X月X日
    pattern = r'\d\d\d\d年\d+月\d+日'
    result = re.findall(pattern, _date_str)
    if result:
        return result

    # 匹配季节信息 19XX年春 19XX年春夏
    pattern_season = r'\d\d\d\d年[春夏秋冬]'
    result = re.findall(pattern_season, _date_str)
    if result:
        return result

    # 匹配月份信息 19XX年x月底
    pattern = r'\d\d\d\d年\d+月底'
    result = re.findall(pattern, _date_str)
    if result:
        return result

    # 匹配月份信息 19XX年x月下旬
    pattern = r'\d\d\d\d年\d+月下旬'
    result = re.findall(pattern, _date_str)
    if result:
        return result

    # 匹配月份信息 19XX年x月
    pattern = r'\d\d\d\d年\d+月'
    result = re.findall(pattern, _date_str)
    if result:
        return result

    # 匹配月份信息 19XX年x月-x月
    pattern = r'\d\d\d\d年(\d+月)-(\d+月)'
    result = re.findall(pattern, _date_str)
    if result:
        return result

    # 匹配月份信息 19XX年x-x月
    pattern = r'\d\d\d\d年\d+-\d+月'
    result = re.findall(pattern, _date_str)
    if result:
        return result

    # 匹配年份信息 19XX年底
    pattern = r'\d\d\d\d年底'
    result = re.findall(pattern, _date_str)
    if result:
        return result

    # 匹配年份信息 19XX年
    pattern = r'\d\d\d\d年'
    result = re.findall(pattern, _date_str)
    if result:
        return result


def split_para_2_sentence(_para_text):
    _pattern = r'，|。|！|？|——'
    return re.split(_pattern, _para_text)


def extract_brackets(_target_text):
    return re.findall(r".*\((.*)\).*", _target_text)
