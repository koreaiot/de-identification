from tqdm.gui import tqdm_gui
from src.main.result.domain_info import DomainInfo


def online_to_excel(domain_cls_lst):
    online = DomainInfo(domain_cls_lst, "online")
    file_path = "../data/온라인 구어체 문장.txt"
    with open(file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
    for s in tqdm_gui(lines):
        sentence = s.rstrip("\n")
        online.func_run(sentence)

    print(online.domain_cnt_dict)
    print(online.domain_time_dict)
    online.subject.make_excel(online.domain_time_dict, online.domain_cnt_dict, online.domain_lst)


def online_bank(target_class, target, sentence, excel) -> object:
    global target_dict, target_time_dict, original_lst, changed_lst, filter_word_lst
    for i in bank_account_regex_list:
        target_class.account_regex = re.compile(i)
        if eval(f'target_class(sentence).find_{target}()'):
            comp_sentence = eval(
                f're.sub(target_class(sentence).{target}_regex, target_class(sentence).filter_{target},sentence)')
            if sentence == comp_sentence:
                continue
            elif excel != "Excel":
                with open(f"C:/Users/kjsta/Desktop/test_온라인_{now.today().date()}.txt",
                          "a", encoding='utf-8') as t:
                    t.write("☆원본 : ")
                    t.write(sentence + "\n")
                    t.write("★필터(" + target + ") : " + comp_sentence + "\n")
                    t.write("▶바뀐문장 :" + eval(
                        f"', '.join(target_class.result_{target})") + "\n\n\n")
            else:
                filter_word = eval(f"target_class.result_{target}")
                make_df(sentence, comp_sentence, target, filter_word)
                sentence = comp_sentence
                target_dict = target_cnt(target_dict, target, len(eval(f"target_class.result_{target}")))
    return sentence


def online_to_txt(domain_lst) -> object:
    file_path = "../data/온라인 구어체 문장.txt"
    with open(file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
    for s in tqdm_gui(lines):
        sentence = s.rstrip("\n")
        for target_class in domain_lst:
            target = "_".join(target_class.__name__.split("_")[1:])
            if target == "account":
                sentence = online_bank(target_class, target, sentence)

            elif eval(f'target_class(sentence).find_{target}()'):
                comp_sentence = eval(
                    f're.sub(target_class(sentence).{target}_regex, target_class(sentence).filter_{target},sentence)')
                if sentence == comp_sentence:
                    continue

                else:
                    with open(f"C:/Users/kjsta/Desktop/test_온라인_{now.today().date()}.txt",
                              "a", encoding='utf-8') as t:
                        t.write("☆원본 : ")
                        t.write(sentence + "\n")
                        t.write("★필터(" + target + ") : " + comp_sentence + "\n")
                        t.write("▶바뀐문장 :" + eval(
                            f"', '.join(target_class.result_{target})") + "\n\n\n")

