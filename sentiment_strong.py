# Words Sentiment as weights
import csv
from collections import defaultdict

import numpy as np
from processing import *
import csv

# создаем словарь слов из linis dictonary
def get_linis_dictionary():
    linis = defaultdict()
    with open("words_all_full_rating.csv", "r") as f:
        f.readline()
        reader = csv.reader(f, delimiter=';', quotechar='"')
        for row in reader:
            linis[row[0]] = abs(float(row[3])) #берем по модулю
    print(linis)
    return linis


linis_dict = get_linis_dictionary()


def get_sentiment_indices(text):
    # X - матрица n*1, где n -количество предложений в тексте для реферирования
    # Если удобнее, то можно просто использовать список вместо numpy-матрицы
    # Значения в матрицу следует подбирать на основе сантимент-словаря linis-crowd.org или на его аналоге
    # Желательно использовать словарь 2015 года с усреднением по разметчикам, но можете попробовать и
    # со словарём 2016 года разобраться.
    # Как формировать сантимент предложения - это основная задача для эксперимента.
    # Это может быть суммарный сантимент, усреднённый или что-то более сложное.
    # Также можно поэкспериментировать с объёмом автореферата - на данный момент это max (2, длина_текста div 4),
    # но можно, например, поставить пороговое значение сантимента
    # или вроде того (у меня ничего приличного с пороговым TF-IDF не вышло)
    X = np.array([])
    '''
    Напишите код для формирования веса предложения с помощью сантиментов отдельных слов
    '''
    for line in text:
        words_cnt = 0
        sentiment_strong = 0

        for word in line.split():
            #words_cnt += 1
            word = word.split('_')[0]

            if word in linis_dict and (linis_dict[word] == -2 or linis_dict[word] == 2):
                sentiment_strong += linis_dict[word]


        X = np.append(X, sentiment_strong) #сентимент с учетом только -2 и 2

    print(X)

    # Определение объёма автореферата
    i = max(2, len(text) // 4)
    # Выбор i предложений с максимальными присвоенными весами
    res = X.argsort(0)[-i:].reshape(i).tolist()
    # Сортировка полученных индексов, чтобы вернуть предложения в правильном порядке
    res.sort()
    #print(res)
    return res

def summarize(filename):
    xml = get_sample()
    with open(filename, 'w', encoding='utf8') as ouf:
        ouf.write("<?xml version='1.0' encoding='UTF8'?>\n<data>\n<corpus>\n")
        for tag in xml.find_all('paraphrase'):
            tagg = [str(item) for item in tag.contents]
            sums = []
            for i in (19, 21):
                text = [s.strip() for s in str(tag.contents[i].contents[0]).split('\n')]
                lem = lemmatize_texts(text)
                ind = get_sentiment_indices(lem)
                sums.append('\n'.join([text[j] for j in ind]))
            tagg.extend(
                ['<value name="summarize_1">{0}</value>'.format(sums[0]), '\n',
                 '<value name="summarize_2">{0}</value>'.format(sums[1]), '\n'])
            ouf.write('<paraphrase>{0}</paraphrase>\n'.format(''.join(tagg)))
        ouf.write('</corpus>\n</data>')


if __name__ == '__main__':
    summarize('sentiment_strong.xml')
