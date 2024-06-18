from src.main.CheckException.exceptional import ChkException
import re


class deidentify_email(ChkException):
    email_regex = re.compile('[a-zA-Z0-9+\-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    result_email = []
    range_email = []

    def find_email(self):

        email_in_sentence = deidentify_email.email_regex.search(self.sentence)
        if email_in_sentence:
            deidentify_email.result_email.clear()
            deidentify_email.range_email.clear()
            return True
        else:
            return False

    def filter_email(self, sentence_group):
        email_group = sentence_group.group()
        idx_a = email_group.index("@")
        idx_dot = email_group.rfind(".")
        deidentify_email.result_email.append(email_group)
        deidentify_email.range_email.append(sentence_group.span())
        return email_group[0]+'*'*(idx_a-1)+'@'+'*'*(idx_dot-idx_a-1)+email_group[idx_dot:]


