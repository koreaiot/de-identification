import json
import zipfile
from tqdm import tqdm
import urllib.parse
from django.contrib import auth

from django.shortcuts import redirect, render
from .models import Report
from .forms import SentenceForm, ExcelForm, ZipJsonForm, UploadForm, ReportForm
from src.main.main import django_main, excel_main, sample_zip_json_main, user_zip_json_main
from src.main.result.testcase.client_jsondata import get_file_cnt
from django.core.files.storage import FileSystemStorage
import os.path
import os
from django.http import FileResponse, HttpResponse
from .models import Sentence
import datetime
from jsonpath_ng import parse
from django.conf import settings
from tqdm import tqdm
import time
import threading
from django.contrib import messages
from django.contrib import auth


def home(request):
    """
    사용자의 문장을 입력 받아 django_main으로 보내서 사이클 돌리고 다시 화면으로 보냄
    """
    user = auth.get_user(request)
    print(user)
    if user.is_authenticated:
        print("유저 인증:", user)

    if request.method == 'POST' or request.method == 'FILES':

        form = SentenceForm(request.POST, request.FILES)
        report_form = ReportForm(request.POST, request.FILES)
        sentence_django = request.POST.get('sentence')
        sentence_after, domain_lst, rich_info_lst, rich_original_lst = django_main(sentence_django)
        keep_context = {   # 폼에 작성한 원본, 필터링 유지 context
            'form': form,
            'sentence_django': sentence_django,
            'sentence_after': sentence_after,
            'domain_lst': domain_lst,
            'rich_info_lst': rich_info_lst,
            'rich_original_lst': rich_original_lst
        }

        if 'report_submit' in request.POST:
            title = request.POST.get('title')
            report = request.POST.get('report')
            reporter = request.POST.get('reporter')
            if title == "" or report == "":  # 제목 or 내용에 빈 값이 있을 때, 알람.
                alert = True
                show_report_form = True
                report_form = ReportForm(initial={'report': f"{sentence_django}",
                                                  'reporter': user})
                return render(request, 'index.html', {'form': form,
                                                      'sentence_django': sentence_django,
                                                      'report_form': report_form,
                                                      'show_report_form': show_report_form,
                                                      'sentence_after': sentence_after,
                                                      'domain_lst': domain_lst,
                                                      'rich_info_lst': rich_info_lst,
                                                      'rich_original_lst': rich_original_lst,
                                                      'alert': alert,
                                                      })
            else:   # 값이 전부 있을 때, 신고 성공
                report_complete = True
                report_form.save()
                return render(request, 'index.html', {'form': form,
                                                      'sentence_django': sentence_django,
                                                      'sentence_after': sentence_after,
                                                      'domain_lst': domain_lst,
                                                      'rich_info_lst': rich_info_lst,
                                                      'rich_original_lst': rich_original_lst,
                                                      'report_complete': report_complete})

        if 'report_cancel' in request.POST:
            return render(request, 'index.html', keep_context )

        if 'report_btn' in request.POST:  # 문장 신고하기 폼 보여주는 리포트 버튼
            show_report_form = True
            report_form = ReportForm(initial={'report': f"{sentence_django}",
                                              'reporter': user})
            return render(request, 'index.html', {'form': form,
                                                  'show_report_form': show_report_form,
                                                  'sentence_django': sentence_django,
                                                  'report_form': report_form,
                                                  'sentence_after': sentence_after,
                                                  'domain_lst': domain_lst,
                                                  'rich_info_lst': rich_info_lst,
                                                  'rich_original_lst': rich_original_lst
                                                  })

        if 'sentence' in request.POST:
            print(end="\n\n")
            print("=======================제출========================")
            print("내가 입력 받은건 :", sentence_django)
            print("바뀐 문장  :", sentence_after)

            form.save()
            return render(request, 'index.html', keep_context)

        if form.is_valid():
            print("유효성 검사 들어옴")
            form.save()
            return redirect('home')

    else:
        form = SentenceForm()
        # return redirect('home')
    return render(request, 'index.html', {'form': form})


# def report(request):
#     if request.method == 'POST':
#         sentence_django = SentenceForm(request.POST)
#         report_form = ReportForm(request.POST)
#         if report_form.is_valid():
#             report_form.save()
#             print("report 함수임")
#
#             return redirect('home')
#     else:
#         form = ReportForm()
#     print("report 함수임22")
#
#     return render(request, 'index.html', {'report_form': report_form})
#

def download_excel(request):
    # 나의 example 샘플 다운로드
    time_now = click_time_now()
    print("---------------------엑셀----------------------")
    if request.method == 'POST' or request.method == 'FILES':
        print(request.POST.get('FILES'))
        form = ExcelForm(request.POST, request.FILES)
        tmp = request.POST.get('excel')

        if 'excelbtn' in request.POST:
            excel_main(time_now)
            file_path = os.path.expanduser('~').replace('\\', '/') + "/Desktop/" + f"my_example_{time_now}.xlsx"
            file_name = f"my_example_{time_now}.xlsx"

            with open(file_path, 'rb') as excel_file:
                response = HttpResponse(excel_file.read(), content_type="application/vnd.ms-excel")
                response["Content-Disposition"] = f"attachment; filename={file_name}"
                return response

        # 유효성 검사
        if form.is_valid():
            print("유효성 검사 들어옴")
            return redirect('excel')

    else:
        form = ExcelForm()
        # return redirect('home')
    return render(request, 'excel.html', {'form': form})


def zip_json_excel(request):
    # ZIP 샘플 다운로드 (SNS 고도화 파일 3,000개)
    time_now = click_time_now()
    print("---------------------zip----------------------")
    if request.method == 'POST' or request.method == 'FILES':
        form = ZipJsonForm(request.POST, request.FILES)
        tmp = request.POST.get('zip_json_excel')

        if 'zip_json_btn' in request.POST:
            target = "utterance"
            zip_file_path = ''

            sample_zip_json_main(zip_file_path, target, time_now)
            file_path = os.path.expanduser('~').replace('\\', '/') + "/Desktop/" + f"sample_zip_{time_now}.xlsx"
            file_name = f"sample_zip_{time_now}.xlsx"

            with open(file_path, 'rb') as excel_file:
                response = HttpResponse(excel_file.read(), content_type="application/vnd.ms-excel")
                response["Content-Disposition"] = f"attachment; filename={file_name}"
                return response

        # 유효성 검사
        if form.is_valid():
            print("유효성 검사 들어옴")
            return redirect('excel')

    else:
        form = ExcelForm()
        # return redirect('home')
    return render(request, 'excel.html', {'form': form})


def zip_json_upload(request):
    # 사용자 ZIP파일 업로드 이용
    time_now = click_time_now()
    print("---------------------zip_upload----------------------")
    if request.method == 'POST' or request.method == 'FILES':
        form = ZipJsonForm(request.POST)
        uploaded_file = request.FILES.get('file')
        if uploaded_file is None:
            return render(request, 'excel.html')
        print("파일 이름:", uploaded_file.name)
        print("파일 사이즈:", uploaded_file.size)
        user_file_name = ".".join(uploaded_file.name.split('.')[:-1])
        print(user_file_name)

        if "file_input_btn" in request.POST:
            print("file_input_btn")
            return render(request, 'excel.html', {'uploaded_file': uploaded_file})

        if "zipjsonBtn" in request.POST:
            target_key = request.POST.get('userInput')
            if not target_key:
                print("target_key 비어있음")
                return render(request, 'excel.html', {'uploaded_file': uploaded_file})
            else:
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    error_file_num = 0
                    for item in zip_ref.infolist():
                        try:
                            first_file = item.filename.encode('cp437', errors='replace').decode('cp949')
                            if first_file.endswith('.json'):
                                json_data = json.loads(zip_ref.read(item))
                                result = create_jsonpath_for_key(json_data, target_key)
                                if result is None:
                                    print("target_key가 없음.!!")
                                    target_key_x = True
                                    return render(request, 'excel.html', {'uploaded_file': uploaded_file,
                                                                          'target_key_x': target_key_x,
                                                                          'target_key': target_key})
                        except:
                            error_file_num += 1
                    print("error_file_num:", error_file_num)


                    # print(item.filename.encode('cp437').decode('cp949'))

            user_zip_json_main(uploaded_file, target_key, user_file_name, time_now)
            return render(request, 'excel.html')

        
    else:
        form = ZipJsonForm
        return render(request, 'excel.html')
    return render(request, 'excel.html', {'uploaded_file':uploaded_file})


def progress(request):
    # 사용자 ZIP파일 업로드 이용
    time_now = click_time_now()
    print("---------------------progress----------------------")
    if request.method == 'POST' or request.method == 'FILES':
        form = ZipJsonForm(request.POST)

        progress_uploaded_file = request.FILES.get('progress_file')
        if progress_uploaded_file is None:
            return render(request, 'excel.html')
        print("파일 이름:", progress_uploaded_file.name)
        print("파일 사이즈:", progress_uploaded_file.size)

        desktop_path = os.path.expanduser('~').replace('\\', '/') + "/Desktop/"
        user_file_name = progress_uploaded_file.name.split('.')[0]

        file_path = desktop_path + \
                    f"{user_file_name}_{time_now}.zip"

        with open(file_path, 'wb') as f:
            for chunk in progress_uploaded_file.chunks():
                f.write(chunk)

        print("집파일 위치:",file_path)

        if os.path.exists(file_path):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                first_file = zip_ref.namelist()[0]
                zip_ref.extract(first_file, desktop_path)
                first_file_path = os.path.join(desktop_path, first_file)

            if "progress_bar_btn" in request.POST:
                progress_target_key = request.POST.get('progress_userInput')
                if not progress_target_key:
                    print("progress_target_key 비어있음")
                    return render(request, 'excel.html', {'progress_uploaded_file':progress_uploaded_file})

                else:
                    with open(first_file_path, 'r', encoding="utf-8") as jsonfile:
                        json_data = json.load(jsonfile)
                        result = create_jsonpath_for_key(json_data, progress_target_key)
                        if result is None:
                            print("progress_target_key가 없음.!!")
                            progress_target_key_x = True
                            return render(request, 'excel.html', {'progress_uploaded_file': progress_uploaded_file,
                                                                  'progress_target_key_x': progress_target_key_x,
                                                                  'progress_target_key': progress_target_key})
                        # expression = parse(".".join(["$", result.replace("[0]", "[*]")]))
                        # matches = [match.value for match in expression.find(json_data)]

                print("업로드 버튼 누름")
                thread = threading.Thread(target=main_thread, args=(file_path, progress_target_key, user_file_name, time_now))
                thread.start()
                for _ in range(15):
                    time.sleep(0.2)
                    now_file, sum_file = get_file_cnt()
                    print("현재 파일 수 : ", now_file, sum_file)

                    return render(request, 'excel.html', {'progress_uploaded_file': progress_uploaded_file,
                                                          'progress_target_key': progress_target_key,
                                                          'file_total_num': sum_file,
                                                          'file_current_num': now_file
                                                          })

                else:
                    thread.join()


                # print("thread:", thread)
                # user_zip_json_main(file_path, progress_target_key, user_file_name, time_now)
                excel_file_path = os.path.expanduser('~').replace('\\', '/') + "/Desktop/" + f"{user_file_name}_{time_now}.xlsx"
                excel_file_name = f"{user_file_name}_{time_now}.xlsx"
                # print(get_file_cnt)

                # thread.join()
                #
                # with open(excel_file_path, 'rb') as excel_file:
                #     response = HttpResponse(excel_file.read(), content_type="application/vnd.ms-excel")
                #     encoded_file_name = urllib.parse.quote(excel_file_name)
                #     response["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_file_name}"
                #     return response

                # return render(request, 'excel.html')

            # user_zip_json_main(file_path, target)
        else:
            print("그저 대기")
    else:
        form = ZipJsonForm
        return render(request, 'excel.html')
    return render(request, 'excel.html', {'progress_uploaded_file':progress_uploaded_file})


def main_thread(file_path, progress_target_key, user_file_name, time_now):
    user_zip_json_main(file_path, progress_target_key, user_file_name, time_now)


# def progress(request):
#     if request.method == 'POST' or request.method == 'FILES':
#         if 'progress_bar_btn' in request.POST:
#             file_total_num = 100
#             file_current_num = 0
#             for file_current_num in range(file_total_num):
#                 file_current_num += 1
#                 print(get_file_cnt)
#
#                 context = {'file_total_num' : file_total_num,
#                            'file_current_num' : file_current_num}
#
#                 return render(request, 'progress.html', context)

def upload_file2(request):
    if request.meethod == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            uploadzipfile2 = form.save(commit=False)



def create_jsonpath_for_key(json_data, target_key):
    def _create_jsonpath(json_data, target_key, current_path=''):
        if isinstance(json_data, dict):
            if target_key in json_data:
                return f"{current_path}.{target_key}"
            else:
                for key, value in json_data.items():
                    result = _create_jsonpath(value, target_key, f"{current_path}.{key}")
                    if result is not None:
                        return result

        elif isinstance(json_data, list):
            for index, item in enumerate(json_data):
                result = _create_jsonpath(item, target_key, f"{current_path}[{index}]")
                if result is not None:
                    return result
        return None

    if _create_jsonpath(json_data, target_key) is not None:
        return _create_jsonpath(json_data, target_key)[1:]  # Remove the leading '.'
    else:
        return None


def click_time_now():
    now = datetime.datetime.now()
    time_ymdhm = now.strftime('%Y%m%d_%H%M')
    start_program_time = time_ymdhm
    print("누른 시간 :", start_program_time)
    return start_program_time