from src.main.CheckException.exceptional import ChkException
import re


class deidentify_url(ChkException):
    url_regex = re.compile(
        '((https?|file|ftp|mailto|ssh|tel)://)?(www\.)?[a-zA-Z]+[a-zA-Z0-9-@:%._+~#=@]{2,256}\.[\?:+%@a-zA-Z0-9/.#&=_-]+')
    result_url = []
    range_url = []

    def find_url(self):

        url_in_sentence = deidentify_url.url_regex.search(self.sentence)
        if url_in_sentence:
            deidentify_url.result_url.clear()
            deidentify_url.range_url.clear()
            return True
        else:
            return False

    def filter_url(self, sentence_group):
        url_group = sentence_group.group()
        if ".." in url_group:
            return url_group
        if ".com" in url_group or ".kr" in url_group or ".net" in url_group or \
                ".org" in url_group or ".edu" in url_group or ".gov" in url_group or \
                ".mil" in url_group or ".info" in url_group or ".biz" in url_group or \
                ".cat" in url_group or ".ai" in url_group or ".asia" in url_group or \
                ".jobs" in url_group or ".mobi" in url_group or ".tel" in url_group or \
                ".xxx" in url_group or ".so" in url_group or ".io" in url_group:
            deidentify_url.result_url.append(url_group)
            deidentify_url.range_url.append(sentence_group.span())
            url_group_split = url_group.split(".")
            if len(url_group_split) == 2:
                if "/" in url_group_split[1]:
                    url_group_split_1_split = url_group_split[1].split("/")
                    masked_strings_with_slash = "/".join([url_group_split_1_split[0]] + ['*' * len(s) for s in url_group_split_1_split[1:]])
                    return "*" * len(url_group_split[0]) + "." + masked_strings_with_slash
                else:
                    return "*" * len(url_group_split[0]) + "." + url_group_split[1]
            period = ".".join([url_group_split[0], "*" * len(".".join(url_group_split[1:-1]))]) + "."
            if "/" in url_group_split[-1]:
                result = url_group_split[-1].split("/")[0]
                for slash in url_group_split[-1].split("/")[1:]:
                    result += "/" + "*" * len(slash)
                return period + result
            else:
                return period + url_group_split[-1]
        else:
            return url_group



