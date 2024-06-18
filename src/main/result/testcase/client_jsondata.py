from ...setting_variable import sentence_lst
from ..domain_info import DomainInfo
from ..jsonpath import create_jsonpath_for_key
import zipfile
import json
from jsonpath_ng import parse
from tqdm import tqdm
import time

file_cnt = 0
def sample_zip_to_excel(domain_cls_lst, zip_file_path, target_key, time_now):
    sample_zip = DomainInfo(domain_cls_lst, "sample_zip", time_now)
    sum_sentence = 0
    with zipfile.ZipFile(zip_file_path, 'r') as archive:
        file_list = archive.namelist()
        result = None
        for file_name in tqdm(file_list[:]):
            with archive.open(file_name, 'r') as file:
                json_data = json.load(file)
                if result is None:
                    result = create_jsonpath_for_key(json_data, target_key)
                    expression = parse(".".join(["$", result.replace("[0]", "[*]")]))
                matches = [match.value for match in expression.find(json_data)]

                for sentence in matches:
                    sum_sentence += 1
                    sample_zip.func_run(sentence)

    sample_zip.subject.make_excel(sample_zip.domain_time_dict,
                                  sample_zip.domain_cnt_dict,
                                  sample_zip.domain_lst,
                                  len(file_list),
                                  sum_sentence)


def user_zip_to_excel(domain_cls_lst, user_zip_file_path, target_key, user_file_name, time_now):

    global file_cnt, sum_file_cnt
    user_zip = DomainInfo(domain_cls_lst, user_file_name, time_now)
    file_cnt, sum_file_cnt, sum_sentence = 0, 0, 0

    with zipfile.ZipFile(user_zip_file_path, 'r') as archive:
        error_jsonfile_num = 0
        for item in tqdm(archive.infolist()):
            # json_file = item.filename.encode('cp437').decode('cp949')
            if not item.is_dir():
                file_cnt += 1
                get_file_cnt()

                with archive.open(item, 'r') as file:
                    try:
                        json_data = json.load(file)
                        result = create_jsonpath_for_key(json_data, target_key)
                        expression = parse(".".join(["$", result.replace("[0]", "[*]")]))
                        matches = [match.value for match in expression.find(json_data)]

                        for sentence in matches:
                            user_zip.func_run(sentence, file.name)
                            sum_sentence += 1
                    except:
                        error_jsonfile_num += 1

                # json_data = json.loads(archive.read(item))
                # result = create_jsonpath_for_key(json_data, target_key)
                # expression = parse(".".join(["$", result.replace("[0]", "[*]")]))
                # matches = [match.value for match in expression.find(json_data)]
                #
                # for sentence in matches:
                #     user_zip.func_run(sentence)
    print("error_jsonfile_num:", error_jsonfile_num)
    user_zip.subject.make_excel(user_zip.domain_time_dict,
                                user_zip.domain_cnt_dict,
                                user_zip.domain_lst,
                                get_file_cnt()[0],
                                sum_sentence)
    print("총 파일 수 : " , get_file_cnt()[0])
    print("총 문장 수 : ", sum_sentence)


# def user_zip_to_excel(domain_cls_lst, user_zip_file_path, target_key, user_file_name, time_now):
#     # with open(zip_first_file_path, 'r', encoding='utf-8') as jsonfile:
#     #     json_data = json.load(jsonfile)
#     #     result = create_jsonpath_for_key(json_data, target_key)
#     #     expression = parse(".".join(["$", result.replace("[0]", "[*]")]))
#     #     matches = [match.value for match in expression.find(json_data)]
#     #     return matches
#
#     global file_cnt, sum_file_cnt
#     user_zip = DomainInfo(domain_cls_lst, user_file_name, time_now)
#     file_cnt, sum_file_cnt = 0, 0
#
#     with zipfile.ZipFile(user_zip_file_path, 'r') as archive:
#         file_list = archive.namelist()
#         sum_file_cnt = len(file_list)
#         result = None
#         for file_name in tqdm(file_list[:]):
#             file_cnt += 1
#             get_file_cnt()
#             with archive.open(file_name, 'r') as file:
#                 json_data = json.load(file)
#                 if result is None:
#                     result = create_jsonpath_for_key(json_data, target_key)
#                     expression = parse(".".join(["$", result.replace("[0]", "[*]")]))
#                 matches = [match.value for match in expression.find(json_data)]
#
#                 for sentence in matches:
#                     user_zip.func_run(sentence)
#
#     user_zip.subject.make_excel(user_zip.domain_time_dict,
#                                 user_zip.domain_cnt_dict,
#                                 user_zip.domain_lst)


def get_file_cnt():
    fn = file_cnt
    return fn, sum_file_cnt
