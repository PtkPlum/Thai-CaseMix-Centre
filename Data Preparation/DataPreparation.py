import pandas as pd
import glob
import os
import numpy as np

def UnitCostData(DataReport): # รวมชื่อแฟ้มทุกแฟ้มใน data dict
    Column = [i for i in DataReport]
    File = []
    for i in range(len(DataReport)):
        File.append(DataReport[Column[0]][i])
    return File
            

def Name(file):  # เอาชื่อจริง + นามสกุล
    j = 0
    while file[-j] != ".":
        j += 1
    return file[:(len(file)-j)], file[(len(file)-j+1):]
          
def Character(shortfile): # มีฟิลด์ไหนที่ป็น character
    CharField = {}
    CharField["hosccid"]    =  ["hcode", "bgr"]
    CharField["acc2bsub"]   =  ["hcode", "bsub"]
    CharField["hosbsub"]    =  ["hcode", "bgr", "bsub"]
    CharField["lbperson"]   =  ["hcode", "idcard"] # or Lb2CC
    CharField["doctor"]     =  ["hcode", "idcard", "licence"] # or LbDrWk or LbDrOT 
    CharField["mat2i"]      =  ["hcode", "chargecode", "cscode"]
    CharField["dmuc4"]      =  ["hcode", "bgr", "bsub", "chargecode", "cscode", "stdcode"]
    CharField["dmuc4drug"]  =  ["hcode", "bgr", "bsub", "chargecode", "tmttpu", "code24"]
    CharField["hosdep"]     =  ["hcode", "depcode"]
    CharField["opmain"]     =  ["hcode", "vn", "hn", "pidpat", "timeopd", "clinic", "hmain"]
    CharField["ipmain"]     =  ["hcode", "an", "hn", "pidpat", "timeadm", "timedsc", "wardadm", "warddsc", "hmain"]
    CharField["ortime"]     =  ["hcode", "ornumber", "vn", "hn", "an", "timebeg"]
    CharField["orperson"]   =  ["hcode", "ornumber", "vn", "hn", "an", "timebeg", "idcard"]
    CharField["bg4charge"]  =  ["hcode", "chargecode", "code24", "bgr", "cscode", "stdcode", "bsub"]
    CharField["charge"]     =  ["hcode", "an", "vn", "hn", "chargecode", "bgr", "depcode", "pttype"]
    CharField["er"]         =  ["hcode", "an", "vn", "hn", "pidpat", "timein", "timeout"]
    CharField["iptransfer"] =  ["hcode", "an", "hn", "pidpat", "timein", "wardin", "wardout"]
    CharField["ipdxop"]     =  ["hcode", "an", "hn"]
    CharField["opdxop"]     =  ["hcode", "vn", "hn", "code"]
    CharField["instype"]    =  ["hcode", "inscl", "pttype"]
    CharField["palliative"] =  ["hcode", "an", "hn", "pidpat", "pdx"]
    for i in CharField:
        if shortfile.lower() == i:
            return CharField[i]
    return ["hcode"]
        
def GivenFieldName(df, CharFieldFormat): # รพ.ตั้งชื่อฟิลด์ว่าไรบ้าง
    CharFieldName = []
    for i in df:
        for j in CharFieldFormat:  
            if i.lower() == j:
                CharFieldName.append(i)
    return CharFieldName


def ImportData(file): 
    fileName, Surnamefile = Name(file)
    if Surnamefile == "xlsx" or Surnamefile == "xlx":
        df = pd.read_excel(file)
    elif Surnamefile == "csv":
        return pd.read_csv(file)
    CharFieldFormat = Character(fileName)
    CharFieldName = GivenFieldName(df, CharFieldFormat)
    convert = {}
    for i in CharFieldName:
        convert[i] = str
    if Surnamefile == "xlsx" or Surnamefile == "xlx":
        return pd.read_excel(file, converters=convert)
    elif Surnamefile == "csv":
        return pd.read_csv(file, converters=convert)

    
def Save(file, df, name=""):
    if name == "":
       name = Name(file)[0]
    df.to_csv("FileResultText\\" + name + ".txt", index=None, sep='|', mode='w')
    df.to_excel("FileResultExcel\\" + name + ".xlsx", index=None)
    print("เซฟไฟล์ " + name + ".txt เรียบร้อย")
    

AllFile = glob.glob('*.xlx') + glob.glob('*.xlsx') + glob.glob('*.csv')
dataReport = pd.read_excel("Report\EmptyDataReport.xlsx")
dataReport["nFile"] = [0 for i in dataReport["nFile"]]

i = 1
for file in AllFile:
    print("ไฟล์ที่ ", i)
    df = ImportData(file)
    print("โหลด " + file + " เรียบร้อย")
    
    Save(file, df)
    print("------------------------------------------\n")
    i += 1
    
dataReport.to_excel("Report\DataReport.xlsx", index=False)
'''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
\\\\\\\\\\\\\\\\\\\\\\\\\\                       ////////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\        C C I D        ////////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\                       ////////////////////////////
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''


'''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
\\\\\\\\\\\\\\\\\\\\\\                              /////////////////////////
\\\\\\\\\\\\\\\\\\\\\\        T O P - D O W N       /////////////////////////
\\\\\\\\\\\\\\\\\\\\\\                              /////////////////////////
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''


'''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
\\\\\\\\\\\\\\\\\\\\\\                              /////////////////////////
\\\\\\\\\\\\\\\\\\\\\\       B O T T O M - U P      /////////////////////////
\\\\\\\\\\\\\\\\\\\\\\                              /////////////////////////
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''
