import os
from tqdm.gui import tqdm_gui
from src.main.setting_variable import bank_account_regex_list
from src.main.result.domain_info import DomainInfo


def purpose_conversation_to_excel(domain_cls_lst):

    purpose_conv = DomainInfo(domain_cls_lst, "purpose_conv")
    dir_path = "C:/Users/#/Desktop/021.용도별 목적대화 데이터"
    for (root, directories, files) in tqdm_gui(os.walk(dir_path)):
        for file in files:
            if '.txt' in file:
                file_path = os.path.join(root, file)
                with open(file_path, encoding='utf-8') as f:
                    lines = f.readlines()
                    for s in lines:
                        sentence = s.rstrip("\n")
                        purpose_conv.func_run(sentence)

    print(purpose_conv.domain_cnt_dict)
    print(purpose_conv.domain_time_dict)
    purpose_conv.subject.make_excel(purpose_conv.domain_time_dict,
                                    purpose_conv.domain_cnt_dict,
                                    purpose_conv.domain_lst)


def purpose_conversation_bank(target_class, target, sentence):
    for i in bank_account_regex_list:
        target_class.account_regex = re.compile(i)
        if eval(f'target_class(sentence).find_{target}()'):
            comp_sentence = eval(
                f're.sub(target_class(sentence).{target}_regex, target_class(sentence).filter_{target},sentence)')
            if sentence == comp_sentence:
                continue
            else:
                with open(f"C:/Users/#/Desktop/test_용도별_{now.today().date()}.txt",
                          "a", encoding='utf-8') as t:
                    t.write("☆원본 : ")
                    t.write(sentence + "\n")
                    t.write("★필터(" + target + ") : " + comp_sentence + "\n")
                    t.write("▶바뀐문장 :" + eval(
                        f"', '.join(target_class.result_{target})") + "\n\n\n")
    return sentence


def purpose_conversation_to_txt(domain_lst):
    dir_path = "C:/Users/#/Desktop/021.용도별 목적대화 데이터"
    for (root, directories, files) in tqdm_gui(os.walk(dir_path)):
        for file in files:
            if '.txt' in file:
                file_path = os.path.join(root, file)
                with open(file_path, encoding='utf-8') as f:
                    lines = f.readlines()
                    for s in lines:
                        sentence = s.rstrip("\n")
                        for target_class in domain_lst:
                            target = "_".join(target_class.__name__.split("_")[1:])
                            if target == "account":
                                sentence = purpose_conversation_bank(target_class, target, sentence)

                            elif eval(f'target_class(sentence).find_{target}()'):
                                comp_sentence = eval(
                                    f're.sub(target_class(sentence).{target}_regex, target_class(sentence).filter_{target},sentence)')
                                if sentence == comp_sentence:
                                    continue

                                else:
                                    with open(f"C:/Users/#/Desktop/test_용도별_{now.today().date()}.txt",
                                              "a", encoding='utf-8') as t:
                                        t.write("☆원본 : ")
                                        t.write(sentence + "\n")
                                        t.write("★필터(" + target + ") : " + comp_sentence + "\n")
                                        t.write("▶바뀐문장 :" + eval(
                                            f"', '.join(target_class.result_{target})") + "\n\n\n")
