from src.main.CheckException.exceptional import ChkException
import re


class deidentify_age(ChkException):
    age_regex = re.compile("(\d{1,2}[-.,~])?\d{1,4}(년생(각)?|살(까|래|지)?|세(대|기|트)?)|([1-6]학년 ?\d{1,2}반)")
    result_age = []
    range_age = []

    def find_age(self):

        age_in_sentence = deidentify_age.age_regex.search(self.sentence)
        if age_in_sentence:
            deidentify_age.result_age.clear()
            deidentify_age.range_age.clear()
            return True
        else:
            return False

    def filter_age(self, sentence_group):
        age_group = sentence_group.group()
        if age_group[-1] in ["기", "대", "트","까","래","지","각"]:
            return age_group
        else:
            numbers = re.findall('\d+', age_group)
            strings = re.findall('[가-힣~,.-]+', age_group)
            if strings[0] != "년생" and len(numbers[0]) > 2: #100살이 넘을 때,
                return age_group
            elif numbers[0] == "2" and strings[0] == "세":  #2세일 때,
                return age_group
            elif len(numbers) == 2 and len(strings) == 2:
                deidentify_age.result_age.append(age_group)
                deidentify_age.range_age.append(sentence_group.span())
                return "".join(["*"*len(numbers[0]), strings[0],"*"*len(numbers[1]),strings[1]])
            else:
                deidentify_age.result_age.append(age_group)
                deidentify_age.range_age.append(sentence_group.span())
                return "".join(["*" * len(numbers[0]), strings[0]])
