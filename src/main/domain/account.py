from src.main.CheckException.exceptional import ChkException
import re

class deidentify_account(ChkException):

    regex_str = "(d{3}-\d{2}-\d{4}-\d{3})|(\d{6}-\d{2}-\d{6})|(\d{3}-\d{6}-\d{2}-\d{3})|(\d{3}-\d{4}-\d{4}-\d{2})|(\d{3}-\d{2}-\d{6})|(\d{3}-\d{3}-\d{6})|(\d{4}-\d{3}-\d{6})|(\d{3}-\d{6}-\d{5})|(\d{3}-\d{6}-\d{3})|(\d{3}-\d{6}-\d{3})|(\d{3}-\d{2}-\d{6}-\d{1})|(\d{3}-\d{4}-\d{4}-\d{2})|(\d{3}-\d{2}-\d{6})|(\d{3}-\d{3}-\d{6})|(\d{4}-\d{2}-\d{7})|(\d{3}-\d{7}-\d{1}-\d{3})|(\d{3}-\d{2}-\d{6}-\d{1})|(\d{4}-\d{4}-\d{4}-\d{1})"
    account_regex = re.compile(regex_str)
    result_account = []
    range_account = []

    def find_account(self):
        account_in_sentence = deidentify_account.account_regex.search(self.sentence)
        if account_in_sentence:
            deidentify_account.result_account.clear()
            deidentify_account.range_account.clear()
            return True
        else:
            return False

    def filter_account(self, sentence_group):
        account_group = sentence_group.group()
        if deidentify_account.chk_only_number(self, sentence_group):
            account_group_split = account_group.split("-")
            if deidentify_account.chk_arithmetic_sequence(self, "-".join([i for i in account_group_split if len(i) > 4])):
                deidentify_account.result_account.append(account_group)
                deidentify_account.range_account.append(sentence_group.span())
                tmp = account_group_split[0]
                for i in account_group_split[1:]:
                    tmp = "-".join([tmp, len(i)*"*"])
                return tmp
            else:
                return account_group
        else:
            return account_group
