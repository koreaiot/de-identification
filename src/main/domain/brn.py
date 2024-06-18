from src.main.CheckException.exceptional import ChkException
import re


"""
    개인정보 해당 안됨.
    해당 도메인 삭제 예정
"""
class deidentify_brn(ChkException):
    # 123-45-67890
    brn_regex = re.compile("\d{3}[-]\d{2}[-]\d{5}")
    result_brn = []
    range_brn = []

    def find_brn(self):

        brn_in_sentence = deidentify_brn.brn_regex.search(self.sentence)
        if brn_in_sentence:
            deidentify_brn.result_brn.clear()
            deidentify_brn.range_brn.clear()
            return True
        else:
            return False

    def filter_brn(self, sentence_group):
        brn_group = sentence_group.group()
        if deidentify_brn.chk_only_number(self, sentence_group) and \
                deidentify_brn.chk_arithmetic_sequence(self, brn_group):
            deidentify_brn.result_brn.append(brn_group)
            deidentify_brn.range_brn.append(sentence_group.span())
            return "***-**-*****"
        else:
            return brn_group
