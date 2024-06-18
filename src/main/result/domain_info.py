"""domain_info.py

    * 도메인 리스트, 데이터 셋 이름을 가져옴.
    * 도메인 별 추출 갯수, 시간 정보 ToExcel.py 전달
    * func_run(): 실행
"""
import datetime
import os
import re
import sys
import time

from .ToExcel import ToExcel
from ..setting_variable import bank_account_regex_list


class DomainInfo:

    def __init__(self, domain_cls_lst, name, time_now):
        self.domain_cnt_dict = {}
        self.domain_time_dict = {}
        self.domain_lst = []
        self.domain_cls_lst = domain_cls_lst
        self.subject = ToExcel(time_now, name)
        for domain_class in self.domain_cls_lst:
            domain = "_".join(domain_class.__name__.split("_")[1:])
            self.domain_lst.append(domain)
        self.domain_cnt_dict = dict(zip(self.domain_lst, [0] * len(self.domain_lst)))
        self.domain_time_dict = dict(zip(self.domain_lst, [0] * len(self.domain_lst)))

    @staticmethod
    def domain_cnt(domain_cnt_dict, domain, cnt):
        domain_cnt_dict[domain] += cnt
        return domain_cnt_dict

    @staticmethod
    def domain_time(domain_time_dict, domain, diff_time):
        domain_time_dict[domain] += diff_time
        return domain_time_dict

    def func_run(self, sentence, json_file_name):
        original_sentence = sentence
        all_filter_word_lst, all_filter_domain_lst, all_filter_range_lst = [], [], []  # 도메인 전체 통합

        for domain_class, domain in zip(self.domain_cls_lst, self.domain_lst):
            start_time = time.time()
            # if domain == "account":
            #     for i in bank_account_regex_list:
            #         domain_class.account_regex = re.compile(i)
            #         if eval(f'domain_class(sentence).find_{domain}()'):  # 기본 정규식 필터 통과
            #             comp_sentence = eval(
            #                 f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
            #             if not eval(f'domain_class(sentence).range_{domain}'):
            #                 continue
            #             else:  # 전체 필터 통과
            #                 filter_word = eval(f"domain_class.result_{domain}")
            #
            #                 self.subject.make_lst(sentence, comp_sentence, domain, filter_word,
            #                                       eval(f"domain_class.range_{domain}"), "unit")
            #                 sentence = comp_sentence
            #                 self.domain_cnt_dict = DomainInfo.domain_cnt(self.domain_cnt_dict, domain,
            #                                                              len(eval(f"domain_class.result_{domain}")))
            #                 all_filter_word_lst += filter_word
            #                 all_filter_domain_lst.append(domain)
            #                 all_filter_range_lst += eval(f"domain_class.range_{domain}")

            if eval(f'domain_class(sentence).find_{domain}()'):
                comp_sentence = eval(
                    f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
                if not eval(f'domain_class(sentence).range_{domain}'):
                    continue
                else:
                    filter_word = eval(f"domain_class.result_{domain}")
                    self.subject.make_lst(sentence, comp_sentence, domain, filter_word,
                                          eval(f"domain_class.range_{domain}"), "unit", json_file_name)
                    sentence = comp_sentence
                    self.domain_cnt_dict = DomainInfo.domain_cnt(self.domain_cnt_dict, domain,
                                                                 len(eval(f"domain_class.result_{domain}")))
                    all_filter_word_lst += filter_word
                    all_filter_domain_lst.append(domain)
                    all_filter_range_lst += eval(f"domain_class.range_{domain}")
            end_time = time.time()
            self.domain_time_dict = DomainInfo.domain_time(self.domain_time_dict, domain, end_time - start_time)

        if all_filter_range_lst:
            self.subject.make_lst(sentence, original_sentence,
                                  all_filter_domain_lst,
                                  all_filter_word_lst,
                                  all_filter_range_lst,
                                  "union", json_file_name)

            # bad_word는 모델로 불러오기
            # elif domain == "bad_word":
            #     for i in bad_word_lst:
            #         if i in sentence:
            #             i = i.replace("^", "\^").replace("$", "\$").replace("?", "\?").replace("|","\|")
            #             domain_class.bad_word_regex = re.compile(i)
            #             if eval(f'domain_class(sentence).find_{domain}()'):  # 기본 정규식 필터 통과
            #                 comp_sentence = eval(
            #                     f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
            #                 if not eval(f'domain_class(sentence).range_{domain}'):
            #                     continue
            #                 else:  # 전체 필터 통과
            #                     filter_word = eval(f"domain_class.result_{domain}")
            #                     try:
            #                         self.subject.make_lst(sentence, comp_sentence, domain, filter_word,
            #                                               eval(f"domain_class.range_{domain}"), "unit")
            #                     except:
            #                         print(i, sentence, eval(f"domain_class.range_{domain}"))
            #                     sentence = comp_sentence
            #                     self.domain_cnt_dict = DomainInfo.domain_cnt(self.domain_cnt_dict, domain,
            #                                                                  len(eval(f"domain_class.result_{domain}")))
            #                     all_filter_word_lst += filter_word
            #                     all_filter_domain_lst.append(domain)
            #                     all_filter_range_lst += eval(f"domain_class.range_{domain}")