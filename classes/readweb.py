import xml.etree.ElementTree as ET
from time import sleep

from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup

from classes.utils import UtilsIR
from classes.namefile import NameFile


class ReadWeb(object):
    __list_id_deleted = [205, 584, 632, 640, 933, 934, 935, 939, 940, 944]
    __func_utils = UtilsIR()
    __limit = -1

    def __init__(self, limit_search: int = -1):
        self.__limit = limit_search

    def run(self):
        # # step one
        # self.__create_file_links()
        # # step tow
        # dict_links = self.__func_utils.read_file(NameFile.links_json, "json")
        # max_index = len(dict_links)
        # for i in range(max_index):
        #     if i % self.__limit == 0:
        #         self.__download_file_htmls(i)
        #         sleep(20)
        # step three
        self.__export_words_from_htmls()
        # step four
        self.__clear_filed_from_space()
        return

    def __create_file_links(self):
        tree = ET.parse('course.xml')
        root = tree.getroot()
        dict_links = {}
        for child in root:
            link = child[0].text
            dict_links[link.split("/").pop()] = link
        self.__func_utils.write_file(dict_links, NameFile.links_json, "json")
        return dict_links

    def __download_file_htmls(self, start: int = 0):
        dict_links = self.__func_utils.read_file(NameFile.links_json, "json")
        i = 0
        j = 0
        for link in dict_links:
            if start <= i:
                if j >= self.__limit >= 0:
                    break
                url = dict_links[link]
                encoded_url = quote(url, safe=':/')
                try:
                    page = urlopen(encoded_url)
                    html_bytes = page.read()
                    html = html_bytes.decode("utf-8")
                    self.__func_utils.write_file(html, link, "html")
                except:
                    print("error")
                    continue
                j += 1
            i += 1

    def __export_words_from_htmls(self):
        dict_links = self.__func_utils.read_file(NameFile.links_json, "json")
        i = 0
        list_of_information = []
        for link in dict_links:
            if i >= self.__limit >= 0:
                break
            if i not in self.__list_id_deleted:
                html_content = self.__func_utils.read_file(f"{link}", "html")
                soup = BeautifulSoup(html_content, 'html.parser')
                course_content_text = soup.find('div', class_='course-content-text js-collapse-container')
                header_text = course_content_text.contents[0]
                description_text = course_content_text.contents[1]
                tags_content_text = soup.find('div', class_='box-shadow tags-layer')
                if tags_content_text is not None:
                    tags_content_text.contents = tags_content_text.contents[1:]
                list_of_information.append({"id": i, "link": dict_links[link], "title": header_text.text, "plot": description_text.text,
                                            "tags": tags_content_text.text if tags_content_text is not None else ""})
            i += 1
        self.__func_utils.write_file(list_of_information, NameFile.data_website_json, "json")

    def __clear_filed_from_space(self):
        dict_data_website = self.__func_utils.read_file(NameFile.data_website_json, "json")
        for course_key in dict_data_website:
            course_key["title"] = self.__remove_over_space(course_key["title"])
            course_key["plot"] = self.__remove_over_space(course_key["plot"])
            course_key["tags"] = self.__remove_over_space(course_key["tags"])
        self.__func_utils.write_file(dict_data_website, NameFile.dataset_json, "json")

    def __remove_over_space(self, text: str) -> str:
        list_deleted = []
        list_word = text.split(" ")
        for word_index in range(len(list_word)):
            list_word[word_index] = list_word[word_index].lower()
            if list_word[word_index] == "":
                list_deleted.append(word_index)
        i = 0
        for index in list_deleted:
            del list_word[index - i]
            i += 1
        new_text = " ".join(list_word)
        return new_text


