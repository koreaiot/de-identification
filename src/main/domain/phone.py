from src.main.CheckException.exceptional import ChkException
import re


class deidentify_phone_number(ChkException):
    phone_number_regex = re.compile("((01)([0|1|6|7|8|9])|02|0[3-6][1-5]|070)[- ]?\d{3,4}[- ]?\d{4}")
    result_phone_number = []
    range_phone_number = []

    def find_phone_number(self):

        phone_number_in_sentence = deidentify_phone_number.phone_number_regex.search(self.sentence)

        if phone_number_in_sentence:
            deidentify_phone_number.result_phone_number.clear()
            deidentify_phone_number.range_phone_number.clear()
            return True
        else:
            return False

    def filter_phone_number(self, sentence_group):
        phone_group = sentence_group.group()

        if deidentify_phone_number.chk_only_number(self, sentence_group):
            phone_group_filter = phone_group.replace("-", "").replace(" ", "")

            if phone_group_filter[:3] == "010":
                if deidentify_phone_number.chk_arithmetic_sequence(self, "-".join([phone_group_filter[3:7], phone_group_filter[7:]])):
                    deidentify_phone_number.result_phone_number.append(phone_group)
                    deidentify_phone_number.range_phone_number.append((sentence_group.start(), sentence_group.end()))
                    if " " in phone_group:
                        return " ".join([phone_group_filter[:3], "*" * (len(phone_group_filter) - 7), "*" * 4])
                    elif "-" in phone_group:
                        return "-".join([phone_group_filter[:3], "*" * (len(phone_group_filter) - 7), "*" * 4])
                    else:
                        return "".join([phone_group[:3], "*"*(len(phone_group_filter) - 3)])

                else:
                    return phone_group

            elif phone_group_filter[:2] == "02":
                if deidentify_phone_number.chk_arithmetic_sequence(self, "-".join([phone_group_filter[2:-4],phone_group_filter[-4:]])):
                    deidentify_phone_number.result_phone_number.append(phone_group)
                    deidentify_phone_number.range_phone_number.append((sentence_group.start(), sentence_group.end()))
                    if " " in phone_group:
                        return " ".join([phone_group_filter[:2], "*" * (len(phone_group_filter) - 6), "*" * 4])
                    elif "-" in phone_group:
                        return "-".join([phone_group_filter[:2], "*" * (len(phone_group_filter) - 6), "*" * 4])
                    else:
                        return "".join([phone_group[:2], "*"*(len(phone_group_filter) - 2)])
                else:
                    return phone_group

            # elif: 0507, +82-10, +82-010, +82010

            else:  # 010, 02 제외 나머지
                if deidentify_phone_number.chk_arithmetic_sequence(self, "-".join(
                        [phone_group_filter[3:-4], phone_group_filter[-4:]])):
                    deidentify_phone_number.result_phone_number.append(phone_group)
                    deidentify_phone_number.range_phone_number.append((sentence_group.start(), sentence_group.end()))
                    if " " in phone_group:
                        return " ".join([phone_group_filter[:3], "*" * (len(phone_group_filter) - 7), "*" * 4])
                    elif "-" in phone_group:
                        return "-".join([phone_group_filter[:3], "*" * (len(phone_group_filter) - 7), "*" * 4])
                    else:
                        return "".join([phone_group[:3], "*"*(len(phone_group_filter) - 3)])
                else:
                    return phone_group

        else:
            return phone_group
