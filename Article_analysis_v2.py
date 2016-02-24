#coding=utf8
import simplify_word as sw
import re

#读取已掌握单词列表
def load_known_words():
	known_file = u"public/known.txt"
	infile = open(known_file)
	known_words = []
	for eachLine in infile:
	    known_words += [word for word in eachLine.split('\n')
	                            if word != '']
	infile.close()
	return known_words


def analysis_article(path_to_article, known_words):
    #打开要学习的文章
	filename = path_to_article
	infile = open(u"{0}".format(filename))
	all_sentence = []
	wordsLists = []
	for eachLine in infile:
	    #不同编码下的空行有差异，因此限制读入的行的长度必须大于1(万一一行只有一个句子呢？)
	    #干脆就直接处理吧，反正空行也读不出单词来
	    #windows下换行符是\r\n，unix下是\n
	    all_sentence += [sentence for sentence in re.split("[\.]",eachLine) if sentence != ""]
	infile.close()

	for sentence in all_sentence:
		wordsLists+=[(sw.simplify_word(word.lower()), sentence)
							for word in re.split("[^A-Za-z]", sentence)
											if word != ""
											and word[-1].islower()
											and word[0].islower()
							]
	ZIDIAN = {}
	for i,a in enumerate(set(wordsLists)):
		ZIDIAN[a[0]] = a[1]

	#没必要统计词的频率并排序啊，真的
	words_to_be_learned = list(set(list([p[0] for p in wordsLists if p[0] not in known_words])))

	return words_to_be_learned, ZIDIAN
	#print "未识别的单词：{0}".format(sw.otherwordlist)
	# print words_to_be_learned
	#20th的th会被加进来诶
