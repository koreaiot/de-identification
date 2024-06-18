from src.main.CheckException.exceptional import ChkException
import re


class deidentify_ssn(ChkException):
    ssn_regex = re.compile("\d{2}([0]\d|[1][0-2])([0][1-9]|[1-2]\d|[3][0-1])[- ][1-8]\d{6}")
    result_ssn = []
    range_ssn = []

    def find_ssn(self):

        ssn_in_sentence = deidentify_ssn.ssn_regex.search(self.sentence)

        if ssn_in_sentence:
            deidentify_ssn.result_ssn.clear()
            deidentify_ssn.range_ssn.clear()
            return True
        else:
            return False

    def filter_ssn(self, sentence_group):
        ssn_group = sentence_group.group()

        if deidentify_ssn.chk_only_number(self, sentence_group):
            ssn_group_filter = ssn_group.replace("-", "").replace(" ", "")
            if deidentify_ssn.chk_arithmetic_sequence(self, ssn_group_filter[6:]):
                if ssn_group_filter[0] < "3":  # 2000년대
                    if ssn_group_filter[6] == "3" or ssn_group_filter[6] == "4" or ssn_group_filter[6] == "7" or \
                            ssn_group_filter[6] == "8":  # 성별숫자 확인
                        deidentify_ssn.result_ssn.append(ssn_group)
                        deidentify_ssn.range_ssn.append(sentence_group.span())
                        return "".join([ssn_group_filter[0], "*" * 5, "-", ssn_group_filter[6], "*" * 6])
                    else:
                        return ssn_group
                else:  # 1900년대
                    if ssn_group_filter[6] == "1" or ssn_group_filter[6] == "2" or ssn_group_filter[6] == "5" or \
                            ssn_group_filter[6] == "6":  # 성별숫자 확인

                        deidentify_ssn.result_ssn.append(ssn_group)
                        deidentify_ssn.range_ssn.append(sentence_group.span())
                        return "".join([ssn_group_filter[0], "*" * 5, "-", ssn_group_filter[6], "*" * 6])
                    else:
                        return ssn_group
            else:
                return ssn_group
        else:
            return ssn_group
