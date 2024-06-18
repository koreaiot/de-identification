from src.main.CheckException.exceptional import ChkException
from src.main.result.testcase.my_example import my_example_to_django
from src.main.result.testcase.django_data import django_data
from src.main.result.testcase.client_jsondata import sample_zip_to_excel, user_zip_to_excel
from src.main.result.testcase.my_example import my_example_to_excel
from src.main.result.testcase.web_data import web_data_to_excel

import datetime
from src.main.domain.account import deidentify_account
from src.main.domain.address import deidentify_address
from src.main.domain.age import deidentify_age
from src.main.domain.card import deidentify_card_number
from src.main.domain.driver_license import deidentify_driver_license
from src.main.domain.email import deidentify_email
from src.main.domain.ipv4 import deidentify_ipv4
from src.main.domain.rare_disease import deidentify_rare_disease
from src.main.domain.ssn import deidentify_ssn
from src.main.domain.url import deidentify_url
from src.main.domain.phone import deidentify_phone_number
from src.main.domain.military_number import deidentify_military_number

# from src.main.domain.ipv6 import deidentify_ipv6
# from src.main.domain.bad_word import deidentify_bad_word
# from src.main.domain.car import deidentify_car_number
# from src.main.domain.pccc import deidentify_pccc
# from src.main.domain.zipcode import deidentify_zipcode
# from src.main.domain.passport import deidentify_passport
# from src.main.domain.brn import deidentify_brn


def django_main(django_sentence):
    domain_cls_lst = ChkException.__subclasses__()
    return django_data(domain_cls_lst, django_sentence)


def excel_main(time_now):
    domain_cls_lst = ChkException.__subclasses__()
    return my_example_to_excel(domain_cls_lst, time_now)


def sample_zip_json_main(zip_file_path, target_key, time_now):
    domain_cls_lst = ChkException.__subclasses__()
    return sample_zip_to_excel(domain_cls_lst, zip_file_path, target_key, time_now)


def user_zip_json_main(user_zip_file_path, target_key, user_file_name, time_now):
    domain_cls_lst = ChkException.__subclasses__()
    return user_zip_to_excel(domain_cls_lst, user_zip_file_path, target_key, user_file_name, time_now)




if __name__ == '__main__':
    """
        cd myproj -> python manage.py runserver 192.168.1.49:5500으로 실행
        sns_data_to_excel() : 한국어 SNS 데이터 고도화
        online_to_excel() : 온라인 구어체 데이터
        ethic_to_excel() : 텍스트 윤리 데이터
        purpose_conversation_to_excel(): 용도별 목적 대화 데이터
        web_data_to_excel(): 웹데이터 기반 대규모 한국어 말뭉치 데이터
        only_address() : address_example.csv
        only_url() : homepage.csv
        my_example_to_excel() : 나의 예시
    """
    domain_cls_lst = ChkException.__subclasses__()
    web_data_to_excel(domain_cls_lst)

    # with cProfile.Profile() as pr:
    #     my_example_to_excel(domain_cls_lst)
    #
    # pr.print_stats()
