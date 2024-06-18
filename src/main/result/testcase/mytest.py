import re
import datetime
import pandas as pd
import os
from tqdm.gui import tqdm_gui
from src.main.setting_variable import address_example_lst, address_example_data
from src.main.setting_variable import homepage_example_lst, homepage_example_data
from src.main.result.domain_info import DomainInfo
from tqdm.gui import tqdm_gui

now = datetime.datetime.now()


def only_address_to_excel(domain_cls_lst) -> object:
    """
        address.csv 불러와서
    """
    only_address = DomainInfo(domain_cls_lst, "only_address")

    for sentence in tqdm_gui(address_example_lst):
        only_address.func_run(sentence)

    print(only_address.domain_cnt_dict)
    print(only_address.domain_time_dict)
    only_address.subject.make_excel(only_address.domain_time_dict,
                                    only_address.domain_cnt_dict,
                                    only_address.domain_lst)



