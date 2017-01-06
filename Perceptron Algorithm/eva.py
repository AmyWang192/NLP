import os
import sys

name = sys.argv[1]

result_data = open(name, "r", encoding = "latin1").readlines()
total_spam = 0
total_ham = 0
right_spam = 0
right_ham = 0
i_think_is_ham = 0
i_think_is_spam = 0

for each_lines in result_data:
	each_word = each_lines.split();
	flag1 = each_word[0]
	if flag1 == "ham":
		i_think_is_ham += 1
	elif flag1 == "spam":
		i_think_is_spam += 1
	rest_of_sen = each_word[1]
	if "ham" in rest_of_sen:
		flag2 = "ham"
	elif "spam" in rest_of_sen:
		flag2 = "spam"
		
	if flag2 == "ham":
		total_ham += 1
		if flag1 == "ham":
			right_ham += 1
	elif flag2 == "spam":
		total_spam += 1
		if flag1 == "spam":
			right_spam += 1
			
precision_spam = right_spam/i_think_is_spam
precision_ham = right_ham/i_think_is_ham
recall_spam = right_spam/total_spam
recall_ham = right_ham/total_ham

F1_spam = (2*precision_spam*recall_spam)/(precision_spam+recall_spam)
F1_ham = (2*precision_ham*recall_ham)/(precision_ham + recall_ham)

print("total_spam" , total_spam)
print("total_ham", total_ham)
print("right_ham", right_ham)
print("right_spam", right_spam)
print("i_think_is_ham", i_think_is_ham)
print("i_think_is_spam",i_think_is_spam)

print("precision_spam %s" %precision_spam)
print("recall_spam %s" %recall_spam)
print("F1_spam %s" %F1_spam)

print("precision_ham %s" %precision_ham)
print("recall_ham %s" %recall_ham)
print("F1_ham %s" %F1_ham)


	
