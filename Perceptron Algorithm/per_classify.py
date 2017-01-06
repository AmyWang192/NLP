import sys
import os
import math

class dev_file:
    def __init__(self,name):
        self.name = name
        self.label = ""
        self.token_dict = {}
    def addfeatures(self, token):
    	if token not in self.token_dict:
    		self.token_dict[token] = 1
    	else:
    		self.token_dict[token] += 1

document_path = sys.argv[1]
output_filename = sys.argv[2]

spam_data_dict = {}
ham_data_dict = {}
test_data_dict ={}

train_data = open("per_model.txt", "r", encoding = "latin1").readlines()



prepare_ham_data = train_data[0].split()
ham_message_count = prepare_ham_data[len(prepare_ham_data) - 1]

prepare_spam_data = train_data[1].split()
spam_message_count = prepare_spam_data[len(prepare_spam_data) - 1]

prepare_bia_data = train_data[2].split()
bia_data = float(prepare_bia_data[len(prepare_bia_data) - 1])
token_weight_table = {}
result_table = {}
#complete training data
for i in range(3, len(train_data)):
	token_and_weight = train_data[i].split()
	token_weight_table[token_and_weight[0]] = float(token_and_weight[len(token_and_weight) - 1])

#complete dev data
file_list = []
for root, dirs, files in os.walk(document_path):
	for files_name in files:
		if files_name.endswith(".txt"):
			new_file = dev_file(root +"/"+files_name)
			dev_file_line = open(root +"/"+ files_name, "r", encoding = "latin1").readlines()
			for eveLines in dev_file_line:
				dev_token_list = eveLines.split()
				for eveToken in dev_token_list:
					new_file.addfeatures(eveToken)
			file_list.append(new_file)

#calculation
for i in range (0, len(file_list)):
	dev_each_file = file_list[i]
	dev_table = dev_each_file.token_dict
	alpha_value  = 0
	for dis_token in dev_table:
		if dis_token in token_weight_table:
			alpha_value += dev_table[dis_token]*token_weight_table[dis_token]
	alpha_value += bia_data
	if alpha_value > 0:
		dev_each_file.label = "spam"
	else:
		dev_each_file.label = "ham"

#output
result_files = open(output_filename, "w",encoding = "latin1")
for i in range(0, len(file_list)):
	each_files = file_list[i]
	result_files.write("%s %s" %(each_files.label, each_files.name))
	result_files.write("\n")





