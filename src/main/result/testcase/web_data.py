from tqdm.gui import tqdm_gui
from src.main.result.domain_info import DomainInfo


def web_data_to_excel(domain_cls_lst):
    web_data = DomainInfo(domain_cls_lst, "web_data")
    with open(f"C:/Users/#/Desktop/#/개인정보 비식별화/data/웹데이터 기반 한국어 말뭉치.txt", "r", encoding='utf-8') as f:
        lines = f.readlines()

    for s in tqdm_gui(lines):
        sentence = s.rstrip("\n")
        web_data.func_run(sentence)

    print(web_data.domain_cnt_dict)
    print(web_data.domain_time_dict)
    web_data.subject.make_excel(web_data.domain_time_dict,
                                web_data.domain_cnt_dict,
                                web_data.domain_lst)