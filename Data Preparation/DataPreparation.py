import pandas as pd
import glob
import os
import numpy as np
from time import time


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
    CharField["matutil"]    =  ["hcode", "matgrp"]
    CharField["matproj"]    =  ["hcode", "matgrp"]
    CharField["mathire"]    =  ["hcode", "matgrp"]
    CharField["matmsup"]    =  ["hcode", "matgrp"]
    CharField["matlab"]     =  ["hcode", "matgrp"]
    CharField["matdent"]    =  ["hcode", "matgrp"]
    CharField["matdrug"]    =  ["hcode", "matgrp"]
    CharField["matgen"]     =  ["hcode", "matgrp"]
    CharField["mat2imsup"]  =  ["hcode", "chargecode", "cscode"]
    CharField["mat2ilab"]   =  ["hcode", "chargecode", "cscode"]
    CharField["mat2ioth"]   =  ["hcode", "chargecode", "cscode"]
    CharField["mat2idrug"]  =  ["hcode", "chargecode", "cscode"]
    CharField["dmuc4msup"]  =  ["hcode", "bgr", "bsub", "chargecode", "cscode", "stdcode"]
    CharField["dmuc4lab"]   =  ["hcode", "bgr", "bsub", "chargecode", "cscode", "stdcode"]
    CharField["dmuc4oth"]   =  ["hcode", "bgr", "bsub", "chargecode", "cscode", "stdcode"]
    CharField["dmuc4drug"]  =  ["hcode", "bgr", "bsub", "chargecode", "tmttpu", "code24"]
    CharField["hosdep"]     =  ["hcode", "depcode"]
    CharField["opmain"]     =  ["hcode", "vn", "hn", "pidpat", "timeopd", "clinic", "hmain", "inscl"]
    CharField["ipmain"]     =  ["hcode", "an", "hn", "pidpat", "timeadm", "timedsc", "wardadm", "warddsc", "hmain", "inscl"]
    CharField["ortime"]     =  ["hcode", "ornumber", "vn", "hn", "an", "timebeg"]
    CharField["orperson"]   =  ["hcode", "ornumber", "vn", "hn", "an", "timebeg", "idcard"]
    CharField["bg4charge"]  =  ["hcode", "chargecode", "code24", "bgr", "cscode", "stdcode", "bsub"]
    CharField["allcharge"]  =  ["hcode", "an", "vn", "hn", "chargecode", "bgr", "depcode", "pttype"]
    CharField["allcharge"]  =  ["hcode", "an", "vn", "hn", "chargecode", "bgr", "depcode", "pttype"]
    CharField["allcharge1"] =  ["hcode", "an", "vn", "hn", "chargecode", "bgr", "depcode", "pttype"]
    CharField["allcharge2"] =  ["hcode", "an", "vn", "hn", "chargecode", "bgr", "depcode", "pttype"]
    CharField["bg4charge"]  =  ["hcode", "an", "vn", "hn", "chargecode", "bgr", "depcode", "pttype"]
    CharField["ipcharge"]   =  ["hcode", "an", "vn", "hn", "chargecode", "bgr", "depcode", "pttype"]
    CharField["opcharge"]   =  ["hcode", "an", "vn", "hn", "chargecode", "bgr", "depcode", "pttype"]
    CharField["er"]         =  ["hcode", "an", "vn", "hn", "pidpat", "timein", "timeout"]
    CharField["iptransfer"] =  ["hcode", "an", "hn", "pidpat", "timein", "wardin", "wardout", "wdin", "wdout"]
    CharField["ipdxop"]     =  ["hcode", "an", "hn"]
    CharField["opdxop"]     =  ["hcode", "vn", "hn", "code"]
    CharField["instype"]    =  ["hcode", "inscl", "pttype"]
    CharField["palliative"] =  ["hcode", "an", "hn", "pidpat", "pdx"]
    CharField["dccdist"]    =  ["hcode", "ccid", "ccname"]
    CharField["d2bdefs"]    =  ["hcode", "distname", "bsub", "bsdesc"]
    
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
    if Surnamefile == "xlsx" or Surnamefile == "xlx" or Surnamefile == "xls":
        df = pd.read_excel(file, skiprows=range(100000, 10000000))
    elif Surnamefile == "csv":
        df = pd.read_csv(file, skiprows=range(100000, 10000000))
        
    CharFieldFormat = Character(fileName)
    CharFieldName   = GivenFieldName(df, CharFieldFormat)
    convert = {}
    for i in CharFieldName:
        convert[i] = str
    if Surnamefile == "xlsx" or Surnamefile == "xlx" or Surnamefile == "xls":
        Excel = pd.ExcelFile(file)
        ExcelDict = {}
        for i in Excel.sheet_names:
            ExcelDict[i] = pd.read_excel(file, sheet_name=i)
        return [pd.read_excel(file, converters=convert)]
    elif Surnamefile == "csv":
        return [pd.read_csv(file, converters=convert)]

    
def Save(file, df, name=""):
    name = Name(file)[0] if name == "" else name
    df.to_csv("FileResultText\\" + name + ".txt", index=None, sep='|', mode='w')
    df.to_excel("FileResultExcel\\" + name + ".xlsx", index=None)
    print("เซฟไฟล์ " + name + ".txt เรียบร้อย")
    
Start = time()

AllFile = glob.glob('*.xlx') + glob.glob('*.xlsx') + glob.glob('*.xls') #+ glob.glob('*.csv')
#dataReport = pd.read_excel("Report\Reference\EmptyDataReport.xlsx")
#dataReport["nFile"] = [0 for i in dataReport["nFile"]]

i = 1
for file in AllFile:
    print("ไฟล์ที่ ", i)
    dfList = ImportData(file)    
    for j in dfList:
        print("โหลด " + file + " เรียบร้อย")
        Save(file, j)

    print("------------------------------------------\n")
    i += 1

runTime = time() - Start
if runTime < 60:    
    print("เรียบร้อย ใช้เวลารันไป", round(runTime, 2), "วินาที")
elif runTime < 60 * 60:
    print("เรียบร้อย ใช้เวลารันไป", int(runTime / 60), "นาที", round(runTime % 60, 2), "วินาที")
else:
    print("เรียบร้อย ใช้เวลารันไป", int(runTime / (60 * 60)), "ชั่วโมง", int((runTime % 60 * 60) // 60), "นาที", round(runTime % 60, 2), "วินาที")

#dataReport.to_excel("Report\DataReport.xlsx", index=False)
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
