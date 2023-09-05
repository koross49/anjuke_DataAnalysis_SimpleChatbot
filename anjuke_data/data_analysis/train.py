import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump

# 车机的命令与回复数组
command=[['请打开车窗','好的，车窗已打开'],
         ['我要听陈奕迅的歌','为你播放富士山下'],
         ['我好热','已为你把温度调到25度'],
         ['帮我打电话给小猪猪','已帮你拨小猪猪的电话'],
         ['现在几点钟','现在是早上10点'],
         ['我要导航到中华广场','高德地图已打开'],
         ['明天天气怎么样','明天天晴']
        ]


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
    # 获取车机命令的 TF-IDF 向量
    data0 = model.transform(getWords()).toarray().reshape(len(command), -1)
    return data0, command


if __name__ == '__main__':
    maintrain()