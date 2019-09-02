class rulessegmation(object):
    def __init__(self, dic_path):
        self.dictionary = set()
        self.maximum = 0
        #读取字典
        with open(dic_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if self.maximum < len(line):
                    self.maximum = len(line)

    def mmmcut(self,text):
        result = []
        index = 0
        while index < len(text):
            matched = False
            for i in range(self.maximum,0,-1):
                cand_word = text[index:index+i]
                if cand_word in self.dictionary:
                    result.append(cand_word)
                    matched = True
                    break
            if not matched:
                i = 1
                result.append(text[index])
            index +=i
        return result


    def rmmcut(self,text):
        result = []
        index = len(text)
        while index > 0:
            matched = False
            for i in range(self.maximum, 0 ,-1):
                tmp = i+1
                cand_word = text[index-tmp : index]
                if cand_word in self.dictionary:
                    result.append(cand_word)
                    matched = True
                    break
            if not matched:
                tmp = 1
                result.append(text[index-1])
            index -= tmp
        return result[::-1]

    def compute_single(word_list):
        num = 0
        for word in word_list:
            if len(word) == 1:
                num = num+1
        return num

    def bidiretionmmcut(self,text):
        forward_list = self.mmmcut(text)
        backward_list = self.rmmcut(text)
        count_forward_list = len(forward_list)
        count_backward_list = len(backward_list)
        count_single_forward_list = rulessegmation.compute_single(forward_list)
        print(count_single_forward_list)
        count_single_backward_list = rulessegmation.compute_single(backward_list)
        print(count_single_backward_list)
        if count_forward_list == count_backward_list:
            if count_single_forward_list > count_single_backward_list:
                return backward_list
            else:
                return forward_list
        elif count_backward_list >count_forward_list:
            return forward_list
        else:
            return backward_list


def main():
    text = '乒乓球拍卖完了南京市长江大桥'

    tokenizer = rulessegmation('./diction.txt')
    print(tokenizer.mmmcut(text))
    print(tokenizer.rmmcut(text))
    print(tokenizer.bidiretionmmcut(text))
main()