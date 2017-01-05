<h2>Implemented conditional random fields(with CRFsuite) to label sequence.</h2>
<p>The raw data is ".csv" formatted and each document contains a whole Dialogue</p>
<p>Separated about 25% data in to development data for about 20 times, to see the range of accuracy of both
baseline and advanced features</p>
Accuracy of baseline features was: 0.724</br>
Accuracy of advanced features was: 0.732</br>
<p>The iteration of both of them is 150</p>
<p>Used Bigram to get Advanced features</p>
<p>For example:</p>
He likes cat</br>
PRP VBZ  NN</br>
My features is:
'TOKEN[0]=he','POS[0]=PRP','BOS','TOKEN[1]=likes','POS[1]=VBZ','TOKEN[0]|TOKEN[1]=he|likes','POS[0]|POS[1]=PRP|VBZ'<br>
And if it is the end of utterance, I will insert "EOS". If it is start of the utterance, I will insert "BOS"</br>
