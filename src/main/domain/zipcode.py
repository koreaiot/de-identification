from src.main.CheckException.exceptional import ChkException
import re


class deidentify_zipcode(ChkException):
    zipcode_regex = re.compile("\((0[1-9]|[1-5][0-9]|6[0-3])\d{3}\)")
    result_zipcode = []

    def find_zipcode(self):

        zipcode_in_sentence = deidentify_zipcode.zipcode_regex.search(self.sentence)
        if zipcode_in_sentence:
            deidentify_zipcode.result_zipcode.clear()
            return True
        else:
            return False

    def filter_zipcode(self, sentence_group):
        zipcode_group = sentence_group.group()
        if deidentify_zipcode.chk_only_number(self, sentence_group):
            deidentify_zipcode.result_zipcode.append(zipcode_group)
            return "*****"
        else:
            return zipcode_group
