from datetime import datetime
import pandas as pd
import numpy as np

changed_lst, target_lst, filter_word_lst, ttt = [], [], [], []


def make_df(sentence, comp_sentence, target, filter_word, tmp_lst):
    global changed_lst, target_lst, filter_word_lst, ttt

    now_time = datetime.today().strftime("%Y%m%d")[2:]
    file_path = f'C:/Users/kjsta/Desktop/tmp_{now_time}.xlsx'
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    workbook = writer.book
    bold = workbook.add_format({'bold': True})
    no_bold = workbook.add_format({'bold': False})
    blue = workbook.add_format({'color': 'blue'})
    red = workbook.add_format({'color': 'red', 'bold': True})

    span_lst = list(np.concatenate(tmp_lst))

    sen = []

    for i in range(len(span_lst)):
        if i == 0:
            if sentence[:span_lst[i]] != "":
                sen.append(no_bold)
                sen.append(sentence[0:span_lst[i]])
        elif i % 2 == 0:
            if sentence[span_lst[i - 1]:span_lst[i]] != "":
                sen.append(no_bold)
                sen.append(sentence[span_lst[i - 1]:span_lst[i]])
        elif i % 2 == 1:
            if sentence[span_lst[i - 1]:span_lst[i]] != "":
                sen.append(red)
                sen.append(sentence[span_lst[i - 1]:span_lst[i]])
    else:
        if sentence[span_lst[i]:] != "":
            sen.append(no_bold)
            sen.append(sentence[span_lst[i]:])

    ttt.append(sen)
    changed_lst.append(str(comp_sentence))
    target_lst.append(target)
    filter_word_lst.append(str(filter_word))

    writer.close()


def to_excel(name, all_time, all_filter_word, target_dict, target_uniq_lst) -> object:
    global changed_lst, filter_word_lst, ttt

    now_time = datetime.today().strftime("%Y%m%d")[2:]
    df = pd.DataFrame(changed_lst, columns=["비식별화"])
    df_target = pd.DataFrame.from_dict(target_dict, orient='index')
    df_target = df_target.reset_index()
    df_target.columns = ["Domain", "Count"]

    # df["비식별화"] = changed_lst
    df["원본"] = ttt
    df["도메인"] = target_lst
    df["추출단어"] = filter_word_lst

    file_path = f'C:/Users/kjsta/Desktop/{name}_{now_time}.xlsx'
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        for domain_name in target_uniq_lst:
            globals()[f"df_{domain_name}"] = df[df["도메인"] == f"{domain_name}"].reset_index(drop=True)
            df_target.to_excel(writer, sheet_name=f'{name}', startrow=4, index=False)
            globals()[f'df_{domain_name}'].to_excel(writer, sheet_name=f'{domain_name}', startrow=0, index=False,
                                                    freeze_panes=(1, 0))

            workbook = writer.book
            red = workbook.add_format({'color': 'red'})
            cellboldform = workbook.add_format({'bold': True})
            cellboldform2 = workbook.add_format({'align': 'center'})
            line_break = workbook.add_format()
            line_break.set_text_wrap()
            worksheet1 = writer.sheets[f"{name}"]
            globals()["worksheet_{}".format(domain_name)] = writer.sheets[f'{domain_name}']

            for idx, x in globals()["df_{}".format(domain_name)]['원본'].items():

                if len(x) == 2:
                    globals()[f"worksheet_{domain_name}"].write(f'B{idx + 2}', x[1], red)
                # if len(x) == 2 and df['도메인'].loc[idx] == "phone_number":
                #     worksheet.write(f'B{idx+3}', x[1], red)
                globals()[f"worksheet_{domain_name}"].write_rich_string(f'B{idx + 2}', *x)

            globals()[f"worksheet_{domain_name}"].set_column('A:A', 70, line_break)
            globals()[f"worksheet_{domain_name}"].set_column('B:B', 70, line_break)
            globals()[f"worksheet_{domain_name}"].set_column('C:C', 18, cellboldform2)
            globals()[f"worksheet_{domain_name}"].set_column('D:D', 35)
            globals()[f"worksheet_{domain_name}"].set_column('F:F', 13, cellboldform2)
            worksheet1.write('A1', f'검사 대상  :  {name}', cellboldform)
            worksheet1.write('A2', f"총 검사 시간  :  {round(all_time, 4)} 초", cellboldform)
            worksheet1.write('A3', f'추출 단어 수  :  {all_filter_word}', cellboldform)
            worksheet1.set_column('A:A', 40)
            (max_row, max_col) = df_target.shape
            # worksheet.autofilter(1, 2, 1 + max_row, 2)

            chart = workbook.add_chart({'type': 'bar'})
            chart.add_series({
                'categories': [f'{name}', 5, 0, max_row + 4, 0],
                'values': [f'{name}', 5, 1, max_row + 4, 1]
            })

            chart.set_title({'name': '도메인별 count'})
            chart.set_x_axis({'categories': 'filter_word'})
            chart.set_y_axis({'values': 'count'})

            worksheet1.insert_chart(4, 3, chart, {'x_scale': 1.6, 'y_scale': 1.2})
