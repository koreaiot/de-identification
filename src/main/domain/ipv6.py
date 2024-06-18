from src.main.CheckException.exceptional import ChkException
import re


class deidentify_ipv6(ChkException):
    ipv6 = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{" \
           "1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1," \
           "3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1," \
           "5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0," \
           "4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3," \
           "3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0," \
           "1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    ipv6_regex = re.compile(ipv6)
    result_ipv6 = []
    range_ipv6 = []

    def find_ipv6(self):

        ipv6_in_sentence = deidentify_ipv6.ipv6_regex.search(self.sentence)
        if ipv6_in_sentence:
            deidentify_ipv6.result_ipv6.clear()
            deidentify_ipv6.range_ipv6.clear()
            return True
        else:
            return False

    def filter_ipv6(self, sentence_group):
        ipv6_group = sentence_group.group()
        deidentify_ipv6.result_ipv6.append(ipv6_group)
        deidentify_ipv6.range_ipv6.append(sentence_group.span())

        ipv6_group_split = ipv6_group.split(":")
        tmp = ipv6_group_split[0]
        for i in ipv6_group_split[1:]:
            tmp = ":".join([tmp, len(i) * "*"])
        return tmp

        """
            MAC주소 = ([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}
        """
