from django import forms
from .models import Sentence, Excel, ZipJson, UploadJson, Report
from dataclasses import field


class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence

        fields = ['sentence']
        # exclude = ['user_id']
        widgets = {
            "sentence": forms.Textarea(attrs={"class": "form-control mt-3", "cols":60, "rows":10})
        }
        labels = {
            "sentence": ""
        }


class ExcelForm(forms.ModelForm):
    class Meta:
        model = Excel

        fields = '__all__'
        print(fields)

        # fields = ['sentence']


class ZipJsonForm(forms.ModelForm):
    class Meta:
        model = ZipJson

        fields = '__all__'
        print(fields)


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadJson
        fields = ['imgfile']
        labels = {
            'imgfile':'이미지 이름'
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        # 내가 지정한 문장을 report 필드의 초기값으로 설정
        self.fields['title'].widget.attrs['placeholder'] = "*필수값"
        self.fields['report'].widget.attrs['placeholder'] = "*필수값"
        