from dbf import *
import pandas as pd
import os
import numpy as np
import glob
from TextCountProb import TextCountProb
from TextPlayer import TextPlayer
from fuzzy_match import algorithims
from time import time


class Checklist:
    def __init__(self, DataReport):
        self.DataReport     = DataReport
        self.DataReport2    = pd.DataFrame({"FileName"      : [],
                                            "SheetName"     : [],
                                            "Classification": [],
                                            "Probability"   : [],
                                            "nRecord"       : []})
        self.UnitCostData   = [self.DataReport["File name"][i] for i in range(len(self.DataReport))] # รวมชื่อแฟ้มทุกแฟ้มใน data dict
        self.UnitCostDataTH = [self.DataReport["File name Thai"][i] for i in range(len(self.DataReport))] # รวมชื่อแฟ้มทุกแฟ้มใน data dict
        self.TxtPClass      = TextPlayer()
        self.AllSplit       = []
        self.Dict           = {}  # สร้าง dictionary โล่งๆ เพื่อจะนำไปบันทึก รากศัพท์ในภายภาคหน้า
        self.TxtCntPb       = TextCountProb()
            
        
    def ScoreWithinSplit(self, name, Name, score=0, weight=0, show=False):
        score = weight = 0 
        UpLetList = []    # เอามาหา prob, ถ้า P อยู่ถัดจาก b ก็มีความน่าจะเป็น LbPerson มากขึ้น
        for i in self.AllSplit[Name][1:]:   # ไม่เอาตัวแรก เพราะตัวแรกคือทั้งชื่อไฟล์ and สำหรับ LbDrOt ทำ 3 iterations (Lb, Dr แล้วค่อย Ot)
            UpLetList.append([i[0], i[-1]]) # ใน LbDrOt เก็บคำว่า i[0] = D(ตัวแรก เอาไว้เชื่อมกับ b) กับ i[-1] = r(ตัวสุดท้าย เอาไว้เชื่อมกับ O) 
            if len(i) > 1: # BG4Charge, B ไม่มีพิมพ์เล็กมาต่อ เลยไม่ต้องหา prob แต่ Charge ต้องหาเพราะมีพิมพ์เล็ก
                for j in range(1,len(i)):
                    if j == 1: # สำหรับตัวพิมพ์ใหญ่
                        score += self.TxtCntPb.CondProb(name, i[1], i[0])
                        weight += 1
                        if show == True:
                            print("P(",i[1],"|",i[0],") =",self.TxtCntPb.CondProb(name, i[1], i[0]))
                            print("weight = 1")
                    elif j > 1: # สำหรับตัวพิมพ์เล็ก
                        score += 0.5 * self.TxtCntPb.CondProb(name, i[j], i[:j]) # P(n ถัดจาก Perso), n คือ j=5 แต่ Perso มี j=0,1,2,3,4
                        weight += 0.5
                        if show == True:
                            print("P(",i[j],"|",i[:j],") =",self.TxtCntPb.CondProb(name, i[j], i[:j]))
                            print("weight = 0.5")
        return score, weight, UpLetList
        

    def ScoreBetweenSplit(self, name, Name, UpLetList, score=0, weight=0, show=False):
        for i in range(1, len(UpLetList)): # [Lb, Dr, Ot] --> UpLetList = [(L,b), (D,r), (O,t)] เริ่มที่ i=1 ก็คือ (D,r) ถึง i=2 คือ (O,t)
            score += self.TxtCntPb.CondProb(name, UpLetList[i][0], UpLetList[i-1][1]) # ถ้า i=1 --> P(D ถัดจาก b), i=2 --> P(O ถัดจาก r)
            weight += 1
            if show == True:
                print("P(",UpLetList[i][0],"|",UpLetList[i-1][1],") =",self.TxtCntPb.CondProb(name, UpLetList[i][0], UpLetList[i-1][1]))
                print("weight = 1")
        return score, weight
        
    def rootScore(self, name, Name):
        found = scoreUnion = 0
        for i in self.Dict:
            if i in name and i in self.UnitCostData[Name]:# and self.UnitCostData[Name] in Dict[i]:
                #print()
                A = self.TxtPClass.RemoveWord(name, i)
                #print("name is", name, ", i is", i, ", A is", A)
                B = self.TxtPClass.RemoveWord(self.UnitCostData[Name], i)
                #print("UnitCostData[Name] is", self.UnitCostData[Name], ", i is", i, ", B is", B)
                
                TriGram = algorithims.trigram( A, B )
                if type(TriGram) == NoneType:
                    scoreUnion += 1
                else:
                    scoreUnion += algorithims.trigram( A, B ) #self.TxtCntPb.UnionProb(A, B)
                

                #print("\tP(", A, " , ", B,") =", algorithims.trigram( A, B ))
                found += 1
        if found > 0:
            #print()
            return scoreUnion / found
        else:
            return 0
    
    def NLPscore(self, NameList, name, show):
        Score = []
        for Name in range(len(NameList)-1): # ไฟล์อื่นๆ คือไฟล์ที่ชื่อไม่ตรงกับไฟล์ในเล่ม เลยไม่ต้องมาหา prob
            '''
            #score, weight, UpLetList = self.ScoreWithinSplit(name, Name, show=show)
            # UpLetList ใช้เป็น index เอามาหา prob, ถ้า P อยู่ถัดจาก b ก็มีความน่าจะเป็น LbPerson มากขึ้น
            #score, weight = self.ScoreBetweenSplit(name, Name, UpLetList, score, weight, show=show)
            #score /= weight
            '''
            Root3Gram = self.rootScore(name, Name)
            TriGram   = algorithims.trigram( name, self.UnitCostData[Name] )
            
            score = (Root3Gram + TriGram) / 2            
            Score.append(score)
        return Score
        
    
    # DataReport["File name"]
    def ConvertName(self, name, show=False):
        Eng = self.NLPscore(self.UnitCostData, name, show)
        TH  = [0] #self.NLPscore(self.UnitCostDataTH, name, show)
                
        if max(Eng) >= max(TH):
            if max(Eng) >= 0.25:
                return self.UnitCostData[np.argmax(Eng)], np.argmax(Eng), max(Eng)
            else:
                return self.UnitCostData[-1], len(self.UnitCostData)-1, max(Eng)
        else:
            if max(TH) >= 0.25:
                return self.UnitCostDataTH[np.argmax(TH)], np.argmax(TH), max(TH)
            else:
                return self.UnitCostDataTH[-1], len(self.UnitCostDataTH)-1, max(TH)
            
    
        
    def ImportData(self, FullName): 
        fileName, Surnamefile = self.TxtPClass.NameSur(FullName)
        Surnamefile = Surnamefile.lower()
        if Surnamefile == "xlsx" or Surnamefile == "xlx" or Surnamefile == "xls":
            Excel = pd.ExcelFile(FullName)
            Dict = {}
            for i in Excel.sheet_names:
                Dict[i] = pd.read_excel(FullName, sheet_name=i)
            return Dict
        elif Surnamefile == "csv":
            return {file : pd.read_csv(FullName)}
        elif Surnamefile == "dbf":
            return {file : VfpTable(FullName)}
        elif Surnamefile == "txt":
            return {file : pd.read_csv(FullName, delimiter="|")}
                
        
    def Main(self, name, df, fileName, sheet_num=1, show=False): # กรอกเช็คลิสต์
        Oriname = name
        Orifile = fileName
        name = TxtP.NameSur(name)[0]
        removed = [" ", "0", "-", "_", "#", "!", "?", "@", "$", "%", "^", "*", "(", ")", "+", "=", "\\", "."]
        for j in removed:
            name = self.TxtPClass.RemoveWord(name, j)
            fileName = self.TxtPClass.RemoveWord(fileName, j)
    
        for i in self.UnitCostData[:-1]:
            self.AllSplit.append(self.TxtPClass.SplitWord(i))
        self.TxtPClass.AllSplit = self.AllSplit
        
        self.TxtPClass.Dict = self.Dict
        self.Dict = self.TxtPClass.rootDict()
        
        
        name, fileName, self.UnitCostData = name.lower(), fileName.lower(), [i.lower() for i in self.UnitCostData]
        
        print("ชื่อชีทโดนตัดเหลือ", name)
        name, index, prob = self.ConvertName(name, show)
        print("ชื่อไฟล์โดนตัดเหลือ", fileName)
        if prob < 0.25 and sheet_num <= 2:
            name2, index2, prob2 = self.ConvertName(fileName, show)
            if prob < prob2:
                prob, index, prob = prob2, index2, prob2
            
            
        print("\nความน่าจะเป็นที่จะเป็นแฟ้ม ", self.UnitCostData[index], "=", prob)
        self.DataReport["nRecord"][index] = len(df)
        self.DataReport[ "nFile" ][index] += 1
        Present = pd.DataFrame({"FileName"     : [Orifile],
                               "SheetName"     : [Oriname],
                               "Classification": [self.UnitCostData[index]],
                               "Probability"   : [prob],
                               "nRecord"       : [len(df)]})
        
        self.DataReport2 = pd.concat([self.DataReport2, Present], ignore_index=True)
        
    
Start = time()
AllFile = glob.glob('*.xlx') + glob.glob('*.xls') + glob.glob('*.xlsx') + glob.glob('*.csv') + glob.glob('*.txt') + glob.glob('*.dbf')

dataReport = pd.read_excel("Report\Reference\EmptyDataReport.xlsx")
dataReport["nFile"] = [0 for i in dataReport["nFile"]]
checklist = Checklist(dataReport)
TxtP = TextPlayer()

i = 1
for file in AllFile:
    df = checklist.ImportData(file)
    fileName = TxtP.NameSur(file)[0]
    for j in df:
        print("ไฟล์ที่ ", i)
        #print(df)
        checklist.Main(j, df[j], fileName, sheet_num = len(df))

        print("------------------------------------------\n")
        i += 1
    
dataReport.to_excel("Report\DataReport.xlsx", index=False)
checklist.DataReport2.to_excel("Report\DataReportProb.xlsx", index=False)














runTime = time() - Start
if runTime < 60:    
    print("เรียบร้อย ใช้เวลารันไป", round(runTime, 2), "วินาที")
elif runTime < 60 * 60:
    print("เรียบร้อย ใช้เวลารันไป", int(runTime / 60), "นาที", round(runTime % 60, 2), "วินาที")
else:
    print("เรียบร้อย ใช้เวลารันไป", int(runTime / (60 * 60)), "ชั่วโมง", int((runTime % 60 * 60) // 60), "นาที", round(runTime % 60, 2), "วินาที")
    
    