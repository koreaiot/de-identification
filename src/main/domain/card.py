from ..CheckException.exceptional import ChkException
from ..setting_variable import bin_number_list
import re


class deidentify_card_number(ChkException):
    card_number_regex = re.compile("[34569][0-9]{3}[- ]\d{4}[- ]\d{4}[- ]\d{4}")
    result_card_number = []
    range_card_number = []

    def find_card_number(self):

        card_number_in_sentence = deidentify_card_number.card_number_regex.search(self.sentence)

        if card_number_in_sentence:
            deidentify_card_number.result_card_number.clear()
            deidentify_card_number.range_card_number.clear()
            return True
        else:
            return False

    def filter_card_number(self, sentence_group):

        card_idx = {
            "3": (0, 48),
            "4": (48, 208),
            "5": (208, 348),
            "6": (348, 414),
            "9": (414, 558)
        }
        card_number_group = sentence_group.group()

        if deidentify_card_number.chk_only_number(self, sentence_group):
            card_number_group_filter = card_number_group.replace("-", "").replace(" ", "")
            first_card_number = card_number_group_filter[0]
            first_group_card_number = card_number_group_filter[:6]
            if first_card_number in card_idx.keys() and \
                    first_group_card_number in bin_number_list[card_idx[first_card_number][0]:card_idx[first_card_number][1]]:
                digits = []
                for i in card_number_group_filter:
                    digits.append(int(i))
                sum_ = 0
                is_even_number = False

                for i in range(len(digits) - 1, -1, -1):
                    if is_even_number:  # 짝수인 경우
                        digits[i] *= 2
                        if digits[i] > 9:
                            digits[i] -= 9

                    sum_ += digits[i]
                    is_even_number = not is_even_number

                # 10의 배수인 경우 유효함
                if sum_ % 10 != 0:
                    return card_number_group

                else:
                    deidentify_card_number.result_card_number.append(card_number_group)
                    deidentify_card_number.range_card_number.append(sentence_group.span())
                    return "-".join([card_number_group_filter[:4], "*" * 4, "*" * 4, "*" * 4])
            else:
                return card_number_group
        else:
            return card_number_group
