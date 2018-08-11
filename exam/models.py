from django.db import models
from tinymce.models import HTMLField
import tinymce


# 学生表（学生编号，姓名，密码）
class Student(models.Model):
    stuId = models.CharField(max_length=20, verbose_name=u'编号')
    stuName = models.CharField(max_length=20, verbose_name=u'登录名')
    stuPassword = models.CharField(max_length=30, verbose_name=u'登录密码')


# 老师表（老师编号，姓名，密码）
class Teacher(models.Model):
    teaId = models.CharField(max_length=20, verbose_name=u'编号')
    teaName = models.CharField(max_length=20, verbose_name=u'登录名')
    teaPassword = models.CharField(max_length=30, verbose_name=u'登录密码')


# 管理员表（管理员编号，姓名，密码）
class Admin(models.Model):
    admId = models.CharField(max_length=20, verbose_name=u'编号')
    admName = models.CharField(max_length=20, verbose_name=u'登录名')
    admPassword = models.CharField(max_length=30, verbose_name=u'登录密码')


'''
# 单选题表（科目类别，题干，选项A，选项B，选项C，选项D，答案）
class SingleChoice(models.Model):
    scCourse = models.CharField(max_length=30)
    scContent = models.CharField(max_length=200)
    # scImg = models.ImageField(null=True)
    scOpA = models.CharField(max_length=50)
    scOpB = models.CharField(max_length=50)
    scOpC = models.CharField(max_length=50)
    scOpD = models.CharField(max_length=50)
    scAnswer = models.CharField(max_length=2)


# 判断题（科目类别，题干，答案）
class Judgement(models.Model):
    judCourse = models.CharField(max_length=20)
    judContent = models.CharField(max_length=100)
    judAnswer = models.BooleanField()
'''


# 填空题（科目类别，难度[A,B,C]，题干，答案） 最多有十个填空
class FillBlank(models.Model):
    fbCourse = models.CharField(max_length=20, verbose_name=u'科目类别')
    fbGrade = models.CharField(max_length=5, verbose_name=u'难度等级')
    fbContent = models.CharField(max_length=200, verbose_name=u'题目内容')
    fbAnswer1 = models.CharField(max_length=100, verbose_name=u'填空1答案')
    fbAnswer2 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空2答案')
    fbAnswer3 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空3答案')
    fbAnswer4 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空4答案')
    fbAnswer5 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空5答案')
    fbAnswer6 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空6答案')
    fbAnswer7 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空7答案')
    fbAnswer8 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空8答案')
    fbAnswer9 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空9答案')
    fbAnswer10 = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'填空10答案')


# 简答题（科目类别，难度[A,B,C]，题干，答案）
class ShortAnswer(models.Model):
    saCourse = models.CharField(max_length=20, verbose_name=u'科目类别')
    saGrade = models.CharField(max_length=5, verbose_name=u'难度等级')
    saContent = models.CharField(max_length=200, verbose_name=u'题目内容')
    saAnswer = models.TextField(max_length=500, verbose_name=u'答案')



