import jieba
import copy
import pymysql
from exam.models import Glossary

'''
class Glossary:
    def __init__(self):
        self.id = 0
        self.word = ""
        self.type  = ""
        self.sememes  = ""
    def __eq__(self, other):
        return self.id == other.id
'''

'''
three mode: 0 -- exact 精确匹配
            1 -- key word 关键词匹配
            2 -- sememe 义原即意义匹配
'''


STOP_FILE = "static/stop_word.txt"

def mark(mode, answer, inputs, key_words):
    if mode == 0:
         return exact_mark(key_words, inputs)
    elif mode == 1:
        #input and deal the answer in mode 1
        '''
        answer_list = get_word_list(answer)
        show_words(answer_list)             #show to teacher for choose
        '''
        #key_words = get_key_word()          #simulate input key word, choose word by random
        key_list = []
        for key_dict in key_words:
            key_list.extend(list(key_dict.keys()))

        inputs_list = get_word_list(inputs, key_list)
        return key_word_mark(key_words, inputs_list)

    elif mode == 2:

        #sememe_set = get_sememe_set(answer)
        #show_words(sememe_set)

        #show to the teacher for selecting
        '''
        concept_set = get_concept_set(answer)
        show_words(concept_list)
        '''

        #key_words = get_key_word()

        inputs_concept = get_concept_set(inputs)
        show_words(inputs_concept)
        return concept_mark(key_words, inputs_concept)
    else:
        print("mode error")
        return 0

# answer is a list, like [{"first": 1.0, "second": 0.5}]
def exact_mark(answer, inputs):
    if len(answer) > 0 and inputs in answer[0].keys():
        return answer[0][inputs], [(inputs, answer[0][inputs])]
    else:
        return 0, []

# answer is a phrase or a sentence
def get_word_list(string, word_list=[]):
    for word in word_list:
        jieba.add_word(word)
    cut_list = jieba.cut(string)
    #for cut in cut_list:
    #    print(cut)
    #stop_word = load_stop_word()
    word_list = [word for word in cut_list]  #[word for word in cut_list if word not in stop_word]
    return word_list

'''
def get_sememe_set(string):
    word_list = get_word_list(string)
    sememe_set = set()
    for word in word_list:
        concept_list = Glossary.objects.filter(word=word)
        for concept in concept_list:
            line_list = concept.sememes.split("\n")
            for line in range(2):
                sememe_list = line_list[line].split(",")
                sememe_set.union(set(sememe_list))
    return sememe_set
'''

def get_sememe_set(string):
    word_list = get_word_list(string)
    sememe_set = set()
    for word in word_list:
        concept_list = DB_connect(word)

        #can't find the word in the hownet, search by character
        if len(concept_list) == 0:
            print("00000")
            for character in word:
                concept_list.extend(DB_connect(character))

        for concept in concept_list:
            print(concept)
            line_list = concept.concept.split("\n")
            for line in range(2):
                sememe_list = line_list[line].split(",")
                sememe_set = sememe_set.union(set(sememe_list))
    return sememe_set


def get_concept_set(answer):
    word_list = get_word_list(answer)
    concept_set = set()
    for word in word_list:
        concept_set = concept_set.union(set(Glossary.objects.filter(word = word)))
    return concept_set

def load_stop_word():
    stop_file = open(STOP_FILE, "r", encoding='UTF-8')
    stop_word = []
    for line in stop_file:
        stop_word.append(line.strip())
    return stop_word

def show_words(words):
    print(words)

def key_word_mark(key_words, inputs_list):
    key_list = copy.deepcopy(key_words)
    percentage = 0.0
    detail_list = []
    for word in inputs_list:
        for key_dict in key_list:
            if word in key_dict.keys():
                percentage += key_dict[word]
                key_list.remove(key_dict)
                detail_list.append((word, key_dict[word]))
                break
    return percentage, detail_list

def concept_mark(key_concept_list, input_concepts):
    detail_list = []
    percentage = 0
    new_list = []
    for key_concept_dict in key_concept_list:
        new_dict = {}
        for key_concept in key_concept_dict.keys():
            glossary = Glossary.objects.get(id=int(key_concept))
            new_dict[glossary] = key_concept_dict[key_concept]
        new_list.append(new_dict)
    for input_concept in input_concepts:
        for concept_dict in new_list:
            for concept_key in concept_dict:
                if concept_key.concept.split() == input_concept.concept.split():
                    percentage += concept_dict[concept_key]
                    if concept_dict[concept_key] != 0:
                        detail_list.append((input_concept.word+'->'+concept_key.word, concept_dict[concept_key]))
                    concept_dict[concept_key] = 0
    return percentage, detail_list

'''
def get_key_word():
    key_words = []
    word_set = set()
    total_percentage = 0
    choose = "2"
    while choose != "3":
        max_percentage = 0
        key_word = {}
        choose = "2"
        while choose == "2":
            word = input("输入关键词：")
            while word in word_set:
                word = input("关键词已经存在，请重新输入：")
            percentage = input("输入分值比例：")
            while isinstance(percentage,float):
                percentage = input("输入不是数字，请重新输入：")
            percentage = float(percentage)
            key_word[word] = percentage
            word_set.add(word)
            if percentage > max_percentage:
                max_percentage = percentage
            choose =input("请输入对应的序号：1.输入其他关键词 2.输入并列关键词 3.结束输入：")
            while choose != "1" and choose != "2" and choose != "3":
                choose = input("请输入对应的序号：1.输入其他关键词 2.输入并列关键词 3.结束输入：")
        total_percentage += max_percentage
        if total_percentage > 1:
            print("输入分值已经超过100%，请从头开始重新输入关键词")
            key_words.clear()
            total_percentage = 0
            choose = "2"
        elif choose == "3" and total_percentage < 1:
            print("输入分数不够，请再输入其他关键词")
            choose = "2"
            key_words.append(key_word)
        else:
            key_words.append(key_word)
    return key_words
'''


def get_answer_list_from_txt(filename = "exact.txt"):
    lines = open(filename, "r", encoding='UTF-8').readlines()
    mode = int(lines[0].strip())
    answer = lines[1].strip()
    answer_list = []
    for num in range(2, len(lines)):
        items = lines[num].strip().split(" ")
        answer_dict = {}
        for item in items:
            item_list = item.split(":")
            answer_dict[item_list[0]] = float(item_list[1])
        answer_list.append(answer_dict)
    return mode, answer, answer_list

def DB_connect(word):
    #print(word)
    db = pymysql.connect("localhost", "root", "gqy", "onlinetest")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("select * from exam_glossary where word = \'%s\';"  % word)
    # 使用 fetchall() 方法获取数据.
    results = cursor.fetchall()
    concept_list = []
    for row in results:
        glossary = Glossary()
        glossary.id = row[0]
        glossary.word = row[1]
        glossary.type = row[2]
        glossary.concept = row[3]
        #print(row[3])
        concept_list.append(glossary)
    # 关闭数据库连接
    db.close()
    return concept_list

'''
def main():
    mode, answer, answer_list = get_answer_list_from_txt("../static/test/sememe.txt")
    print(mode, answer, answer_list)
    result = mark(mode, answer, "增加", answer_list)
    print(result)
'''
'''
test_set = set()
test_set.add("a")
test_set.add("b")
test_set.add("c")
test_set.add("d")
new_set = set()
new_set = new_set.union(test_set)
print("new_set size : %d" % len(new_set))
print(new_set)
'''