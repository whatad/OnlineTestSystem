import jieba
from numpy import *
from exam.langconv import *

tolerant = 3

def get_word_list(input_list):
    word_set = set(input_list)
    result = list(word_set)
    return result

def get_bag_list(word_list, sentence):
    word_list = list(word_list)
    word_len = len(word_list)
    sen_vec = [0] * word_len
    cut_list = jieba.cut(sentence)
    for word in cut_list:
        if word in word_list:
            index = word_list.index(word)
            sen_vec[index] += 1
    return sen_vec

def get_example_for_txt(file_name):
    train_file = open(file_name, "r", encoding='UTF-8')
    words = []
    sentence_list = []
    score_list = []
    data_mat = []
    for line in train_file.readlines():
        split_list = line.split('\t')
        sentence_list.append(split_list[0])
        score_list.append(int(split_list[1]))
        cut_list = jieba.cut(split_list[0])
        for word in cut_list:
            words.append(word)
    word_list = get_word_list(words)
    for sentence in sentence_list:
        sec_vec = get_bag_list(word_list, sentence)
        data_mat.append(sec_vec)
    return word_list, data_mat, score_list

def get_example_for_db(training_dict):
    words = []
    sentence_list = []
    score_list = []
    data_mat = []
    for key, value in training_dict.items():
        key = Converter('zh-hans').convert(key).encode('utf-8')
        sentence_list.append(key)
        score_list.append(int(value))
        cut_list = jieba.cut(key)
        for word in cut_list:
            words.append(word)
    word_list = get_word_list(words)
    for sentence in sentence_list:
        sec_vec = get_bag_list(word_list, sentence)
        data_mat.append(sec_vec)
    return word_list, data_mat, score_list



def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix)
    weights = zeros(n)
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001    #apha decreases with iteration, does not
            randIndex = int(random.uniform(0,len(dataIndex)))#go to 0 because of the constant
            #print(randIndex)
            h = sum(dataMatrix[randIndex]*weights)
            err = classLabels[randIndex] - h
            error = 0
            if err > 3:
                error = 1
            elif err < -3:
                error = -1
            #error = 20 if classLabels[randIndex] - h > 3 else 0
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def colicTest(training_dict, answer):
    #word_list, data_mat, score_list = get_example_for_txt('../static/test/training.txt')
    word_list, data_mat, score_list = get_example_for_db(training_dict)
    trainWeights = stocGradAscent1(array(data_mat), score_list, 10)
    '''
    print(word_list)
    print(trainWeights)
    '''
    #answer = "商鞅变法促进了封建经济的发展。"
    answer = Converter('zh-hans').convert(answer).encode('utf-8')
    vec = get_bag_list(word_list, answer)
    result = sum(trainWeights * vec)
    '''
    print(vec)
    print(result)
    '''
    return result


'''
def multiTest():
    numTests = 10
    errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest()
    print("after %d iterations the average error rate is: %f" % (numTests, errorSum / float(numTests)))
'''

#colicTest()