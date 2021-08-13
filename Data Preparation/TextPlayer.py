class TextPlayer:
    def __init__(self):
        self.Dict = {}
        self.AllSplit = []


    def NameSur(self, filename):  # เอาชื่อจริง, นามสกุล
        if filename.count(".") == 0:
            return filename, ""
        j = -1
        while filename[j] != ".":
            j -= 1
        return filename[:j], filename[j+1:]
    
    
    def SplitWord(self, word):  # แบ่งคำ เช่น LbPerson แบ่งคำได้เป็น [lb, person] โดยใช้หลักการว่าถ้าตัวถัดไปเป็นตัวพิมพ์ใหญ่หรือตัวเลขก็ยัดลง array
        Split, split = [word.lower()], ""
        for i in range(len(word)-1):   
            split += word[i].lower()
            if word[i+1] == word[i+1].upper() or type(word[i+1]) == int:
                Split.append(split)
                split = ""
        Split.append(split+word[-1].lower())
        return Split 
    
    
    def RemoveWord(self, word, RemovedWord):
        RemoveIndex, i = [], 0
        while len(RemovedWord) + i <= len(word):
            if RemovedWord == word[i : i+len(RemovedWord)]:
                RemoveIndex.append(i)
            i += 1
        for i in range(len(RemoveIndex)):
            word = word[:RemoveIndex[i] - len(RemovedWord) * i] + word[RemoveIndex[i] - len(RemovedWord) * (i-1):]
        return word


    def AddToDict(self, root, FileName1, FileName2): # เติมชื่อใหม่ในรากศัพท์ใน dictionary, Dict คือพจนานุกรมที่บันทึกรากศัพท์, root คือรากศัพท์, FileName1,2 คือคำที่มีรากศัพท์อยู่ข้างใน
        if root in [i for i in self.Dict]:              # ถ้ารากศัพท์นี้เคยถูกบันทึกแล้ว ก็แค่ append ต่อท้าย
            if FileName1 not in self.Dict[root]:         # ถ้าชื่อไฟล์นี้เคยถูกบันทึกใน dictionary ในส่วนรากศัพท์นี้ ให้ข้ามไปเลย แต่ถ้ายังก็ต้องบันทึก เช่น รากศัพท์ Op ตอนนี้บันทึกชื่อไฟล์ [OpCharge, OpDxOp] --> ถ้าเจอไฟล์ใหม่ OpMain ซึ่งยังไม่เคยถูกบันทึก ก็ต้องถูกบันทึก
                self.Dict[root].append(FileName1)
            if FileName2 not in self.Dict[root]:    
                self.Dict[root].append(FileName2)
        else:    # ถ้ารากศัพท์นี้ไม่เคยถูกบันทึก ให้นิยามใหม่เลย
            self.Dict[root] = [FileName1, FileName2]
        return self.Dict
    
    
    def rootDict(self):
        # บันทึกรากศัพท์ ลงใน dictionary อย่าง Op เป็นรากศัพท์ที่พบใน OpCharge, OpMain, OpDxOp, IpDxOp
        # และ Charge เป็นรากศัพท์ที่พบใน AllCharge, IpCharge, OpCharge, BG4Charge ซึ่งรากศัพท์จะมีความสำคัญในการเปรียบเทียบไฟล์ที่มีชื่อคล้ายกัน เพื่อลด bias ของความน่าจะเป็น
        for i in range(len(self.AllSplit)):
            for j in range(i):
                for k in self.AllSplit[i]:
                    if k in self.AllSplit[j]:
                        self.Dict = self.AddToDict(k, self.AllSplit[i][0], self.AllSplit[j][0])
        return self.Dict


    def isEnglish(self, alphabet):
        if type(alphabet) != str:
            return print("\n\tฟังก์ชั่น isEnglish() รับได้เฉพาะ character เท่านั้น --> ประเภท", type(alphabet), "ไม่รับนะ\n")
        try:
            alphabet.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True
        
    
    def EngOnly(self, word):
        NewWord = ""
        for i in word:
            if self.isEnglish(i):
                NewWord += i
        return NewWord

if __name__ == "__main__":

    A = TextPlayer()
    print(A.EngOnly("สวัสดี English"))
    print(A.NameSur("WordReport@yahoo.com.xlsx"))
    print(A.RemoveWord("helloWorld", "o"))
    print(A.isEnglish([5.3]))