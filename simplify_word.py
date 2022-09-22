#coding=utf8
from pattern.en import tag
import time
# otherwordlist = []
def simplify_word(a):
    """
    # print "[{0}],正在分析词汇: {1}".format(time.ctime().split()[3], a),

    try:#测试是否为动词,如果是则返回
        try_present_verb = en.verb.present(a)#try
        if en.is_verb(try_present_verb):
            # if try_present_verb != a:
            #     print " 动词现在时化：{0} -> {1}".format(a,try_present_verb)
            # else:
            #     print ""
            return try_present_verb
    except:#否则继续检查
        pass

    #测试是否是名词
    try_singular_noun = en.noun.singular(a)
    if en.is_noun(try_singular_noun):
        # if try_singular_noun != a:
        #     print " 名词单数化：{0} -> {1}".format(a,try_singular_noun)
        # else:
        #     print ""
        return try_singular_noun

    #如果已经可以判断是名词,动词,形容词,副词,连词
    if en.is_noun(a) or en.is_verb(a) or en.is_adjective(a) or en.is_adverb(a) or en.is_connective(a):
        # print ""
        return a

    return ''

    # print "!无法归类，舍弃"

    #print "无法识别{0}".format(a)
    #otherwordlist.append(a)
    #这么屌的库都不认识的单词还返回个毛线，自己查字典去...

    #return a
    """
    _ = tag(a)
    return a
