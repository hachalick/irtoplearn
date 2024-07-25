import json
import re


class UtilsIR:
    def write_file(self, data: list | dict, name_file: str, format_file: str):
        print(f"\033[95msaving {name_file}.{format_file} ...\033[0m")
        if format_file == "txt":
            f = open(f"files/txts/{name_file}.txt", "w", encoding='utf-8')
            f.write(str(data))
            f.close()
        elif format_file == "json":
            f = open(f"files/jsons/{name_file}.json", "w", encoding='utf-8')
            f.write(json.dumps(data))
            f.close()
        elif format_file == "html" or format_file == "htm":
            f = open(f"files/htmls/{name_file}.html", "w", encoding='utf-8')
            f.write(str(data))
            f.close()

    def read_file(self, name_file: str, format_file: str):
        print(f"\033[95mreading {name_file}.{format_file} ...\033[0m")
        if format_file == "txt":
            f = open(f"files/txts/{name_file}.txt", "r", encoding='utf-8')
            return f.read()
        elif format_file == "json":
            f = open(f"files/jsons/{name_file}.json", "r", encoding='utf-8')
            return json.loads(f.read())
        elif format_file == "html" or format_file == "htm":
            f = open(f"files/htmls/{name_file}.html", "r", encoding='utf-8')
            return f.read()

    def remove_frequency_words_from_list(self, data: list) -> list:
        return list(dict.fromkeys(data))

    def int_to_binary(self, number: int, bite: int = 0) -> str:
        if bite == 0:
            return bin(number)[2:]
        else:
            count = int(len(bin(number)[2:])/bite)+1
            return bin(number)[2:].zfill(bite * count)

    def binary_to_int(self, number: str) -> int:
        return int(number, 2)

    def binary_to_vb_code(self, number: str, bite: int) -> str:
        vb_code = []
        length_number = len(number)
        for i in range(int(length_number/bite)):
            if (i + 1) * bite == length_number:
                vb_code.append("1")
            else:
                vb_code.append("0")
            vb_code.append(number[i*bite:(i+1)*bite])
        return "".join(vb_code)

    def create_list_bigrams(self, word: str, return_reg: bool = True) -> list :
        list_k_gram = []
        word = word.lower()
        for i in range(len(word) - 1):
            if return_reg:
                list_k_gram.append(".*"+word[i:i+2]+".*")
            else:
                list_k_gram.append(word[i:i+2])
        return list_k_gram

    def get_list_int_value_from_dict(self, dict_word: dict, reverse: bool = True) -> list:
        """
        get dict of word - frequency and return list of frequencies without duplicates sorted from highest to lowest
        :param dict_word: dict of tokens
        :param reverse: bool, sort by frequency
        :return: [ highest_frequency, ..., lowest_frequency ]
        """
        new_list = []
        for i in dict_word:
            new_list.append(dict_word[i])
        new_list = list(dict.fromkeys(new_list))
        new_list.sort(reverse=reverse)
        return new_list

    def get_input(self, type_input: str, text_input: str = "enter: ") -> str | int | float | bool:
        """
        set type of input and return a value with that type
        :param type_input:str -> "str" | "int" | "float" | "bool"
        :param text_input:str -> default "enter: "
        :return: "" | 0 | 0.0 | True or False
        """
        print(type_input)
        while True:
            text = input(text_input)
            if type_input == "str":
                return text
            elif type_input == "int":
                try:
                    return int(text)
                except ValueError:
                    print("invalid input -> int")
            elif type_input == "float":
                try:
                    return float(text)
                except ValueError:
                    print("invalid input -> float")
            elif type_input == "bool":
                if text == "true" or text == "True" or text == "1":
                    return True
                elif text == "false" or text == "False" or text == "0":
                    return False
                else:
                    print("invalid input -> bool")
            else:
                raise ValueError('get input have not type')

    def sort_list_of_dicts(self, list_of_dicts: list[dict], base_key: str, reverse: bool = True) -> list[dict]:
        sorted_data = sorted(list_of_dicts, key=lambda x: x[base_key], reverse=reverse)
        list_of_dicts.sort(key=lambda x: x[base_key], reverse=reverse)
        return sorted_data

    def remove_stopword(self, dict_of_word: dict, limit: int) -> dict:
        list_word_del = []
        for word in dict_of_word:
            if dict_of_word[word]["frequency"] > limit:
                list_word_del.append(word)
        for word in list_word_del:
            del dict_of_word[word]
        return dict_of_word

    def color_text(self, text: str) -> str:
        return f"\033[92m{text}\033[0m"

    def print_dict(self, dict_of_data: dict, end="\n") -> None:
        list_len_key = []
        for key in dict_of_data.keys():
            list_len_key.append(len(key))
        max_len = max(list_len_key)
        for key in dict_of_data:
            title = self.fill_text(key, " ", max_len)
            print(f"\033[93m{title} )\033[0m {dict_of_data[key]}", end=end)

    def fill_text(self, text: str, place: str, number: int) -> str:
        mines = number - len(text)
        for i in range(mines):
            text += place
        return text

    def detect_language(self, word: str) -> str:
        """
        Detects the word is english or farsi
        :param word: str -> word
        :return:str -> "en" | "fa"
        """
        if re.match("^[a-z0-9#]*$", word):
            detected_language = "en"
        elif re.match("^[\u0600-\u06FF\s]+$", word):
            detected_language = "fa"
        else:
            detected_language = "com"
        return detected_language
