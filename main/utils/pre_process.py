# -*- coding: utf-8 -*-
import MeCab
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def pre_processing(filename):
    m = MeCab.Tagger()
    op = []
    with open(filename, mode='r') as f:  # open the file
        data = f.read()
        content = m.parse(data)  # segmentation
        for row in content.split('\n'):
            word = row.split('\t')[0]
            if word == 'EOS':
                break
            else:
                if (word != '\u3000'):
                    op.append(word)  # transfer txt to list
    # creat a sparse matrix with words*appear_times
    tf = CountVectorizer().fit_transform(op)
    # can train more iterations for higher accuracy
    model = LatentDirichletAllocation(max_iter=100)
    # return words*probability(for every theme)
    result = model.fit_transform(tf)
    result_ = np.argmax(result, axis=1)  # label all words with the label
    np.array(op).dump('main/uploads/article_list')  # save article
    np.array(result_).dump('main/uploads/words_theme')  # save theme


if __name__ == "__main__":
    pre_processing('kokoro.txt')
