import sys
import os
import random
import shutil




if os.path.exists("data/temp"):
    shutil.rmtree("data/temp")
    os.mkdir("data/temp")
else:
    os.mkdir("data/temp")
if os.path.exists("data/test_temp"):
    shutil.rmtree("data/test_temp")
    os.mkdir("data/test_temp")
else:
    os.mkdir("data/test_temp")

file_path = sys.argv[1]

for root, dir, files in os.walk(file_path):
    files_num = len(files)
    # print(os.listdir(root))
    if(files_num>1):
        sfpercent = round(files_num*0.75)
        rest = files_num - sfpercent
        # print(sfpercent)
        random.shuffle(files)
        for item in range(sfpercent):
            choose_file = files[item]
            src = root + "/" + choose_file
            if(os.path.isfile(src)==True):
                shutil.copy(src, "data/temp")
        for item in range(files_num):
            test_file = files[item]
            test_src = root + "/" + test_file
            check = "data/temp/" + test_file
            if(os.path.isfile(check)==False):
                shutil.copy(test_src, "data/test_temp")