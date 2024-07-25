from classes.utils import UtilsIR
from classes.namefile import NameFile
import hazm
import re
import math


class irsystem:
    __func_utils = UtilsIR()
    __limit = -1
    __normalizer = hazm.Normalizer()
    __fa_stemmer = hazm.Stemmer()
    __fa_lemmatizer = hazm.Lemmatizer()

    def __init__(self, limit: int = 5):
        self.__limit = limit

    def create_posting_list(self):
        list_all_tokenize_word = self.__func_utils.read_file(NameFile.list_all_word_json, "json")
        itr = 0
        list_all_word = []
        for index_data in range(len(list_all_tokenize_word)):
            if 0 <= self.__limit <= itr:
                break
            itr += 1
            for word in list_all_tokenize_word[index_data]["title"]:
                if word not in list_all_word:
                    list_all_word.append(word)
            for word in list_all_tokenize_word[index_data]["plot"]:
                if word not in list_all_word:
                    list_all_word.append(word)
            for word in list_all_tokenize_word[index_data]["tags"]:
                if word not in list_all_word:
                    list_all_word.append(word)
        list_all_word.sort()
        all_dict_words = {}
        for i in list_all_word:
            all_dict_words[i] = {"frequency": 0, "title": [], "plot": [], "tags": []}
        for word in all_dict_words:
            itr = 0
            for data in list_all_tokenize_word:
                if 0 <= self.__limit <= itr:
                    break
                itr += 1
                for index_word_title in range(len(data["title"])):
                    if data["title"][index_word_title] == word:
                        all_dict_words[word]["title"].append({data["id"]: index_word_title})
                for index_word_plot in range(len(data["plot"])):
                    if data["plot"][index_word_plot] == word:
                        all_dict_words[word]["plot"].append({data["id"]: index_word_plot})
                for index_word_tags in range(len(data["tags"])):
                    if data["tags"][index_word_tags] == word:
                        all_dict_words[word]["tags"].append({data["id"]: index_word_tags})
        for i in all_dict_words:
            all_dict_words[i]["frequency"] = (len(all_dict_words[i]["title"]) + len(all_dict_words[i]["plot"]) +
                                              len(all_dict_words[i]["tags"]))
        self.__func_utils.write_file(all_dict_words, NameFile.posting_list_json, "json")

    def normalizer_data(self):
        list_dataset = self.__func_utils.read_file(NameFile.dataset_json, "json")
        itr = 0
        for index_data in range(len(list_dataset)):
            if 0 <= self.__limit <= itr:
                break
            itr += 1
            title = list_dataset[index_data]["title"]
            plot = list_dataset[index_data]["plot"]
            tags = list_dataset[index_data]["tags"]

            list_tokenize_title = self.__tokenize_text(title)
            list_word_title_without_punctuation = self.__remove_punctuation_from_list(list_tokenize_title)
            list_word_title_without_frequency = self.__remove_frequency_word(list_word_title_without_punctuation)
            list_word_title_after_lem_stem = self.__lemmatizer_and_stemmer(list_word_title_without_frequency)
            list_dataset[index_data]["title"] = self.__remove_punctuation_from_list(list_word_title_after_lem_stem)

            list_tokenize_plot = self.__tokenize_text(plot)
            list_word_plot_without_punctuation = self.__remove_punctuation_from_list(list_tokenize_plot)
            list_word_plot_without_frequency = self.__remove_frequency_word(list_word_plot_without_punctuation)
            list_word_plot_after_lem_stem = self.__lemmatizer_and_stemmer(list_word_plot_without_frequency)
            list_dataset[index_data]["plot"] = self.__remove_punctuation_from_list(list_word_plot_after_lem_stem)

            list_tokenize_tags = self.__tokenize_text(tags)
            list_word_tags_without_punctuation = self.__remove_punctuation_from_list(list_tokenize_tags)
            list_word_tags_without_frequency = self.__remove_frequency_word(list_word_tags_without_punctuation)
            list_word_tags_after_lem_stem = self.__lemmatizer_and_stemmer(list_word_tags_without_frequency)
            list_dataset[index_data]["tags"] = self.__remove_punctuation_from_list(list_word_tags_after_lem_stem)

        self.__func_utils.write_file(list_dataset, NameFile.list_all_word_json, "json")

    def __tokenize_text(self, text: str) -> list:
        text = text.replace("\xa0", " ")
        text = text.replace("؟", " ")
        text = text.replace(".", " ")
        text = text.replace("_", " ")
        text = text.replace("=", " ")
        text = text.replace("=", " ")
        text = text.replace("/", " ")
        text = text.replace("\\", " ")
        text = text.replace(",", " ")
        text = text.replace("(", " ")
        text = text.replace(")", " ")
        text = text.replace("!", " ")
        text = text.replace("@", " ")
        text = text.replace("$", " ")
        text = text.replace("%", " ")
        text = text.replace("^", " ")
        text = text.replace("&", " ")
        text = text.replace("*", " ")
        text = text.replace("&", " ")
        text = text.replace(":", " ")
        text = text.replace("اند", " ")
        text = text.replace("آ", "ا")
        list_word = text.split(" ")
        list_tokenize = []
        for index_word in range(len(list_word)):
            list_word[index_word] = list_word[index_word].casefold()
            if list_word[index_word] == "c#" or list_word[index_word] == "#c":
                list_tokenize.append("c#")
                continue
            list_word[index_word] = re.sub("""â€™s""", "", list_word[index_word])
            list_word[index_word] = re.sub("""â€™""", "", list_word[index_word])
            list_word[index_word] = re.sub("""â€œ""", "", list_word[index_word])
            list_word[index_word] = re.sub("""â€¦""", "", list_word[index_word])
            list_word[index_word] = re.sub("""â€""", "", list_word[index_word])
            list_word[index_word] = re.sub("""أ©""", "", list_word[index_word])
            list_word[index_word] = re.sub("""\\.$""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^\\.""", "", list_word[index_word])
            list_word[index_word] = re.sub("""/$""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^/""", "", list_word[index_word])
            list_word[index_word] = re.sub("""-$""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^-""", "", list_word[index_word])
            list_word[index_word] = re.sub("""_$""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^_""", "", list_word[index_word])
            list_word[index_word] = re.sub("""/$""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^/""", "", list_word[index_word])
            list_word[index_word] = re.sub("""\\($""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^\\(""", "", list_word[index_word])
            list_word[index_word] = re.sub("""\\)$""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^\\)""", "", list_word[index_word])
            list_word[index_word] = re.sub(""",$""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^,""", "", list_word[index_word])
            list_word[index_word] = re.sub("""؟$""", "", list_word[index_word])
            list_word[index_word] = re.sub("""^؟""", "", list_word[index_word])
            list_word[index_word] = re.sub("""ترین""", "", list_word[index_word])
            list_word[index_word] = re.sub("""تری""", "", list_word[index_word])
            list_word[index_word] = re.sub("""تر""", "", list_word[index_word])
            list_word[index_word] = re.sub("""دسس""", "", list_word[index_word])
            lang_word = self.__func_utils.detect_language(list_word[index_word])
            if lang_word == "fa":
                list_tokenize = list_tokenize + hazm.word_tokenize(list_word[index_word])
            elif lang_word == "en":
                list_tokenize = list_tokenize + nltk.word_tokenize(list_word[index_word])
            elif lang_word == "com":
                word = self.__split_combine_lang(list_word[index_word])
                word_split = word.split(" ")
                for nw in word_split:
                    lang_nw = self.__func_utils.detect_language(nw)
                    if lang_nw == "fa":
                        list_tokenize = list_tokenize + hazm.word_tokenize(nw)
                    elif lang_nw == "en":
                        list_tokenize = list_tokenize + nltk.word_tokenize(nw)
        for index_word in range(len(list_tokenize)):
            match list_tokenize[index_word]:
                case "n't":
                    list_tokenize[index_word] = "not"
                case "'ll":
                    list_tokenize[index_word] = "will"
                case "'s":
                    list_tokenize[index_word] = "is"
                case "'ve":
                    list_tokenize[index_word] = "have"
                case "'re":
                    list_tokenize[index_word] = "are"
                case "#c":
                    list_tokenize[index_word] = "c#"
        return list_tokenize

    def __remove_punctuation_from_list(self, list_tokenize: list) -> list:
        list_index_delete = []
        for index_word in range(len(list_tokenize)):
            match list_tokenize[index_word]:
                case "":
                    list_index_delete.append(index_word)
                case "/":
                    list_index_delete.append(index_word)
                case "\\":
                    list_index_delete.append(index_word)
                case ".":
                    list_index_delete.append(index_word)
                case "..":
                    list_index_delete.append(index_word)
                case "...":
                    list_index_delete.append(index_word)
                case "....":
                    list_index_delete.append(index_word)
                case ",":
                    list_index_delete.append(index_word)
                case ";":
                    list_index_delete.append(index_word)
                case ":":
                    list_index_delete.append(index_word)
                case "?":
                    list_index_delete.append(index_word)
                case "!":
                    list_index_delete.append(index_word)
                case "@":
                    list_index_delete.append(index_word)
                case "$":
                    list_index_delete.append(index_word)
                case "%":
                    list_index_delete.append(index_word)
                case "^":
                    list_index_delete.append(index_word)
                case "&":
                    list_index_delete.append(index_word)
                case "*":
                    list_index_delete.append(index_word)
                case "(":
                    list_index_delete.append(index_word)
                case ")":
                    list_index_delete.append(index_word)
                case "-":
                    list_index_delete.append(index_word)
                case "--":
                    list_index_delete.append(index_word)
                case "_":
                    list_index_delete.append(index_word)
                case "=":
                    list_index_delete.append(index_word)
                case "+":
                    list_index_delete.append(index_word)
                case "#":
                    list_index_delete.append(index_word)
                case '“':
                    list_index_delete.append(index_word)
                case '”':
                    list_index_delete.append(index_word)
                case '``':
                    list_index_delete.append(index_word)
                case "\'":
                    list_index_delete.append(index_word)
                case "\'\'":
                    list_index_delete.append(index_word)
                case "\'\'":
                    list_index_delete.append(index_word)
                case "\'\'":
                    list_index_delete.append(index_word)
                case "،":
                    list_index_delete.append(index_word)
                case "؟":
                    list_index_delete.append(index_word)
                case "؛":
                    list_index_delete.append(index_word)
                case ",":
                    list_index_delete.append(index_word)
                case "\xa0":
                    list_index_delete.append(index_word)
        ite = 0
        for i in list_index_delete:
            del list_tokenize[i - ite]
            ite += 1
        return list_tokenize

    def __remove_frequency_word(self, list_tokenize: list) -> list:
        list_index_delete = []
        for index_word in range(len(list_tokenize)):
            match list_tokenize[index_word]:
                # case "و":
                #     list_index_delete.append(index_word)
                # case "از":
                #     list_index_delete.append(index_word)
                # case "را":
                #     list_index_delete.append(index_word)
                # case "یا":
                #     list_index_delete.append(index_word)
                case "ای":
                    list_index_delete.append(index_word)
                case "های":
                    list_index_delete.append(index_word)
                case "ها":
                    list_index_delete.append(index_word)
                case "هایی":
                    list_index_delete.append(index_word)
                # case "در":
                #     list_index_delete.append(index_word)
                # case "بر":
                #     list_index_delete.append(index_word)
                # case "این":
                #     list_index_delete.append(index_word)
                # case "که":
                #     list_index_delete.append(index_word)
                # case "به":
                #     list_index_delete.append(index_word)
                case "هر":
                    list_index_delete.append(index_word)
                # case "تا":
                #     list_index_delete.append(index_word)
                case "این":
                    list_index_delete.append(index_word)
                # case "آن":
                #     list_index_delete.append(index_word)
                case "می":
                    list_index_delete.append(index_word)
                # case "ما":
                #     list_index_delete.append(index_word)
                case "تون":
                    list_index_delete.append(index_word)
                case "مندان":
                    list_index_delete.append(index_word)
                case "ایم":
                    list_index_delete.append(index_word)
                case "کنل":
                    list_index_delete.append(index_word)
                case "مندی":
                    list_index_delete.append(index_word)
                case "هاو":
                    list_index_delete.append(index_word)
                case "هارا":
                    list_index_delete.append(index_word)
                case "برمی":
                    list_index_delete.append(index_word)
        ite = 0
        for i in list_index_delete:
            del list_tokenize[i - ite]
            ite += 1
        return list_tokenize

    def __lemmatizer_and_stemmer(self, list_tokenize: list) -> list:
        for index_word in range(len(list_tokenize)):
            lang_word = self.__func_utils.detect_language(list_tokenize[index_word])
            if lang_word == "en":
                match list_tokenize[index_word]:
                    case "windows":
                        list_tokenize[index_word] = "ویندوز"
                        continue
                    case "phone":
                        list_tokenize[index_word] = "تلفن"
                        continue
                    case "ios":
                        list_tokenize[index_word] = "ای او اس"
                        continue
                    case "cross":
                        list_tokenize[index_word] = "کراس"
                        continue
                    case "platform":
                        list_tokenize[index_word] = "پلتفرم"
                        continue
                    case "xamarin":
                        list_tokenize[index_word] = "زامارین"
                        continue
                    case "android":
                        list_tokenize[index_word] = "اندروید"
                        continue
                    case "microsoft":
                        list_tokenize[index_word] = "ماکروسافت"
                        continue
                    case "visual":
                        list_tokenize[index_word] = "ویژوال"
                        continue
                    case "studio":
                        list_tokenize[index_word] = "استدیو"
                        continue
                    case "gps":
                        list_tokenize[index_word] = "جی پی اس"
                        continue
                    case "sqlite":
                        list_tokenize[index_word] = "اس کیو لایت"
                        continue
                    case "webapi":
                        list_tokenize[index_word] = "وب ای پی ای"
                        continue
                    case "material":
                        list_tokenize[index_word] = "متریال"
                        continue
                    case "design":
                        list_tokenize[index_word] = "دیزاین"
                        continue
                    case "forms":
                        list_tokenize[index_word] = "فرم"
                        continue
                    case "froms":
                        list_tokenize[index_word] = "فرم"
                        continue
                    case "form":
                        list_tokenize[index_word] = "فرم"
                        continue
                    case "c#":
                        list_tokenize[index_word] = "سی شارپ"
                        continue
                    case "toolkit":
                        list_tokenize[index_word] = "تولکیت"
                        continue
                    case "api":
                        list_tokenize[index_word] = "ای پی ای"
                        continue
                    case "google":
                        list_tokenize[index_word] = "گوگل"
                        continue
                    case "support":
                        list_tokenize[index_word] = "ساپورت"
                        continue
                    case "coremotion":
                        list_tokenize[index_word] = "کورموشن"
                        continue
                    case "passkit":
                        list_tokenize[index_word] = "پسکیت"
                        continue
                    case "storekit":
                        list_tokenize[index_word] = "استورکیت"
                        continue
                    case "play":
                        list_tokenize[index_word] = "پلی"
                        continue
                    case "web":
                        list_tokenize[index_word] = "وب"
                        continue
                    case "kotlin":
                        list_tokenize[index_word] = "کاتلین"
                        continue
                    case "whatsapp":
                        list_tokenize[index_word] = "واتساپ"
                        continue
                    case "jdk":
                        list_tokenize[index_word] = "جی دی کا"
                        continue
                    case "bytecode":
                        list_tokenize[index_word] = "بی کد"
                        continue
                    case "inline":
                        list_tokenize[index_word] = "این لاین"
                        continue
                    case "lambda":
                        list_tokenize[index_word] = "لامبدا"
                        continue
                    case "proguard":
                        list_tokenize[index_word] = "پروگارد"
                        continue
                    case "100k":
                        list_tokenize[index_word] = "صد هزار"
                        continue
                    case "build":
                        list_tokenize[index_word] = "بیلد"
                        continue
                    case "koans":
                        list_tokenize[index_word] = "کوانس"
                        continue
                    case "pages":
                        list_tokenize[index_word] = "صفحه"
                        continue
                    case "layout":
                        list_tokenize[index_word] = "لایه"
                        continue
                    case "command":
                        list_tokenize[index_word] = "کامند"
                        continue
                    case "controls":
                        list_tokenize[index_word] = "کنترل"
                        continue
                    case "and":
                        list_tokenize[index_word] = "و"
                        continue
                    case "pluginsstyles":
                        list_tokenize[index_word] = "پلاگین استایل"
                        continue
                    case "authorized":
                        list_tokenize[index_word] = "اتورایز"
                        continue
                    case "storage":
                        list_tokenize[index_word] = "استورج"
                        continue
                    case "ionic":
                        list_tokenize[index_word] = "ایونیک"
                        continue
                    case "application":
                        list_tokenize[index_word] = "اپلیکیشن"
                        continue
                    case "sass":
                        list_tokenize[index_word] = "سس"
                        continue
                    case "ui":
                        list_tokenize[index_word] = "یو ای"
                        continue
                    case "angular":
                        list_tokenize[index_word] = "انگولار"
                        continue
                    case "vue":
                        list_tokenize[index_word] = "ویو"
                        continue
                    case "react":
                        list_tokenize[index_word] = "ریکت"
                        continue
                    case "js":
                        list_tokenize[index_word] = "جاوااسکریپت"
                        continue
                    case "component":
                        list_tokenize[index_word] = "کامپوننت"
                        continue
                    case "element":
                        list_tokenize[index_word] = "المنت"
                        continue
                    case "shadow":
                        list_tokenize[index_word] = "سایه"
                        continue
                    case "dom":
                        list_tokenize[index_word] = "دام"
                        continue
                    case "progressive":
                        list_tokenize[index_word] = "پروگرسیو"
                        continue
                    case "app":
                        list_tokenize[index_word] = "اپلیکیشن"
                        continue
                    case "apps":
                        list_tokenize[index_word] = "اپلیکیشن"
                        continue
                    case "animation":
                        list_tokenize[index_word] = "انیمیشن"
                        continue
                    case "load":
                        list_tokenize[index_word] = "لود"
                        continue
                    case "java":
                        list_tokenize[index_word] = "جاوا"
                        continue
                    case "intent":
                        list_tokenize[index_word] = "اینتنت"
                        continue
                    case "handler":
                        list_tokenize[index_word] = "هندلر"
                        continue
                    case "picasso":
                        list_tokenize[index_word] = "پیکاسو"
                        continue
                    case "manager":
                        list_tokenize[index_word] = "منیجر"
                        continue
                    case "screen":
                        list_tokenize[index_word] = "اسکرین"
                        continue
                    case "notification":
                        list_tokenize[index_word] = "نتیفیکیشن"
                        continue
                    case "push":
                        list_tokenize[index_word] = "پوش"
                        continue
                    case "insert":
                        list_tokenize[index_word] = "اینزرت"
                        continue
                    case "update":
                        list_tokenize[index_word] = "اپدیت"
                        continue
                    case "delete":
                        list_tokenize[index_word] = "دیلیت"
                        continue
                    case "firebase":
                        list_tokenize[index_word] = "فایربیس"
                        continue
                    case "lottie":
                        list_tokenize[index_word] = "لاتی"
                        continue
                    case "json":
                        list_tokenize[index_word] = "جبسون"
                        continue
                    case "performance":
                        list_tokenize[index_word] = "پرفورمنس"
                        continue
                    case "backend":
                        list_tokenize[index_word] = "بک اند"
                        continue
                    case "php":
                        list_tokenize[index_word] = "پی اچ پی"
                        continue
                    case "navigation":
                        list_tokenize[index_word] = "نویگیشن"
                        continue
                    case "drawer":
                        list_tokenize[index_word] = "دراور"
                        continue
                    case "crash":
                        list_tokenize[index_word] = "کراش"
                        continue
                    case "reporting":
                        list_tokenize[index_word] = "ریپورتینگ"
                        continue
            elif lang_word == "fa":
                match list_tokenize[index_word]:
                    case "شارپ":
                        list_tokenize[index_word] = "سی شارپ"
                        list_tokenize[index_word - 1] = ""
                        continue
                    case "آسانی":
                        list_tokenize[index_word] = "آسان"
                        continue
                    case "یکی":
                        list_tokenize[index_word] = "یک"
                        continue
                    case "روی":
                        list_tokenize[index_word] = "رو"
                        continue
                    case "پشتیبانی":
                        list_tokenize[index_word] = "پشتیبان"
                        continue
                    case "متقابلا":
                        list_tokenize[index_word] = "تقابل"
                        continue
                    case "موارد":
                        list_tokenize[index_word] = "مورد"
                        continue
                    case "کاربری":
                        list_tokenize[index_word] = "کاربر"
                        continue
                    case "میتوانیم":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "میدهد":
                        list_tokenize[index_word] = "ده"
                        continue
                    case "کند":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "بردارید":
                        list_tokenize[index_word] = "بردار"
                        continue
                    case "وردپرسی":
                        list_tokenize[index_word] = "وردپرس"
                        continue
                    case "قدرتمند":
                        list_tokenize[index_word] = "قدرت"
                        continue
                    case "آموزشی":
                        list_tokenize[index_word] = "آموزش"
                        continue
                    case "بیشتری":
                        list_tokenize[index_word] = "بیشتر"
                        continue
                    case "داشته":
                        list_tokenize[index_word] = "دارد"
                        continue
                    case "زبانی":
                        list_tokenize[index_word] = "زبان"
                        continue
                    case "توانایی":
                        list_tokenize[index_word] = "توان"
                        continue
                    case "گرفته":
                        list_tokenize[index_word] = "گرفت"
                        continue
                    case "چندسکویی":
                        list_tokenize[index_word] = "چندسکو"
                        continue
                    case "دارای":
                        list_tokenize[index_word] = "دارا"
                        continue
                    case "خریداری":
                        list_tokenize[index_word] = "خریدار"
                        continue
                    case "مقدماتی":
                        list_tokenize[index_word] = "مقدمه"
                        continue
                    case "پیشرفته":
                        list_tokenize[index_word] = "پیشرفت"
                        continue
                    case "داده":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "کاملا":
                        list_tokenize[index_word] = "کامل"
                        continue
                    case "حافظپروژه":
                        list_tokenize[index_word] = ["پروژه"] + ["حافظ"]
                        continue
                    case "دوم":
                        list_tokenize[index_word] = "دو"
                        continue
                    case "دیدنی":
                        list_tokenize[index_word] = "دیدن"
                        continue
                    case "اطلاعاتی":
                        list_tokenize[index_word] = "اطلاع"
                        continue
                    case "سازی":
                        list_tokenize[index_word] = "ساخت"
                        continue
                    case "خبری":
                        list_tokenize[index_word] = "خبر"
                        continue
                    case "معرفی":
                        list_tokenize[index_word] = "معرف"
                        continue
                    case "اتمام":
                        list_tokenize[index_word] = "تمام"
                        continue
                    case "رسیده":
                        list_tokenize[index_word] = "رسید"
                        continue
                    case "شده":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "بومی":
                        list_tokenize[index_word] = "بوم"
                        continue
                    case "محدودیت":
                        list_tokenize[index_word] = "محدود"
                        continue
                    case "میتوانید":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "کدنویسی":
                        list_tokenize[index_word] = "کدنویس"
                        continue
                    case "خروجی":
                        list_tokenize[index_word] = "خروج"
                        continue
                    case "میکنیم":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "آشنایی":
                        list_tokenize[index_word] = "آشنا"
                        continue
                    case "عملی":
                        list_tokenize[index_word] = "عمل"
                        continue
                    case "خوبی":
                        list_tokenize[index_word] = "خوب"
                        continue
                    case "میباشد":
                        list_tokenize[index_word] = "بود"
                        continue
                    case "اساسی":
                        list_tokenize[index_word] = "اساس"
                        continue
                    case "محدودیت":
                        list_tokenize[index_word] = "محدود"
                        continue
                    case "سازگاری":
                        list_tokenize[index_word] = "سازگار"
                        continue
                    case "قدیمی":
                        list_tokenize[index_word] = "قدیم"
                        continue
                    case "خطی":
                        list_tokenize[index_word] = "خط"
                        continue
                    case "نوشته":
                        list_tokenize[index_word] = "نوشت"
                        continue
                    case "کارآمدی":
                        list_tokenize[index_word] = "کارامد"
                        continue
                    case "کارامدی":
                        list_tokenize[index_word] = "کارامد"
                        continue
                    case "اضافی":
                        list_tokenize[index_word] = "اضاف"
                        continue
                    case "تمامی":
                        list_tokenize[index_word] = "تمام"
                        continue
                    case "امکانات":
                        list_tokenize[index_word] = "امکان"
                        continue
                    case "آشنایی":
                        list_tokenize[index_word] = "اشنا"
                        continue
                    case "اشنایی":
                        list_tokenize[index_word] = "اشنا"
                        continue
                    case "بیشتر":
                        list_tokenize[index_word] = "بیش"
                        continue
                    case "بیشترین":
                        list_tokenize[index_word] = "بیش"
                        continue
                    case "ویدیو":
                        list_tokenize[index_word] = "ویدئو"
                        continue
                    case "مقدمات":
                        list_tokenize[index_word] = "مقدمه"
                        continue
                    case "میتو":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "ارائه":
                        list_tokenize[index_word] = "ارایه"
                        continue
                    case "میکند":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "پیشین":
                        list_tokenize[index_word] = "پیش"
                        continue
                    case "برداشته":
                        list_tokenize[index_word] = "برداشت"
                        continue
                    case "دیگری":
                        list_tokenize[index_word] = "دیگر"
                        continue
                    case "شخصی":
                        list_tokenize[index_word] = "شخص"
                        continue
                    case "امروزه":
                        list_tokenize[index_word] = "امروز"
                        continue
                    case "معنیست":
                        list_tokenize[index_word] = "معنی"
                        continue
                    case "دهندگان":
                        list_tokenize[index_word] = "دهنده"
                        continue
                    case "کارکرده":
                        list_tokenize[index_word] = "کارکرد"
                        continue
                    case "مفاهیم":
                        list_tokenize[index_word] = "مفهوم"
                        continue
                    case "والبته":
                        list_tokenize[index_word] = "البته"
                        continue
                    case "میشه":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "کارا":
                        list_tokenize[index_word] = "کار"
                        continue
                    case "کارا":
                        list_tokenize[index_word] = ["هم"] + ["با"]
                        continue
                    case "آخرین":
                        list_tokenize[index_word] = "اخر"
                        continue
                    case "اخرین":
                        list_tokenize[index_word] = "اخر"
                        continue
                    case "گزروندن":
                        list_tokenize[index_word] = "گذشت"
                        continue
                    case "مراحل":
                        list_tokenize[index_word] = "مرحله"
                        continue
                    case "اصلی":
                        list_tokenize[index_word] = "اصل"
                        continue
                    case "مون":
                        list_tokenize[index_word] = "ما"
                        continue
                    case "میش":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "رو":
                        list_tokenize[index_word] = "را"
                        continue
                    case "باقابلیت":
                        list_tokenize[index_word] = ["قابلیت"] + ["با"]
                        continue
                    case "هرکابر":
                        list_tokenize[index_word] = "کاربر"
                        continue
                    case "کاربرانبعد":
                        list_tokenize[index_word] = ["بعد"] + ["کاربران"]
                        continue
                    case "میتونید":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "خودتون":
                        list_tokenize[index_word] = "خودتان"
                        continue
                    case "بسازیدبیاید":
                        list_tokenize[index_word] = ["یافت"] + ["ساخت"]
                        continue
                    case "کنیمپیشنیاز":
                        list_tokenize[index_word] = ["پیشنیاز"] + ["کرد"]
                        continue
                    case "بصری":
                        list_tokenize[index_word] = "بصر"
                        continue
                    case "کرده":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "میکنند":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "زمانی":
                        list_tokenize[index_word] = "زمان"
                        continue
                    case "جدیدی":
                        list_tokenize[index_word] = "جدید"
                        continue
                    case "میشود":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "راحتی":
                        list_tokenize[index_word] = "راحت"
                        continue
                    case "منتقل":
                        list_tokenize[index_word] = "نقل"
                        continue
                    case "متفاوت":
                        list_tokenize[index_word] = "تفاوت"
                        continue
                    case "تعدادی":
                        list_tokenize[index_word] = "تعداد"
                        continue
                    case "آنها":
                        list_tokenize[index_word] = "ان"
                        continue
                    case "انها":
                        list_tokenize[index_word] = "ان"
                        continue
                    case "کنیمدوستان":
                        list_tokenize[index_word] = ["دوست"] + ["کرد"]
                        continue
                    case "عزیزی":
                        list_tokenize[index_word] = "عزیز"
                        continue
                    case "نویس":
                        list_tokenize[index_word] = "نوشت"
                        continue
                    case "بودبرای":
                        list_tokenize[index_word] = ["برای"] + ["بود"]
                        continue
                    case "هااستفاده":
                        list_tokenize[index_word] = "استفاده"
                        continue
                    case "موضوعات":
                        list_tokenize[index_word] = "موضوع"
                        continue
                    case "گفته":
                        list_tokenize[index_word] = "گفت"
                        continue
                    case "بسیاری":
                        list_tokenize[index_word] = "بسیار"
                        continue
                    case "گرایی":
                        list_tokenize[index_word] = "گرا"
                        continue
                    case "امروزی":
                        list_tokenize[index_word] = "امروز"
                        continue
                    case "کردن":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "میتوانند":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "داشتن":
                        list_tokenize[index_word] = "داشت"
                        continue
                    case "کافیه":
                        list_tokenize[index_word] = "کافی"
                        continue
                    case "دلیلی":
                        list_tokenize[index_word] = "دلیل"
                        continue
                    case "میتونه":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "باشه":
                        list_tokenize[index_word] = "بود"
                        continue
                    case "ایننت":
                        list_tokenize[index_word] = "اینترنت"
                        continue
                    case "میبندند":
                        list_tokenize[index_word] = "دید"
                        continue
                    case "زیادی":
                        list_tokenize[index_word] = "زیاد"
                        continue
                    case "میزنند":
                        list_tokenize[index_word] = "زد"
                        continue
                    case "میگیرد":
                        list_tokenize[index_word] = "گرفت"
                        continue
                    case "ظاهری":
                        list_tokenize[index_word] = "ظاهر"
                        continue
                    case "دوستان":
                        list_tokenize[index_word] = "دوست"
                        continue
                    case "نوشتن":
                        list_tokenize[index_word] = "نوشت"
                        continue
                    case "قبلی":
                        list_tokenize[index_word] = "قبل"
                        continue
                    case "برقراری":
                        list_tokenize[index_word] = "برقرار"
                        continue
                    case "حیاتی":
                        list_tokenize[index_word] = "حیات"
                        continue
                    case "باهم":
                        list_tokenize[index_word] = ["هم"] + ["با"]
                        continue
                    case "دفچه":
                        list_tokenize[index_word] = "دفترچه"
                        continue
                    case "اپلیکیشنی":
                        list_tokenize[index_word] = "اپلیکیشن"
                        continue
                    case "وانرژی":
                        list_tokenize[index_word] = "انرژی"
                        continue
                    case "تاسیس":
                        list_tokenize[index_word] = "تأسیس"
                        continue
                    case "داده":
                        list_tokenize[index_word] = "داده" if list_tokenize[index_word - 1] == "پایگاه" else "داد"
                        continue
                    case "اولیه":
                        list_tokenize[index_word] = "اول"
                        continue
                    case "بخشی":
                        list_tokenize[index_word] = "بخش"
                        continue
                    case "طراحی":
                        list_tokenize[index_word] = "طرح"
                        continue
                    case "بهمراه":
                        list_tokenize[index_word] = ["همراه"] + ["به"]
                        continue
                    case "زیبایی":
                        list_tokenize[index_word] = "زیبا"
                        continue
                    case "خاصی":
                        list_tokenize[index_word] = "خاص"
                        continue
                    case "طراح":
                        list_tokenize[index_word] = "طرح"
                        continue
                    case "تکراری":
                        list_tokenize[index_word] = "تکرار"
                        continue
                    case "اینها":
                        list_tokenize[index_word] = "این"
                        continue
                    case "قبلا":
                        list_tokenize[index_word] = "قبل"
                        continue
                    case "شایانی":
                        list_tokenize[index_word] = "شایان"
                        continue
                    case "چندانی":
                        list_tokenize[index_word] = "چندان"
                        continue
                    case "کاملی":
                        list_tokenize[index_word] = "کامل"
                        continue
                    case "بالایی":
                        list_tokenize[index_word] = "بالا"
                        continue
                    case "میخونند":
                        list_tokenize[index_word] = "خواند"
                        continue
                    case "انتخابی":
                        list_tokenize[index_word] = "انتخاب"
                        continue
                    case "براش":
                        list_tokenize[index_word] = "برای"
                        continue
                    case "هارو":
                        list_tokenize[index_word] = "را"
                        continue
                    case "رمزنگاری":
                        list_tokenize[index_word] = "رمزنگار"
                        continue
                    case "تقریبا":
                        list_tokenize[index_word] = "تقریب"
                        continue
                    case "کارکردن":
                        list_tokenize[index_word] = ["کرد"] + ["کار"]
                        continue
                    case "بافایل":
                        list_tokenize[index_word] = ["فایل"] + ["با"]
                        continue
                    case "تقریبا":
                        list_tokenize[index_word] = "تقریب"
                        continue
                    case "اختیارتون":
                        list_tokenize[index_word] = "اختیار"
                        continue
                    case "بدم":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "مقدماتیحاصل":
                        list_tokenize[index_word] = ["حاصل"] + ["مقدماتی"]
                        continue
                    case "دیج":
                        list_tokenize[index_word] = ["حاصل"] + ["مقدماتی"]
                        continue
                    case "تنهایی":
                        list_tokenize[index_word] = "تنهایی"
                        continue
                    case "اموزشی":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "کشویی":
                        list_tokenize[index_word] = "کشو"
                        continue
                    case "میخواهید":
                        list_tokenize[index_word] = "خواست"
                        continue
                    case "ایننتی":
                        list_tokenize[index_word] = "اینترنت"
                        continue
                    case "کلیه":
                        list_tokenize[index_word] = "کل"
                        continue
                    case "مباحث":
                        list_tokenize[index_word] = "مبحث"
                        continue
                    case "برگزاری":
                        list_tokenize[index_word] = "برگزار"
                        continue
                    case "هستی":
                        list_tokenize[index_word] = "است"
                        continue
                    case "نمیدونی":
                        list_tokenize[index_word] = "دانست"
                        continue
                    case "ازی":
                        list_tokenize[index_word] = ["این"] + ["از"]
                        continue
                    case "خودت":
                        list_tokenize[index_word] = "خود"
                        continue
                    case "میخوای":
                        list_tokenize[index_word] = "خواست"
                        continue
                    case "وبه":
                        list_tokenize[index_word] = "به"
                        continue
                    case "ایرانی":
                        list_tokenize[index_word] = "ایران"
                        continue
                    case "یادگیری":
                        list_tokenize[index_word] = "یادگرفت"
                        continue
                    case "بشی":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "نمایید":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "اپلیکیششنی":
                        list_tokenize[index_word] = "اپلیکیشن"
                        continue
                    case "زبانهاتصال":
                        list_tokenize[index_word] = ["اتصال"] + ["زبان"]
                        continue
                    case "سرورکتابخانه":
                        list_tokenize[index_word] = ["سرور"] + ["کتابخانه"]
                        continue
                    case "معمار":
                        list_tokenize[index_word] = "معمار"
                        continue
                    case "گوگلاموزش":
                        list_tokenize[index_word] = ["اموزش"] + ["گوگل"]
                        continue
                    case "انتشار":
                        list_tokenize[index_word] = "نشر"
                        continue
                    case "بازاراموزش":
                        list_tokenize[index_word] = ["اموزش"] + ["بازار"]
                        continue
                    case "مایکتاموزش":
                        list_tokenize[index_word] = ["اموزش"] + ["مایکت"]
                        continue
                    case "پلیاموزش":
                        list_tokenize[index_word] = ["اموزش"] + ["پلی"]
                        continue
                    case "هاامن":
                        list_tokenize[index_word] = "امن"
                        continue
                    case "انتشارراه":
                        list_tokenize[index_word] = ["راه"] + ["انتشار"]
                        continue
                    case "خطای":
                        list_tokenize[index_word] = "خطا"
                        continue
                    case "بیاموزیم":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "زیباساخت":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "اموزیم":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "کاردویواستفاده":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "تایمرایجاد":
                        list_tokenize[index_word] = ["ایجاد"] + ["تایمر"]
                        continue
                    case "زیباایجاد":
                        list_tokenize[index_word] = ["ایجاد"] + ["زیبا"]
                        continue
                    case "زیباساخت":
                        list_tokenize[index_word] = ["ساخت"] + ["زیبا"]
                        continue
                    case "دیتابیسی":
                        list_tokenize[index_word] = "دیتابیس"
                        continue
                    case "تلاشمو":
                        list_tokenize[index_word] = "تلاش"
                        continue
                    case "شما":
                        list_tokenize[index_word] = "تلاش"
                        continue
                    case "بتونید":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "بندازید":
                        list_tokenize[index_word] = "انداخت"
                        continue
                    case "امیدوارم":
                        list_tokenize[index_word] = "امیدوار"
                        continue
                    case "عزیزاین":
                        list_tokenize[index_word] = ["این"] + ["عزیز"]
                        continue
                    case "دوستانی":
                        list_tokenize[index_word] = "دوست"
                        continue
                    case "سوالاشونو":
                        list_tokenize[index_word] = "سوال"
                        continue
                    case "پرسشو":
                        list_tokenize[index_word] = "پرسش"
                        continue
                    case "کنن":
                        list_tokenize[index_word] = "پرسش"
                        continue
                    case "بهشون":
                        list_tokenize[index_word] = "به"
                        continue
                    case "پیداکرده":
                        list_tokenize[index_word] = "پیدا"
                        continue
                    case "محبوبیت":
                        list_tokenize[index_word] = "حب"
                        continue
                    case "میکنم":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "خودمون":
                        list_tokenize[index_word] = "خود"
                        continue
                    case "مید":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "سروره":
                        list_tokenize[index_word] = "سرور"
                        continue
                    case "کلی":
                        list_tokenize[index_word] = "کل"
                        continue
                    case "رااز":
                        list_tokenize[index_word] = "کل"
                        continue
                    case "میدهند":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "محصولات":
                        list_tokenize[index_word] = "محصول"
                        continue
                    case "خدمات":
                        list_tokenize[index_word] = "خدمت"
                        continue
                    case "میشوددر":
                        list_tokenize[index_word] = "خدمت"
                        continue
                    case "کنیمبا":
                        list_tokenize[index_word] = "کنیم"
                        continue
                    case "میدهیمو":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "میاییم":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "میخواهیم":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "میپردازیم":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "توضیحات":
                        list_tokenize[index_word] = "توضیح"
                        continue
                    case "میده":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "اپلیکیشنو":
                        list_tokenize[index_word] = "اپلیکیشن"
                        continue
                    case "دادهو":
                        list_tokenize[index_word] = "داده"
                        continue
                    case "پرداختخب":
                        list_tokenize[index_word] = "پرداخت"
                        continue
                    case "سالی":
                        list_tokenize[index_word] = "سال"
                        continue
                    case "فلا":
                        list_tokenize[index_word] = "فلاتر"
                        continue
                    case "نویسان":
                        list_tokenize[index_word] = "نوشت"
                        continue
                    case "بتونن":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "اومدیم":
                        list_tokenize[index_word] = "امد"
                        continue
                    case "میخوان":
                        list_tokenize[index_word] = "خواست"
                        continue
                    case "بشن":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "کامله":
                        list_tokenize[index_word] = "کامل"
                        continue
                    case "میانپوشش":
                        list_tokenize[index_word] = "کامل"
                        continue
                    case "مید":
                        list_tokenize[index_word] = "کامل"
                        continue
                    case "بشه":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "سلامتی":
                        list_tokenize[index_word] = "سلامت"
                        continue
                    case "هوایی":
                        list_tokenize[index_word] = "هوا"
                        continue
                    case "هوای":
                        list_tokenize[index_word] = "هوا"
                        continue
                    case "بافایر":
                        list_tokenize[index_word] = "هوا"
                        continue
                    case "بیسبعد":
                        list_tokenize[index_word] = "هوا"
                        continue
                    case "گذروندن":
                        list_tokenize[index_word] = "هوا"
                        continue
                    case "بشید":
                        list_tokenize[index_word] = "هوا"
                        continue
                    case "قویبشه":
                        list_tokenize[index_word] = "هوا"
                        continue
                    case "دستورات":
                        list_tokenize[index_word] = "دستور"
                        continue
                    case "دهنده":
                        list_tokenize[index_word] = "دستور"
                        continue
                    case "نیستید":
                        list_tokenize[index_word] = "است"
                        continue
                    case "شماست":
                        list_tokenize[index_word] = "شما"
                        continue
                    case "میگیرم":
                        list_tokenize[index_word] = "گرفت"
                        continue
                    case "پیشرفتهطراحی":
                        list_tokenize[index_word] = "گرفت"
                        continue
                    case "دوربیننقشه":
                        list_tokenize[index_word] = "گرفت"
                        continue
                    case "تنظیمات":
                        list_tokenize[index_word] = "تنظیم"
                        continue
                    case "پیرفرنس":
                        list_tokenize[index_word] = "تنظیم"
                        continue
                    case "ارتباطات":
                        list_tokenize[index_word] = "ارتباط"
                        continue
                    case "هاضبط":
                        list_tokenize[index_word] = "ضبط"
                        continue
                    case "رویدالگو":
                        list_tokenize[index_word] = "ضبط"
                        continue
                    case "حرکات":
                        list_tokenize[index_word] = "حرکت"
                        continue
                    case "رویدتبدیل":
                        list_tokenize[index_word] = "حرکت"
                        continue
                    case "لرندر":
                        list_tokenize[index_word] = "لرن"
                        continue
                    case "معمولا":
                        list_tokenize[index_word] = "معمول"
                        continue
                    case "پردرامد":
                        list_tokenize[index_word] = "معمول"
                        continue
                    case "اموزید":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "ریسپانسیوکار":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "پرداختساخت":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "کاربریارتباط":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "خریدطراحی":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "اختصاصیساخت":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "اختصاصیطراحی":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "صفحه":
                        list_tokenize[index_word] = "اموزش"
                        continue
                    case "همکاری":
                        list_tokenize[index_word] = "همکار"
                        continue
                    case "جلسات":
                        list_tokenize[index_word] = "جلسه"
                        continue
                    case "میطلبد":
                        list_tokenize[index_word] = "جلسه"
                        continue
                    case "رقبا":
                        list_tokenize[index_word] = "جلسه"
                        continue
                    case "شیء":
                        list_tokenize[index_word] = "شی"
                        continue
                    case "ازمزیت":
                        list_tokenize[index_word] = "مزیت"
                        continue
                    case "لرنی":
                        list_tokenize[index_word] = "لرن"
                        continue
                    case "سرویساز":
                        list_tokenize[index_word] = "لرن"
                        continue
                    case "استنفاده":
                        list_tokenize[index_word] = "استفاده"
                        continue
                    case "درپروژه":
                        list_tokenize[index_word] = "پروژه"
                        continue
                    case "کاربردیو":
                        list_tokenize[index_word] = "کاربرد"
                        continue
                    case "دیدن":
                        list_tokenize[index_word] = "دید"
                        continue
                    case "محم":
                        list_tokenize[index_word] = "مهم"
                        continue
                    case "هاساخت":
                        list_tokenize[index_word] = "ساخت"
                        continue
                    case "بودن":
                        list_tokenize[index_word] = "است"
                        continue
                    case "ایندوره":
                        list_tokenize[index_word] = "است"
                        continue
                    case "دهیمو":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "نظرات":
                        list_tokenize[index_word] = "نظر"
                        continue
                    case "عزیر":
                        list_tokenize[index_word] = "عزیز"
                        continue
                    case "عزیزانی":
                        list_tokenize[index_word] = "عزیز"
                        continue
                    case "دنیای":
                        list_tokenize[index_word] = "دنیا"
                        continue
                    case "کتابی":
                        list_tokenize[index_word] = "کتاب"
                        continue
                    case "خارجی":
                        list_tokenize[index_word] = "خارج"
                        continue
                    case "داخلی":
                        list_tokenize[index_word] = "داخل"
                        continue
                    case "کاربرارسال":
                        list_tokenize[index_word] = "داخل"
                        continue
                    case "کاربرطراحی":
                        list_tokenize[index_word] = "داخل"
                        continue
                    case "کلیمحدودیت":
                        list_tokenize[index_word] = "داخل"
                        continue
                    case "کاربرانخرید":
                        list_tokenize[index_word] = "داخل"
                        continue
                    case "ماهانه":
                        list_tokenize[index_word] = "ماه"
                        continue
                    case "پالاضافه":
                        list_tokenize[index_word] = "ماه"
                        continue
                    case "کامنتاضافه":
                        list_tokenize[index_word] = "ماه"
                        continue
                    case "پیچیدگی":
                        list_tokenize[index_word] = "پیچیده"
                        continue
                    case "کسانی":
                        list_tokenize[index_word] = "کس"
                        continue
                    case "بهمعماری":
                        list_tokenize[index_word] = "معمار"
                        continue
                    case "معماری":
                        list_tokenize[index_word] = "معمار"
                        continue
                    case "بالام":
                        list_tokenize[index_word] = "بالا"
                        continue
                    case "دورهکاملا":
                        list_tokenize[index_word] = "بالا"
                        continue
                    case "مطالبی":
                        list_tokenize[index_word] = "مطالب"
                        continue
                    case "امادر":
                        list_tokenize[index_word] = "مطالب"
                        continue
                    case "بهشدت":
                        list_tokenize[index_word] = "مطالب"
                        continue
                    case "فراموشی":
                        list_tokenize[index_word] = "فراموش"
                        continue
                    case "اتفاقی":
                        list_tokenize[index_word] = "اتفاق"
                        continue
                    case "معروفیت":
                        list_tokenize[index_word] = "معروف"
                        continue
                    case "دموی":
                        list_tokenize[index_word] = "دمو"
                        continue
                    case "مشاهد":
                        list_tokenize[index_word] = "شاهد"
                        continue
                    case "حدودی":
                        list_tokenize[index_word] = "حدود"
                        continue
                    case "نمیخواهیم":
                        list_tokenize[index_word] = "خواست"
                        continue
                    case "اپلیکیشناست":
                        list_tokenize[index_word] = "خواست"
                        continue
                    case "دنیای":
                        list_tokenize[index_word] = "دنیا"
                        continue
                    case "ویژهخود":
                        list_tokenize[index_word] = "دنیا"
                        continue
                    case "کنونی":
                        list_tokenize[index_word] = "کنون"
                        continue
                    case "امارو":
                        list_tokenize[index_word] = "امار"
                        continue
                    case "نیزبرای":
                        list_tokenize[index_word] = "امار"
                        continue
                    case "اطلاعات":
                        list_tokenize[index_word] = "اطلاع"
                        continue
                    case "وابستگی":
                        list_tokenize[index_word] = "وابسته"
                        continue
                    case "ازه":
                        list_tokenize[index_word] = "از"
                        continue
                    case "چندیدن":
                        list_tokenize[index_word] = "چند"
                        continue
                    case "بسیارکاهش":
                        list_tokenize[index_word] = "بسیار"
                        continue
                    case "میابد":
                        list_tokenize[index_word] = "امد"
                        continue
                    case "میدهید":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "تغییرات":
                        list_tokenize[index_word] = "تغییر"
                        continue
                    case "میتوانیدکار":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "چهزبانی":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "هوشمندانه":
                        list_tokenize[index_word] = "هوش"
                        continue
                    case "چیزی":
                        list_tokenize[index_word] = "چیز"
                        continue
                    case "بهوجود":
                        list_tokenize[index_word] = "وجود"
                        continue
                    case "اورید":
                        list_tokenize[index_word] = "اورد"
                        continue
                    case "عوامل":
                        list_tokenize[index_word] = "عامل"
                        continue
                    case "ماجراست":
                        list_tokenize[index_word] = "ماجراست"
                        continue
                    case "بهمرور":
                        list_tokenize[index_word] = "مرور"
                        continue
                    case "جداگانه":
                        list_tokenize[index_word] = "جدا"
                        continue
                    case "دچارتغییرات":
                        list_tokenize[index_word] = "دچارتغییر"
                        continue
                    case "درشتی":
                        list_tokenize[index_word] = "درشت"
                        continue
                    case "جذاب":
                        list_tokenize[index_word] = "جذب"
                        continue
                    case "شدن":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "گردیده":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "اصولی":
                        list_tokenize[index_word] = "اصل"
                        continue
                    case "انواع":
                        list_tokenize[index_word] = "نوع"
                        continue
                    case "قوانین":
                        list_tokenize[index_word] = "قانون"
                        continue
                    case "روانشناسی":
                        list_tokenize[index_word] = "روانشناس"
                        continue
                    case "میرسیم":
                        list_tokenize[index_word] = "پرسید"
                        continue
                    case "هکری":
                        list_tokenize[index_word] = "هکر"
                        continue
                    case "توی":
                        list_tokenize[index_word] = "داخل"
                        continue
                    case "بش":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "کابردیه":
                        list_tokenize[index_word] = "کاربرد"
                        continue
                    case "هرکس":
                        list_tokenize[index_word] = "کس"
                        continue
                    case "بتونه":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "کنه":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "بدمبا":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "نکات":
                        list_tokenize[index_word] = "نکته"
                        continue
                    case "نمیشه":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "میکنید":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "میخورید":
                        list_tokenize[index_word] = "خورد"
                        continue
                    case "میایم":
                        list_tokenize[index_word] = "امد"
                        continue
                    case "میگ":
                        list_tokenize[index_word] = "گفت"
                        continue
                    case "کنیددوستان":
                        list_tokenize[index_word] = "گفت"
                        continue
                    case "ازتون":
                        list_tokenize[index_word] = "گفت"
                        continue
                    case "خدایی":
                        list_tokenize[index_word] = "خدا"
                        continue
                    case "نکرده":
                        list_tokenize[index_word] = "کرد"
                        continue
                    case "چونکه":
                        list_tokenize[index_word] = "چون"
                        continue
                    case "براتون":
                        list_tokenize[index_word] = "چون"
                        continue
                    case "بتون":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "شالله":
                        list_tokenize[index_word] = "انشالله"
                        list_tokenize[index_word - 1] = ""
                        continue
                    case "مید":
                        list_tokenize[index_word] = "داد"
                        continue
                    case "معلومات":
                        list_tokenize[index_word] = "علم"
                        continue
                    case "حالته":
                        list_tokenize[index_word] = "حالت"
                        continue
                    case "نشده":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "هرکدوم":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "نشون":
                        list_tokenize[index_word] = "نشان"
                        continue
                    case "منوی":
                        list_tokenize[index_word] = "منو"
                        continue
                    case "گرده":
                        list_tokenize[index_word] = "شد"
                        continue
                    case "دوم":
                        list_tokenize[index_word] = "دو"
                        continue
                    case "سوم":
                        list_tokenize[index_word] = "سه"
                        continue
                    case "پنجم":
                        list_tokenize[index_word] = "پنج"
                        continue
                    case "چهارم":
                        list_tokenize[index_word] = "چهار"
                        continue
                    case "ششم":
                        list_tokenize[index_word] = "شش"
                        continue
                    case "هفتم":
                        list_tokenize[index_word] = "هفت"
                        continue
                    case "هشتم":
                        list_tokenize[index_word] = "هشت"
                        continue
                    case "نهم":
                        list_tokenize[index_word] = "نه"
                        continue
                    case "دهم":
                        list_tokenize[index_word] = "ده"
                        continue
                    case "یازدهم":
                        list_tokenize[index_word] = "یازده"
                        continue
                    case "دوازدهم":
                        list_tokenize[index_word] = "دوازده"
                        continue
                    case "درون":
                        list_tokenize[index_word] = "داخل"
                        continue
                    case "بسته":
                        list_tokenize[index_word] = "بست"
                        continue
                    case "خودش":
                        list_tokenize[index_word] = "خوداو"
                        continue
                    case "همانند":
                        list_tokenize[index_word] = "مانند"
                        continue
                    case "شبیه":
                        list_tokenize[index_word] = "مانند"
                        continue
                    case "بتونه":
                        list_tokenize[index_word] = "توانست"
                        continue
                    case "سازنده":
                        list_tokenize[index_word] = "ساخت"
                        continue
                    case "دلایل":
                        list_tokenize[index_word] = "دلیل"
                        continue
                word_lem = self.__fa_lemmatizer.lemmatize(list_tokenize[index_word])
                word_stm = self.__fa_stemmer.stem(list_tokenize[index_word])
                if "#هست" == word_lem:
                    word_lem = "است"
                if re.match(".+#.+", word_lem):
                    list_tokenize[index_word] = word_lem.split("#")[0]
                elif word_stm == word_lem:
                    list_tokenize[index_word] = word_lem
                else:
                    list_tokenize[index_word] = word_lem
        for index_word in range(len(list_tokenize)):
            if type(list_tokenize[index_word]) is list:
                i0 = list_tokenize[index_word][0]
                more = list_tokenize[index_word][1:]
                list_tokenize[index_word] = i0
                list_tokenize += more
            # f = open(f"files/txts/words.txt", "a", encoding='utf-8')
            # f.write(f"{list_tokenize[index_word]}\n")
            # f.close()
        return list_tokenize

    def __split_combine_lang(self, text: str) -> str:
        res_reg_en = re.match("""^[a-z0-9]""", text)
        res_reg_fa = re.match("""^[\u0600-\u06FF\s]""", text)
        if res_reg_en:
            word_reg_en = re.match("""^[a-z0-9]+""", text)
            word = text[:word_reg_en.span()[1]] + " " + text[word_reg_en.span()[1]:]
            return word
        elif res_reg_fa:
            word_reg_fa = re.match("""^[\u0600-\u06FF\s]+""", text)
            word = text[:word_reg_fa.span()[1]] + " " + text[word_reg_fa.span()[1]:]
            return word
        else:
            return text

    def calculate_tf(self, list_of_words: list):
        """
        calculate tf from list of words
        :param list_of_words: [ word, ... ]
        :return:
        """
        dict_of_words = {}
        for i in list_of_words:
            dict_of_words[i] = 0
        for i in list_of_words:
            dict_of_words[i] += 1
        dict_tf = {}
        for i in dict_of_words:
            dict_tf[i] = math.log(dict_of_words[i]) + 1
        return dict_tf

    def create_list_tf(self, query: list, list_dict_title_and_plot: list, weight_tf_title: float = 1.0,
                       weight_tf_plot: float = 1.0, weight_tf_tags: float = 1.0):
        """
        create list of dict id and tf - title and tf of plot from list of words tokenize query and list of dict id and
        list tokenize title and list tokenize plot on titles and plot
        :param query: list[str] -> [ word-tokenize-query, ... ]
        :param list_dict_title_and_plot: list[dict] -> { word: { frequency: 0,
                                                         title: [ { index_row: index_word_in_sense, ... }, ... ],
                                                         plot : [ { index_row: index_word_in_sense, ... }, ... ], ... }
        :param weight_tf_title: float -> 1.0
        :param weight_tf_plot: float -> 1.0
        :param weight_tf_tags: float -> 1.0
        :return: [ { id: 0,
                     score: 0.0,
                     title: { word: tf, ... },
                     plot : { word: tf, ... }, } ... ]
        """
        list_tf = []
        list_id = []
        for i in list_dict_title_and_plot:
            for j in query:
                if j in i["title"] and i["id"] not in list_id:
                    list_id.append(i["id"])
                    list_tf.append({"id": i["id"], "title": self.calculate_tf(i["title"]), "plot": self.calculate_tf(i["plot"])})
        for i in list_tf:
            if weight_tf_title is not 1:
                for j in i["title"]:
                    i["title"][j] *= weight_tf_title
            if weight_tf_plot is not 1:
                for j in i["plot"]:
                    i["plot"][j] *= weight_tf_plot
            if weight_tf_tags is not 1:
                for j in i["tags"]:
                    i["tags"][j] *= weight_tf_tags
        return list_tf
