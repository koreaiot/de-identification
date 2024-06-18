from src.main.setting_variable import sentence_lst
from src.main.result.domain_info import DomainInfo


def tmp_to_excel_test(domain_cls_lst):

    tmp = DomainInfo(domain_cls_lst, "tmp")

    for sentence in sentence_lst:
        tmp.func_run(sentence)

    print(tmp.domain_cnt_dict)
    print(tmp.domain_time_dict)
    tmp.subject.make_excel(tmp.domain_time_dict, tmp.domain_cnt_dict, tmp.domain_lst)


def tmp_to_print(domain_cls_lst) -> None:
    """
        커스텀 문장 필터링 -> print 출력
    """
    global domain_cnt_dict, domain_time_dict
    for sentence in sentence_lst:
        for domain_class in domain_cls_lst:
            start_time = time.time()
            domain = "_".join(domain_class.__name__.split("_")[1:])
            if domain == "account":
                sentence = tmp_bank(domain_class, domain, sentence, "print")

            elif eval(f'domain_class(sentence).find_{domain}()'):
                comp_sentence = eval(
                    f're.sub(domain_class(sentence).{domain}_regex, domain_class(sentence).filter_{domain},sentence)')
                if sentence == comp_sentence:
                    continue
                else:
                    print("위치 : ", eval(f"domain_class(sentence).filter_{domain}"))
                    print("☆원본 :", sentence)
                    print(f"★필터({domain}) :", comp_sentence)
                    print("▶바뀐문장 :", eval(f"domain_class.result_{domain}"), end="\n\n")

                    sentence = comp_sentence
                    domain_cnt_dict = domain_cnt(domain_cnt_dict, domain, len(eval(f"domain_class.result_{domain}")))
            end_time = time.time()
            domain_time_dict = domain_time(domain_time_dict, domain, end_time - start_time)

    print(domain_cnt_dict)
    print(domain_time_dict)

