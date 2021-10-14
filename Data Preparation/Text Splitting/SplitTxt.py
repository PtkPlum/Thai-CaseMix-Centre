import math
from time import time
def Data(filename, NeededLine=50): # Result is the first 50 record of data, and the record number of file
    data = ""
    with open(filename+".txt") as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno < NeededLine:
                data += line + "\n"
    return data, lineno

def Split(data, LinePerFile, Field=False): # split data, Field = True or False
    smallfile, j = None, 1
    with open(filename+".txt") as bigfile:
        if Field == False:
            for lineno, line in enumerate(bigfile):
                if lineno % LinePerFile == 0:
                    if smallfile:
                        smallfile.close()
                    small_filename = '{}({}).txt'.format(filename,j)
                    smallfile = open(small_filename, "w")
                    j+=1
                smallfile.write(line)
                print(lineno / record * 100, "%")
            if smallfile:
                smallfile.close()

        elif Field == True:
            for lineno, line in enumerate(bigfile):
                if lineno == 0:
                    Field = line
                Logic = (lineno % LinePerFile == 0) if j==1 else ((lineno+1) % LinePerFile == 0)
                if Logic:
                    if smallfile:
                        smallfile.close()
                    small_filename = '{}({}).txt'.format(filename,j)
                    smallfile = open(small_filename, "w")
                    smallfile.write(Field)
                    j+=1
                    print(lineno / record * 100, "%")
                if lineno > 0:
                    smallfile.write(line)
                
            if smallfile:
                smallfile.close()


'''

    There are 3 Inputs in this code
        1. filename
        2. Nfile or LinePerFile (Choose one from 2)
        3. show Field or not (True or False)

'''
start = time()
filename = "AllCharge1"
data, record = Data(filename)
Nfile = 40                                 # Choose only one from 2
LinePerFile = math.ceil( record / Nfile )  # ห้ามแก้
#LinePerFile = 100000                      # Choose only one from 2
Split(filename, LinePerFile, Field=True)   # True = show field | False = not show field

print("Done")
print("ใช้เวลาไป {} วินาที".format(time()-start))