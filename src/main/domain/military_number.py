from src.main.CheckException.exceptional import ChkException
import re


class deidentify_military_number(ChkException):
    # 14-71230123
    military_number_regex = re.compile("\d{2}[-]\d{8}")
    result_military_number = []
    range_military_number = []

    def find_military_number(self):

        military_number_in_sentence = deidentify_military_number.military_number_regex.search(self.sentence)
        if military_number_in_sentence:
            deidentify_military_number.result_military_number.clear()
            deidentify_military_number.range_military_number.clear()
            return True
        else:
            return False

    def filter_military_number(self, sentence_group):
        military_number_group = sentence_group.group()
        military_number_group_filter = military_number_group.split("-")
        if deidentify_military_number.chk_only_number(self, sentence_group) and \
                deidentify_military_number.chk_arithmetic_sequence(self, military_number_group_filter[1]):
            deidentify_military_number.result_military_number.append(military_number_group)
            deidentify_military_number.range_military_number.append(sentence_group.span())

            return "**-********"
        else:
            return military_number_group
