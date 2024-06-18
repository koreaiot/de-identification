from src.main.CheckException.exceptional import ChkException
import re


class deidentify_pccc(ChkException):
    pccc_regex = re.compile("(([a-zA-Z가-힣*]){4}\d{7})|[pP]\d{12}")
    result_pccc = []

    def find_pccc(self):

        pccc_in_sentence = deidentify_pccc.pccc_regex.search(self.sentence)
        if pccc_in_sentence:
            deidentify_pccc.result_pccc.clear()
            return True
        else:
            return False

    def filter_pccc(self, sentence_group):
        pccc_group = sentence_group.group()
        if deidentify_pccc.chk_char_number(self, sentence_group):
            if deidentify_pccc.chk_arithmetic_sequence(self, "".join([i for i in pccc_group if i.isdigit()])):
                deidentify_pccc.result_pccc.append(pccc_group)
                return "".join([pccc_group[0], "*" * len(pccc_group[1:])])
            else:
                return pccc_group
        else:
            return pccc_group
