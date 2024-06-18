import src.main.setting_variable
import src.main.result.domain_info
import src.main.setting_variable
from ...setting_variable import bank_account_regex_list
import re
import datetime
import numpy as np

now = datetime.datetime.now()

domain_cnt_dict = {}
domain_time_dict = {}
original_lst, changed_lst, filter_word_lst = [], [], []


def django_data(domain_cls_lst, sentence_django) -> str:
    """
        커스텀 문장 필터링 -> django website 출력
    """
    filter_dict = {}
    filter_range_lst, rich_original_lst, rich_info_lst = [], [], []

    sentence = sentence_django
    domain_lst, filter_domain_lst = [], []
    for domain_class in domain_cls_lst:
        domain = "_".join(domain_class.__name__.split("_")[1:])
        domain_lst.append(domain)
        if domain == "account":
            for i in bank_account_regex_list:
                domain_class.account_regex = re.compile(i)
                if eval(f'domain_class(sentence).find_{domain}()'):
                    comp_sentence = eval(
                        f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
                    if sentence == comp_sentence:
                        continue
                    else:
                        eval(f"domain_class.result_{domain}")
                        filter_range_lst += eval(f"domain_class.range_{domain}")
                        filter_domain_lst.append(domain)
                        sentence = comp_sentence

                        for k in eval(f"domain_class.range_{domain}"):
                            filter_dict[k] = domain
                        # if not domain in filter_dict.keys():
                        #     filter_dict[domain] = eval(f"domain_class.range_{domain}")
                        # else:
                        #     filter_dict[domain] += eval(f"domain_class.range_{domain}")

        elif eval(f'domain_class(sentence).find_{domain}()'):
            comp_sentence = eval(
                f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
            if sentence == comp_sentence:
                continue
            else:
                eval(f"domain_class.result_{domain}")
                filter_range_lst += eval(f"domain_class.range_{domain}")
                filter_domain_lst.append(domain)
                sentence = comp_sentence

                for k in eval(f"domain_class.range_{domain}"):
                    filter_dict[k] = domain

                # if not domain in filter_dict.keys():
                #     filter_dict[domain] = eval(f"domain_class.range_{domain}")
                # else:
                #     filter_dict[domain] += eval(f"domain_class.range_{domain}")

    print(filter_dict)
    tmp = list(dict(sorted(filter_dict.items())).values())

    if filter_dict:
        span_lst = sorted(list(np.concatenate(filter_range_lst)))
        span_lst_length = len(span_lst)

        num = 0
        for i in range(span_lst_length):  # 추출 단어: 굵은 빨간색
            if i == 0:
                if sentence[:span_lst[i]] != "":
                    rich_info_lst.append((sentence[0:span_lst[i]], False, None))
                    rich_original_lst.append((sentence_django[0:span_lst[i]], False, None))
            elif i % 2 == 0:
                if sentence[span_lst[i - 1]:span_lst[i]] != "":
                    rich_info_lst.append((sentence[span_lst[i - 1]:span_lst[i]], False, None))
                    rich_original_lst.append((sentence_django[span_lst[i - 1]:span_lst[i]], False, None))

            elif i % 2 == 1:   # 이것만 True
                if sentence[span_lst[i - 1]:span_lst[i]] != "":
                    rich_info_lst.append((sentence[span_lst[i - 1]:span_lst[i]], True, tmp[num]))
                    rich_original_lst.append((sentence_django[span_lst[i - 1]:span_lst[i]], True, tmp[num]))
                    num += 1

        if sentence[span_lst[span_lst_length - 1]:] != "":
            rich_info_lst.append((sentence[span_lst[i]:], False, None))
            rich_original_lst.append((sentence_django[span_lst[i]:], False, None))
        print("==================오리지날==================", rich_original_lst)
        print("==================문제요소==================", rich_info_lst)
    return sentence, domain_lst, rich_info_lst, rich_original_lst

