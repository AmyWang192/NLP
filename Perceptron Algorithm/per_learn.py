import sys
import os
import random

class message_s:
	def __init__(self,style):
		self.style = style
		self.token_self_dict = {}

	def addFeatures(self, token):
		if token in self.token_self_dict:
			self.token_self_dict[token] += 1
		else:
			self.token_self_dict[token] = 1

#Initialization
document_path = sys.argv[1]

ham_message_count = 0
spam_message_count = 0
message_count = 0;
ham_token_num = 0
spam_token_num = 0
voc_distinct = set()
voc_distinct_ham = set()
voc_distinct_spam = set()
spam_dict = {}
ham_dict = {}
token_table = {}

ham_message_list = []
spam_message_list = []
message_list = []
bia_value = 0


#Prepare token table and message List

for root,dirs, files in os.walk(document_path):
	for files_name in files:
		if files_name.endswith(".txt"):
			message_count += 1
			if "ham" in files_name or "ham" in root:
				ham_message_count += 1
				lines = open(root + "/" + files_name, "r",encoding = "latin1").readlines()
				new_message = message_s("HAM")
				for each_lines in lines:
					token_list = each_lines.split()
					for token in token_list:
						if token not in voc_distinct:
							token_table[token] = 0
						voc_distinct.add(token)
						new_message.addFeatures(token)
				message_list.append(new_message)
			elif "spam" in files_name or "spam" in root:
				spam_message_count += 1
				lines = open(root + "/" + files_name, "r",encoding = "latin1").readlines()
				new_message = message_s("SPAM")
				for each_lines in lines:
					token_list = each_lines.split()
					for token in token_list:
						if token not in voc_distinct:
							token_table[token] = 0
						voc_distinct.add(token)
						new_message.addFeatures(token)
				message_list.append(new_message)


for i in range(0,20):
	random.shuffle(message_list)
	for j in range(0, len(message_list)):
		new_message = message_list[j]
		if new_message.style in "SPAM":
			label_value = 1
			alpha_value = 0
			new_dict_spam = new_message.token_self_dict
			for every_token in new_dict_spam:
				alpha_value += token_table[every_token]*new_dict_spam[every_token]
			alpha_value += bia_value
			if alpha_value*label_value <= 0:
				bia_value = bia_value + label_value
				for each_token in new_dict_spam:
					token_table[each_token] = token_table[each_token] + label_value*new_dict_spam[each_token]
		elif new_message.style in "HAM":
			label_value = -1
			alpha_value = 0
			new_dict_spam = new_message.token_self_dict
			for every_token in new_dict_spam:
				alpha_value += token_table[every_token]*new_dict_spam[every_token]
			alpha_value += bia_value
			if alpha_value*label_value <= 0:
				bia_value = bia_value + label_value
				for each_token in new_dict_spam:
					token_table[each_token] = token_table[each_token] + label_value*new_dict_spam[each_token]


model_file_data = open("per_model.txt", "w",encoding = "latin1")


model_file_data.write("ham_message_count %s" %ham_message_count)
model_file_data.write("\n")
model_file_data.write("spam_message_count %s" %spam_message_count)
model_file_data.write("\n")
model_file_data.write("bia_value %s" %bia_value)
model_file_data.write("\n")

for token in token_table:
	model_file_data.write("%s %d" %(token, token_table[token]))
	model_file_data.write('\n')








