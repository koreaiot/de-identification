from src.main.CheckException.exceptional import ChkException
import re


class deidentify_ipv4(ChkException):
    ipv4_regex = re.compile("(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}(:\d{4})?([/~]\d{0,3})?")
    result_ipv4 = []
    range_ipv4 = []

    def find_ipv4(self):

        ipv4_in_sentence = deidentify_ipv4.ipv4_regex.search(self.sentence)
        if ipv4_in_sentence:
            deidentify_ipv4.result_ipv4.clear()
            deidentify_ipv4.range_ipv4.clear()
            return True
        else:
            return False

    def filter_ipv4(self, sentence_group):
        ipv4_group = sentence_group.group()
        if len(self.sentence) != sentence_group.end() and \
            self.sentence[sentence_group.end()] == ".":
            return ipv4_group
        if deidentify_ipv4.chk_only_number(self, sentence_group):
            # and deidentify_ipv4.chk_arithmetic_sequence(self, ipv4_group):

            deidentify_ipv4.result_ipv4.append(ipv4_group)
            deidentify_ipv4.range_ipv4.append(sentence_group.span())
            if ":" in ipv4_group:
                return ".".join([ipv4_group.split(".")[0],
                                 len(ipv4_group.split(".")[1]) * "*",
                                 len(ipv4_group.split(".")[2]) * "*",
                                 len(ipv4_group.split(".")[3].split(":")[0]) * "*"]) + ":****"

            elif "~" in ipv4_group:
                return ".".join([ipv4_group.split(".")[0],
                                 len(ipv4_group.split(".")[1]) * "*",
                                 len(ipv4_group.split(".")[2]) * "*",
                                 len(ipv4_group.split(".")[3].split("~")[0]) * "*"]) +"~"+ len(ipv4_group.split(".")[3].split("~")[1]) * "*"

            elif "/" in ipv4_group:
                return ".".join([ipv4_group.split(".")[0],
                                 len(ipv4_group.split(".")[1]) * "*",
                                 len(ipv4_group.split(".")[2]) * "*",
                                 len(ipv4_group.split(".")[3].split("/")[0]) * "*"]) +"/"+ len(ipv4_group.split(".")[3].split("/")[1]) * "*"

            else:
                return ".".join([ipv4_group.split(".")[0],
                                 len(ipv4_group.split(".")[1]) * "*",
                                 len(ipv4_group.split(".")[2]) * "*",
                                 len(ipv4_group.split(".")[3]) * "*"])
        else:
            return ipv4_group

        """
            IPv6주소 = (([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|
            ([0-9a-fA-F]{1,4}:){1,7}:|
            ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|
            ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|
            ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|
            ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|
            ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|
            [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|
            fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|
            ::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|
            1{0,1}[0-9]){0,1}[0-9])\.){3,3}
            (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|
            ([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.)
            {3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))
            
            MAC주소 = ([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}
        """
