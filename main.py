import json
import xml.etree.ElementTree as ET
from classes.utils import UtilsIR
from urllib.request import urlopen
from urllib.parse import quote
import re
from bs4 import BeautifulSoup

__func_utils = UtilsIR()

def create_file_links():
    tree = ET.parse('course.xml')
    root = tree.getroot()
    dict_links = {}
    for child in root:
        link = child[0].text
        dict_links[link.split("/").pop()] = link
    __func_utils.write_file(dict_links, "links", "json")
    return dict_links


def download_file_htmls(limit: int = -1):
    dict_links = __func_utils.read_file("links", "json")
    i = 0
    for link in dict_links:
        if i >= limit >= 0:
            break
        url = dict_links[link]
        encoded_url = quote(url, safe=':/')
        page = urlopen(encoded_url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        __func_utils.write_file(html, link, "html")
        i += 1


def export_words_from_htmls(limit: int = -1):
    dict_links = __func_utils.read_file("links", "json")
    i = 0
    list_of_information = []
    for link in dict_links:
        if i >= limit >= 0:
            break
        html_content = __func_utils.read_file(f"{link}", "html")
        soup = BeautifulSoup(html_content, 'html.parser')
        course_content_text = soup.find('div', class_='course-content-text js-collapse-container')
        header_text = course_content_text.contents[0]
        description_text = course_content_text.contents[1]
        tags_content_text = soup.find('div', class_='box-shadow tags-layer')
        tags_content_text.contents = tags_content_text.contents[1:]
        list_of_information.append({"id": i, "title": header_text.text.strip(), "plot": description_text.text.strip(),
                                    "tags": tags_content_text.text.strip()})
        i += 1
    __func_utils.write_file(list_of_information, "data_website", "json")


limit = 3
# create_file_links()
# download_file_htmls(limit)
export_words_from_htmls(limit)

