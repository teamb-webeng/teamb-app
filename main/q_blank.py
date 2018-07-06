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


#ここがメインプログラム。filenameと、q_num(欲しい問題数)で、問題をq_num問だけ出力する。
#Ansをどういう形式にすべきかわからなかったので（ページ下部に出力？それとも、ページ上で答えられるようにする？）、暫定的に無視しています。
def q_blank(filename, q_num):
	f = open(filename, 'r')
	text = f.read()
	f.close()
	words = find_important_words(text)
	q_sets = make_blanked_question_set(words, text)
	print_questions(q_sets, 10) 

#文章を入力すると、重要単語と、その重要度(tf-idf)をdictk型で返す関数。
#本来はドキュメントがいくつもあるべきなんだけど、とりあえず一個の文章だけでやってます。(tf-idfの意味なしてないですね、すみません笑)
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
    # 重要度が高い順に並べ替えて出力
    words_dict = dict()
    data_collection = collections.Counter(term_imp)
    for cmp_noun, value in data_collection.most_common():
        word = termextract.core.modify_agglutinative_lang(cmp_noun)
        words_dict.update({word:value})
    return words_dict

#文章から単語を検索して、単語部分を＿＿＿に変更した問題文を作る関数。
#問題文はランダムでその単語を含む文章を持ってくる。各単語について、問題文一つを対応させたdictが出力
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

#問題文をq_num個分だけプリントする(多分ここは修正が必要)
def print_questions(q_dict, q_num):
    print("以下の空欄を埋めよ。\n")
    i = 0
    for q,a in q_dict.items():
        i = i + 1
        print("第" + str(i) + "問")
        print(q + '\n')
        if i == q_num: break

#プログラムが動くか確認する。sample.txtから問題を10問作る。
if __name__ == "__main__":
    q_blank('uploads/sample.txt', 10)


