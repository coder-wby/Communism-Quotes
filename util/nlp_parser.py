# -*- coding: utf-8 -*-

import os

import thulac

from util.html_parse import parse_html_file

html_file_folder = "maozedong"
text_file_folder = "maozedong"+"_txt"

if __name__ == '__main__':

    thu1 = thulac.thulac(seg_only=True)

    html_name_list = [item for item in os.listdir(html_file_folder) if item.endswith(".html")]

    for html_name in html_name_list:
        html_title, html_content = parse_html_file(os.path.join(html_file_folder, html_name))

        if not os.path.exists(text_file_folder):
            os.mkdir(text_file_folder)

        with open(os.path.join(text_file_folder, html_name), "a+", encoding="utf-8") as f:
            print("Writing " + html_title)

            for i in html_content:
                i = thu1.cut(i, text=True)
                f.write(i + "\n")
