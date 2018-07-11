# -*- coding: utf-8 -*-
import MeCab
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
m = MeCab.Tagger()
op = []
with open('kokoro.txt', mode = 'r') as f:        #open the file
    data = f.read()
    content = m.parse(data)                      #segmentation
    for row in content.split('\n'):           
        word = row.split('\t')[0]
        if word == 'EOS':
            break
        else:
            if (word != '\u3000'):
                op.append(word)                  #transfer txt to list
tf = CountVectorizer().fit_transform(op)         #creat a sparse matrix with words*appear_times
model = LatentDirichletAllocation(max_iter=100)  #can train more iterations for higher accuracy  
result = model.fit_transform(tf)                 #return words*probability(for every theme)
result_ = np.argmax(result,axis=1)               #label all words with the label
np.array(op).dump('article_list')                #save article
np.array(result_).dump('words_theme')            #save theme
demo = op[8:117]                                 #first paragraph
demo[17] = '__'                                  #choose the word 'sensei' as the question
sensei = result_[17]                             #theme No. of 'sensei'
choise = []
for i,j in enumerate(result_):
    if (j == sensei and op[i]!=op[17]):
        choise.append(op[i])
    if np.size(choise)==3:
        break
choise.append(op[17])                            #creat 4 choises
ans = ['A:',choise[0],'B:',choise[1],'C:',choise[2],'D:',choise[3]]
print('Question:\n',demo,'\nAnswer:\n',ans)
