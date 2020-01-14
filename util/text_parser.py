# -*- coding: utf-8 -*-

import re


def split_para_2_sentence(_para_text):
    _pattern = r'，|。|！|？|——'
    return re.split(_pattern, _para_text)
