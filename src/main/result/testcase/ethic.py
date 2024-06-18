from src.main.result.domain_info import DomainInfo
from tqdm.gui import tqdm_gui


def ethic_to_excel(domain_cls_lst):

    ethic = DomainInfo(domain_cls_lst, "text_ethic")
    file_path = "../data/텍스트 윤리 데이터.txt"
    with open(file_path, "r", encoding='utf-8') as t:
        lines = t.readlines()

    for s in tqdm_gui(lines):
        sentence = s.rstrip("\n")
        ethic.func_run(sentence)

    print(ethic.domain_cnt_dict)
    print(ethic.domain_time_dict)
    ethic.subject.make_excel(ethic.domain_time_dict,
                             ethic.domain_cnt_dict,
                             ethic.domain_lst)
