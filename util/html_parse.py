# -*- coding: utf-8 -*-

from lxml import etree

gbk_parser = etree.HTMLParser(encoding='GBK')


def parse_html_file(html_file_path):

    html = etree.parse(html_file_path,
                       parser=gbk_parser)

    title = html.findtext('.//title')
    title.replace(" ", "")

    sub_title = html.findtext('.//p[@class="title1"]')
    date_text = html.findtext('.//p[@class="date"]')

    text_content_list = list(map(str, html.xpath("//text()")))

    # Remove un-Chinese
    text_content_list = [s for s in text_content_list if check_contain_chinese(s)]

    # Remove \n and \u3000
    text_content_list = [s.replace("\n", "") for s in text_content_list]
    text_content_list = [s.replace("\u3000", "") for s in text_content_list]

    return title, sub_title, date_text, text_content_list


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


if __name__ == '__main__':
    print(parse_html_file("./material/lenin-cworks/10/001.html"))
