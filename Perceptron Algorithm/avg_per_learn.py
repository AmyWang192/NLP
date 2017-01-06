import os
import sys
import random

class message_info:
	"""docstring for message_info"""
	def __init__(self, style):
		self.style = style
		self.message_token = {}
	def addFeature(self, token):
		if token not in self.message_token:
			self.message_token[token] = 1
		else:
			self.message_token[token] += 1

class token_info:
	"""docstring for token_info"""
	def __init__(self, name):
		self.name = name
		self.weight = 0
		self.avg_weight = 0

	def change_weight(self, weight_value):
		self.weight = weight_value
	def change_avg_weight(self, weight_avg_value):
		self.avg_weight = weight_avg_value

document_path = sys.argv[1]

ham_message_count = 0
spam_message_count = 0
message_list = []
count_value = 1
bia_value = 0
avg_bia_value = 0
voc_dis = set()
weight_table = {}
avg_weight_table = {}
#get training data

for root, dirs, files in os.walk(document_path):
	for file_name in files:
		if file_name.endswith(".txt"):
			if "ham" in file_name or "ham" in root:
				ham_message_count += 1
				lines = open(root +"/"+file_name, "r",encoding = "latin1").readlines()
				new_message = message_info("ham")
				for everylines in lines:
					token_list = everylines.split()
					for every_token in token_list:
						if every_token not in voc_dis:
							weight_table[every_token] = 0
							avg_weight_table[every_token] = 0
						voc_dis.add(every_token)
						new_message.addFeature(every_token)
				message_list.append(new_message)
			elif "spam" in file_name or "spam" in root:
				spam_message_count += 1
				lines = open(root +"/"+ file_name, "r", encoding = "latin1").readlines()
				new_message = message_info("spam")
				for everylines in lines:
					token_list = everylines.split()
					for every_token in token_list:
						if every_token not in voc_dis:
							weight_table[every_token] = 0
							avg_weight_table[every_token] = 0
						voc_dis.add(every_token)
						new_message.addFeature(every_token)
				message_list.append(new_message)


#get weight and avg weight

for i in range(0,30):
	random.shuffle(message_list)
	for j in range(0, len(message_list)):
		tmp_message = message_list[j]
		tmp_style = tmp_message.style
		tmp_table = tmp_message.message_token
		if tmp_style in "spam":
			alpha_value = 0
			label_value = 1
			for tmp_token in tmp_table:
				alpha_value += tmp_table[tmp_token]*weight_table[tmp_token]
			alpha_value += bia_value
			if alpha_value*label_value <= 0:
				bia_value = bia_value + label_value
				avg_bia_value = avg_bia_value + count_value*label_value
				for tmp_token_value in tmp_table:
					weight_table[tmp_token_value] = weight_table[tmp_token_value] + label_value*tmp_table[tmp_token_value]
					avg_weight_table[tmp_token_value] = avg_weight_table[tmp_token_value] + label_value*count_value*tmp_table[tmp_token_value]
		elif tmp_style in "ham":
			alpha_value = 0
			label_value = -1
			for tmp_token in tmp_table:
				alpha_value += tmp_table[tmp_token]*weight_table[tmp_token]
			alpha_value += bia_value
			if alpha_value*label_value <= 0:
				bia_value = bia_value + label_value
				avg_bia_value = avg_bia_value + count_value*label_value
				for tmp_token_value in tmp_table:
					weight_table[tmp_token_value] = weight_table[tmp_token_value] + label_value*tmp_table[tmp_token_value]
					avg_weight_table[tmp_token_value] = avg_weight_table[tmp_token_value] + label_value*count_value*tmp_table[tmp_token_value]
		count_value += 1


#calculation final model

for tokens in weight_table:
	avg_weight_table[tokens] = weight_table[tokens] -  avg_weight_table[tokens]/count_value

avg_bia_value = bia_value - avg_bia_value/count_value


model_file_data = open("per_model.txt", "w",encoding = "latin1")



model_file_data.write("ham_message_count %s" %ham_message_count)
model_file_data.write("\n")
model_file_data.write("spam_message_count %s" %spam_message_count)
model_file_data.write("\n")
model_file_data.write("bia_value %s" %avg_bia_value)
model_file_data.write("\n")

for token_s in avg_weight_table:
	model_file_data.write("%s %f" %(token_s, avg_weight_table[token_s]))
	model_file_data.write('\n')
	






		
