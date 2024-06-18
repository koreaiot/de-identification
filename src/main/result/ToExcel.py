"""ToExcel.py

    * 1) 원본, 바뀐 문장, 식별 도메인, 식별 단어 리스트 저장
    * 2) 원본은 하나씩 쓰기(식별 단어 빨간 표시 위함), 나머지는 데이터프레임으로 변환 후 쓰기
    * 3) 엑셀: 첫장-전체 정보 및 차트, 이후 시트: 각 도메인 별 식별 문장
    * func_run(): 실행

"""

import pandas as pd
import numpy as np
import os
from django.http import FileResponse
from django.utils.encoding import smart_str


class ToExcel:

    # changed_sentence_lst, original_lst, extracted_domain_lst, filter_word_lst = [], [], [], []
    # all_changed_sentence_lst, all_original_lst, all_extracted_domain_lst, all_filter_word_lst = [], [], [], []
    tmp_file_path = ''

    def __init__(self, date, name):
        self.date = date
        self.name = name
        self.file_path = f'~/Desktop/{self.name}_{self.date}.xlsx'
        self.changed_sentence_lst, self.original_lst, self.extracted_domain_lst, self.filter_word_lst, self.json_file_name_lst = [], [], [], [], []
        self.all_changed_sentence_lst, self.all_original_lst, self.all_extracted_domain_lst, self.all_filter_word_lst, self.all_json_file_name_lst = [], [], [], [], []
        with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
            self.workbook = writer.book
            self.no_bold = self.workbook.add_format({'bold': False})
            self.blue = self.workbook.add_format({'color': 'blue'})
            self.text_red_bold = self.workbook.add_format({'color': 'red', 'bold': True})

    def make_lst(self, sentence, comp_sentence, extracted_domain, filter_word, range_lst, kind, json_file_name):

        span_lst = sorted(list(np.concatenate(range_lst)))
        span_lst_length = len(span_lst)
        rich_info_lst = []  # 폰트 결정 리스트
        rich_info_change_lst = []
        if kind == "unit":
            for i in range(span_lst_length):  # 추출 단어: 굵은 빨간색
                if i == 0:
                    if sentence[:span_lst[i]] != "":
                        rich_info_lst.append(self.no_bold)
                        rich_info_lst.append(sentence[0:span_lst[i]])
                        rich_info_change_lst.append(self.no_bold)
                        rich_info_change_lst.append(comp_sentence[0:span_lst[i]])
                elif i % 2 == 0:
                    if sentence[span_lst[i - 1]:span_lst[i]] != "":
                        rich_info_lst.append(self.no_bold)
                        rich_info_lst.append(sentence[span_lst[i - 1]:span_lst[i]])
                        rich_info_change_lst.append(self.no_bold)
                        rich_info_change_lst.append(comp_sentence[span_lst[i - 1]:span_lst[i]])
                elif i % 2 == 1:
                    if sentence[span_lst[i - 1]:span_lst[i]] != "":
                        rich_info_lst.append(self.text_red_bold)
                        rich_info_lst.append(sentence[span_lst[i - 1]:span_lst[i]])
                        rich_info_change_lst.append(self.blue)
                        rich_info_change_lst.append(comp_sentence[span_lst[i - 1]:span_lst[i]])
            if sentence[span_lst[span_lst_length-1]:] != "":
                rich_info_lst.append(self.no_bold)
                rich_info_lst.append(sentence[span_lst[i]:])
                rich_info_change_lst.append(self.no_bold)
                rich_info_change_lst.append(comp_sentence[span_lst[i]:])

            self.original_lst.append(rich_info_lst)
            self.changed_sentence_lst.append(rich_info_change_lst)
            self.extracted_domain_lst.append(extracted_domain)
            self.filter_word_lst.append(str(filter_word))
            self.json_file_name_lst.append(json_file_name)

        if kind == "union":
            for i in range(span_lst_length):  # 추출 단어: 굵은 빨간색
                if i == 0:
                    if comp_sentence[:span_lst[i]] != "":
                        rich_info_lst.append(self.no_bold)
                        rich_info_lst.append(comp_sentence[0:span_lst[i]])
                        rich_info_change_lst.append(self.no_bold)
                        rich_info_change_lst.append(sentence[0:span_lst[i]])
                elif i % 2 == 0:
                    if comp_sentence[span_lst[i - 1]:span_lst[i]] != "":
                        rich_info_lst.append(self.no_bold)
                        rich_info_lst.append(comp_sentence[span_lst[i - 1]:span_lst[i]])
                        rich_info_change_lst.append(self.no_bold)
                        rich_info_change_lst.append(sentence[span_lst[i - 1]:span_lst[i]])
                elif i % 2 == 1:
                    if comp_sentence[span_lst[i - 1]:span_lst[i]] != "":
                        rich_info_lst.append(self.text_red_bold)
                        rich_info_lst.append(comp_sentence[span_lst[i - 1]:span_lst[i]])
                        rich_info_change_lst.append(self.blue)
                        rich_info_change_lst.append(sentence[span_lst[i - 1]:span_lst[i]])
            if comp_sentence[span_lst[span_lst_length-1]:] != "":
                rich_info_lst.append(self.no_bold)
                rich_info_lst.append(comp_sentence[span_lst[i]:])
                rich_info_change_lst.append(self.no_bold)
                rich_info_change_lst.append(sentence[span_lst[i]:])

            self.all_changed_sentence_lst.append(rich_info_change_lst)
            self.all_original_lst.append(rich_info_lst)
            self.all_extracted_domain_lst.append(extracted_domain)
            self.all_filter_word_lst.append(str(filter_word))
            self.all_json_file_name_lst.append(json_file_name)

    def make_excel(self, domain_time_dict, domain_cnt_dict, domain_lst, file_cnt, sum_sentence):
        df = pd.DataFrame(zip(self.original_lst,
                              self.changed_sentence_lst,
                              self.extracted_domain_lst,
                              self.filter_word_lst,
                              self.json_file_name_lst))

        df_all = pd.DataFrame(zip(self.all_original_lst,
                                  self.all_changed_sentence_lst,
                                  self.all_extracted_domain_lst,
                                  self.all_filter_word_lst,
                                  self.all_json_file_name_lst))

        if df.empty:
            columns = ["원본", "비식별화", "도메인", "추출 단어", "파일명"]
            df = pd.DataFrame(columns=columns)
            df_all = pd.DataFrame(columns=columns)

        df.columns = ["원본", "비식별화", "도메인", "추출 단어", "파일명"]
        df_all.columns = ["원본", "비식별화", "도메인", "추출 단어", "파일명"]
        df_profile = pd.DataFrame.from_dict(domain_cnt_dict, orient='index')
        df_profile['1'] = np.round(list(domain_time_dict.values()), 4)
        df_profile = df_profile.reset_index()
        df_profile.columns = ["Domain", "Count", "Test_time(s)"]

        with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            text_red_bold = workbook.add_format({'color': 'red', 'bold': True})
            text_bold = workbook.add_format({'bold': True})
            text_blue = workbook.add_format({'color': 'blue'})
            text_center = workbook.add_format({'align': 'center'})
            line_break = workbook.add_format()
            line_break.set_text_wrap()

            df_profile.to_excel(writer, sheet_name='Profile', startrow=4, index=False)
            worksheet_profile = writer.sheets["Profile"]

            worksheet_profile.write('A1', f'검사 파일 명  :  {self.name}', text_bold)
            worksheet_profile.write('A2',
                                    f"총 검사 시간  :  {round(sum(domain_time_dict.values()), 4)}초, 총 파일 수 : {file_cnt}",
                                    text_bold)
            worksheet_profile.write('A3',
                                    f'추출 단어 수  :  {sum(domain_cnt_dict.values())}, 총 문장 수 : {sum_sentence}',
                                    text_bold)
            worksheet_profile.set_column('A:A', 40)
            (max_row, max_col) = df_profile.shape
            chart = workbook.add_chart({'type': 'bar'})
            chart.add_series({
                'categories': ['Profile', 5, 0, max_row + 4, 0],
                'values': ['Profile', 5, 1, max_row + 4, 1]
            })
            chart.set_title({'name': '도메인 별 count'})
            chart.set_x_axis({'categories': 'filter_word'})
            chart.set_y_axis({'values': 'count'})
            worksheet_profile.insert_chart(4, 3, chart, {'x_scale': 1.6, 'y_scale': 1.2})

            df_all.to_excel(writer, sheet_name=f'비식별화 종합', startrow=1, index=False, freeze_panes=(2, 0))
            worksheet_all = writer.sheets[f"비식별화 종합"]
            for idx, x in df_all['원본'].items():
                if len(x) == 2:
                    worksheet_all.write(f'A{idx + 3}', x[1], text_red_bold)
                worksheet_all.write_rich_string(f'A{idx + 3}', *x)

            for idx, x in df_all['비식별화'].items():
                if len(x) == 2:
                    worksheet_all.write(f'B{idx + 3}', x[1], text_blue)
                worksheet_all.write_rich_string(f'B{idx + 3}', *x)
            worksheet_all.set_column('A:A', 70, line_break)
            worksheet_all.set_column('B:B', 70, line_break)
            worksheet_all.set_column('C:C', 18, text_center)
            worksheet_all.set_column('D:D', 35, line_break)
            worksheet_all.set_column('E:E', 40, text_center)
            worksheet_all.set_column('F:F', 30, text_center)
            domain_idx = 5
            for domain in domain_lst:
                domain_idx += 1
                rule_image_path = f"src/data/domain_rule/example_rule.png"
                globals()[f"df_{domain}"] = df[df["도메인"] == f"{domain}"].reset_index(drop=True)

                globals()[f'df_{domain}'].to_excel(writer, sheet_name=f'{domain}',
                                                   startrow=1, index=False, freeze_panes=(2, 0))

                globals()["worksheet_{}".format(domain)] = writer.sheets[f'{domain}']
                for idx, x in globals()["df_{}".format(domain)]['원본'].items():
                    if len(x) == 2:
                        globals()[f"worksheet_{domain}"].write(f'A{idx + 3}', x[1], text_red_bold)
                    globals()[f"worksheet_{domain}"].write_rich_string(f'A{idx + 3}', *x)

                for idx, x in globals()["df_{}".format(domain)]['비식별화'].items():
                    if len(x) == 2:
                        globals()[f"worksheet_{domain}"].write(f'B{idx + 3}', x[1], text_blue)
                    globals()[f"worksheet_{domain}"].write_rich_string(f'B{idx + 3}', *x)

                globals()[f"worksheet_{domain}"].set_column('A:A', 70, line_break)
                globals()[f"worksheet_{domain}"].set_column('B:B', 70, line_break)
                globals()[f"worksheet_{domain}"].set_column('C:C', 18, text_center)
                globals()[f"worksheet_{domain}"].set_column('D:D', 35, line_break)
                globals()[f"worksheet_{domain}"].set_column('E:E', 40, text_center)
                globals()[f"worksheet_{domain}"].set_column('F:F', 30, text_center)
                # globals()[f"worksheet_{domain}"].insert_image("F3", rule_image_path, {"x_offset": 12, "y_offset": 8}) 이미지 삽입.
                globals()[f"worksheet_{domain}"].write_url(f"A1", 'internal:Profile!A1', string="Profile")
                worksheet_profile.write_url(f"A{domain_idx}", f'internal:{domain}!A1', string=domain)

        # file_name = os.path.basename(self.file_path)
        # print(file_name)
        # excel_file_path = os.path.join(os.path.expanduser('~').replace('\\', '/')+'/Desktop/', file_name)
        # print(self.file_path)
        # print("홈", os.path.expanduser('~'))
        # print("여기", excel_file_path)
        # excel_test = "test 중"
        # response = FileResponse(open(excel_file_path), 'rb')
        # response['Content-Disposition'] = f'attachment; filename={smart_str(file_name+excel_test)}'
        # return response
