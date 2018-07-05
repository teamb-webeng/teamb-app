import sys
import dbm
from janome.tokenizer import Tokenizer
import termextract.janome
import termextract.core
import MeCab
import termextract.mecab
#import termextract.core
import collections
import re
import random


def q_blank(filename, q_num):
	f = open(filename, 'r')
	text = f.read()
	f.close()
	words = find_important_words(text)
	q_sets = make_blanked_question_set(words, text)
	print_questions(q_sets, 10) 

#
def find_important_words(text):
    m = MeCab.Tagger()
    result = m.parse(text)
    tagged_text = result
	# 複合語を抽出し、重要度を算出
    frequency = termextract.mecab.cmp_noun_dict(tagged_text)
    LR = termextract.core.score_lr(frequency,
         ignore_words=termextract.mecab.IGNORE_WORDS,
         lr_mode=1, average_rate=1)   
    term_imp = termextract.core.term_importance(frequency, LR)
    # 重要度が高い順に並べ替えて出
    words_dict = dict()
    data_collection = collections.Counter(term_imp)
    for cmp_noun, value in data_collection.most_common():
        word = termextract.core.modify_agglutinative_lang(cmp_noun)
        words_dict.update({word:value})
    return words_dict

def make_blanked_question_set(words_dict, text):
    sentences = re.split('。', text) 
    q_dict = dict()
    for word, value in words_dict.items():
        q_for_word = list()
        for sentence in sentences:
            m = re.search(word, sentence)
            if m is not None:
                q = re.sub(word, '_____', sentence)
                q_for_word.append(q)
        q_random = q_for_word[random.randrange(len(q_for_word))]
        q_dict.update({q_random:word})   
    return q_dict 

def print_questions(q_dict, q_num):
    print("以下の空欄を埋めよ。")
    i = 0
    for q,a in q_dict.items():
        i = i + 1
        print("第" + str(i) + "問")
        print(q)
        if i == q_num: break

if __name__ == "__main__":
    q_blank('uploads/sample.txt', 10)


