from src.main.CheckException.exceptional import ChkException
import re


class deidentify_passport(ChkException):
    passport_regex = re.compile("[MSGDRmsgdr](\d{8}|\d{3}[a-zA-Z]\d{4})")

    result_passport = []

    def find_passport(self):

        passport_in_sentence = deidentify_passport.passport_regex.search(self.sentence)
        if passport_in_sentence:
            deidentify_passport.result_passport.clear()
            return True
        else:
            return False

    def filter_passport(self, sentence_group):
        passport_group = sentence_group.group()
        if deidentify_passport.chk_char_number(self, sentence_group):
            if deidentify_passport.chk_arithmetic_sequence(self,"".join([i for i in passport_group if i.isdigit()])):
                deidentify_passport.result_passport.append(passport_group)
                return "".join([passport_group[0], "*" * len(passport_group[1:])])
            else:
                return passport_group
        else:
            return passport_group
