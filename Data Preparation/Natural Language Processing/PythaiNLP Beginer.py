import pythainlp as thnlp
from pythainlp.soundex import lk82, metasound, udom83
from time import time

def Time(Start):
    runTime = time() - Start
    if runTime < 60:    
        print("เรียบร้อย ใช้เวลารันไป", round(runTime, 2), "วินาที")
    elif runTime < 60 * 60:
        print("เรียบร้อย ใช้เวลารันไป", int(runTime / 60), "นาที", round(runTime % 60, 2), "วินาที")
    else:
        print("เรียบร้อย ใช้เวลารันไป", int(runTime / (60 * 60)), "ชั่วโมง", int((runTime % 60 * 60) // 60), "นาที", round(runTime % 60, 2), "วินาที")

Start = time()

Char = thnlp.thai_characters
Cons = thnlp.thai_consonants
Vol  = thnlp.thai_vowels
Tone = thnlp.thai_tonemarks
Sign = thnlp.thai_signs
Digt = thnlp.thai_digits
Syms = thnlp.thai_symbols


Q1 = thnlp.util.isthai("สวัสดีตอนเช้า")
Q2 = thnlp.util.isthai("สวัสดีตอนเช้า กินข้าวหรือยัง?")
Q3 = thnlp.util.isthai("สวัสดีตอนเช้า กินข้าวหรือยัง?", ignore_chars="?")
Q4 = thnlp.util.isthai("สวัสดีตอนเช้า กินข้าวหรือยัง?", ignore_chars=" ?")
Q5 = thnlp.util.isthai("ดัชนีช่วงเช้าปิดที่ระดับ 60,596.53 จุด เพิ่มขึ้น 18.01 จุด หรือ 2.51% มูลค่าการซื้อขาย 8.95 หมื่นล้านบาท", 
                       ignore_chars=" 0123456789,.%")

Q6 = thnlp.util.countthai("แมวสีสวาท")
Q7 = thnlp.util.countthai("วันอาทิตย์ที่ 24 มีนาคม 2562")
Q8 = thnlp.util.countthai("วันอาทิตย์ที่ 24 มีนาคม 2562", ignore_chars="")
# โดย Default แล้ว countthai จะ ignore พวก Whitespace อักษรพิเศษบางตัว และตัวเลข 
#    ดังนี้ ' \t\n\r\x0b\x0c0123456789!"#$...' 


Q9  = lk82("ค่า") == lk82("ข้า")
Q10 = (metasound("สวิทช์") == metasound("สวิส"))
Q11 = udom83("เพชรรัช") == udom83("เพชรรัศม์")
'''
texts = ["ค่า", "ข้า", "ฆ่า", "การ", "กาล", "การณ์", "เพ็ชรรัตน์ ", "เพชรรัตติ์", "รัก", "รักษ์"]
for text in texts:
    print(f"Text: {text}, lk82:, {lk82(text)}, udom83: {udom83(text)}, metasound: {metasound(text)}")
'''

text = "เมืองเชียงรายมีประวัติศาสตร์อันยาวนาน        เป็นที่ตั้งของหิรัญนครเงินยางเชียงแสน"
Q12 = thnlp.sent_tokenize(text)
Q13 = thnlp.word_tokenize(text)
Q14 = thnlp.word_tokenize(text, keep_whitespace=False)
Q15 = thnlp.word_tokenize("มานั่งตากลม")
Q16 = thnlp.word_tokenize("คนรวยสวยจนงง")

text = "เป็งปุ๊ด หรือ เพ็ญพุธ เป็นประเพณีตักบาตรเที่ยงคืนค่อนรุ่งเข้าสู่วันเพ็ญขึ้น15 ค่ำที่ตรงกับวันพุธ ตามวัฒนธรรมและความเชื่อของบรรพบุรุษล้านนาไทย"
Q17 = set(thnlp.corpus.common.thai_words())
words = ["เป็งปุ๊ด", "เพ็ญพุธ"]
Q17.update(words)

    ## add word
    #custom_words_list.add('เป็งปุ๊ด')
    #custom_words_list.add('เพ็ญพุธ')

Q18 = thnlp.tokenize.core.dict_trie(dict_source=Q17)
Q19 = thnlp.word_tokenize(text, custom_dict=Q18, engine="newmm", keep_whitespace=False)


word = ["อร่าย", "ออฟฟิส", "สเน่ห์", "ฆราวาท", "ศีรีษระ", "เสี่เหลี่ยม"]
Q20 = [thnlp.spell(i) for i in word]

Time(Start)