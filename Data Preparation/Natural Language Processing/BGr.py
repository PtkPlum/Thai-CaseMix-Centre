import pandas as pd
import pythainlp as thnlp
from pythainlp.word_vector import doesnt_match
from fuzzy_match import algorithims
from time import time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from gensim import models

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
X = {}

for j in range(len(Ref)):
    if Ref["csname"][j] == Ref["csname"][j]:
        Q3 = thnlp.word_vector.sentence_vectorizer(Clean(Ref["csname"][j]))
        train = [Q3[0][i] for i in range(300)]
        for i in Key:
            Q4 = thnlp.word_tokenize(Clean(Ref["csname"][j]), custom_dict=Q2, keep_whitespace=False)
            if i in Q4:
                train.append( 1 )
            else:
                train.append( 0 )
    else:
        train = [0 for i in range(300+len(Key))]
    Train.append(train)
    if j % 100 == 0 or j == len(Ref)-1:
        print("Word2Vec : Train complete {} %".format(100 * (j+1)/len(Ref)))

Train = np.array(Train)
Train = Train.transpose()
for i in range(300):
    X[str(i)] = Train[i]
for j in Key:
    i += 1
    X[j] = Train[i]
'''
X["Class"] = label
df = pd.DataFrame(X)
df.to_excel("Input.xlsx", index=False)
'''

model = LogisticRegression()
Train = Train.transpose()
model.fit(Train, label)
print("\tFit model leaw")

Test = []
for j in range(len(BGr)):
    Q3 = thnlp.word_vector.sentence_vectorizer(Clean(BGr["ChargeName"][j]))
    test = [Q3[0][i] for i in range(300)]
    for i in Key:
        Q4 = thnlp.word_tokenize(Clean(BGr["ChargeName"][j]), custom_dict=Q2, keep_whitespace=False)
        if i in Q4:
            test.append( 1 )
        else:
            test.append( 0 )
    Test.append(test)
    if j % 100 == 0 or j == len(BGr)-1:
        print("\t\tWord2Vec : Test complete {} %".format(100 * (j+1)/len(BGr)))
    
Result = []
Class  = model.classes_
Prob   = model.predict_proba(Test)
for i in range(len(Prob)):
    if max(Prob[i]) < 0.25:
        Result.append( 0 )
    else:
        index = np.argmax(Prob[i])
        Result.append( Class[index] )
    if j % 100 == 0 or j == len(Prob)-1:
        print("\t\t\tPredict Finalize : {} %".format(100 * (i+1)/len(Prob)))

BGr["BGr"] = Result 
BGr.to_excel("BGrPredict.xlsx", index=False)


'''
model.intercept_
model.coef_
'''
Time(Start)
