import sys
import os
import hw3_corpus_tool

# devdir = sys.argv[1]
# outputfile = sys.argv[2]
devdir = sys.argv[1]
outputfile = sys.argv[2]

tags = []
mytags = []

def generate_tag(path, taglist):
    features = hw3_corpus_tool.get_data(path)
    for file in features:
        for i in file:
            tag = i.act_tag
            taglist.append(tag)

def generate_tag_from_outputfile(myfile, taglist):
    files = open(myfile, "r").readlines()
    for lines in range(len(files)):
        line = files[lines].split()
        if len(line)!=0:
            if line[0].startswith("Filename"):
                continue
            else:
                taglist.append(line[0])

generate_tag(devdir, tags)
generate_tag_from_outputfile(outputfile, mytags)

count_mine = 0
total = len(tags)
for num in range(total):
    if(mytags[num]==tags[num]):
        count_mine+=1

print(count_mine)
print(total)
print(count_mine/total)