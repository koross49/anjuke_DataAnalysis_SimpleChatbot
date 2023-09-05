import jieba
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump
import csv
import xlrd

# 车机的命令与回复数组
command=[]

with open('output.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row if it exists
    for row in reader:
        if len(row) >= 2:
            command.append([row[0], row[1]])

print(command)

file_path = 'commands.csv'

# 将数据写入CSV文件
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(command)

# 利用 jieba 转换命令格式
def getWords():
    comm = np.array(command)
    list = [jieba.lcut(sentence) for sentence in comm[:, 0]]
    words = [' '.join(word) for word in list]
    return words


# 训练 TfidfVectorizer 模型
def getModel():
    words = getWords()
    vectorizer = TfidfVectorizer()
    model = vectorizer.fit(words)
    return model


def maintrain():
    model = getModel()
    dump(model, 'model.pkl')
    data0 = model.transform(getWords()).toarray().reshape(len(command), -1)
    file_path = 'data.csv'

    # 将数据写入CSV文件
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data0)
    return data0, command


if __name__ == '__main__':
    maintrain()