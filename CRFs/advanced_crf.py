import pycrfsuite
import sys
import os
import hw3_corpus_tool
import random

class message_info:
    """docstring for message_info"""
    def __init__(self, name):
        self.name = name
        self.message_dict = []
    def setDict(self, dict):
        self.message_dict = dict




document_path = sys.argv[1]
dev_data = sys.argv[2]
out_put_name = sys.argv[3]

#prepare for two train set
def get_feature(path):
    resultArr = []
    result = []
    result2 = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".csv"):
                speaker = ""
                dict_to_utter = []
                is_first_speaker = "first:isTrue"
                dict_to_csv = []
                dict_to_csv = hw3_corpus_tool.get_utterances_from_filename(root+"/"+file_name)
                first_speaker = ""
                data_y = []
                for i in range(0,len(dict_to_csv)):
                    data_y.append(dict_to_csv[i].act_tag)
                    utter_each = []
                    isChange = "isChange:isFalse"
                    if first_speaker != dict_to_csv[i].speaker and i > 0:
                        isChange = "isChange:isTrue"
                    utter_each.append(is_first_speaker)
                    utter_each.append(isChange)
                    first_speaker = dict_to_csv[i].speaker
                    is_first_speaker = "first:isFalse"
                    if dict_to_csv[i].pos != None:
                        for p  in range(0,len(dict_to_csv[i].pos)):
                            utter_each.extend(word2features(dict_to_csv[i].pos,p))


                    dict_to_utter.append(utter_each)
                result.append(dict_to_utter)
                result2.append(data_y)
    resultArr.append(result)
    resultArr.append(result2)
    return resultArr

def word2features(sent,i):
    tokens = sent[i].token.lower()
    pos = sent[i].pos.upper()
    features = [
        'TOKEN[0]='+tokens,
        'POS[0]='+pos,
        ]
    if i > 0:
        word1 = sent[i-1].token.lower()
        postag1 = sent[i-1].pos.upper()
        features.extend([
            'TOKEN[-1]=' + word1,
            'POS[-1]=' +  postag1
        ])
        features.extend([
            'TOKEN[-1]|TOKEN[0]='+word1+"|"+ tokens,
            'POS[-1]|POS[0]='+postag1+"|"+pos

        ])
    else:
        features.append('BOS')
    if i < len(sent) - 1:
        word2 = sent[i+1].token.lower()
        postag2 = sent[i+1].pos.upper()
        features.extend([
            'TOKEN[1]=' + word2,
            'POS[1]=' +  postag2
        ])
        features.extend([
            'TOKEN[0]|TOKEN[1]='+tokens+"|"+ word2,
            'POS[0]|POS[1]='+pos+"|"+postag2

        ])
    else:
        features.append('EOS')
    return features


def get_feature_with_name(path):
    result = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".csv"):
                speaker = ""
                message = message_info(file_name)
                dict_to_utter = []
                is_first_speaker = "first:isTrue"
                speaker = ""
                dict_to_csv = []
                dict_to_csv = hw3_corpus_tool.get_utterances_from_filename(root+"/"+file_name)
                for i in range(0,len(dict_to_csv)):
                    utter_each = []
                    isChange = "isChange:isFalse"
                    if speaker != dict_to_csv[i].speaker and i > 0:
                        isChange = "isChange:isTrue"
                    utter_each.append(is_first_speaker)
                    utter_each.append(isChange)
                    is_first_speaker = "first:isFalse"
                    speaker = dict_to_csv[i].speaker
                    if dict_to_csv[i].pos != None:
                        for p  in range(0,len(dict_to_csv[i].pos)):
                            utter_each.extend(word2features(dict_to_csv[i].pos,p))

                    dict_to_utter.append(utter_each)
                message.message_dict = dict_to_utter
                result.append(message)
    return result


result_tmp = get_feature(document_path)

X_train = result_tmp[0]
Y_train = result_tmp[1]

#train model

trainer = pycrfsuite.Trainer(verbose=True)

trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1.0,  # coefficient for L2 penalty
    'max_iterations': 70,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})
trainer.params()
#
for xseq, yseq in zip(X_train, Y_train):
    trainer.append(xseq, yseq)

trainer.train('adoutput.crfsuite')

tagger = pycrfsuite.Tagger()
tagger.open('adoutput.crfsuite')

fea_test_X = get_feature_with_name(dev_data)
test_X = get_feature(dev_data)
#label_test_Y = get_label_data(dev_data)

output_file = open(out_put_name, "w",encoding = "latin1")

for mes in fea_test_X:
    output_file.write('Filename="%s"' %mes.name)
    output_file.write("\n")
    result_dict = tagger.tag(mes.message_dict)
    for label in result_dict:
        output_file.write(label)
        output_file.write("\n")
    output_file.write("\n")
output_file.write("\n")
output_file.close()








