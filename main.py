import json
import xml.etree.ElementTree as ET
from urllib.error import HTTPError

from classes.utils import UtilsIR
from urllib.request import urlopen
from urllib.parse import quote
import re
from bs4 import BeautifulSoup

__func_utils = UtilsIR()

list_id_deleted = [205, 584, 632, 640, 933, 934, 935, 939, 940, 944]

def create_file_links():
    tree = ET.parse('course.xml')
    root = tree.getroot()
    dict_links = {}
    for child in root:
        link = child[0].text
        dict_links[link.split("/").pop()] = link
    __func_utils.write_file(dict_links, "links", "json")
    return dict_links


def download_file_htmls(limit: int = -1, start: int = 0):
    dict_links = __func_utils.read_file("links", "json")
    print(len(dict_links))
    i = 0
    j = 0
    for link in dict_links:
        if start <= i:
            if j >= limit >= 0:
                break
            url = dict_links[link]
            print(url)
            encoded_url = quote(url, safe=':/')
            try:
                print(i)
                page = urlopen(encoded_url)
                html_bytes = page.read()
                html = html_bytes.decode("utf-8")
                __func_utils.write_file(html, link, "html")
            except:
                print("errrrrrrorrrrrrrrrr")
                continue
            j += 1
        i += 1


def export_words_from_htmls(limit: int = -1):
    dict_links = __func_utils.read_file("links", "json")
    i = 0
    list_of_information = []
    for link in dict_links:
        if i >= limit >= 0:
            break
        if i not in list_id_deleted:
            print(i, dict_links[link])
            html_content = __func_utils.read_file(f"{link}", "html")
            soup = BeautifulSoup(html_content, 'html.parser')
            course_content_text = soup.find('div', class_='course-content-text js-collapse-container')
            header_text = course_content_text.contents[0]
            description_text = course_content_text.contents[1]
            tags_content_text = soup.find('div', class_='box-shadow tags-layer')
            if tags_content_text is not None:
                tags_content_text.contents = tags_content_text.contents[1:]
            list_of_information.append({"id": i, "title": header_text.text.strip(), "plot": description_text.text.strip(),
                                        "tags": tags_content_text.text.strip() if tags_content_text is not None else ""})
        i += 1
    __func_utils.write_file(list_of_information, "data_website", "json")


limit = -1
# create_file_links()
# download_file_htmls(limit, 1000)
# export_words_from_htmls(limit)

