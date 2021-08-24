import pandas as pd
import pythainlp as thnlp
from pythainlp.word_vector import doesnt_match
from fuzzy_match import algorithims
from time import time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer

def Time(Start):
    runTime = time() - Start
    if runTime < 60:    
        print("เรียบร้อย ใช้เวลารันไป", round(runTime, 2), "วินาที")
    elif runTime < 60 * 60:
        print("เรียบร้อย ใช้เวลารันไป", int(runTime / 60), "นาที", round(runTime % 60, 2), "วินาที")
    else:
        print("เรียบร้อย ใช้เวลารันไป", int(runTime / (60 * 60)), "ชั่วโมง", int((runTime % 60 * 60) // 60), "นาที", round(runTime % 60, 2), "วินาที")

def RemoveWord(word, RemovedWord):
    RemoveIndex, i = [], 0
    while len(RemovedWord) + i <= len(word):
        if RemovedWord == word[i : i+len(RemovedWord)]:
            RemoveIndex.append(i)
        i += 1
    for i in range(len(RemoveIndex)):
        word = word[:RemoveIndex[i] - len(RemovedWord) * i] + word[RemoveIndex[i] - len(RemovedWord) * (i-1):]
    return word

def Clean(word):
    RemW = [str(i) for i in range(10)] + ["(", ")", "[", "]", ",", ".", "?", "!", " ", "/", "\\", "-", "_", "+"]
    for i in RemW:
        word = RemoveWord(word, i)
    return word

def isEnglish(alphabet):
    if type(alphabet) != str:
        return print("\n\tฟังก์ชั่น isEnglish() รับได้เฉพาะ character เท่านั้น --> ประเภท", type(alphabet), "ไม่รับนะ\n")
    try:
        alphabet.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
        
def EngOnly(word):        
    NewWord = ""
    for i in word:
        if isEnglish(i):
            NewWord += i
    return NewWord


Start = time()
BGr = pd.read_excel("BGr.xlsx")
Ref = pd.read_excel("Bg4ChargeCSCode.xlsx")
Mod = pd.read_excel("BGrRef.xlsx", sheet_name="Model")

label = Ref["bgr"]
Train = []
Key = list(Mod["Keyword"])
Q1 = set(thnlp.corpus.common.thai_words())
Q1.update(Key)
Q2 = thnlp.tokenize.core.dict_trie(dict_source=Q1)

for j in range(len(Ref)):
    train = {}
    Q3 = thnlp.word_vector.sentence_vectorizer(Ref["csname"][j])
    for i in range(300):    
        train[str(i)] = Q3[0][i]
    for i in Key:
        Q4 = thnlp.word_tokenize(Ref["csname"][j], custom_dict=Q2, keep_whitespace=False)
        if i in Q4:
            train[i] = 1
    Train.append(train)
    if j % 100 == 0 or j == len(Ref)-1:
        print("\tWord2Vec : complete {} %".format(100 * (j+1)/len(Ref)))

dv = DictVectorizer(sparse=True)
model = LogisticRegression()
TrainSparse = dv.fit_transform(Train)
model.fit(TrainSparse, label)

test = {}
Q5 = thnlp.word_vector.sentence_vectorizer(BGr["ChargeName"][0])
for i in range(300):    
    test[str(i)] = Q5[0][i]
for i in Key:
    Q6 = thnlp.word_tokenize(Ref["csname"][j], custom_dict=Q2, keep_whitespace=False)
    if i in Q6:
        test[i] = 1
test = [[test]]
#model.predict(test)


'''
BGr["PredictBGr"] = PredictBGr
BGr["CSName"] = CSName
BGr.to_excel("Result.xlsx")
'''
Time(Start)