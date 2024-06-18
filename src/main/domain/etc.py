from src.main.CheckException.exceptional import ChkException
import re


class deidentify_etc(ChkException):
    etc_regex = re.compile("[a-zA-Z가-힣]+은행")
    result_etc = []

    def find_etc(self):

        etc_in_sentence = deidentify_etc.etc_regex.search(self.sentence)
        if etc_in_sentence:
            deidentify_etc.result_etc.clear()
            return True
        else:
            return False

    def filter_etc(self, sentence_group):
        etc_group = sentence_group.group()
        deidentify_etc.result_etc.append(etc_group)
        return "*"*(len(etc_group)-2) + etc_group[-2:]


