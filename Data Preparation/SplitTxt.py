FileName = "Dat.txt"
lines_per_file = 100000 
smallfile = None
with open(FileName, errors="ignore", encoding = "utf8") as bigfile:
    for lineno, line in enumerate(bigfile):
        if lineno % lines_per_file == 0:
            if smallfile:
                smallfile.close()
            small_filename = 'small_file_{}.txt'.format(lineno + lines_per_file)
            smallfile = open(small_filename, "w",  encoding = "utf8")
        smallfile.write(line)
    if smallfile:
        smallfile.close()