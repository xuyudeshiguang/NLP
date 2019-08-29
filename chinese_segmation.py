# -*- coding; utf-8 -*-
#基于规则的分词是一种机械分词的方法,主要是通过维护字典,在切分语句时,将语句的每个字符串与词表中的词进行逐一匹配,找到则切分,否则不予切分.
#正向匹配(Maximum Match Method)
#假定分词词典中的最长词有i个字符,则用被处理文档的当前字符串中的前i个字作为匹配字段,查找字典.
#若字典中存在这样的一个i字词,则匹配成功,匹配字段被作为一个词切分出来.
#如果字典中找不到,则匹配失败,将匹配字段中的最后一个字去掉,对剩下的字串重新进行匹配处理.
#如此循环下去,直到匹配成功,即切分出一个词或剩余字串的长度为零为止.
#这样就完成了一轮匹配,然后取下一个i个字串进行匹配处理直到文档被扫描完为止.
def max_forward_cut(sentence):
    cutlist = []
    index = 0
    max_wordlen = 3
    while index < len(sentence):
        matched = False
        for i in range(max_wordlen, 0, -1):
            cand_word = sentence[index : index + i]
            if cand_word in word_dict:
                cutlist.append(cand_word)
                matched = True
                break
        #如果没有匹配上,则按字符切分
        if not matched:
            i = 1
            cutlist.append(sentence[index])
        index += i
    return cutlist

#逆向匹配(Reverse Maximum Match Method)
#从被处理文档的末端开始匹配扫描,每次去最末端的i个字符作为匹配字段
#若匹配成功,则切分,匹配失败,则去掉匹配字段最前面的一个字,继续匹配.
def max_backward_cut(sentence):
    cutlist = []
    index = len(sentence)
    max_wordlen = 3
    while index > 0 :
        matched = False
        for i in range(max_wordlen, 0, -1):
            tmp = i+1
            cand_word = sentence[index -tmp : index]
            #如果匹配上, 则将字典中的字符加入到切分字符中
            if cand_word in word_dict:
                cutlist.append(cand_word)
                matched = True
                break
        #如果没有匹配上,则按字符切分
        if not matched:
            tmp = 1
            cutlist.append(sentence[index-1])

        index -= tmp

    return cutlist[::-1]


#双向匹配.根据启发式规则进行选取:1,如果正反向分词结果词数不同,则取分词数量较少的那个
#2,如果正反向分词结果词数相同, 则对比分词结果. 分词结果相同,则没有歧义,返回任意结果. 分词结果不同,返回其中单字较少的那个.
def compute_single(word_list):
    num = 0
    for word in word_list:
        if len(word) == 1:
            num = num+1
    return num

def max_biward_cut(sentence):
    forward_cutlist = max_forward_cut(sentence)
    backward_cutlist = max_backward_cut(sentence)
    count_forward_cutlist = len(forward_cutlist)
    count_backward_cutlist = len(backward_cutlist)

    if count_forward_cutlist == count_backward_cutlist:
        if compute_single(forward_cutlist) > compute_single(backward_cutlist):
            return backward_cutlist
        else:
            return forward_cutlist
    elif count_backward_cutlist > count_forward_cutlist:
        return forward_cutlist
    else:
        return backward_cutlist


#待分词的句子
raw_sent = u'乒乓球拍卖完了'

#构建字典
words = u"乒乓 乒乓球 球拍 拍卖 卖完 "
word_dict = words.strip().split(" ")
print('字典内容;')
for word in word_dict:
    print(word)
forward_seg_list = max_forward_cut(raw_sent)
print(forward_seg_list)
backward_seg_list = max_backward_cut(raw_sent)
print(backward_seg_list)
biward_seg_lsit = max_biward_cut(raw_sent)
print(biward_seg_lsit)
