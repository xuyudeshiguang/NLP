# -*- coding; utf-8 -*-

#正向匹配
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

#逆向匹配
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