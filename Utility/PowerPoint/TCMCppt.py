from PowerPoint import PowerPoint
import pandas as pd
from pptx.util import Inches
from pptx.util import Pt
import numpy as np

def Page1(ppt):
    ppt.NewPage()
    ppt.Title('ข้อมูลโรงพยาบาล')

def Page2(ppt):
    ppt.NewPage()
    ppt.TextBox('Logo', layout="center", color=[0,0,250])
    ppt.Image("Image\BoxPlot.png")

def Page3(ppt):
    ppt.NewPage()
    ppt.TextBox('ข้อมูลตารางของโรงพยาบาล', FontName="Tahoma", FontSize=Pt(50), top=Inches(-0.3), color=[250,0,0], layout="center")
    ppt.Table(DataFrame)
    
def Page4(ppt):
    ppt.NewPage()
    text = "ผลการศึกษาต้นทุนรายโรค ปีที่ 3"
    ppt.AutoShape(text=text, Col="blueTCMC", left=0, top=0, width=Inches(16.0), height=Inches(2.5), FontSize=Pt(110), layout="center", color=[255,255,255])
    
def Page5(ppt):
    ppt.NewPage()
    DF = pd.DataFrame(abs(np.random.randn(10, 4)))
    DF.columns = [['ต้นทุนต่อหน่วย', ' ', 'ราคาขายต่อหน่วย', ' '], ['ทางตรง', 'ทางอ้อม', 'ทางตรง', 'ทางอ้อม']]
    ppt.Table(DF)



if __name__ == '__main__':
    df = pd.read_csv("Excel\h11317tb3.1CostPerOPVisitDisease.csv")
    df = pd.read_excel("Excel\h11317tb1.4Top10Laboratory.xlsx")
    DataFrame = pd.DataFrame()
    for i in df:
        DataFrame[i] = df[i][:10]
    
    ppt = PowerPoint()
    
    ppt.prs.slide_height = Inches(9)
    ppt.prs.slide_width = Inches(16)
    
    Page1(ppt)
    Page2(ppt)
    Page3(ppt)
    Page4(ppt)
    #Page5(ppt)
    
    ppt.Save()