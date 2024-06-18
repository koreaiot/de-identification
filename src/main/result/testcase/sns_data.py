from tqdm.gui import tqdm_gui
import pandas as pd
from src.main.result.domain_info import DomainInfo


def sns_data_to_excel(domain_cls_lst):

    sns_data = DomainInfo(domain_cls_lst, "SNS")
    dir_path = "../data/3-22. SNS_data_final(230110).csv"
    chunksize = 10 ** 3
    for cnt, chunk in tqdm_gui(enumerate(pd.read_csv(dir_path, chunksize=chunksize))):
        for i in range(len(chunk['utterance'])):
            sentence = chunk['utterance'].loc[chunksize * cnt + i]
            sns_data.func_run(sentence)

    print(sns_data.domain_cnt_dict)
    print(sns_data.domain_time_dict)
    sns_data.subject.make_excel(sns_data.domain_time_dict, sns_data.domain_cnt_dict, sns_data.domain_lst)
