import src.main.result.domain_info
import src.main.setting_variable
from ...setting_variable import bank_account_regex_list, sentence_lst
from ..domain_info import DomainInfo

import re
import time

domain_cnt_dict = {}
domain_time_dict = {}
original_lst, changed_lst, filter_word_lst = [], [], []


def my_example_to_excel(domain_cls_lst, time_now):

    my_example = DomainInfo(domain_cls_lst, "my_example", time_now)
    for sentence in sentence_lst:
        my_example.func_run(sentence,"파일명.json")

    my_example.subject.make_excel(my_example.domain_time_dict,
                                  my_example.domain_cnt_dict,
                                  my_example.domain_lst,
                                  1,
                                  len(sentence_lst))


def my_example_bank(domain_class, domain, sentence, excel) -> str:
    global domain_cnt_dict, original_lst, changed_lst, filter_word_lst, tmp
    for i in bank_account_regex_list:
        domain_class.account_regex = re.compile(i)
        if eval(f'domain_class(sentence).find_{domain}()'):
            comp_sentence = eval(
                f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
            if sentence == comp_sentence:
                continue
            elif excel == "print":
                print("☆원본 :", sentence)
                print(f"★필터({domain}) :", comp_sentence)
                print("▶바뀐문장 :", eval(f"domain_class.result_{domain}"), end="\n\n")
                sentence = comp_sentence
            elif excel == "django":
                eval(f"domain_class.result_{domain}")
                sentence = comp_sentence
            else:  # Excel 추출
                filter_word = eval(f"domain_class.result_{domain}")
                tmp.make_lst(sentence, comp_sentence, domain, filter_word, eval(f"domain_class.range_{domain}"))
                sentence = comp_sentence
    return sentence


def my_example_to_print(domain_cls_lst) -> None:
    """
        커스텀 문장 필터링 -> print 출력
    """
    global domain_cnt_dict, domain_time_dict
    for sentence in sentence_lst:
        for domain_class in domain_cls_lst:
            start_time = time.time()
            domain = "_".join(domain_class.__name__.split("_")[1:])
            if domain == "account":
                sentence = my_example_bank(domain_class, domain, sentence, "print")

            elif eval(f'domain_class(sentence).find_{domain}()'):
                comp_sentence = eval(
                    f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
                if sentence == comp_sentence:
                    continue
                else:
                    print("☆원본 :", sentence)
                    print(f"★필터({domain}) :", comp_sentence)
                    print("▶바뀐문장 :", eval(f"domain_class.result_{domain}"), end="\n\n")

                    sentence = comp_sentence
            end_time = time.time()


def my_example_to_django(domain_cls_lst, sentence_django) -> str:
    """
        커스텀 문장 필터링 -> print 출력
    """
    global domain_cnt_dict, domain_time_dict

    sentence = sentence_django
    domain_lst = []
    for domain_class in domain_cls_lst:
        domain = "_".join(domain_class.__name__.split("_")[1:])
        domain_lst.append(domain)
        if domain == "account":
            sentence = my_example_bank(domain_class, domain, sentence, "django")

        elif eval(f'domain_class(sentence).find_{domain}()'):
            comp_sentence = eval(
                f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
            if sentence == comp_sentence:
                continue
            else:
                eval(f"domain_class.result_{domain}")
                sentence = comp_sentence
    print("검사 도메인 리스트:", domain_lst)

    return sentence
