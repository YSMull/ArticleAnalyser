#coding=utf8
import simplify_word as sw
import re

#读取已掌握单词列表
def load_known_words():
    known_file = u"public/known.txt"
    with open(known_file) as infile:
        known_words = []
        for eachLine in infile:
            known_words += [word for word in eachLine.split('\n')
                            if word != '']
        return known_words

def analysis_article(path_to_article, known_words):
    #打开要学习的文章

    filename = path_to_article
    with open(u"{0}".format(filename)) as infile:
        wordsLists = []
        for eachLine in infile:
            wordsLists += [sw.simplify_word(word.lower())
                                for word in re.split("[^A-Za-z]", eachLine)
                                    if word != ""
                                    and word[-1].islower()
                                    and word[0].islower()
                            ]#list comprehension
    #创建字典
    freq_of_eachword = {}
    for word in wordsLists:#初始化字典
        freq_of_eachword[word] = 0
    for word in wordsLists:#把单词加进来
        freq_of_eachword[word] += 1

    wordlist_order_by_freq = sorted(freq_of_eachword.iteritems(), key = lambda e:e[1], reverse = True)

    words_to_be_learned = list([p[0] for p in wordlist_order_by_freq if p[0] not in known_words])
    #print (str('do') in known_words)
    #print known_words
    print("words_to_be_learned", len(words_to_be_learned))


    result_file = open(u"r_{0}".format(re.split("[^a-zA-Z0-9\_\.]", path_to_article)[-1]), "w")

    for word in words_to_be_learned:
        result_file.write(u"{0}\n".format(word))

    #print "未识别的单词：{0}".format(sw.otherwordlist)
    return words_to_be_learned

