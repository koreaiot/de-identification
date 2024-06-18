from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Sentence(models.Model):
    sentence = models.TextField()
    # user_id = models.CharField(max_length=30)

    def __str__(self):
        return self.sentence


class Excel(models.Model):
    excel = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


class ZipJson(models.Model):
    file_upload_path = 'C:/Users/kjsta/Desktop/'
    zip_json = models.ImageField(upload_to=file_upload_path, null=True)


class UploadJson(models.Model):
    file_upload_path = 'C:/Users/kjsta/Desktop/'
    imgfile = models.ImageField(null=True, upload_to=file_upload_path, blank=True)

    def __str__(self):
        return self.imgfile


class Report(models.Model):
    title = models.CharField(verbose_name="제목 ",
                             max_length=50,
                             default="",
                             blank=True,
                             )

    report = models.TextField(  verbose_name="내용 ",
                                max_length=500,
                                blank=True,
    )

    reporter = models.CharField(verbose_name="신고자 ",
                             max_length=20,
                             default="",
                             blank=True,
                             )

    def __str__(self):
        return self.title
