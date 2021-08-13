class TextCountProb():
    
    def UnionProb(self, A, B):   # P(A U B) โดยเจอที่ A, and B เป็น text เช่น UnionProb("hello world", "lo") มันก็จะรู้ว่าหา prob ที่เจอ l หรือ o ใน "hello world"
        if len(A) == 0:
            return 0
        else:
            return  self.UnionCount(A, B) / len(A)
    
    
    def CondProb(self, word, A, B):
    # หา prob ที่ข้อความ A จะอยู่หลัง B เช่น prob ที่คำว่า s จะอยู่หลัง ho เพื่อจะได้คำว่า hos 
    # คำนวณโดยเอา จำนวนคำว่า ho ทั้งหมดที่พบเป็นตัวส่วน และเอาจำนวนคำว่า hos ที่พบเป็นตัวเศษ
        N = self.Count(word[:-1], B)
        if N == 0:
            return 0
        return self.Count(word, B+A) / N
    

    def Count(self, word, A):
        return word.count(A)
    
    
    def UnionCount(self, A, B): # B เป็น text เช่น UnionProb("hello world", "lo") มันก็จะรู้ว่าหาจำนวน ที่เจอ l หรือ o ใน "hello world"
        score = 0
        for j in A:
            if j in B:
                score += 1
        return score