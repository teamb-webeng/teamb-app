import numpy as np
import random

article_list = np.load('article_list')
words_theme = np.load('words_theme')

'''
To generate a problem, letting word at word_index to become a blank
'''
def generateProblem(word_index, words, themes):
    # First, save the answer word
    ans = words[word_index]
    # Second, set the original place as blank
    words[word_index] = '____'
    # Save the theme of that word, which is a int number
    mytheme = themes[word_index]
    choices = list()
    # Random generate the answer index
    ans_index = random.randint(0, 3)
    L = len(words)
    # Generate selection
    for i in range(4):
        if i == ans_index:
            choices.append(ans)
        else:
            flag = 0
            while not flag:
                random_candidate_index = random.choice(range(L))
                if themes[random_candidate_index] == mytheme and words[random_candidate_index] != ans:
                    choices.append(words[random_candidate_index])
                    flag = 1

    question = words[word_index]
    for i in range(word_index+1, L):
        question += words[i]
        if words[i] == '。':
            break
    for i in range(1, word_index+1):
        if words[word_index - i] == '。':
            break
        question = words[word_index - i] + question
    ret = {'question': question, 'choices': choices, 'answer': ans_index}
    words[word_index] = ans
    return ret


def genMultiProblems(multiIndex, words, themes):
    ret = list()
    for index in multiIndex:
        ret.append(generateProblem(index, words, themes))
    return ret


if __name__ == '__main__':
    print(generateProblem(110, article_list, words_theme))
    print(genMultiProblems([110, 26, 200], article_list, words_theme))
